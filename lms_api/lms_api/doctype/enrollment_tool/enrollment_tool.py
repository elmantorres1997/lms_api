# -*- coding: utf-8 -*-
# Copyright (c) 2020, Wela School System and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class EnrollmentTool(Document):

	def get_students(self):
		students = frappe.db.sql(f"select student, student_name from `tabProgram Enrollment` "
								 f"where program='{escape(self.program)}' and docstatus=1", as_dict=1)
		return students

	def enroll_students(self):
		total = len(self.select_student)
		return_value = []
		for i, stud in enumerate(self.select_student):
			frappe.publish_realtime("program_enrollment_tool", dict(progress=[i+1, total]), user=frappe.session.user)

			if stud.student:
				# get Student Info
				student_name = frappe.db.get_value("Student", stud.student, "title")
				prog_enrollment = frappe.new_doc("Program Enrollment")
				prog_enrollment.student = stud.student
				prog_enrollment.student_name = student_name
				prog_enrollment.program = self.program
				prog_enrollment.academic_year = self.school_year
				prog_enrollment.submit()
				return_value.append({
					"student": stud.student,
					"student_name": student_name
				})

			frappe.db.commit()
		return return_value

	def get_programs(self):
		if frappe.session.user != "Administrator":
			assigned_subjects = frappe.db.sql(
				f"SELECT distinct course FROM `tabCourses` JOIN `tabTeacher Assignment` ON `tabCourses`.parent=`tabTeacher Assignment`.name "
				f"WHERE `tabCourses`.parent LIKE '%{frappe.session.user}%' "
				f"AND `tabTeacher Assignment`.docstatus=1 ", as_dict=1
			)
			subject_list = []
			for subject in assigned_subjects:
				if subject['course'] not in subject_list:
					subject_list.append(subject['course'])
			published_programs = []
			published_courses = [frappe.get_all("Program Course", fields=['distinct parent', 'name'], filters=[["course", "in", tuple(subject_list)]], group_by="parent")]
			for programs in published_courses:
				for program in programs:
					if program['parent'] not in published_programs:
						published_programs.append(program['parent'])
		else:

			programs = frappe.db.sql("SELECT name from `tabProgram` WHERE 1", as_dict=1)
			published_programs = []
			for prog in programs:
				published_programs.append(prog['name'])

		return published_programs

def escape(text):
	if text:
		return text.replace("'","\\'")
	return text