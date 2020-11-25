# -*- coding: utf-8 -*-
# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from functools import reduce

class CourseEnrollment(Document):
	def get_progress(self, student):
		"""
		Returns Progress of given student for a particular course enrollment

			:param self: Course Enrollment Object
			:param student: Student Object
		"""
		course = frappe.get_doc('Course', self.course)
		topics = course.get_topics()
		progress = []
		for topic in topics:
			progress.append(student.get_topic_progress(self.name, topic))
		if progress:
			return reduce(lambda x,y: x+y, progress) # Flatten out the List
		else:
			return []

	def validate_duplication(self):
		enrollment = frappe.get_all("Course Enrollment", filters={
			"student": self.student,
			"course": self.course,
			"program_enrollment": self.program_enrollment
		})
		if enrollment:
			frappe.throw(_("Student is already enrolled."))

	def add_quiz_activity(self, quiz_name, quiz_response, answers, score, status):
		try:
			result ={}
			# v is either True, False, "Essay" or [list of True and False]
			for k,v in answers.items():
				if isinstance(v,list):
					if sum(v) == len(v):
						result.update({
							k: 'Correct'
						})
					else:
						result.update({
							k: 'Wrong'
						})
				elif v == True:
					result.update({
						k: 'Correct'
					})
				elif v == False:
					result.update({
						k: 'Wrong'
					})
				else:
					result.update({
						k: 'Essay'
					})

			result_data = []
			item = {}
			for key in answers:
				item.clear()
				item = {}
				item['question'] = key
				if result[key] != "Essay":
					item['result_silid'] = result[key]
					item['quiz_result'] = result[key]
				else:
					item['quiz_result'] = 'Correct'

				if type(answers[key]) == list:
					item['evaluation_result'] = ", ".join('Correct' if is_correct else 'Wrong' for is_correct in answers[key])
				else:
					item['evaluation_result'] = result[key]

				selected_option = ""
				try:
					if not quiz_response[key]:
						item['selected_option'] = "Unattempted"
					elif isinstance(quiz_response[key], list):
						try:
							item['selected_option'] = ', '.join(frappe.get_value('Options', res, 'option') for res in quiz_response[key])
							selected_option = item['selected_option']
						except:
							selected_option = ', '.join(quiz_response[key])
							item['selected_option'] = ', '.join(quiz_response[key])
					else:
						item['selected_option'] = frappe.get_value('Options', quiz_response[key], 'option')
						selected_option = item['selected_option']
						if not item['selected_option']:
							item['selected_option'] = quiz_response[key]
				except:
					item['selected_option'] = "Unattempted"

				item['answer'] = selected_option or quiz_response[key]
				if type(item) == dict:
					result_data.append(item)
			quiz_info = None
			try:
				quiz_info = frappe.get_doc("Quiz", quiz_name)
			except:
				pass
			if quiz_info is not None:
				quiz_json = {
					"doctype": "Quiz Activity",
					"enrollment": self.name,
					"quiz": quiz_name,
					"quiz_title": quiz_info.title or "",
					"activity_date": frappe.utils.datetime.datetime.now(),
					"result": result_data,
					"score": score,
					"status": status,
					"course": quiz_info.subject or "",
					"program": quiz_info.program or "",
					"topic": quiz_info.topic or "",
					"quarter": quiz_info.quarter or "",
					"highest_possible_score": quiz_info.max_points or ""
				}
				quiz_activity = frappe.get_doc(quiz_json).insert(ignore_permissions = True)
				frappe.db.commit()
			else:
				quiz_json = {
					"doctype": "Quiz Activity",
					"enrollment": self.name,
					"quiz": quiz_name,
					"activity_date": frappe.utils.datetime.datetime.now(),
					"result": result_data,
					"score": score,
					"status": status,
				}
				quiz_activity = frappe.get_doc(quiz_json).insert(ignore_permissions=True)
				frappe.db.commit()
		except Exception as e:
			frappe.log_error(frappe.get_traceback())
			raw_data = {
				"quiz_name":quiz_name,
				"quiz_response": quiz_response,
				"answers": answers,
				"score": score,
				"status":status
			}

			quiz_info = None
			try:
				quiz_info = frappe.get_doc("Quiz", quiz_name)
			except:
				pass
			result_data = []
			if quiz_info is not None:
				quiz_json = {
					"doctype": "Quiz Activity",
					"enrollment": self.name,
					"quiz": quiz_name,
					"quiz_title": quiz_info.title or "",
					"activity_date": frappe.utils.datetime.datetime.now(),
					"result": result_data,
					"score": score,
					"status": status,
					"program": quiz_info.program or "",
					"topic": quiz_info.topic or "",
					"quarter": quiz_info.quarter or "",
					"highest_possible_score": quiz_info.max_points or ""
				}
			else:
				quiz_json = {
					"doctype": "Quiz Activity",
					"enrollment": self.name,
					"quiz": quiz_name,
					"activity_date": frappe.utils.datetime.datetime.now(),
					"result": result_data,
					"score": score,
					"status": status,
				}
			try:
				quiz_activity_log = frappe.get_doc({
					"doctype": "Quiz Activity Error Log",
					"raw_inputs": raw_data,
					"quiz_name": quiz_name,
					"quiz_activity_json": quiz_json
				}).insert(ignore_permissions=True)
			except:
				pass




	def add_activity(self, content_type, content):
		activity = check_activity_exists(self.name, content_type, content)
		if activity:
			return activity
		else:
			activity = frappe.get_doc({
				"doctype": "Course Activity",
				"enrollment": self.name,
				"content_type": content_type,
				"content": content,
				"activity_date": frappe.utils.datetime.datetime.now()
			})

			activity.insert(ignore_permissions=True)
			return activity.name

def check_activity_exists(enrollment, content_type, content):
	activity = frappe.get_all("Course Activity", filters={'enrollment': enrollment, 'content_type': content_type, 'content': content})
	if activity:
		return activity[0].name
	else:
		return None