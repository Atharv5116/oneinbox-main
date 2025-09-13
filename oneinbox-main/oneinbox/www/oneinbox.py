
from __future__ import unicode_literals
import frappe
import frappe.sessions
from frappe import _

import json
import re

no_cache = 1

SCRIPT_TAG_PATTERN = re.compile(r"\<script[^<]*\</script\>")
CLOSING_SCRIPT_TAG_PATTERN = re.compile(r"</script\>")


def get_context(context):
	csrf_token = frappe.sessions.get_csrf_token()
	# Manually commit the CSRF token here
	frappe.db.commit()  # nosemgrep

	if frappe.session.user == "Guest":
		boot = frappe.website.utils.get_boot_data()
	else:
		try:
			boot = frappe.sessions.get()
		except Exception as e:
			raise frappe.SessionBootFailed from e


	boot_json = frappe.as_json(boot, indent=None, separators=(",", ":"))
	boot_json = SCRIPT_TAG_PATTERN.sub("", boot_json)

	boot_json = CLOSING_SCRIPT_TAG_PATTERN.sub("", boot_json)
	boot_json = json.dumps(boot_json)

	context.update(
		{"build_version": frappe.utils.get_build_version(), "boot": boot_json, "csrf_token": csrf_token}
	)

	app_name = frappe.get_website_settings("app_name") or frappe.get_system_settings("app_name")

	if app_name and app_name != "Frappe":
		context["app_name"] = app_name + " | " + "OneInbox"

	else:
		context["app_name"] = "OneInbox"

	return context


# def get_context():
#     csrf_token = frappe.sessions.get_csrf_token()

#     # Manually commit the CSRF token here
#     frappe.db.commit()

#     try:
#       boot = frappe.sessions.get()
#     except Exception as e:
#       raise frappe.SessionBootFailed from e
    
#     boot_json = frappe.as_json(boot, indent=None, separators=(",", ":"))
#     context = frappe._dict()
#     context.boot = get_boot()
#     return context


@frappe.whitelist(methods=["POST"], allow_guest=True)
def get_context_for_dev():
    if not frappe.conf.developer_mode:
        frappe.throw("This method is only meant for developer mode")
    return json.loads(get_boot())

def get_boot():
    try:
      boot = frappe.sessions.get()
    except Exception as e:
      raise frappe.SessionBootFailed from e

    boot_json = frappe.as_json(boot, indent=None, separators=(",", ":"))
    boot_json = SCRIPT_TAG_PATTERN.sub("", boot_json)

    boot_json = CLOSING_SCRIPT_TAG_PATTERN.sub("", boot_json)
    boot_json = json.dumps(boot_json)

    return boot_json

def get_default_route():
    return "/oneinbox"