import frappe
import os
import json
import requests
from frappe.utils.file_manager import save_file
# from .events import send_message_event

# {
#   "recipient": {
#     "id": "595057866390475"
#   },
#   "messaging_type": "MESSAGE_TAG",
#   "tag": "HUMAN_AGENT",
#   "notification_type": "REGULAR",
#   "message": {
#     "text": "test"
#   }
# }

# 17841469373342139/messages?access_token=EAAQtJkWiBZCMBO4XqvhZAGi6YzdR5ZAM5cjjguKdDHe071DcC3HgBj7tF3dhybCnd94Xzph0yd37EPjuZA43EXx088Vf9qZCtzF1diOMDK0cw4PQQMcLXugN9y4dCquqe1yMIMc2f5OHfZBuo1BFliR3Vs6y53IQHYcr5OuC9lLF9GJ0SKhVKk9cLZARPLcbf0j5VjdrGa0hAZDZD

def send_to_meta(doc):
    """
    Sends a message to Meta API based on the Messenger Message document.
    """
    try:
        platform_id = doc.page_id if doc.platform == "Messenger" else "me"
        # Fetch Meta API Configuration
        config = frappe.get_doc("Messenger Config")
        access_token = config.get_password("access_token")
        url = f"{config.meta_url}/{config.meta_api_version}/{platform_id}/messages?access_token={access_token}"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        # Prepare payload
        payload = {
            "recipient": {
                "id": doc.to
            },
            "messaging_type": "MESSAGE_TAG",
            "tag": "HUMAN_AGENT",
            "notification_type": "REGULAR"
        }

        # Handle different message types
        if doc.message_type == "text":
            payload["message"] = {"text": doc.message}
        elif doc.message_type in ["file", "audio", "video", "image"]:
            if not doc.attachment_files:
                raise Exception("No attachment URL found for this message.")
            payload_url = json.loads(doc.attachment_files)[0].get("url", None)
            if payload_url:
                payload["message"] = {
                    "attachment": {
                        "type": doc.message_type.lower(),
                        "payload": {"url": payload_url}
                    }
            }
        # elif doc.message_type == "reaction":
        #     payload["sender_action"] = doc.reaction_action
        #     payload["payload"] = {
        #         "message_id": doc.reply_to_message_id,
        #         "reaction": doc.reaction_emoji
        #     }
        # elif doc.message_type == "sticker":
        #     payload["message"] = {
        #         "attachment": {
        #             "type": doc.sticker_type
        #         }
        #     }

        else:
            raise Exception(f"Unsupported message type: {doc.message_type}")

        # Send the message using Meta API
        response = requests.post(url, headers=headers, json=payload)

        # Handle HTTP errors
        if not response.ok:
            error_message = f"Meta API error: {response.status_code} {response.text}"
            frappe.log_error("Meta API Error", error_message)
            raise Exception(f"Meta API sending error: {error_message}")
            response.raise_for_status()

        # Parse and return response
        return response.json()

    except requests.exceptions.RequestException as e:
        # Log and throw request-related errors
        frappe.log_error("Meta API Request Error", frappe.get_traceback())
        raise frappe.ValidationError(f"Error sending message to Meta API: {str(e)}")

    except Exception as e:
        print(frappe.get_traceback())
        # Log and handle other unexpected exceptions
        frappe.logger().error( "Meta API General Error", frappe.get_traceback())
        raise frappe.ValidationError(f"An unexpected error occurred: {str(e)}")


def process_message(doc, method=None):
    """
    Triggered after a Messenger Message is created.
    Sends the message to Meta API for delivery.
    """
    if doc.flow != "Outgoing" or doc.status in ["Sending", "Sent", "Received"]:
        return

    try:
        # Attempt to send the message to Meta API
        response = send_to_meta(doc)
        doc.message_id = response.get("message_id", "")
        doc.status = "Sent"
    except frappe.ValidationError as e:
        # Handle specific Frappe-related errors
        doc.status = "Failed"
        doc.error = str(e)
        frappe.log_error("Message Processing Error", frappe.get_traceback())
    except Exception as e:
        # Handle unexpected errors
        doc.status = "Failed"
        doc.error = f"An unexpected error occurred: {str(e)}"
        frappe.log_error("Unhandled Message Processing Error", frappe.get_traceback())
    finally:
        # Save the document state regardless of success or failure
        doc.save(ignore_permissions=True)
        # send_message_event(doc)
