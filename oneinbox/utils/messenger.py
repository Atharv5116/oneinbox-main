"""Webhook."""
import frappe
import json
import hmac
import hashlib
import pytz
from werkzeug.wrappers import Response
from datetime import datetime
from frappe.utils import format_datetime


@frappe.whitelist(allow_guest=True)
def webhook():
    """Meta webhook."""
    try:
        frappe.logger().info(f"Incoming request: {frappe.local.request.method} {frappe.local.form_dict}")
        if frappe.request.method == "GET":
            return validate()
        elif frappe.request.method == "POST":
            return log_webhook_entries()
        else:
            frappe.logger().error(f"Unsupported HTTP method: {frappe.request.method}")
            return Response("Unsupported HTTP method", status=405)
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error in Webhook Handling")
        return Response("Internal Server Error", status=500)

# def messaging_webhook():
# 	pass
	# // Check if a token and mode is in the query string of the request
	# if (mode && token) {
	#   // Check the mode and token sent is correct
	#   if (mode === "subscribe" && token === config.verifyToken) {
	#     // Respond with the challenge token from the request
	#     console.log("WEBHOOK_VERIFIED");
	#     res.status(200).send(challenge);
	#   } else {
	#     // Respond with '403 Forbidden' if verify tokens do not match
	#     res.sendStatus(403);
	#   }
	# }

# TODO: when user sets token and messagin setting. it should trigger verification request.
# USE: /app/subscriptionns endpoint 



def validate():
	"""Validate connection by webhook token verification"""
	hub_challenge = frappe.form_dict.get("hub.challenge")
	verify_token = frappe.form_dict.get("hub.verify_token")
	mode = frappe.form_dict.get("hub.mode")

	webhook_verify_token = frappe.db.get_single_value(
		"Messenger Config", "webhook_verify_token"
	)

	if verify_token != webhook_verify_token and mode != "subscribe":
		frappe.throw("Verify token does not match or webhook is not subscribed")

	return Response(hub_challenge, status=200)

# TODO: not called anywhere currently, to allow smooth testing.
def verify_signature():
    """Verify the signature of the incoming webhook request."""
    try:
        # Retrieve the signature from the request headers
        signature_header = frappe.request.headers.get("X-Hub-Signature-256")
        if not signature_header:
            frappe.logger().error("Missing X-Hub-Signature-256 header")
            frappe.throw("Missing X-Hub-Signature-256 header")

        # Retrieve the request payload
        payload = frappe.request.get_data()

        # Get the app secret from your configuration
        app_secret = frappe.db.get_single_value("Messenger Config", "app_secret")
        if not app_secret:
            frappe.logger().error("App secret not configured in Messenger Config")
            frappe.throw("App secret not configured")

        # Calculate the HMAC-SHA256 hash of the payload
        calculated_signature = "sha256=" + hmac.new(
            key=app_secret.encode("utf-8"),
            msg=payload,
            digestmod=hashlib.sha256
        ).hexdigest()

        # Compare the calculated signature with the one in the header
        if not hmac.compare_digest(calculated_signature, signature_header):
            frappe.logger().error("Invalid signature: Verification failed")
            frappe.throw("Invalid signature: Verification failed")

        # Signature is valid
        frappe.logger().info("Signature verification successful")
        return True

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error in Signature Verification")
        frappe.throw("Signature verification error")

def log_webhook_entries():
    """Log each entry in the Messenger Webhook Log with error handling."""
    try:
        data = frappe.local.form_dict
        frappe.logger().info(f"Webhook data received: {json.dumps(data)}")

        if not data.get("entry"):
            frappe.logger().error("No 'entry' field found in webhook data.")
            return Response("Bad Request: Missing 'entry' field", status=400)

        for entry in data.get("entry", []):
            frappe.logger().info(f"Processing entry: {entry}")
            log_doc = {
                "doctype": "Messenger Webhook Log",
                "object": data.get("object"),
                "timestamp": convert_epoch_to_datetime(entry.get("time")),
                # "event_type": determine_event_type(entry),
                "entry_status": "Pending",
                "event_data": json.dumps(entry)  # Store only the entry data
            }

            # Determine if the object is "page" or "instagram" and set appropriate fields
            if data.get("object") == "page":
                log_doc["page"] = entry.get("id")
            else:
                log_doc["instagram"] = entry.get("id")

            # Create and insert the log entry
            frappe.logger().info(f"Creating log entry with data: {log_doc}")
            log_entry = frappe.get_doc(log_doc)
            log_entry.insert(ignore_permissions=True)
            frappe.logger().info(f"Log entry created successfully: {log_entry.name}")

        return Response("Logged Successfully", status=200)

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error in Messenger Webhook")
        frappe.logger().error(f"Exception occurred: {str(e)}")
        return Response("Internal Server Error", status=500)

def convert_epoch_to_datetime(epoch_milliseconds, target_timezone='Asia/Kolkata'):
    epoch_seconds = epoch_milliseconds / 1000
    utc_datetime = datetime.fromtimestamp(epoch_seconds, tz=pytz.utc)

    # Convert UTC datetime to the target timezone
    target_tz = pytz.timezone(target_timezone)
    message_datetime = utc_datetime.astimezone(target_tz)

    frappe_datetime = message_datetime.strftime('%Y-%m-%d %H:%M:%S')  # Force correct format
    return frappe_datetime

# ============================ Deprecated Below Here====================================== 
# def determine_event_type(entry):
#     """Determine the type of event from an entry, with error handling."""
#     try:
#         for message in entry.get("messaging", []):
#             if "message" in message:
#                 return "Message Received"
#             elif "delivery" in message:
#                 return "Delivery Confirmation"
#             elif "read" in message:
#                 return "Read Receipt"
#             elif "reaction" in message:
#                 return "Reaction Added"
#     except KeyError as e:
#         frappe.log_error(f"Error determining event type: {str(e)}", "Webhook Event Type Error")
#     return "Unknown"


# NOTE: Inspiration from frappe_whatsapp. 
def receive_message():
	data = frappe.local.form_dict
	frappe.get_doc({
		"doctype": "Webhook Logs FB",
		"json_data": json.dumps(data)
	}).insert(ignore_permissions=True)

	if data["object"] == "instagram":
		return process_instagram_webook(data)

	messages = []
	# try:
	messages = data["entry"][0]["messaging"]
	# except KeyError:

	if messages:
		for item in messages:
			if "read" in item:
				# Set all the messages as read between these two conversation. by timestamp <
				page_id = data["entry"][0]["id"]
				from_message = item["sender"]["id"]
				to_message = item["recipient"]["id"]
	
				frappe.db.sql("""
									UPDATE `tabMessages_fb`
									SET `status` = "Read"
									Where `page_id` = %s
									and `from` = %s
									and `to` = %s
									and `status` IN ('Sent', 'Delivered')
									""", (page_id, to_message, from_message))
			
				frappe.db.commit() 
				return
				# Call async function and set messages read, and return the API
			elif "delivery" in item:
				delivered_message = item["delivery"]["mids"]

				if delivered_message:
					try:
						frappe.db.sql("""
								UPDATE `tabMessages_fb`
								SET `status` = "Delivered"
								WHERE `message_id` IN (%s)
						""" % ','.join(['%s'] * len(delivered_message)), tuple(delivered_message))
						frappe.db.commit()
					except Exception as e:
						frappe.log_error(frappe.get_traceback(), "Error updating message Delivery Status")
						frappe.throw(_("An error occurred while updating message status."))
				return

			doc = {
				"plateform": "page",
				"doctype": "Messages_fb",
				"flow": "Incoming",
				"from": item["sender"]["id"] if "sender" in item else "",
				"to": item["recipient"]["id"] if "recipient" in item else "",
				"page_id": data["entry"][0]["id"],
			}
		
			if "message_edit" in item:
				doc["message"] = item["message_edit"]["text"]
				doc["message_id"] = item["message_edit"]["mid"]
				# Call async function to update the message. 
			elif "reaction" in item: 
				doc["message_id"] = item["reaction"]["mid"]
				action = item["reaction"]["action"]
				if action == "react":
					doc["reaction_emoji"] = item["reaction"]["emoji"] # emoji 
					doc["reaction_text"] = item["reaction"]["reaction"] # text content describing emoji, in case emoji does not work

			if "quick_reply" in item:
				doc["is_quick_reply"] = True
				doc["quick_reply"] = item["quick_reply"]["payload"]
			if "reply_to" in item:
				doc["is_reply"] = True
				doc["reply_to"] = item["reply_to"]["mid"]
			if "attachments" in item:
				# TODO: what kind of attachments are these? file type attachments are below within messages.

				doc['attachments_json'] = json.dumps(item["attachments"])
			if "referral" in item:
				# TODO: referral data should be properly structured. right now it's just JSON stored. referral data shows where user sent message, ad, product etc. 
				doc["is_referral"] = True
				doc["referral_json"] = json.dumps(item["referral"])
			
			if "message" in item:
				doc["message_id"] = item["message"]["mid"] if "message" in item else ""
				if "text" in item["message"]:
					doc["message"] = item["message"]["text"]
				elif "attachments" in item["message"]:
					for file in item["message"]["attachments"]:
						file_type = file["type"]
						if file_type in ["image", "audio", "video", "file"]:
							doc["message_type"] = file_type
							file_url = file["payload"]["url"]
							# doc["attach"] = file_url

							# config = frappe.get_conf()

							# token = config.get("fb_page_token")
							# # url = f"{settings.url}/{settings.version}/"


							# # media_id = message[message_type]["id"]
							# headers = {
							# 	'Authorization': 'Bearer ' + token
							# }
							# response = requests.get(file_url)
							# print(response)
							# if response.status_code == 200:
								# media_data = response.json()
								# media_url = media_data.get("url")
								# mime_type = response.json()
								# file_extension = response.split('/')[1]

								# media_response = requests.get(media_url, headers=headers)
								# if media_response.status_code == 200:

							# 	file_data = response.content
							# 	file_name = f"{frappe.generate_hash(length=10)}"

							# 	doc["message"] = file_url #item[file_type].get("caption",f"/files/{file_name}")
							# 	doc["message_type"] = file_type
							# 	message_doc = frappe.get_doc(doc).insert(ignore_permissions=True)
							# 	file = frappe.get_doc(
							# 		{
							# 			"doctype": "File",
							# 			"file_name": file_name,
							# 			"attached_to_doctype": "Messages_fb",
							# 			"attached_to_name": message_doc.name,
							# 			"content": file_data,
							# 			"attached_to_field": "attach"
							# 		}
							# 	).save(ignore_permissions=True)
							# else:
							doc["attach"] = file_url
								# frappe.get_doc(doc).insert(ignore_permissions=True)
				# return
			if "reaction" in item:
				doc["reaction"] = json.dump(item["reaction"])
				doc["message_id"] = item["reaction"]["mid"]

			frappe.get_doc(doc).insert(ignore_permissions=True)
	return

def process_instagram_webook(data):
		messages = []
		# try:
		messages = data["entry"][0]["messaging"]
		# except KeyError:

		if messages:
			for item in messages:
				if "read" in item:
					# Set all the messages as read between these two conversation. by timestamp <
					page_id = data["entry"][0]["id"]
					from_message = item["sender"]["id"]
					to_message = item["recipient"]["id"]
		
					frappe.db.sql("""
										UPDATE `tabMessages_fb`
										SET `status` = "Read"
										Where `page_id` = %s
										and `from` = %s
										and `to` = %s
										and `status` IN ('Sent', 'Delivered')
										""", (page_id, to_message, from_message))
				
					frappe.db.commit() 
					return
					# Call async function and set messages read, and return the API
				elif "delivery" in item:
					delivered_message = item["delivery"]["mids"]

					if delivered_message:
						try:
							frappe.db.sql("""
									UPDATE `tabMessages_fb`
									SET `status` = "Delivered"
									WHERE `message_id` IN (%s)
							""" % ','.join(['%s'] * len(delivered_message)), tuple(delivered_message))
							frappe.db.commit()
						except Exception as e:
							frappe.log_error(frappe.get_traceback(), "Error updating message Delivery Status")
							frappe.throw(_("An error occurred while updating message status."))
					return
				
				if "is_deleted" in item:
					# TODO: turn the flag is deleted to true. 
					pass

				if "is_unsupported" in item:
					# TODO: turn the flag is_unsupported to true for non-supported media file
					pass

				# TODO: is_echo field handle in message. if message is sent from application to keep sync.
				flow = "Outgoing" if "is_echo" in item and "is_echo" == True else "Incoming"
				doc = {
					"plateform": "instagram",
					"doctype": "Messages_fb",
					"flow": flow,
					"from": item["sender"]["id"] if "sender" in item else "",
					"to": item["recipient"]["id"] if "recipient" in item else "",
					"page_id": data["entry"][0]["id"],
				}
			
				if "message_edit" in item:
					doc["message"] = item["message_edit"]["text"]
					doc["message_id"] = item["message_edit"]["mid"]
					# Call async function to update the message. 
				elif "reaction" in item: 
					doc["message_id"] = item["reaction"]["mid"]
					action = item["reaction"]["action"]
					if action == "react":
						doc["reaction_emoji"] = item["reaction"]["emoji"] # emoji 
						doc["reaction_text"] = item["reaction"]["reaction"] # text content describing emoji, in case emoji does not work
					if action == "unreact":
						# TODO: delete the message entry? or modify existing doc. would make sense to delete the entry.
						pass
				elif "postback" in item:
					# TODO: Ice braker messages, like button selection from temps.
					# "postback": {
					#   "mid":"MESSAGE-ID",           // ID for the message sent to your business
					#   "title": "SELECTED-ICEBREAKER-REPLY-OR-CTA-BUTTON",
					#   "payload": "CUSTOMER-RESPONSE-PAYLOAD",  // The payload with the option selected by the customer
					# }
					pass

				# TODO: Messaging Referral ?? in webhook


				if "quick_reply" in item:
					doc["is_quick_reply"] = True
					doc["quick_reply"] = item["quick_reply"]["payload"]
				if "reply_to" in item:
					doc["is_reply"] = True
					if "mid" in item["reply_to"]:
						doc["reply_to"] = item["reply_to"]["mid"]
					if "story" in item["reply_to"]:
						doc["reply_story_url"] = item["reply_to"]["story"]["url"]
						doc["reply_story_id"] = item["reply_to"]["story"]["id"]
				if "attachments" in item:
					# TODO: what kind of attachments are these? file type attachments are below within messages.

					doc['attachments_json'] = json.dumps(item["attachments"])
				if "referral" in item:
					# TODO: referral data should be properly structured. right now it's just JSON stored. referral data shows where user sent message, ad, product etc.
						# "referral": {              // Included when a customer clicks an Instagram Shop product
						#   "product": {
						#     "id": "PRODUCT-ID"
						# }      
			
						# "referral": {                   // Included when a customer clicks an CTD ad
						#   "ref": "REF-DATA-IN-AD-IF-SPECIFIED"
						#   "ad_id": AD-ID,
						#   "source": "ADS",
						#   "type": "OPEN_THREAD",
						#   "ads_context_data": {
						#     "ad_title": TITLE-FOR-THE-AD,
						#     "photo_url": IMAGE-URL-THAT-WAS-CLICKED,
						#     "video_url": THUMBNAIL-URL-FOR-THE-AD-VIDEO,
						#   }
						# }
					doc["is_referral"] = True
					doc["referral_json"] = json.dumps(item["referral"])
				
				if "message" in item:
					doc["message_id"] = item["message"]["mid"] if "message" in item else ""
					if "text" in item["message"]:
						doc["message"] = item["message"]["text"]
					elif "attachments" in item["message"]:
						for file in item["message"]["attachments"]:
							file_type = file["type"]
							if file_type in ["image", "audio", "video", "file"]:
								doc["message_type"] = file_type
								file_url = file["payload"]["url"]
								doc["attach"] = file_url
																																																																																																																		
				if "reaction" in item:
					doc["reaction"] = json.dump(item["reaction"])
					doc["message_id"] = item["reaction"]["mid"]

				frappe.get_doc(doc).insert(ignore_permissions=True)
		return


# 	messages = []
# 	try:
# 		messages = data["entry"][0]["changes"][0]["value"].get("messages", [])
# 	except KeyError:
# 		messages = data["entry"]["changes"][0]["value"].get("messages", [])

# 	if messages:
# 		for message in messages:
# 			message_type = message['type']
# 			is_reply = True if message.get('context') else False
# 			reply_to_message_id = message['context']['id'] if is_reply else None
# 			if message_type == 'text':
# 				frappe.get_doc({
# 					"doctype": "WhatsApp Message",
# 					"type": "Incoming",
# 					"from": message['from'],
# 					"message": message['text']['body'],
# 					"message_id": message['id'],
# 					"reply_to_message_id": reply_to_message_id,
# 					"is_reply": is_reply,
# 					"content_type":message_type
# 				}).insert(ignore_permissions=True)
# 			elif message_type == 'reaction':
# 				frappe.get_doc({
# 					"doctype": "WhatsApp Message",
# 					"type": "Incoming",
# 					"from": message['from'],
# 					"message": message['reaction']['emoji'],
# 					"reply_to_message_id": message['reaction']['message_id'],
# 					"message_id": message['id'],
# 					"content_type": "reaction"
# 				}).insert(ignore_permissions=True)
# 			elif message_type == 'interactive':
# 				frappe.get_doc({
# 					"doctype": "WhatsApp Message",
# 					"type": "Incoming",
# 					"from": message['from'],
# 					"message": message['interactive']['nfm_reply']['response_json'],
# 					"message_id": message['id'],
# 					"content_type": "flow"
# 				}).insert(ignore_permissions=True)
# 			elif message_type in ["image", "audio", "video", "document"]:
# 				settings = frappe.get_doc(
# 							"WhatsApp Settings", "WhatsApp Settings",
# 						)
# 				token = settings.get_password("token")
# 				url = f"{settings.url}/{settings.version}/"


# 				media_id = message[message_type]["id"]
# 				headers = {
# 					'Authorization': 'Bearer ' + token

# 				}
# 				response = requests.get(f'{url}{media_id}/', headers=headers)

# 				if response.status_code == 200:
# 					media_data = response.json()
# 					media_url = media_data.get("url")
# 					mime_type = media_data.get("mime_type")
# 					file_extension = mime_type.split('/')[1]

# 					media_response = requests.get(media_url, headers=headers)
# 					if media_response.status_code == 200:

# 						file_data = media_response.content
# 						file_name = f"{frappe.generate_hash(length=10)}.{file_extension}"

# 						message_doc = frappe.get_doc({
# 							"doctype": "WhatsApp Message",
# 							"type": "Incoming",
# 							"from": message['from'],
# 							"message_id": message['id'],
# 							"reply_to_message_id": reply_to_message_id,
# 							"is_reply": is_reply,
# 							"message": message[message_type].get("caption",f"/files/{file_name}"),
# 							"content_type" : message_type
# 						}).insert(ignore_permissions=True)

# 						file = frappe.get_doc(
# 							{
# 								"doctype": "File",
# 								"file_name": file_name,
# 								"attached_to_doctype": "WhatsApp Message",
# 								"attached_to_name": message_doc.name,
# 								"content": file_data,
# 								"attached_to_field": "attach"
# 							}
# 						).save(ignore_permissions=True)


# 						message_doc.attach = file.file_url
# 						message_doc.save()
# 			else:
# 				frappe.get_doc({
# 					"doctype": "WhatsApp Message",
# 					"type": "Incoming",
# 					"from": message['from'],
# 					"message_id": message['id'],
# 					"message": message[message_type].get(message_type),
# 					"content_type" : message_type
# 				}).insert(ignore_permissions=True)

# 	else:
# 		changes = None
# 		try:
# 			changes = data["entry"][0]["changes"][0]
# 		except KeyError:
# 			changes = data["entry"]["changes"][0]
# 		update_status(changes)
# 	return

# def update_status(data):
# 	"""Update status hook."""
# 	if data.get("field") == "message_template_status_update":
# 		update_template_status(data['value'])

# 	elif data.get("field") == "messages":
# 		update_message_status(data['value'])

# def update_template_status(data):
# 	"""Update template status."""
# 	frappe.db.sql(
# 		"""UPDATE `tabWhatsApp Templates`
# 		SET status = %(event)s
# 		WHERE id = %(message_template_id)s""",
# 		data
# 	)

# def update_message_status(data):
# 	"""Update message status."""
# 	id = data['statuses'][0]['id']
# 	status = data['statuses'][0]['status']
# 	conversation = data['statuses'][0].get('conversation', {}).get('id')
# 	name = frappe.db.get_value("WhatsApp Message", filters={"message_id": id})

# 	doc = frappe.get_doc("WhatsApp Message", name)
# 	doc.status = status
# 	if conversation:
# 		doc.conversation_id = conversation
# 	doc.save(ignore_permissions=True)