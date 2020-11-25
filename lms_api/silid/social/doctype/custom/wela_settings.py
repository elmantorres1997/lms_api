import frappe
from frappe.service import *

@frappe.whitelist()
def get_wela_settings():
    filters = { 'doctype': 'Wela Settings' }
    settings = execute_query("GET_WELA_SETTINGS",as_dict=1, filters=filters)
    print(settings)
    return settings
