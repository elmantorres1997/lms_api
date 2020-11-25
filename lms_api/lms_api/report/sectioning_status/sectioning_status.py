# Copyright (c) 2013, Wela School System and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	columns = [
		{
			"label": "Student Name",
			'width': 250,
			"fieldname": "fullname"
		},
	]
	student_list = frappe.get_all("Student", fields=['*'])
	if filters['status'] == "Sectioned":
		columns.append(
			{
				"label": "Section",
				'width': 250,
				"fieldname": "section"
			}
		)
		columns.append(
			{
				"label": "Permission",
				'width': 250,
				"fieldname": "permission"
			}
		)
		for student in student_list:
			email = escape(student['user'])
			is_program_enrolled = frappe.db.sql(f"SELECT * FROM `tabProgram Enrollment` WHERE student='{student.name}' AND docstatus=1", as_dict=1)
			no_permission = []
			for program in is_program_enrolled:
				is_user_permission = frappe.db.sql(f"SELECT * FROM `tabUser Permission` WHERE user='{email}' AND allow='Program' AND for_value='{program['program']}'", as_dict=1)
				if len(is_user_permission) > 0:
					first_name = student.first_name if student.first_name else ""
					last_name = student.last_name if student.last_name else ""
					full_name = first_name + " " + last_name
					data.append({
						"fullname": full_name,
						"section": program['program'],
						"permission": "<span style='color:green'>Has Permission</span>"
					})
				else:
					first_name = student.first_name if student.first_name else ""
					last_name = student.last_name if student.last_name else ""
					full_name = first_name + " " + last_name
					no_permission.append({
						"fullname": full_name,
						"section": program['program'],
						"permission": "<span style='color:red'>No Permission</span>"
					})
			for no_perm in no_permission:
				data.insert(0, no_perm)
	else:
		columns.append(
			{
				"label": "Grade Level",
				'width': 250,
				"fieldname": "grade_level"
			}
		)
		for student in student_list:
			is_program_enrolled = frappe.db.sql(f"SELECT * FROM `tabProgram Enrollment` WHERE student='{student.name}' AND docstatus=1",as_dict=1)

			if len(is_program_enrolled) == 0:
				first_name = student.first_name if student.first_name else ""
				last_name = student.last_name if student.last_name else ""
				full_name = first_name + " " + last_name
				data.append({
					"fullname": full_name,
					"grade_level": student['level']
				})
	return columns, data

def escape(text):
	if text:
		return text.replace("'","\\'")
	return text