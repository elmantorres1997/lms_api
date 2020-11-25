# -*- coding: utf-8 -*-
# Copyright (c) 2020, Wela School System and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from lms_api.lms_api.doctype.written_activity.written_activity import written_to_master_grade

class Article(Document):
	def validate(self):
		frappe.db.sql(f"UPDATE `tabMaster Grade` SET component='{self.classwork_category}', "
					  f"highest_possible_score='{self.highest_possible_score}',"
					  f"activity_title='{escape(self.title)}',"
					  f"activity_name='{self.name}',"
					  f"course='{escape(self.course)}' "
					  f"WHERE activity_name='{self.name}' OR activity_title='{self.name}'")
		frappe.db.commit()

	def get_article(self):
		pass

def escape(text):
	if text:
		return text.replace("'","\\'")
	return text

@frappe.whitelist()
def carry_over(docname):
	all_wa = frappe.db.sql(f"SELECT name FROM `tabWritten Activity` WHERE activity='{docname}'", as_dict=1)
	for wa in all_wa:
		written_activity = frappe.get_doc("Written Activity", wa['name'])
		written_to_master_grade(written_activity)

