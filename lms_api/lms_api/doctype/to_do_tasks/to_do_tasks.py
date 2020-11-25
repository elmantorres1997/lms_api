# -*- coding: utf-8 -*-
# Copyright (c) 2020, Wela School System and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ToDoTasks(Document):
	pass

@frappe.whitelist()
def get_link(content_id,task_type):
	if task_type == "Quiz":
		infos = frappe.get_all(task_type,fields =['program','subject','topic','name'],filters={"content_silid":content_id},limit_page_length=1)
	else:
		infos = frappe.get_all(task_type,fields =['program','course','topic','name'],filters={"content_silid":content_id},limit_page_length=1)
	link_template = ""
	if infos:
		if task_type == "Quiz":
			link_template = f"/lms/content?program={infos[0].program}&course={infos[0].subject}&topic={infos[0].topic}&type=Quiz&content={infos[0].name}"
		elif task_type == "Article":
			link_template = f"/lms/content?program={infos[0].program}&course={infos[0].course}&topic={infos[0].topic}&type=Article&content={infos[0].name}"
		else:
			link_template = f"/lms/content?program={infos[0].program}&course={infos[0].course}&topic={infos[0].topic}&type=Video&content={infos[0].name}"

	return link_template


@frappe.whitelist()
def get_subject_filters():
	entries = frappe.get_all("To Do Tasks", fields=['distinct course'], filters={"owner": frappe.session.user})
	return entries