# -*- coding: utf-8 -*-
# Copyright (c) 2020, Wela School System and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from lms_api.lms_api.doctype.quiz_activity.quiz_activity import quiz_to_master_grade
from lms_api.lms_api.doctype.written_activity.written_activity import written_to_master_grade
import sys
import time
import datetime
class ScheduleMG(Document):
	pass

# bench --site all execute lms_api.lms_api.doctype.schedule_mg.schedule_mg.execute_schedules
@frappe.whitelist()
def execute_schedules():
	stop_time = datetime.datetime.now() + datetime.timedelta(minutes=4)

	schedules = frappe.db.sql("SELECT name,activity_type,activity_name FROM `tabSchedule MG` WHERE 1", as_dict=1)
	total_to_execute = len(schedules)
	count = 0
	for schedule in schedules:
		count+=1
		try:
			if schedule['activity_type'] == "Quiz Activity":
				activity = frappe.get_doc("Quiz Activity", schedule['activity_name'])
				quiz_to_master_grade(activity)

			else:
				activity = frappe.get_doc("Written Activity", schedule['activity_name'])
				written_to_master_grade(activity)
			frappe.db.sql(f"DELETE FROM `tabSchedule MG` WHERE name='{schedule['name']}'")
			frappe.db.commit()
		except Exception as e:
			frappe.log_error(frappe.get_traceback())
			pass


		sys.stdout.write('\r')
		sys.stdout.write(f"Progress: {count}/{total_to_execute}")
		sys.stdout.flush()
		if datetime.datetime.now() > stop_time:
			exit()

@frappe.whitelist()
def execute_schedules_nonstop():

	schedules = frappe.db.sql("SELECT name,activity_type,activity_name FROM `tabSchedule MG` WHERE 1", as_dict=1)
	total_to_execute = len(schedules)
	count = 0
	for schedule in schedules:
		count+=1
		try:
			if schedule['activity_type'] == "Quiz Activity":
				activity = frappe.get_doc("Quiz Activity", schedule['activity_name'])
				quiz_to_master_grade(activity)

			else:
				activity = frappe.get_doc("Written Activity", schedule['activity_name'])
				written_to_master_grade(activity)
			frappe.db.sql(f"DELETE FROM `tabSchedule MG` WHERE name='{schedule['name']}'")
			frappe.db.commit()
		except Exception as e:
			frappe.log_error(frappe.get_traceback())
			pass


		sys.stdout.write('\r')
		sys.stdout.write(f"Progress: {count}/{total_to_execute}")
		sys.stdout.flush()