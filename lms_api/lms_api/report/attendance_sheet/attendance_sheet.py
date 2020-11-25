# Copyright (c) 2013, Wela School System and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe.service import  *
def execute(filters=None):
	columns, data = [], []
	active_logs = []
	columns = [
		{
			"label": "Fullname",
			'width': 250,
			"fieldname": "fullname"
		},
		{
			"label": "Activity",
			'width': 250,
			"fieldname": "activity"
		},
		{
			"label": "Timestamp",
			'width': 250,
			"fieldname": "timestamp"
		}
	]
	not_empty = ["`tabActivity Log`.operation"]
	try:
		print(filters['program'])
		program_list = frappe.db.sql(
			f"SELECT student FROM `tabProgram Enrollment` WHERE program='{filters['program']}'",as_dict=1
		)
	except:
		program_list = frappe.db.sql(
			f"SELECT student FROM `tabProgram Enrollment`", as_dict=1
		)

	program_list_list = []
	for program in program_list:
		if program['student'] not in program_list_list:
			program_list_list.append(program['student'])

	if len(program_list_list) == 1:
		program_list_tuple = str(tuple(program_list_list))
		program_list_tuple = program_list_tuple.replace(",","")
	else:
		program_list_tuple = str(tuple(program_list_list))
	if program_list_tuple:
		student_info = frappe.db.sql(f"SELECT user, student_email_id FROM `tabStudent` WHERE name in {program_list_tuple}",as_dict=1)
	else:
		columns = []
		data = []
		return columns, data

	student_list = []
	for student in student_info:
		if student['user'] not in student_list:
			student_list.append(student['user'])

	if len(student_list) == 1:
		student_list_tuple = str(tuple(student_list))
		student_list_tuple = student_list_tuple.replace(",","")
	else:
		student_list_tuple = str(tuple(student_list))

	if len(student_list) >0:
		activity_logs = frappe.db.sql(
			f"SELECT full_name, operation, creation FROM `tabActivity Log` "
			f"WHERE user in {student_list_tuple} "
			f"AND  DATE(creation)='{filters['date_sect']}' "
			f"AND operation='{filters['activity_type']}' "
			f"GROUP BY full_name "
			f"ORDER BY creation DESC"
		,as_dict=1)
		for logs in activity_logs:
			if len(logs) != 0:
				active_logs.append(logs)



	sortedArray = sorted(
		active_logs,
		key=lambda x: x['creation'], reverse=True
	)

	print(sortedArray)
	for log in sortedArray:
		obj = {
			"fullname": log['full_name'],
			"activity": log['operation'],
			"timestamp": log['creation'].strftime("%B %d, %Y - %H:%M:%p")
		}
		data.append(obj)

	res = {
		"fullname": "<b>Total</b>",
		"activity": f"<b>{filters['program']}</b>",
		"timestamp": f"<b>{len(active_logs)}/{len(program_list)}</b>",

	}
	data.append(res)

	return columns, data
