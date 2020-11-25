# -*- coding: utf-8 -*-
# Copyright (c) 2020, Wela School System and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils.background_jobs import enqueue
import re
from lms_api.silid.service.utils import dotdict

class QuizActivity(Document):
	def validate(self):
		try:
			student_info = frappe.get_doc("Student", self.student)
			first_name = student_info.first_name or ""
			last_name = student_info.last_name or ""
			final_name = first_name + " " + last_name
			self.student_name = final_name.title()

			self.student_name = re.sub('[^A-Za-z0-9 ]+', '', self.student_name)
		except:
			pass

		# enqueue("lms_api.lms_api.doctype.quiz_activity.quiz_activity.schedule_mg",queue='long', name=self.name)
		enqueue("lms_api.lms_api.doctype.quiz_activity.quiz_activity.quiz_to_master_grade",queue='long', self=self)

	def after_insert(self):
		enqueue("lms_api.lms_api.doctype.quiz_activity.quiz_activity.enqueue_mark_to_do_done",
				queue='long', doc=self)

	def on_trash(self):
		if self.quiz:
			frappe.db.sql(f"DELETE FROM `tabSchedule MG` WHERE activity_name='{self.name}' OR activity_name='{self.quiz}'")

def enqueue_mark_to_do_done(doc):
	content_silid = frappe.get_all("Quiz", fields=['content_silid'], filters={"name": doc.quiz},
									   limit_page_length=1)
	if content_silid:
		get_to_dos = frappe.get_all("To Do Tasks", fields=['name'], filters={"content_id": content_silid[0]['content_silid'],"owner":frappe.session.user})
		for to_mark in get_to_dos:
			# to_do = frappe.delete_doc("To Do Tasks", to_mark['name'],ignore_permissions=True,force=1)
			frappe.db.sql("""update `tabTo Do Tasks` set status='Done' where name=%s""", (to_mark['name']))
			frappe.db.commit()

def schedule_mg(name):
	is_exist = frappe.get_all("Schedule MG",fields=['name'],filters={'activity_name': name})
	if len(is_exist) == 0:
		schedule_mg = frappe.get_doc({
			"doctype": "Schedule MG",
			"activity_type": "Quiz Activity",
			"activity_name": name
		})
		schedule_mg.insert(ignore_permissions=True)
		frappe.db.commit()

@frappe.whitelist()
def quiz_to_master_grade(self):
	# This will only be called when saving using Direct buttons save
	if (type(self)) == str:
		import json
		import ast
		try:
			self = json.loads(self)
		except:
			self = ast.literal_eval(self)
		self = dotdict(self)
	try:
		frappe.db.sql("""update `tabQuiz Activity` set student_name=%s where name=%s""",(self.student_name,self.name))

		# self.save(ignore_permissions=True)
		"""INSERT ENTRY TO MASTER GRADE"""
		# Check if entry exist in Master Grade
		is_exist = frappe.db.sql("""SELECT * FROM `tabMaster Grade` WHERE student=%s 
							AND student_name=%s AND activity_name=%s """,
								 (self.student,self.student_name,self.quiz), as_dict=1)


		# If exists just update the score
		if len(is_exist):
			quiz_info = None
			try:
				quiz_info = frappe.get_doc("Quiz", self.quiz)
			except:
				pass
			if quiz_info is not None:
				doc = frappe.get_doc("Master Grade", is_exist[0]['name'])
				doc.raw_score = self.score or 0
				doc.status = self.status or ""
				doc.course = self.course or quiz_info.subject
				doc.program = self.program or quiz_info.program
				doc.school_year = self.school_year or quiz_info.school_year
				doc.quarter = self.quarter or quiz_info.quarter
				doc.component = quiz_info.classwork_category
				doc.highest_possible_score = quiz_info.max_points
				doc.activity_title = self.quiz_title or quiz_info.title
				doc.activity_name = self.quiz
				doc.activity_link_type = "Quiz"
				doc.save(ignore_permissions=True)
				frappe.db.commit()
			else:
				doc = frappe.get_doc("Master Grade", is_exist[0]['name'])
				doc.raw_score = self.score or 0
				doc.status = self.status or ""
				doc.course = self.course
				doc.program = self.program
				doc.school_year = self.school_year
				doc.quarter = self.quarter
				doc.activity_title = self.quiz_title
				doc.activity_name = self.quiz
				doc.activity_link_type = "Quiz"
				doc.save(ignore_permissions=True)
				frappe.db.commit()
		else:
			# It does not exist so Create new Master Grade Entry
			# Get Quiz info
			quiz_info = None
			try:
				quiz_info = frappe.get_doc("Quiz", self.quiz)
			except:
				pass
			if quiz_info is not None:
				master_grade = frappe.get_doc({
					"doctype":"Master Grade",
					"student": self.student,
					"student_name": self.student_name or "",
					"activity_type": "Quiz Activity",
					"activity_link_type": "Quiz",
					"activity_name": self.quiz or "",
					"activity_title": self.quiz_title or "",
					"status": self.status or "",
					"raw_score": self.score or 0,
					"highest_possible_score": quiz_info.max_points,
					"teacher": quiz_info.owner,
					"component": quiz_info.classwork_category,
					"quarter": quiz_info.quarter or "",
					"school_year": quiz_info.school_year or "",
					"course": quiz_info.subject,
					"program": quiz_info.program
				})
				master_grade.insert(ignore_permissions=True)
				frappe.db.commit()
			else:
				master_grade = frappe.get_doc({
					"doctype": "Master Grade",
					"student": self.student,
					"student_name": self.student_name or "",
					"activity_type": "Quiz Activity",
					"activity_link_type": "Quiz",
					"activity_name": self.quiz or "",
					"activity_title": self.quiz_title or "",
					"status": self.status or 0,
					"raw_score": self.score or "",
				})
				master_grade.insert(ignore_permissions=True)
				frappe.db.commit()
	except Exception as e:
		frappe.log_error(frappe.get_traceback())
		pass


@frappe.whitelist()
def change_quiz_result(question,text):
	try:
		return frappe.db.sql(f"UPDATE `tabQuiz Result` SET `tabQuiz Result`.quiz_result='{text}' WHERE `tabQuiz Result`.question='{question}'")

	except Exception as e:
		return False

@frappe.whitelist()
def get_subject_filters():
	entries = frappe.get_all("Quiz Activity", fields=['distinct course'], filters={"owner": frappe.session.user})
	return entries


@frappe.whitelist()
def get_subject_filters_teacher():
	entries = frappe.get_all("User Permission", fields=['distinct for_value as course'], filters={"allow": "Course", "user": frappe.session.user},limit_page_length=1000)
	return entries

@frappe.whitelist()
def get_option(code,question):
	option = frappe.get_all("Options", fields=['option'], filters={"name": code})
	question = frappe.get_all("Question", fields=['type_of_question'], filters={"name": question})
	if question:
		if question[0]['type_of_question'] == "Multiple Choice" and code:
			if option:
				return option[0]['option']
	return code

@frappe.whitelist()
def get_quiz(name):
	quiz_info = frappe.get_all("Quiz",fields="*",filters={'name':name},limit_page_length=1000)
	if quiz_info:
		return quiz_info[0]
	return None

@frappe.whitelist()
def get_quiz_silid(name):
	quiz_info_items = frappe.get_all("Quiz Silid Items",fields="*",filters={'parent':name},limit_page_length=1000,order_by="idx ASC")
	if quiz_info_items:
		return quiz_info_items
	return None


