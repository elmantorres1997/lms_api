# -*- coding: utf-8 -*-
# Copyright (c) 2020, Wela School System and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class AmendSectioning(Document):
	def on_submit(self):
		if self.delete_existing:
				# try:
			# Uncheck in Sectioning
			try:
				frappe.db.sql(
					f"DELETE FROM `tabEnrollees Silid` WHERE student='{self.student}'"
				)
			except:
				pass

			program_es = frappe.db.sql(f"SELECT name FROM `tabProgram Enrollment` "
									  f"WHERE `tabProgram Enrollment`.student='{self.student}' "
									  ,as_dict=1)
			for program_e in program_es:

				# Course Enrollment is not Submittable so delete immediately
				course_es = frappe.db.sql(f"SELECT name FROM `tabCourse Enrollment` "
										  f"WHERE `tabCourse Enrollment`.program_enrollment='{program_e['name']}' "
										  f"AND `tabCourse Enrollment`.student='{self.student}'",as_dict=True)
				for course_e in course_es:
					try:
						course_enrollment = frappe.get_doc("Course Enrollment", course_e['name'])
						course_enrollment.delete()
					except:
						pass
				try:
					frappe.db.commit()
				except:
					pass

				program_enrollment = frappe.get_doc("Program Enrollment", program_e['name'])
				try:
					try:
						if program_enrollment.docstatus==1:
							program_enrollment.cancel()
					except:
						pass
					program_enrollment.delete()
				except:
					pass


			get_student = frappe.db.sql(f"SELECT user FROM `tabStudent` WHERE name='{self.student}'")
			permission_es = frappe.db.sql(f"select name FROM `tabUser Permission` "
										 f"WHERE `tabUser Permission`.user='{get_student[0][0]}'"
										 f" AND allow='Program'", as_dict=1)
			for permission_e in permission_es:
				permission = frappe.get_doc("User Permission", permission_e['name'])
				# permission.cancel()
				try:
					permission.delete()
				except:
					pass

		courses = [self.program]
		programs = [self.program]
		for course in courses:
			exists_program = frappe.db.sql(f"SELECT name FROM `tabCourse` WHERE course_name='{course}'")

			if exists_program == ():
				frappe.get_doc({
					"doctype": "Course",
					"course_name": course
				}).insert(ignore_permissions=True)
				frappe.db.commit()

		for program in programs:
			exists_program = frappe.db.sql(
				f"SELECT name FROM `tabProgram Enrollment` WHERE program='{program}' AND student='{self.student}'")
			if exists_program == ():
				frappe.get_doc({
					"doctype": "Program Enrollment",
					"student": self.student,
					"academic_year": self.academic_year,
					"program": program,
					"enrollment_date": frappe.utils.get_datetime().date(),
					"docstatus": 1
				}).insert(ignore_permissions=True)
				frappe.db.commit()
			get_student = frappe.db.sql(f"SELECT user FROM `tabStudent` WHERE name='{self.student}'")
			exists_permission = frappe.db.sql(
				f"SELECT name FROM `tabUser Permission` WHERE user='{get_student[0][0]}' AND for_value='{program}'")
			if exists_permission == ():
				frappe.get_doc({
					"doctype": "User Permission",
					"user": get_student[0][0],
					"allow": "Program",
					"for_value": program
				}).insert(ignore_permissions=True)
				frappe.db.commit()

			try:
				parent = f"{program}-{self.academic_year}"
				exists_sectioning = frappe.db.sql(
					f"SELECT name FROM `tabEnrollees Silid` WHERE "
					f"student LIKE '%{self.student}%' "
					f"AND parent LIKE '%{parent}%' "
					f"AND docstatus LIKE '%1%' "
				)
				final_parent = frappe.db.sql(
					f"SELECT name FROM `tabSectioning` WHERE "
					f"name LIKE '%{parent}%' "
					f"AND docstatus='1'"
					,as_dict=1
				)
				enrollee_count = frappe.db.count("Enrollees Silid", {"parent": parent, "docstatus": "1"})
				if exists_sectioning == ():
					for final_p in final_parent:
						insert_into_sectioning = frappe.get_doc({
							"doctype": "Enrollees Silid",
							"student": self.student,
							"parentfield": "enrollees",
							"parenttype": "Sectioning",
							"section_check": 1,
							"docstatus": 1,
							"idx": (int(enrollee_count)+1) or "",
							"student_name": self.student_name,
							"parent": f"{final_p['name']}"
						}).insert(ignore_permissions=True)
						frappe.db.commit()
			except Exception as e:
				frappe.msgprint(e)
				pass

@frappe.whitelist()
def get_student_name(student):
	return frappe.get_doc("Student", student)