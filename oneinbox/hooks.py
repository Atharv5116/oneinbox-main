from frappe import __version__ as frappe_version

app_name = "oneinbox"
app_title = "One Inbox"
app_publisher = "RedSoft Solutions Pvt. Ltd."
app_description = "Single Inbox for Facebook Messenger, Instagram DM & Whatsapp Messages"
app_email = "dev@redsoftware.in"
app_license = "MIT"
# required_apps = []

add_to_apps_screen = [
	{
		"name": "oneinbox",
		# "logo": "/assets/crm/images/logo.svg",
		"title": "One Inbox",
		"route": "/oneinbox",
		"has_permission": "oneinbox.utils.api.check_app_permission",
	}
]


# is_frappe_above_v13 = int(frappe_version.split('.')[0]) > 13

# Includes in <head>
# ------------------

# # include js, css files in header of desk.html
# app_include_css = ['oneinbox.bundle.css'] if is_frappe_above_v13 else [
#     '/assets/css/oneinbox.css']
# app_include_js = ['oneinbox.bundle.js'] if is_frappe_above_v13 else [
#     '/assets/js/oneinbox.js']

# # include js, css files in header of web template
# web_include_css = ['oneinbox.bundle.css'] if is_frappe_above_v13 else [
#     '/assets/css/oneinbox.css']
# web_include_js = ['oneinbox.bundle.js'] if is_frappe_above_v13 else [
#     '/assets/js/oneinbox.js']


# sounds = [
#     {'name': 'chat-notification', 'src': '/assets/oneinbox/sounds/chat-notification.mp3', 'volume': 0.2},
#     {'name': 'chat-message-send', 'src': '/assets/oneinbox/sounds/chat-message-send.mp3', 'volume': 0.2},
#     {'name': 'chat-message-receive', 'src': '/assets/oneinbox/sounds/chat-message-receive.mp3', 'volume': 0.5}
# ]

doc_events = {
    "Messenger Message": {
        "before_save": "oneinbox.utils.messanger_user.ensure_profile_exists",
        "after_insert": "oneinbox.utils.message_send.process_message",
        "on_update": "oneinbox.utils.events.send_message_event"
    },
    "Messenger Webhook Log": {
        "after_insert": "oneinbox.utils.message_entry.process_webhook_log"
    },
    "Messenger User": {
        "on_update": "oneinbox.utils.events.emit_user_update_event"
    }
}

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/oneinbox/css/oneinbox.css"
# app_include_js = "/assets/oneinbox/js/oneinbox.js"

# include js, css files in header of web template
# web_include_css = "/assets/oneinbox/css/oneinbox.css"
# web_include_js = "/assets/oneinbox/js/oneinbox.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "oneinbox/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "oneinbox/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

website_route_rules = [
	{"from_route": "/oneinbox/<path:app_path>", "to_route": "oneinbox"},
]

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "oneinbox.utils.jinja_methods",
#	"filters": "oneinbox.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "oneinbox.install.before_install"
# after_install = "oneinbox.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "oneinbox.uninstall.before_uninstall"
# after_uninstall = "oneinbox.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "oneinbox.utils.before_app_install"
# after_app_install = "oneinbox.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "oneinbox.utils.before_app_uninstall"
# after_app_uninstall = "oneinbox.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "oneinbox.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"oneinbox.tasks.all"
#	],
#	"daily": [
#		"oneinbox.tasks.daily"
#	],
#	"hourly": [
#		"oneinbox.tasks.hourly"
#	],
#	"weekly": [
#		"oneinbox.tasks.weekly"
#	],
#	"monthly": [
#		"oneinbox.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "oneinbox.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "oneinbox.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "oneinbox.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["oneinbox.utils.before_request"]
# after_request = ["oneinbox.utils.after_request"]

# Job Events
# ----------
# before_job = ["oneinbox.utils.before_job"]
# after_job = ["oneinbox.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"oneinbox.auth.validate"
# ]

website_route_rules = [{'from_route': '/oneinbox/<path:app_path>', 'to_route': 'oneinbox'},]
website_route_rules = [{'from_route': '/oichat/<path:app_path>', 'to_route': 'oichat'},]
