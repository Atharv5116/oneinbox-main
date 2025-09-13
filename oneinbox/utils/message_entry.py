import frappe
import json
import requests
import uuid
import os
import pytz
from datetime import datetime
from frappe.utils import now
from frappe.utils.file_manager import save_file
from frappe.utils import format_datetime, get_datetime_str
from .messanger_user import fetch_user_profile, update_last_message_time
# from .events import send_message_event

def process_webhook_log(doc, method):
    """Process each log entry in Messenger Webhook Log and handle multiple messages within the entry."""
    try:
        try:
            frappe.set_user("Administrator")
        except Exception as e:
                frappe.logger().error("Error Setting User", f"Failed to set user to Administrator: {str(e)}")
        # Parse the event data from the log entry, which represents a single entry from the webhook payload
        entry_data = json.loads(doc.event_data)
        
        # Loop through each messaging item in the entry to process multiple messages
        for message in entry_data.get("messaging", []):
            process_message_data(doc, message)

        for message in entry_data.get("standby", []):
            process_message_data(doc, message)
            
            # Insert a new Messenger Message document based on the message data
            # frappe.get_doc(message_data).insert(ignore_permissions=True)
        
        # Update the log entry status to "Processed"
        doc.entry_status = "Processed"
        doc.processed_timestamp = now()
        doc.save()
        
    except json.JSONDecodeError as e:
        handle_processing_error(doc, f"JSON decode error: {str(e)}")
    except Exception as e:
        handle_processing_error(doc, frappe.get_traceback())

def handle_processing_error(doc, error_message):
    """Handles errors during processing by updating the log status and saving the error message."""
    frappe.log_error("Webhook Log Processing Error", error_message)
    doc.entry_status = "Fail"
    doc.error = error_message
    doc.save()

def process_message_data(doc, message):
    try:
        if "message" in message:
            # handle deleted message: 
            if "is_deleted" in message["message"]:
                message_doc = delete_message(doc, message["message"])
            else:
                message_doc = handle_incoming_message(doc, message)
            
            # if message_doc:
            #     send_message_event(message_doc)  # This might fail

        elif "read" in message:
            handle_read_receipt(doc, message)

        elif "delivery" in message:
            handle_delivery_receipt(doc, message)

        elif "reaction" in message:
            handle_reaction(doc, message)

        elif "message_edit" in message:
            handle_message_edit(doc, message)

        if "referral" in message:
            handle_referral(doc, message)

    except Exception as e:
        # handle_processing_error(doc, f"Error processing message data: {str(e)}")
        raise e
    # elif "postback" in message and "referral" in message["postback"]:
    #     handle_referral(doc, message["postback"])

# Make new Message Entry.
def handle_incoming_message(doc, item):
    """Handles incoming messages, including text and attachments."""
    try:
        sender_id = item["sender"].get("id")
        recipient_id = item["recipient"].get("id")

        message_data = {
            "doctype": "Messenger Message",
            "from": sender_id,
            "to": recipient_id,
            "timestamp": convert_epoch_to_datetime(item["timestamp"]),
            "status": "Received",
        }

        if doc.object == "page":
            message_data["platform"] = "Messenger"
            message_data["page_id"] = doc.page
        elif doc.object == "instagram":
            message_data["platform"] = "Instagram"
            message_data["instagram_id"] = doc.instagram
        else:
            raise Exception("Only Messenger(page) and Instagram platform are supported.")

        message = item.get("message", {})
        message_data["flow"] = "Outgoing" if message.get("is_echo") else "Incoming"
        message_data["status"] = "Sent" if message.get("is_echo") else "Received"
        message_id =  message["mid"]
        message_data["message_id"] = message_id

         # Check for duplicate message_id
        if frappe.db.exists("Messenger Message", {"message_id": message_id}):
            frappe.logger().info(f"Duplicate message_id {message_id} detected. Skipping processing.")
            return None  # Skip processing if message_id already exists


        # access_token
        messenger_config = frappe.get_single("Messenger Config")
        page_access_token = messenger_config.get_password("access_token")

        # Check if sender or receiver "USER" profiles exist
        # if not frappe.db.exists("Messenger User", {"user_id": sender_id}):
            # fetch_user_profile(sender_id, message_data["platform"], page_access_token)
        user_id = sender_id if message_data["flow"] == "Incoming" else recipient_id

        if not frappe.db.exists("Messenger User", {"user_id": user_id}):
            fetch_user_profile(user_id, message_data["platform"], page_access_token)

        # update last message time
        update_last_message_time(user_id,
                                message_data["platform"],
                                item.get("timestamp"), True)

        if "text" in message:
            message_data["message"] = message["text"]
            message_data["message_type"] = "text"


        # Handle attachments
        if "attachments" in message:
            attachments = message["attachments"]
            attachment_data = handle_file_attachments(message_data["message_id"], attachments)

            # Save file URLs as a comma-separated string or a JSON array
            message_data["attachment_files"] = json.dumps(attachment_data["files"])

            # Save product data as JSON
            if attachment_data["products"]:
                message_data["attachment_products"] = json.dumps(attachment_data["products"])

            # Save fallback data as JSON
            if attachment_data["fallbacks"]:
                message_data["attachment_fallbacks"] = json.dumps(attachment_data["fallbacks"])

        if "attachments" in message:
            
            message_data["message_type"] = message["attachments"][0]["type"]
            message_data["is_attachment"] = True    

            # Save file URLs as JSON
            if len(attachment_data["files"]) > 0:
                message_data["attachment_files"] = json.dumps(attachment_data["files"])

            # Save product data as JSON
            if len(attachment_data["products"]) > 0:
                message_data["attachment_products"] = json.dumps(attachment_data["products"])

            # Save fallback data as JSON
            if len(attachment_data["fallbacks"]) > 0:
                message_data["attachment_fallbacks"] = json.dumps(attachment_data["fallbacks"])

            # Save reels data as JSON
            if len(attachment_data["reels"]) > 0:
                message_data["attachment_reels"] = json.dumps(attachment_data["reels"])

        if "quick_reply" in message:
            message_data["is_quick_reply"] = True
            message_data["quick_reply"] = message["quick_reply"].get("payload")
        
        if "reply_to" in message:
            message_data["is_reply"] = True
            message_data["reply_to"] = message["reply_to"]["mid"]

        if "referral" in message:
            referral = message.get("referral", {})

            # Extract referral details
            ref = referral.get("ref", None)
            source = referral.get("source", None)  # SHORTLINK, ADS, CUSTOMER_CHAT_PLUGIN
            type_ = referral.get("type", None)  # Usually OPEN_THREAD
            ad_id = referral.get("ad_id", None)  # For ads
            referer_uri = referral.get("referer_uri", None)  # For Customer Chat Plugin
            ads_context_data = referral.get("ads_context_data", None)  # Ad-specific data

            product_id = referral.get("product", {}).get("id", None)

            # Add referral details to the message data
            message_data.update({
                "is_referral": True,
                "ref": ref,
                "source": source,
                "ref_type": type_,
                "ad_id": ad_id,
                "referrer_url": referer_uri,
            })

            # If there are ad context details, include them
            if ads_context_data:
                message_data.update({
                    "ad_title": ads_context_data.get("ad_title"),
                    "photo_url": ads_context_data.get("photo_url"),
                    "video_url": ads_context_data.get("video_url"),
                    "post_id": ads_context_data.get("post_id"),
                    "product_id": ads_context_data.get("product_id"),
                })
            if product_id:
                message_data.update({"product_id": product_id})

            # Log the referral details for debugging or analytics
            frappe.log(f"Processed referral embedded in message: {json.dumps(referral, indent=2)}", "Referral in Message")

        if "commands" in message:
            pass

        # Insert the message and return the document
        message_doc = frappe.get_doc(message_data)
        message_doc.insert(ignore_permissions=True)
        return message_doc
    except Exception as e:
        # handle_processing_error(doc, f"Error handling incoming message: {str(e)}")
        raise e

def handle_referral(doc, item):
    """Process referral object and populate relevant fields in Messenger Message."""
    referral = item.get("referral", {})
    if not referral:
        frappe.log_error("Referral Processing Error", "No referral data found in the webhook payload.")
        return
    
    # Extract sender and recipient information
    is_guest_user = referral.get("is_guest_user", False)  # For Customer Chat Plugin guest users
    sender_id = item.get("sender", {}).get("id", item.get("sender", {}).get("user_ref"))  # Handle user_ref for Customer Chat Plugin
    recipient_id = item.get("recipient", {}).get("id")

    # access_token
    messenger_config = frappe.get_single("Messenger Config")
    page_access_token = messenger_config.get_password("access_token")

    platform = "Messenger" if doc.object == "page" else "Instagram"

    # Check if sender profiles exist
    if not is_guest_user and not frappe.db.exists("Messenger User", {"user_id": sender_id}):
        fetch_user_profile(sender_id, platform, page_access_token)

    # if not frappe.db.exists("Messenger User", {"user_id": recipient_id}):
    #     fetch_user_profile(recipient_id, platform, page_access_token)

    # update the last user message timestamp
    if not is_guest_user:
        update_last_message_time(sender_id, platform, item.get("timestamp"), True)


    # Extract details from the referral object
    ref = referral.get('ref')
    source = referral.get('source')
    type_ = referral.get('type')
    ad_id = referral.get('ad_id', None)
    referer_uri = referral.get('referer_uri', None)
    ads_context_data = referral.get("ads_context_data", None)  # For Ad Referral data

        # Prepare Messenger Message data
    message_data = {
        "doctype": "Messenger Message",
        "message_id": item.get("timestamp"),
        "from": sender_id,
        "to": recipient_id if source != "CUSTOMER_CHAT_PLUGIN" else "",
        "flow": "Incoming",
        "timestamp": doc.timestamp,
        "status": "Received",
        "is_referral": True,
        "source": source,
        "ref": ref,
        "ref_type": type_,
        "ad_id": ad_id,
        "referrer_url": referer_uri,
        "user_ref": sender_id if source == "CUSTOMER_CHAT_PLUGIN" else None,
        "is_guest_user": is_guest_user,
        "platform": platform,
        "page_id": doc.page if doc.object == "page" else None,
        "instagram_id": doc.instagram if doc.object == "instagram" else None,
    }
    if is_guest_user:
        message_data["user_ref"] = sender_id

        # Additional data for Ads
    if ads_context_data:
        message_data.update({
            "ad_title": ads_context_data.get("ad_title", ""),
            "photo_url": ads_context_data.get("photo_url", ""),
            "video_url": ads_context_data.get("video_url", ""),
            "post_id": ads_context_data.get("post_id", ""),
            "product_id": ads_context_data.get("product_id", ""),
        })
    # Log referral details for debugging
    frappe.log(
        f"Processing referral with details: {json.dumps(message_data, indent=2)}", 
        title="Referral Event"
    )

    # Save referral data to Messenger Message
    try:
        frappe.get_doc(message_data).insert(ignore_permissions=True)
    except Exception as e:
        frappe.log_error("Error Saving Referral Data", frappe.get_traceback())


# Edit/update to existing Message
def handle_read_receipt(doc, item):
    """Update message status to 'Read' for all relevant messages."""
    page_id = doc.page
    from_id = item["sender"]["id"]
    to_id = item["recipient"]["id"]

    messages = frappe.get_all("Messenger Message", filters={
        "page_id": page_id,
        "from": to_id,
        "to": from_id,
        "status": ["in", ["Sent", "Delivered"]]
    })

    for message in messages:
        message_doc = frappe.get_doc("Messenger Message", message.name)
        message_doc.status = "Read"
        message_doc.save(ignore_permissions=True)

def handle_delivery_receipt(doc, item):
    """Update message status to 'Delivered' for specified message IDs."""
    delivered_message_ids = item["delivery"].get("mids", [])

    for message_id in delivered_message_ids:
        try:
            message_doc = frappe.get_doc("Messenger Message", {"message_id": message_id})
            message_doc.status = "Delivered"
            message_doc.save(ignore_permissions=True)
        except frappe.DoesNotExistError:
            frappe.log_error("Delivery Receipt Processing Error", f"Message with ID {message_id} not found")

def handle_reaction(doc, item):
    """Handle reaction events, adding or removing reactions as needed."""
    message_id = item.get("reaction", {}).get("mid")
    action = item.get("reaction", {}).get("action")
    timestamp = item.get("timestamp")

    if not message_id or not action:
        raise ValueError("Missing message ID or action in reaction event.")

    try:
        message_doc = frappe.get_doc("Messenger Message", {"message_id": message_id})

        if message_doc.get("flow") == "Incoming":
            update_last_message_time(message_doc.flow("from"), message_doc.get("platform"), timestamp, True)

        if action == "unreact":
            # Remove reaction
            message_doc.update({
                "reaction_emoji": None,
                "reaction_text": None,
                "is_reaction": False,
            })
        else:
            # Add or update reaction
            message_doc.update({
                "reaction_emoji": item["reaction"].get("emoji"),
                "reaction_text": item["reaction"].get("reaction"),
                "is_reaction": True,
            })

        message_doc.save(ignore_permissions=True)
    except frappe.DoesNotExistError as e:
        frappe.log_error("Reaction Processing Error", f"Message with ID {message_id} not found")
        raise e
    except Exception as e:
        raise e

def delete_message(doc, message):
    """Handle deleted messages by updating the message status."""
    message_id = message.get("mid")

    if not message_id:
        raise ValueError("Missing message ID in the deleted message event.")

    try:
        message_doc = frappe.get_doc("Messenger Message", {"message_id": message_id})
        message_doc.update({
            "status": "Deleted",
        })

        message_doc.save(ignore_permissions=True)
        return message_doc
    except frappe.DoesNotExistError as e:
        frappe.log_error("Message Delete Processing Error", f"Message with ID {message_id} not found")
        raise e
    except Exception as e:
        raise e

def handle_message_edit(doc, item):
    """Handle message edits, updating the message content."""
    message_edit = item.get("message_edit", {})
    message_id = message_edit.get("mid")
    edited_text = message_edit.get("text")
    timestamp = item.get("timestamp")

    if not message_id or not edited_text:
        raise ValueError(
            "Missing message ID or edited text in the message_edit event."
        )

    try:
        message_doc = frappe.get_doc("Messenger Message", {"message_id": message_id})
        message_doc.update({
            "message": edited_text,
            "is_edited": True,
            "edited_timestamp": timestamp or now(),
        })

        message_doc.save(ignore_permissions=True)
    except frappe.DoesNotExistError as e:
        frappe.log_error("Message Edit Processing Error", f"Message with ID {message_id} not found")
        raise e
    except Exception as e:
        raise e

# Helper function
def handle_file_attachments(message_id, attachments):
    """Handles file attachments by downloading and saving them to Frappe's file storage."""
    saved_files = []
    products = []
    fallbacks = []
    reels = []

    for attachment in attachments:
        attachment_type = attachment.get("type")

        if attachment_type in ["image", "video", "audio", "file"]:
            # Handle file attachments

            payload = attachment.get("payload", {})
            attachment_url = payload.get("url")
            # if attachment_type in ["reel", "ig_reel"]:
            #     title = payload.get("title", None)
            #     video_id = payload.get("video_id", None)

            if attachment_url:
                try:
                    # Fetch the file from the provided URL
                    response = requests.get(attachment_url, stream=True)
                    response.raise_for_status()

                    # Determine file extension and save it
                    _, extension = os.path.splitext(attachment_url.split("?")[0])  # Get the file extension
                    file_extension = extension.lstrip(".")
                    uuid_str = str(uuid.uuid4())
                    file_name = f"{uuid_str}_{attachment_type}.{file_extension}"

                    saved_file = frappe.get_doc({
                        "doctype": "File",
                        # "attached_to_doctype": doctype,
                        "file_name": file_name,
                        "is_private": False, #TODO: change to private before prod.
                        "content": response.content
                    })
                    saved_file.insert(ignore_permissions=True)

                    # saved_file = save_file(
                    #     file_name,
                    #     response.content,
                    #     "Messenger Message",
                    #     None,  # No parent document
                    #     is_private=False 
                    # )

                    # Append the saved file's URL to the list
                    saved_files.append({
                        "url": saved_file.file_url,
                        "type": attachment_type
                    })

                except requests.exceptions.RequestException as e:
                    frappe.log_error(
                        "Attachment Download Error",
                        f"Failed to download attachment from {attachment_url}. Error: {str(e)}"
                    )
        
        elif attachment_type == "template" and "product" in attachment.get("payload", {}):
            # Handle product attachments
            product_elements = attachment["payload"]["product"]["elements"]
            for product in product_elements:
                product_data = {
                    "product_id": product.get("id"),
                    "retailer_id": product.get("retailer_id"),
                    "image_url": product.get("image_url"),
                    "title": product.get("title"),
                    "subtitle": product.get("subtitle"),
                }
                products.append(product_data)

        elif attachment_type == "fallback":
            # Handle fallback attachments
            fallback_data = {
                "url": attachment["payload"].get("url"),
                "title": attachment["payload"].get("title"),
            }
            fallbacks.append(fallback_data)
        
        elif attachment_type in ["reel", "ig_reel"]:
            # Handle reel and ig_reel attachments
            payload = attachment.get("payload", {})
            attachment_url = payload.get("url")

            if attachment_url:
                reel_data = {
                    "type": attachment_type,
                    "url": attachment_url,
                    "title": payload.get("title", "Reel Attachment"),
                    "video_id": payload.get("video_id", None)
                }
                reels.append(reel_data)
        
    return {
        "files": saved_files,
        "products": products,
        "fallbacks": fallbacks,
        "reels": reels
    }

def convert_epoch_to_datetime(epoch_milliseconds, target_timezone='Asia/Kolkata'):
    epoch_seconds = epoch_milliseconds / 1000
    utc_datetime = datetime.fromtimestamp(epoch_seconds, tz=pytz.utc)

    # Convert UTC datetime to the target timezone
    target_tz = pytz.timezone(target_timezone)
    message_datetime = utc_datetime.astimezone(target_tz)

    frappe_datetime = message_datetime.strftime('%Y-%m-%d %H:%M:%S')  # Force correct format
    return frappe_datetime

# def prepare_message_data(doc, message):
#     """Prepare data for Messenger Message DocType from a messaging item."""
#     message_data = {
#         "doctype": "Messenger Message",
#         "platform": "Messenger",
#         "page_id": doc.page,
#         "from": message.get("sender", {}).get("id"),
#         "to": message.get("recipient", {}).get("id"),
#         "message_flow": "Incoming" if message.get("sender") else "Outgoing",
#         "message_timestamp": doc.timestamp,  # Adjusted based on new field name
#         "status": "Received",
#     }

#     if doc.object == "page":
#         message_data["platform"] = "Messenger"
#         message_data["page_id"] = doc.page
#     elif doc.object == "instagram":
#         message_data["platform"] = "Instagram"
#         message_data["page_id"] = doc.instagram
#     else:
#         raise Exception("Only Messenger(page) and Instagram platform are supported.")

#     # Handle different event types and populate message fields based on the message content
#     if "message" in message:
#         message_item = message["message"]
#         if "text" in message_item:
#             message_data["message"] = message_item["text"]
#             message_data["message_type"] = "text"
#         elif "attachments" in message_item:
#             message_data["message_type"] = message_item["attachments"][0]["type"]
#             message_data["attachments_json"] = json.dumps(message_item["attachments"])

#     elif "reaction" in message:
#         reaction = message.get("reaction", {})
#         message_data["reaction_emoji"] = reaction.get("emoji")
#         message_data["reaction_text"] = reaction.get("reaction")

#     elif "delivery" in message:
#         message_data["status"] = "Delivered"

#     elif "read" in message:
#         message_data["status"] = "Read"

#     # Return prepared data for insertion into Messenger Message
#     return message_data
