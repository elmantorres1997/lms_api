# -*- coding: utf-8 -*-
# Copyright (c) 2020, Wela School System and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class TimeLimit(Document):
	pass


@frappe.whitelist()
def set_limit(content_name, time_started,content_title=""):
	unique_name = f"{content_name}-{frappe.session.user}"
	user_roles = frappe.get_roles(frappe.session.user)
	if "Instructor" not in user_roles and "Student" in user_roles:
		create_time_limit = frappe.get_doc({
			"doctype": "Time Limit",
			"quiz_taker": unique_name,
			"user": frappe.session.user,
			"quiz_code": content_name,
			"quiz_title": content_title,
			"countdown": time_started
		}).insert(ignore_permissions=True)
		frappe.db.commit()


@frappe.whitelist()
def get_limit(content_name):
	unique_name = f"{content_name}-{frappe.session.user}"

	is_exist = frappe.db.sql(f"SELECT name FROM `tabTime Limit` WHERE name='{unique_name}'",as_dict=1)
	if is_exist:
		time_limit = frappe.get_doc("Time Limit", unique_name)
		return time_limit.countdown
	return None

