import frappe
import json
import requests
import pytz
from datetime import datetime
from frappe.utils import now, get_datetime_str
from frappe.utils import format_datetime


def fetch_user_profile(user_id, platform, page_access_token):
    """
    Fetch profile data for a Facebook or Instagram user and save it in the Messenger User doctype.
    
    Args:
        user_id (str): The PSID or IG user ID.
        platform (str): "Messenger" or "Instagram".
        page_access_token (str): The Facebook Page Access Token.

    Returns:
        dict: The user's profile data.
    """
    try:
        # Determine API endpoint based on platform
        if platform == "Messenger":
            url = f"https://graph.facebook.com/v21.0/{user_id}?fields=name,first_name,last_name,profile_pic,gender&access_token={page_access_token}"
        elif platform == "Instagram":
            url = f"https://graph.facebook.com/v21.0/{user_id}?fields=username,name,profile_pic,is_user_follow_business,follower_count&access_token={page_access_token}"
        else:
            raise ValueError("Unsupported platform: must be 'Messenger' or 'Instagram'.")

        # Make the API request
        response = requests.get(url)
        response.raise_for_status()
        profile_data = response.json()

        # Check if user already exists in the Messenger User doctype
        user_doc = frappe.get_all(
            "Messenger User",
            filters={"user_id": user_id, "platform": platform},
            fields=["name"]
        )
        
        messenger_user_doc = {
                "doctype": "Messenger User",
                "user_id": user_id,
                "platform": platform,
                "full_name": profile_data.get("name", None),
                "first_name": profile_data.get("first_name", profile_data.get("name", None)),
                "last_name": profile_data.get("last_name", None),
                "username": profile_data.get("username", None),
                "profile_picture_url": profile_data.get("profile_pic", None),
                "gender": profile_data.get("gender", None)
            }
        if platform == "Messenger":
            # messenger_user_doc.update({
            #     "full_name": profile_data.get("name"),
            #     "first_name": profile_data.get("first_name"),
            #     "last_name": profile_data.get("last_name"),
            # })
            pass
        else:
            # messenger_user_doc["full_name"] = profile_data.get("name")
            messenger_user_doc["follower_count"] = profile_data.get("follower_count")
            
        if not user_doc:
            # Create a new Messenger User entry
            user_doc = frappe.get_doc(messenger_user_doc)
            user_doc.insert(ignore_permissions=True)
        else:
            # Update existing user profile if needed
            user_doc = frappe.get_doc("Messenger User", user_doc[0].get("name"))
            user_doc.first_name = profile_data.get("first_name", None) or user_doc.first_name
            user_doc.last_name = profile_data.get("last_name", None) or user_doc.last_name
            user_doc.full_name = profile_data.get("name", None) or user_doc.full_name
            user_doc.username = profile_data.get("username") or user_doc.username
            user_doc.profile_picture_url = profile_data.get("profile_pic", None) or profile_data.get("profile_picture_url", "")
            user_doc.gender = profile_data.get("gender", "") or user_doc.gender
            user_doc.save(ignore_permissions=True)

        return profile_data

    except requests.exceptions.RequestException as e:
        frappe.log_error("Profile Fetch Error", f"Failed to fetch profile for user ID {user_id}. Error: {str(e)}")
        raise e
    except Exception as e:
        frappe.log_error("Profile Fetch Error", f"Failed to fetch Meta user profile {user_id}")
        raise e

def update_last_message_time(user_id, platform, timestamp=None, increment_unread=False, reset=False):
    """
    Update the last message time in the Messenger User collection.

    Args:
        user_id (str): The PSID or IG user ID.
        platform (str): "Messenger" or "Instagram".
        timestamp (int/float/str, optional): The timestamp of the last message.
        increment_unread (bool, optional): Whether to increment the unread message count.

    Returns:
        None
    """
    try:
        if isinstance(timestamp, (int, float)):
            formatted_timestamp = convert_epoch_to_datetime(timestamp)
        else:
            formatted_timestamp = timestamp if timestamp else now()
    
        user_doc = frappe.get_all(
            "Messenger User",
            filters={"user_id": user_id, "platform": platform},
            fields=["name", "unread_message_count"]
        )

        if user_doc:
            user_doc = frappe.get_doc("Messenger User", user_doc[0]["name"])
            user_doc.last_interaction_timestamp = formatted_timestamp
            if increment_unread:
                user_doc.unread_message_count = (user_doc.unread_message_count or 0) + 1
            if reset:
                user_doc.unread_message_count = 0
            user_doc.save(ignore_permissions=True)
        else:
            frappe.log_error("Timestamp Update Error", f"User ID {user_id} on platform {platform} not found in Messenger User.")
    except Exception as e:
        frappe.log_error("Timestamp Update Error", f"Failed to update last message timestamp for user ID {user_id}. Error: {str(e)}")
        raise e


def ensure_profile_exists(doc, method):
    """Ensure sender and receiver profiles exist before saving the message."""
    page_access_token = frappe.db.get_single_value("Messenger Config", "access_token")

    sender_id = doc.get("from")
    recipient_id = doc.to
    flow = doc.flow
    user_id = sender_id if flow == "Incoming" else recipient_id

    # Check if sender and receiver profiles exist
    if not frappe.db.exists("Messenger User", {"user_id": user_id}):
        fetch_user_profile(user_id, doc.platform, page_access_token)

    # if not frappe.db.exists("Messenger User", {"user_id": recipient_id}):
    #     fetch_user_profile(recipient_id, doc.platform, page_access_token)

def convert_epoch_to_datetime(epoch_milliseconds, target_timezone='Asia/Kolkata'):
    epoch_seconds = epoch_milliseconds / 1000
    utc_datetime = datetime.fromtimestamp(epoch_seconds, tz=pytz.utc)

    # Convert UTC datetime to the target timezone
    target_tz = pytz.timezone(target_timezone)
    message_datetime = utc_datetime.astimezone(target_tz)

    frappe_datetime = message_datetime.strftime('%Y-%m-%d %H:%M:%S')  # Force correct format
    return frappe_datetime