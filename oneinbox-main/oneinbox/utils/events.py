import frappe
import json

def send_message_event(doc, method=None):
    try:
        frappe.logger().info(f"send_message_event triggered for doc: {doc.name}")
        flow = doc.flow  # 'Incoming' or 'Outgoing'

        # Format the document into the desired message structure
        formatted_message = {
            "id": doc.name,
            "message_id": doc.message_id or "",
            "user_id": doc.get("from") if flow == "Incoming" else doc.to,
            "from": doc.get("from"), 
            "to": doc.to,
            "content": {
                "text": doc.message,
                "type": doc.message_type,
                "attachments": json.loads(doc.attachment_files) if doc.attachment_files else [],
                "products": json.loads(doc.attachment_products) if doc.attachment_products else [],
                "fallbacks": json.loads(doc.attachment_fallbacks) if doc.attachment_fallbacks else [],
                "reels": json.loads(doc.attachment_reels) if doc.attachment_reels else []
            },
            "reaction": {
                "emoji": doc.reaction_emoji,
                "text": doc.reaction_text
            } if doc.reaction_emoji else None,
            "reply": {
                "is_reply": bool(doc.is_reply),
                "reply_to": doc.reply_to
            } if doc.is_reply else None,
            "referral": {
                "is_referral": bool(doc.is_referral),
                "ref": doc.ref,
                "source": doc.source,
                "type": doc.ref_type,
                "ad_id": doc.ad_id,
                "referrer_url": doc.referrer_url
            } if doc.is_referral else None,
            "quick_reply": {
                "is_quick_reply": bool(doc.is_quick_reply),
                "payload": doc.quick_reply
            } if doc.is_quick_reply else None,
            "metadata": {
                "platform": doc.platform,
                "platform_id": doc.page_id if doc.platform == "Messenger" else doc.instagram_id,
                "status": doc.status,
                "flow": doc.flow,
                "timestamp": doc.timestamp
            }
        }

        # frappe.logger().info(f"Formatted message to send event: {json.dumps(formatted_message)}")

        # Publish real-time event for the message
        frappe.publish_realtime(
            "one_message",
            formatted_message,
        )
    except Exception as e:
        frappe.logger().error(f"Error Sending Real-Time Message Event: {frappe.get_traceback()}")
        frappe.log_error("Error Sending Real-Time Message Event", frappe.get_traceback())

def emit_user_update_event(doc, method=None):
    try:
        user_update_event = {
            "user_id": doc.user_id,
            "platform": doc.platform,
            "name": doc.full_name,
            "username": doc.username,
            "gender": doc.gender,
            "profile_picture_url": doc.profile_picture_url,
            "last_interaction_timestamp": doc.last_interaction_timestamp,
            "unread_count": doc.unread_message_count
        }
        frappe.publish_realtime(
            "user_update",
            user_update_event,
        )
    except Exception as e:
        frappe.logger().error(f"Error Emitting User Update Event: {frappe.get_traceback()}")
        frappe.log_error("Error Emitting User Update Event", frappe.get_traceback())
