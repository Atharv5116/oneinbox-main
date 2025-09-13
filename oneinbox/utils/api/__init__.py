import frappe

def check_app_permission():
	if frappe.session.user == "Administrator":
		return True

	roles = frappe.get_roles()
	if any(role in ["System Manager", "Sales User", "Sales Manager", "Sales Master Manager"] for role in roles):
		return True

	return False