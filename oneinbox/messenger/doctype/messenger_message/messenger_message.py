# Copyright (c) 2024, RedSoft Solutions Pvt. Ltd. and contributors
# For license information, please see license.txt
import json
import frappe
from frappe.model.document import Document
from frappe.integrations.utils import make_post_request


# {
#   "recipient_id": "1234567890",  // PSID or Instagram-scoped user ID
#   "platform": "Messenger",      // "Messenger" or "Instagram"
#   "message_type": "text",       // "text", "media", "reaction", "sticker"
#   "message": {
#     "text": "Hello, this is a test message!",  // For text messages
#     "attachment": {
#         "type": "",
#         "url": ""

#     }
#     # "sticker_type": null                       // For stickers (e.g., "like_heart")
#     "reply_to": null,  // Message ID being replied to (optional)
#   },
# #   "meta_data": {                // Additional metadata (optional)
# #     "notification_type": "REGULAR",  // "REGULAR", "SILENT_PUSH", "NO_PUSH"
# #     "tag": "HUMAN_AGENT"             // Tag for messages outside the 24-hour window
# #   }
# }
# Emoji
# {"object": "page", "entry": [{"time": 1723573259440, "id": "371024009436368", "messaging": [{"sender": {"id": "8130382090340794"}, "recipient": {"id": "371024009436368"}, "timestamp": 1723573258697, "message": {"mid": "m_3iu-SALivxmSoXSotZyFc0NMoF8eTmEN2YoR5ATAdnriV94FbwvUd5BRCrpvder3v-N3SzTaDjFVWEeJef6o1w", "text": "\ud83d\ude03"}}]}], "cmd": "oneinbox.utils.messenger.webhook"}

# Message Read
# {"object": "page", "entry": [{"time": 1723572732543, "id": "371024009436368", "messaging": [{"sender": {"id": "8130382090340794"}, "recipient": {"id": "371024009436368"}, "timestamp": 1723572730200, "read": {"watermark": 1723572729746}}]}], "cmd": "oneinbox.utils.messenger.webhook"}

# Message Delivery 
# {"object": "page", "entry": [{"time": 1723572268628, "id": "371024009436368", "messaging": [{"sender": {"id": "8130382090340794"}, "recipient": {"id": "371024009436368"}, "timestamp": 1723572268190, "delivery": {"mids": ["m_a1RLKsxJ0xEWQDNAi9EI-kNMoF8eTmEN2YoR5ATAdnpi9qDwqm2b0T9LoEhypwVSqaIUpZOGK1-X2nd9Z79z6w"], "watermark": 1723572267515}}]}], "cmd": "oneinbox.utils.messenger.webhook"}

# Message Edits
# {"object": "page", "entry": [{"time": 1723574672722, "id": "0", "messaging": [{"sender": {"id": "12334"}, "recipient": {"id": "23245"}, "timestamp": "1527459824", "message_edit": {"mid": "test_message_id", "text": "test_message"}}]}], "cmd": "oneinbox.utils.messenger.webhook"}

#  Webhook response
# {"object":"page","entry":[{"time":1723486611083,"id":"371024009436368","messaging":[{"sender":{"id":"8130382090340794"},"recipient":{"id":"371024009436368"},"timestamp":1723486609684,"message":{"mid":"m_i4mymtmxNp9BZDc1F5O9WkNMoF8eTmEN2YoR5ATAdnq06JV30DOmNLCucwmzjOVWkdcfAE7hqRBNRomAGsZH0Q","text":"this is test message"}}]}],"cmd":"oneinbox.utils.messenger.webhook"}

# Reaction
# Form Dict: {'object': 'page', 'entry': [{'time': 1723573250138, 'id': '371024009436368', 'messaging': [{'sender': {'id': '8130382090340794'}, 'recipient': {'id': '371024009436368'}, 'timestamp': 1723573249974, 'reaction': {'mid': 'm_OdGjlso_wA8JlDvsMtqwVkNMoF8eTmEN2YoR5ATAdnqJ4sm4l8EMc4rubf3jgeb2aHdwGct9NyUFc0t3bguY3Q', 'action': 'unreact'}}]}], 'cmd': 'oneinbox.utils.messenger.webhook'}

# file type
    # image
    # video
    # audio
    # file



class MessengerMessage(Document):
    """Message Send"""
    
    # def before_insert(self):
    #     """Send message."""
        # config = frappe.get_conf()

        # config = frappe.get_doc("Messenger Config")
        # if (config.webhook_verify_token)
        # if (config.enabled is not True):
        #     frappe.throw("Please Enable Messenger Config to send messages")

        # if self.flow == "Outgoing" and self.message_type != "Template":
        #     if self.attach and not self.attach.startswith("http"):
        #         link = frappe.utils.get_url() + "/" + self.attach
        #     else:
        #         link = self.attach

        #     data = {
        #         # "messaging_product": "Me",
        #         "recipient": {
        #      	    	"id": self.to
		# 						},
        #         "messaging_type": "MESSAGE_TAG",
        #         "tag": "HUMAN_AGENT",
        #         "notification_type": "REGULAR", # Default
        #         "access_token": config.access_token # Hardcoded for development.
                          
        #     }
        #     # print(data)
        #     # if self.is_reply and self.reply_to:
        #     #     data["context"] = {"message_id": self.reply_to}
        #     if self.message_type in ["file", "image", "video"]:
        #         data["message"] ={
        #           	"attachment": {
        #                     "type": self.message_type.lower(),
        #                     "payload": {
        #                         "url": link,
        #                         # "is_reusable": True,
        #                     }
        #                 }
        #     		}
        #     elif self.message_type == "reaction":
        #         data["reaction"] = {
        #             "mid": self.reply_to_message_id,
        #             "emoji": self.message,
        #         }
        #     elif self.message_type == "text":
        #         data["message"] = {
        #         	"text": self.message
		# 						}

        #     try:
        #         self.notify(data, config)
        #         self.status = "Sending"
        #     except Exception as e:
        #         self.status = "Fail"
        #         frappe.throw(f"Failed to send message {str(e)}")
        # elif self.type == "Outgoing" and self.message_type == "Template" and not self.message_id:
        #     self.send_template()

    # def notify(self, data, config):
    #     """Notify."""
    #     # settings = frappe.get_doc(
    #     #     "WhatsApp Settings",
    #     #     "WhatsApp Settings",
    #     # )
    #     # token = settings.get_password("token")
				
    #     access_token = data.get("access_token")

    #     headers = {
    #         "authorization": f"Bearer {access_token}",
    #         "content-type": "application/json",
    #     }
    #     url_type = f"messages?access_token={access_token}" if "attachment" in data["message"] else "messages"
    #     try:
    #         print(data)
    #         response = make_post_request(
    #             f"{config.meta_url}/{config.meta_api_version}/{self.page_id}/{url_type}",
    #             headers=headers,
    #             data=json.dumps(data),
    #         )
    #         print('return message')
    #         print(response)
    #         self.message_id = response["message_id"] if "message_id" in response else ''
    #         self.status = "Sent"

    #     except Exception as e:
    #         print("Error during Image sending")
    #         print(e)
    #         res = frappe.flags.integration_request.json()["error"]
    #         error_message = res.get("Error", res.get("message"))
    #         frappe.get_doc(
    #             {
    #                 "doctype": "Webhook Logs FB",
    #                 "template": "Text Message",
    #                 "meta_data": frappe.flags.integration_request.json(),
    #             }
    #         ).insert(ignore_permissions=True)

    #         frappe.throw(msg=error_message, title=res.get("error_user_title", "Error"))
