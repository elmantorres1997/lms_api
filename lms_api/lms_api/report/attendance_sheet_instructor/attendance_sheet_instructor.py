# Copyright (c) 2013, Wela School System and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

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
	instructors = frappe.db.sql(f"SELECT `tabUser`.full_name,`tabUser`.email FROM `tabUser` JOIN `tabHas Role`"
								f"ON `tabUser`.name=`tabHas Role`.parent  WHERE `tabHas Role`.role='Instructor'", as_dict=1)
	instructors_list = []
	for instructor in instructors:
		if instructor['email'] not in instructors_list:
			instructors_list.append(instructor['email'])

	if len(instructors_list) == 1:
		tuple_list = str(tuple(instructors_list))
		tuple_list = tuple_list.replace(",","")
	else:
		tuple_list = str(tuple(instructors_list))


	activity_logs = frappe.db.sql(
		f"SELECT full_name, operation, creation, CONCAT(full_name,DATE(creation)) as pledge  FROM `tabActivity Log` "
		f"WHERE user in {tuple_list} "
		f"AND  DATE(creation)>='{filters['date_range'][0]}' AND DATE(creation)<='{filters['date_range'][1]}' "
		f"AND operation='{filters['activity_type']}' "
		f"GROUP BY  pledge "
		f"ORDER BY creation DESC"
		, as_dict=1)
	for logs in activity_logs:
		if len(logs) != 0:
			active_logs.append(logs)

	sortedArray = sorted(
		active_logs,
		key=lambda x: x['creation'], reverse=True
	)
	for log in sortedArray:
		obj = {
			"fullname": log['full_name'],
			"activity": log['operation'],
			"timestamp": log['creation'].strftime("%B %d, %Y - %H:%M:%p")
		}
		data.append(obj)
	return columns, data
