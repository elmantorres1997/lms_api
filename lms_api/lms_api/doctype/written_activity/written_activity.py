# -*- coding: utf-8 -*-
# Copyright (c) 2020, Wela School System and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils.background_jobs import enqueue
from lms_api.silid.service.utils import dotdict

class WrittenActivity(Document):
	def validate(self):
		# is_activity = self.activity
		try:
			fullname = frappe.db.sql(
				f"SELECT `tabUser`.full_name FROM `tabUser` "
				f"WHERE `tabUser`.email='{self.student}'",as_dict=1
			)
			self.student_name = fullname[0]['full_name']

		except:
			pass

	def on_update(self):
		# enqueue("lms_api.lms_api.doctype.written_activity.written_activity.schedule_mg",queue='long', name=self.name)
		enqueue("lms_api.lms_api.doctype.written_activity.written_activity.written_to_master_grade",queue='long', self=self)

	def on_trash(self):
		if self.video:
			frappe.db.sql(f"DELETE FROM `tabSchedule MG` WHERE activity_name='{self.video}'")
		if self.activity:
			frappe.db.sql(f"DELETE FROM `tabSchedule MG` WHERE activity_name='{self.activity}'")


def schedule_mg(name):
	is_exist = frappe.get_all("Schedule MG",fields=['name'],filters={'activity_name': name})
	if len(is_exist) == 0:
		try:
			schedule_mg = frappe.get_doc({
				"doctype": "Schedule MG",
				"activity_type": "Written Activity",
				"activity_name": name
			})
			schedule_mg.insert(ignore_permissions=True)
			frappe.db.commit()
		except:
			pass

@frappe.whitelist()
def written_to_master_grade(self):
	# This will only be called when saving using Direct buttons save
	if (type(self)) == str:
		import json
		import ast
		try:
			self = json.loads(self)
		except:
			self = ast.literal_eval(self)
		self = dotdict(self)

	is_activity = self.activity

	"""INSERT ENTRY TO MASTER GRADE"""
	# Check if entry exist in Master Grade
	# Get student name through his/her email
	student_info = frappe.db.sql(f"SELECT name FROM `tabStudent` WHERE student_email_id='{self.student}'", as_dict=1)

	try:
		student_name = student_info[0]['name']
	except:
		student_name = ""
	try:
		if is_activity:
			is_exist = frappe.db.sql("""SELECT * FROM `tabMaster Grade` 
										WHERE student=%s
										AND student_name=%s
										 AND activity_name=%s""",
									 (student_info[0]['name'], self.student_name, self.activity), as_dict=1)
		else:
			is_exist = frappe.db.sql("""SELECT * FROM `tabMaster Grade` 
										WHERE student=%s AND student_name=%s AND activity_name=%s """,
									 (student_info[0]['name'], self.student_name, self.video), as_dict=1)
	except:
		is_exist = []

	# It does not exist so Create new Master Grade Entry
	# Get Quiz info
	link_type = ""
	quiz_info = None
	try:
		if is_activity:
			quiz_info = frappe.get_doc("Article", self.activity)
			link_type = "Article"
		else:
			quiz_info = frappe.get_doc("Video", self.video)
			link_type = "Video"
	except:
		pass
	# If exists just update the score

	try:
		if is_exist:  # check if student
			if quiz_info is not None:
				doc = frappe.get_doc("Master Grade", is_exist[0]['name'])
				doc.raw_score = self.grade or 0
				doc.course = self.subject
				doc.program = self.program
				doc.activity_name = self.activity or self.video
				doc.activity_title = self.title
				doc.activity_link_type = link_type
				doc.component = quiz_info.classwork_category
				doc.quarter = self.quarter or quiz_info.quarter
				doc.school_year = self.school_year or quiz_info.school_year
				doc.highest_possible_score = self.highest_possible_score or quiz_info.highest_possible_score
				doc.save(ignore_permissions=True)
				frappe.db.commit()
			else:
				doc = frappe.get_doc("Master Grade", is_exist[0]['name'])
				doc.raw_score = self.grade or 0
				doc.course = self.subject
				doc.program = self.program
				doc.quarter = self.quarter
				doc.activity_name = self.activity or self.video
				doc.activity_link_type = link_type
				doc.activity_title = self.title
				doc.school_year = self.school_year
				doc.highest_possible_score = self.highest_possible_score
				doc.save(ignore_permissions=True)
				frappe.db.commit()

		else:

			if quiz_info is not None:
				master_grade = frappe.get_doc({
					"doctype": "Master Grade",
					"student": student_name,
					"student_name": self.student_name,
					"activity_type": "Written Activity",
					"activity_link_type": link_type,
					"activity_name": self.activity or self.video,
					"activity_title": self.title,
					"raw_score": self.grade or 0,
					"highest_possible_score": quiz_info.highest_possible_score,
					"teacher": quiz_info.owner,
					"component": quiz_info.classwork_category,
					"quarter": quiz_info.quarter,
					"school_year": quiz_info.school_year,
					"course": self.subject,
					"program": self.program
				})
				master_grade.insert(ignore_permissions=True)
				frappe.db.commit()
			else:
				master_grade = frappe.get_doc({
					"doctype": "Master Grade",
					"student": student_name,
					"student_name": self.student_name,
					"activity_type": "Written Activity",
					"activity_link_type": link_type,
					"activity_name": self.activity or self.video,
					"activity_title": self.title,
					"raw_score": self.grade or 0,
					"course": self.subject,
					"program": self.program
				})
				master_grade.insert(ignore_permissions=True)
				frappe.db.commit()
	except Exception as e:
		frappe.log_error(frappe.get_traceback())
		pass

@frappe.whitelist()
def get_subject_filters():
	entries = frappe.get_all("Written Activity", fields=['distinct subject'], filters={"owner": frappe.session.user})
	return entries

@frappe.whitelist()
def get_subject_filters_teacher():
	entries = frappe.get_all("User Permission", fields=['distinct for_value as subject'],
							 filters={"allow": "Course", "user": frappe.session.user}, limit_page_length=1000)
	return entries