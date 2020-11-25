# -*- coding: utf-8 -*-
# Copyright (c) 2020, Wela School System and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class TeacherAssignment(Document):
	def on_submit(self):
		self.instructor = escape(self.instructor)
		for course in self.subjects:
			course_parent = escape(course.course)
			teacher = frappe.get_doc({
				"doctype": "Teachers",
				"parent": course.course or "",
				"parentfield": "teachers",
				"parenttype": "Course",
				"teacher": self.instructor
			}).insert(ignore_permissions=True)
			frappe.db.commit()

			exists_permission = frappe.db.sql(
				f"SELECT name FROM `tabUser Permission` WHERE user='{self.instructor}' AND allow='Course' AND for_value='{course_parent}'", as_dict=1)
			if len(exists_permission) == 0:
				frappe.get_doc({
					"doctype": "User Permission",
					"user": self.instructor,
					"allow": "Course",
					"for_value": course.course
				}).insert(ignore_permissions=True)
				frappe.db.commit()

			if self.program_permission:
				program_lists = frappe.db.sql(
					f"SELECT parent FROM `tabProgram Course` WHERE course='{course_parent}'",as_dict=1
				)

				for program_list in program_lists:

					program = escape(program_list['parent'])

					exist_program_permission = frappe.db.sql(
						f"SELECT name FROM `tabUser Permission` WHERE user='{self.instructor}' AND allow='Program' AND for_value='{program}'",as_dict=1
					)
					if len(exist_program_permission) == 0:
						frappe.get_doc({
							"doctype": "User Permission",
							"user": self.instructor,
							"allow": "Program",
							"for_value": program
						}).insert(ignore_permissions=True)
						frappe.db.commit()

		frappe.db.commit()

	def on_cancel(self):
		self.instructor = escape(self.instructor)

		# Delete old courses
		frappe.db.sql(
			f"DELETE FROM tabTeachers WHERE teacher='{self.instructor}'"
		)
		frappe.db.commit()

		for course in self.subjects:
			course_parent = escape(course.course)


			try:
				frappe.db.sql(f"DELETE FROM `tabUser Permission` WHERE `tabUser Permission`.user='{self.instructor}' AND allow='Course' AND for_value='{course_parent}'")

				program_lists = frappe.db.sql(
					f"SELECT parent FROM `tabProgram Course` WHERE course='{course_parent}'", as_dict=1
				)
				for program_list in program_lists:
					program = escape(program_list['parent'])
					frappe.db.sql(
						f"DELETE FROM `tabUser Permission` WHERE `tabUser Permission`.user='{self.instructor}' AND allow='Program' AND for_value='{program}'")
					frappe.db.commit()
			except:
				pass

def escape(text):
	if text:
		return text.replace("'","\\'")
	return text