import frappe
import os
import json
from frappe.utils.file_manager import save_file
from frappe.utils import now
from ..messanger_user import update_last_message_time


@frappe.whitelist()
def send_message(payload):
    """
    API to create and send a message to Messenger or Instagram via Meta API.
    Args:
        payload (str): JSON string containing message details.

    Returns:
        dict: Response with message creation and sending status.
    """
    try:
        # payload = json.loads(payload)

        # Validate required fields
        required_fields = ["recipient_id", "platform", "message_type"]
        missing_fields = [field for field in required_fields if field not in payload]
        if missing_fields:
            frappe.throw(f"Missing required fields: {', '.join(missing_fields)}")

        attachment_files = payload["message"].get("attachment", {}).get("url")
        if attachment_files and not attachment_files.startswith("http"):
            raise KeyError("Invalid file URL provided, please include site base URL starting with http://sitename.com")

        allowed_message_type = ["text", "file", "image", "video", "audio", "reaction"]
        if payload["message_type"] not in allowed_message_type:
            raise KeyError(f"Invalid message type. allowed message types are {allowed_message_type}")
        
        if payload["message_type"] == "text" and not payload["message"].get("text", None):
            raise ValueError(f"Text message can not be empty.")

        platform = payload["platform"]

        message_payload = {
            "doctype": "Messenger Message",
            "to": payload["recipient_id"],
            "timestamp": now(),
            "platform": platform,
            "message_type": payload["message_type"],
            "message": payload["message"].get("text"),
            "attachment_files": json.dumps([payload["message"].get("attachment")]) if payload["message"].get("attachment") else None,
            # "media_type": payload["message"].get("attachment", {}).get("type"),
            # "reaction_action": payload["message"].get("reaction", {}).get("action"),
            # "reaction_emoji": payload["message"].get("reaction", {}).get("reaction_emoji"),
            # "reaction_text": payload["message"].get("reaction", {}).get("reaction_text"),
            "reply_to": payload["message"].get("reply_to", "") if payload["message"].get("reply_to") else None,
            # "sticker_type": payload["message"].get("sticker_type"),
            "flow": "Outgoing",
            "status": "Pending"
        }

        if platform == "Messenger":
            message_payload["page_id"]= payload["platform_id"]
            message_payload["from"]= payload["platform_id"]
        elif platform == "Instagram":
            message_payload["instagram_id"]= payload["platform_id"]
            message_payload["from"]= payload["platform_id"]
        else:
            raise KeyError(f"Unknown platform {platform} value passed. Allowed plateforms are 'Messenger' and 'Instagram'.")

        # Create Messenger Message DocType
        message_doc = frappe.get_doc(message_payload)

        
        message_doc.insert(ignore_permissions=True)
        frappe.db.commit()
        update_last_message_time(payload["recipient_id"],
                                platform,
                                message_payload["timestamp"], reset=True)
        return {
            "request_id": message_doc.name,
            "status": "Sending"
        }

    except Exception as e:
        print(frappe.get_traceback())
        frappe.logger().error(frappe.get_traceback())
        frappe.log_error(frappe.get_traceback(), "Message Creation Error")
        return {"status": "Failed", "error": str(e)}


@frappe.whitelist()
def upload_file():
    """
    Allows guest users to upload a file and returns the file URL.
    """
    try:
        # Get file from request
        uploaded_file = frappe.request.files.get("file")
        if not uploaded_file:
            frappe.throw("No file uploaded")

        # Get optional parameters
        # is_private = frappe.form_dict.get("is_private", "false").lower() == "true"
        doctype = "Messenger Message"
        # docname = frappe.form_dict.get("docname")

        # Define allowed file extensions
        allowed_extensions = [
            "pdf", "doc", "docx", "ppt", "pptx", "xls", "xlsx", "txt",
            "jpg", "jpeg", "png", "gif", "webp",
            "mp4", "mov", "avi", "mkv",
            "mp3", "wav", "aac"
        ]
        file_extension = os.path.splitext(uploaded_file.filename)[1][1:].lower()
        if file_extension not in allowed_extensions:
            frappe.throw(f"File type not allowed, allowed file types are: {allowed_extensions}")

        # Save the file using Frappe's file manager
        # file_doc = save_file(
        #     fname=uploaded_file.filename,
        #     content=uploaded_file.stream.read(),
        #     dt=doctype,
        #     dn=None,
        #     is_private=False # TODO: change to private before prod.
        # )
                # Create a new 'File' document
        file_doc = frappe.get_doc({
            "doctype": "File",
            # "attached_to_doctype": doctype,
            "file_name": uploaded_file.filename,
            "is_private": False,
            "content": uploaded_file.stream.read()
        })
        file_doc.insert(ignore_permissions=True)

        file_res = {
            "url": file_doc.file_url,
            "type": file_extension
        }

        # Return the file URL
        return {
            "status": "success",
            "file_url": file_res
        }

    except Exception as e:
        print(frappe.get_traceback())
        frappe.log_error(frappe.get_traceback(), "File Upload Error")
        return {"status": "error", "message": str(e)}

@frappe.whitelist(methods=["GET"])
def fetch_users(platform=None, limit: int=100, page: int=1, order="desc", search=None):
    """
    API to fetch Messenger/Instagram users sorted by their last interaction time with pagination.

    Args:
        platform (str, optional): The platform to filter users by ("Messenger" or "Instagram").
        limit (int, optional): Maximum number of users to fetch per page (default: 100).
        page (int, optional): Page number to fetch (default: 1).
        order (str, optional): Order of sorting by last interaction time ("asc" or "desc").
        search (str, optional): Keyword to search by username or full name.
    Returns:
        dict: Response with paginated user data.
    """
    try:
        # Validate input arguments
        if order not in ["asc", "desc"]:
            frappe.throw("Invalid order value. Use 'asc' or 'desc'.")
        if limit < 1:
            frappe.throw("Limit must be greater than 0.")
        if page < 1:
            frappe.throw("Page must be greater than 0.")

        # Build filters
        filters = {}
        if platform:
            filters["platform"] = ["=", platform]
        or_filter = None
        if search:
            or_filter = [
                ["full_name", "like", f"%{search}%"],
                ["username", "like", f"%{search}%"]
                ]
        
        # Calculate offset for pagination
        offset = (page - 1) * limit

        # Fetch users sorted by last_interaction_timestamp with pagination
        users = frappe.get_all(
            "Messenger User",
            filters=filters,
            or_filters=or_filter,
            fields=["user_id", "platform", "full_name", "username", "gender", "profile_picture_url", "last_interaction_timestamp", "unread_message_count"],
            order_by=f"last_interaction_timestamp {order}",
            limit_page_length=limit,
            limit_start=offset
        )

        # Format results for the response
        results = []
        for user in users:
            results.append({
                "user_id": user.get("user_id"),
                "platform": user.get("platform"),
                "name": user.get("full_name"),
                "username": user.get("username"),
                "gender": user.get("gender", ""),
                "profile_picture_url": user.get("profile_picture_url"),
                "last_interaction_timestamp": user.get("last_interaction_timestamp"),
                "unread_count": user.get("unread_message_count")
            })

        # Check if more data exists for the next page
        total_count = frappe.db.count("Messenger User", filters=filters)
        has_next = offset + limit < total_count

        return {
            "status": "success",
            "data": results,
            "pagination": {
                "current_page": page,
                "limit": limit,
                "total_users": total_count,
                "has_next": has_next
            }
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Fetch Users Error")
        return {"status": "error", "message": str(e)}

@frappe.whitelist()
def fetch_messages(user_id=None, platform_id=None, platform=None, limit: int=100, page: int=1, order="desc"):
    """
    API endpoint to fetch messages for a particular user, page, and platform in descending order.

    Args:
        user_id (str, optional): User ID to filter messages.
        platform_id (str, optional): Page ID or Instagram ID to filter messages.
        platform (str, optional): Platform to filter messages ("Messenger" or "Instagram").
        limit (int, optional): Number of messages to fetch per page (default: 100).
        page (int, optional): Page number for pagination (default: 1).
        order (str, optional): Sorting order ("asc" or "desc", default: "desc").

    Returns:
        dict: JSON response with fetched messages.
    """
    try:
        page_id = "371024009436368" # hardcoded for temp.

        # Validate parameters
        if not user_id or not platform_id or not platform:
            raise KeyError("User ID, platform ID, and Platform are required fields.")
        if order not in ["asc", "desc"]:
            raise KeyError("Invalid order value. Use 'asc' or 'desc'.")
        if limit < 1:
            raise KeyError("Limit must be greater than 0.")
        if page < 1:
            raise KeyError("Page must be greater than 0.")

        # Calculate offset for pagination
        offset = (page - 1) * limit

        # Build filters
        or_filters= [
                {"from": user_id},
                {"to": user_id}
            ]
        # don't fetch deleted message.
        filters = {
            "platform": platform,
            "status": ["!=", "Deleted"]
        }
        if platform == "Messenger":
            filters["page_id"] = platform_id
        elif platform == "Instagram":
            filters["instagram_id"] = platform_id
        else:
            raise KeyError(f"Unknown platform {platform} value passed. Allowed plateforms are 'Messenger' and 'Instagram'.")

        # Fetch messages from Messenger Message doctype
        messages = frappe.get_all(
            "Messenger Message",
            or_filters=or_filters,
            filters=filters,
            fields=[
                "name", "message_id", "from", "to", "message", "message_type", "instagram_id",
                "timestamp", "attachment_files", "attachment_products",
                "attachment_fallbacks", "attachment_reels", "reaction_emoji",
                "reaction_text", "is_reply", "reply_to", "is_referral", "ref",
                "source", "ref_type", "ad_id", "referrer_url", "platform", 
                "page_id", "status", "flow", "is_quick_reply", "quick_reply"
            ],
            order_by=f"timestamp {order}",
            limit_page_length=limit,
            limit_start=offset
        )

        # Transform messages into the desired JSON structure
        formatted_messages = []
        for message in messages:
            formatted_message = {
                "id": message["name"],
                "message_id": message["message_id"],
                "from": message["from"],
                "to": message["to"],
                "content": {
                    "text": message.get("message"),
                    "type": message.get("message_type"),
                    "attachments": json.loads(message["attachment_files"]) if message["attachment_files"] else [],
                    "products": json.loads(message["attachment_products"]) if message["attachment_products"] else [],
                    "fallbacks": json.loads(message["attachment_fallbacks"]) if message["attachment_fallbacks"] else [],
                    "reels": json.loads(message["attachment_reels"]) if message["attachment_reels"] else []
                },
                "reaction": {
                    "emoji": message.get("reaction_emoji"),
                    "text": message.get("reaction_text")
                } if message.get("is_reaction") else None,
                "reply": {
                    "is_reply": message.get("is_reply"),
                    "reply_to": message.get("reply_to")
                } if message.get("is_reply") else None,
                "referral": {
                    "is_referral": message.get("is_referral"),
                    "ref": message.get("ref"),
                    "source": message.get("source"),
                    "type": message.get("ref_type"),
                    "ad_id": message.get("ad_id"),
                    "referrer_url": message.get("referrer_url")
                } if message.get("is_referral") else None,
                "quick_reply": {
                    "is_quick_reply": message.get("is_quick_reply"),
                    "payload": message.get("quick_reply")
                } if message.get("is_quick_reply") else None,
                "metadata": {
                    "platform": message.get("platform"),
                    "platform_id": message.get("instagram_id") if message.get("platform") == "Instagram" else message.get("page_id"),
                    "status": message.get("status"),
                    "flow": message.get("flow"),
                    "timestamp": message.get("timestamp")
                }
            }
            formatted_messages.append(formatted_message)

        # Pagination metadata
        total_messages = frappe.db.count("Messenger Message", filters=filters)
        has_next = offset + limit < total_messages

        # Return response
        return {
            "status": "success",
            "data": formatted_messages,
            "pagination": {
                "current_page": page,
                "limit": limit,
                "total_messages": total_messages,
                "has_next": has_next
            }
        }

    except Exception as e:
        print(frappe.get_traceback())
        frappe.log_error(frappe.get_traceback(), "Fetch Messages Error")
        return {"status": "error", "message": str(e)}

@frappe.whitelist()
def reset_unread_count(user_id, platform):
    """
    API to reset the unread message count for a specific user.
    
    Args:
        user_id (str): The PSID or IG user ID.
        platform (str): "Messenger" or "Instagram".

    Returns:
        dict: Response with the status of the operation.
    """
    try:
        user_doc = frappe.get_all(
            "Messenger User",
            filters={"user_id": user_id, "platform": platform},
            fields=["name"]
        )

        if user_doc:
            user_doc = frappe.get_doc("Messenger User", user_doc[0]["name"])
            user_doc.unread_message_count = 0
            user_doc.save(ignore_permissions=True)
            return {"status": "success", "message": "Unread message count reset successfully."}
        else:
            return {"status": "error", "message": f"User ID {user_id} on platform {platform} not found in Messenger User."}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Reset Unread Count Error")
        return {"status": "error", "message": str(e)}

