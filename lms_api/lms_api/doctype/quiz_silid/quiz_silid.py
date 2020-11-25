# -*- coding: utf-8 -*-
# Copyright (c) 2020, Wela School System and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils.background_jobs import enqueue
import json

class QuizSilid(Document):
	def on_trash(self):
		quiz_list = frappe.get_all("Quiz",fields=['name'], filters={ "content_silid":self.name })
		for quiz in quiz_list:
			frappe.db.sql(f"DELETE FROM `tabTopic Content` WHERE content='{quiz['name']}'")
			frappe.db.commit()

		to_do_tasks = frappe.get_all("To Do Tasks", fields=['name'], filters={"content_id": self.name})
		if to_do_tasks:
			enqueue("lms_api.lms_api.doctype.quiz_silid.quiz_silid.delete_to_do_tasks",
					queue='long', to_do_tasks=to_do_tasks)

def delete_to_do_tasks(to_do_tasks):
	for to_do in to_do_tasks:
		to_do_task = frappe.delete_doc("To Do Tasks", to_do['name'], ignore_permissions=True,force=1)
		frappe.db.commit()

def escape(text):
	if text:
		return text.replace("'","\\'")
	return text

def return_escape(text):
	if text:
		return text.replace("\'","'")
	return text

@frappe.whitelist()
def remove_time_limit(docname):
	quiz_info = frappe.db.sql(f"SELECT name FROM `tabQuiz` WHERE content_silid='{docname}'", as_dict=1)
	for quiz in quiz_info:
		quiz_name = escape(quiz['name'])
		frappe.db.sql(f"DELETE FROM `tabTime Limit` WHERE name LIKE '%{quiz_name}%'")


@frappe.whitelist()
def move_topic(old_topic, new_program, new_subject, new_topic, content_title, content_name):
	unescaped_new_subject = new_subject
	unescaped_new_topic = new_topic
	old_topic = escape(old_topic)
	new_program = escape(new_program)
	new_subject = escape(new_subject)
	new_topic = escape(new_topic)
	content_title = escape(content_title)
	content_name = escape(content_name)
	frappe.db.sql(f"UPDATE `tabQuiz Silid` SET program='{new_program}', topic='{new_topic}', course='{new_subject}' WHERE name='{content_name}'")

	# Get info
	topic_info = frappe.db.sql(f"SELECT name,content FROM `tabTopic Content` WHERE parent='{old_topic}' AND content_title='{content_title}'", as_dict=1)
	for info in topic_info:
		info_name = escape(info['content'])

		frappe.db.sql(f"UPDATE `tabQuiz` SET program='{new_program}', topic='{new_topic}' WHERE name='{info_name}'")

		# Transfer to new
		frappe.db.sql(f"UPDATE `tabTopic Content` SET parent='{return_escape(new_topic)}' WHERE name='{info['name']}'")

	frappe.db.sql(f"UPDATE `tabTo Do Tasks` SET course='{new_subject}',program='{new_program}',topic='{new_topic}' WHERE content_id='{content_name}'")
	frappe.db.commit()

	exists_topic_in_course = frappe.db.sql("""SELECT Count(*)
				              FROM `tabCourse Topic` WHERE parent=%s AND topic=%s""",
										   (unescaped_new_subject, unescaped_new_topic))
	if exists_topic_in_course[0][0] == 0:
		ct = frappe.get_doc({
			"doctype": "Course Topic",
			"parent": unescaped_new_subject,
			"parenttype": "Course",
			"parentfield": "topics",
			"topic": unescaped_new_topic,
		}).insert(ignore_permissions=True)
		frappe.db.commit()

@frappe.whitelist()
def update_publishdate_deadline(docname, publish_date=None, deadline=None,delete_time_limit=1):
	original_docname = docname
	docname = escape(docname)
	publish_date = publish_date if publish_date != "" else None
	deadline = deadline if deadline != "" else None
	print("Attempt update")

	# Delete Time Limit
	if delete_time_limit:
		quiz_info = frappe.db.sql(f"SELECT name FROM `tabQuiz` WHERE content_silid='{docname}'", as_dict=1)
		for quiz in quiz_info:
			quiz_name = escape(quiz['name'])
			frappe.db.sql(f"DELETE FROM `tabTime Limit` WHERE name LIKE '%{quiz_name}%'")



	quiz_silid_update = frappe.get_doc("Quiz Silid", docname)
	quiz_silid_update.publish_date = publish_date
	quiz_silid_update.deadline = deadline
	quiz_silid_update.save()
	frappe.db.commit()
	
	all_quiz = frappe.get_all("Quiz", fields=['name'], filters={"content_silid": original_docname})

	for quiz in all_quiz:
		quiz_update = frappe.get_doc("Quiz", quiz.name)
		quiz_update.publish_date = publish_date
		quiz_update.deadline = deadline
		quiz_update.save()
		frappe.db.commit()



# @frappe.whitelist()
# def update_publishdate_deadline(docname, publish_date=None, deadline=None,delete_time_limit=1):
# 	docname = escape(docname)
# 	publish_date = publish_date if publish_date != "" else None
# 	deadline = deadline if deadline != "" else None
# 	print("Attempt update")
#
# 	# Delete Time Limit
# 	if delete_time_limit:
# 		quiz_info = frappe.db.sql(f"SELECT name FROM `tabQuiz` WHERE content_silid='{docname}'", as_dict=1)
# 		for quiz in quiz_info:
# 			quiz_name = escape(quiz['name'])
# 			frappe.db.sql(f"DELETE FROM `tabTime Limit` WHERE name LIKE '%{quiz_name}%'")
#
# 	if publish_date is not None and deadline is not None:
# 		try:
# 			frappe.db.sql(f"UPDATE `tabQuiz Silid` SET publish_date='{publish_date}', deadline='{deadline}' WHERE name='{docname}'")
# 		except Exception as e:
# 			frappe.msgprint(e)
# 			pass
#
# 		try:
# 			frappe.db.sql(f"UPDATE `tabQuiz` SET publish_date='{publish_date}', deadline='{deadline}' WHERE content_silid='{docname}'")
# 		except Exception as e:
# 			frappe.msgprint(e)
# 			pass
# 	elif publish_date is not None and deadline is None:
# 		try:
# 			frappe.db.sql(f"UPDATE `tabQuiz Silid` SET publish_date='{publish_date}', deadline=NULL WHERE name='{docname}'")
# 		except Exception as e:
# 			frappe.msgprint(e)
# 			pass
#
# 		try:
# 			frappe.db.sql(f"UPDATE `tabQuiz` SET publish_date='{publish_date}', deadline=NULL WHERE content_silid='{docname}'")
# 		except Exception as e:
# 			frappe.msgprint(e)
# 			pass
# 	elif publish_date is None and deadline is not None:
# 		try:
# 			frappe.db.sql(f"UPDATE `tabQuiz Silid` SET deadline='{deadline}', publish_date=NULL WHERE name='{docname}'")
# 		except Exception as e:
# 			frappe.msgprint(e)
# 			pass
#
# 		try:
# 			frappe.db.sql(f"UPDATE `tabQuiz` SET deadline='{deadline}', publish_date=NULL WHERE content_silid='{docname}'")
# 		except Exception as e:
# 			frappe.msgprint(e)
# 			pass
# 	else:
# 		if publish_date is None:
# 			try:
# 				frappe.db.sql(
# 					f"UPDATE `tabQuiz Silid` SET publish_date=NULL WHERE name='{docname}'")
# 			except Exception as e:
# 				frappe.msgprint(e)
# 				pass
#
# 			try:
# 				frappe.db.sql(
# 					f"UPDATE `tabQuiz` SET publish_date=NULL WHERE content_silid='{docname}'")
# 			except Exception as e:
# 				frappe.msgprint(e)
# 				pass
#
# 		if deadline is None:
# 			try:
# 				frappe.db.sql(
# 					f"UPDATE `tabQuiz Silid` SET deadline=NULL WHERE name='{docname}'")
# 			except Exception as e:
# 				frappe.msgprint(e)
# 				pass
#
# 			try:
# 				frappe.db.sql(
# 					f"UPDATE `tabQuiz` SET deadline=NULL WHERE content_silid='{docname}'")
# 			except Exception as e:
# 				frappe.msgprint(e)
# 				pass

@frappe.whitelist()
def get_content_name(topic,title):
	topic_content = frappe.get_all("Topic Content",fields=['content'], filters={ "parent": topic, "content_title": title})
	if len(topic_content):
		return topic_content[0].content
	return None

@frappe.whitelist()
def make_grade(student,grade,doc):
	doc = json.loads(doc)
	code = get_content_name(doc['topic'],doc['quiz_title'])
	student_info = get_current_student(student)
	enrollment = get_or_create_course_enrollment(student_info,doc['course'], doc['program'])
	params = {
		"doctype": "Quiz Activity",
		"student": student,

		"course": doc['course'],
		"program": doc['program'],
		"topic": doc['topic'],
		"quarter": doc['quarter'],
		"school_year": doc['school_year'],
		"highest_possible_score": doc['highest_possible_score'],
		"quiz_title": doc['quiz_title'],
		"score": grade,
		"quiz": code,
		"enrollment":enrollment.name,
		"owner": student_info.user
	}

	quiz_activity = frappe.get_doc(params)
	quiz_activity.insert(ignore_permissions=True)
	frappe.db.commit()
	return True

def get_or_create_course_enrollment(student,course, program):
	course_enrollment = get_enrollment("course", course, student.name)
	if not course_enrollment:
		program_enrollment = get_enrollment('program', program, student.name)
		if not program_enrollment:
			frappe.throw(_("You are not enrolled in program {0}".format(program)))
			return
		return student.enroll_in_course(course_name=course,program_enrollment=get_enrollment('program', program, student.name))
	else:
		return frappe.get_doc('Course Enrollment', course_enrollment)

# LMS Utils
def get_current_student(student_id):
	return frappe.get_doc("Student", student_id)


def get_enrollment(master, document, student):

	if master == 'program':
		enrollments = frappe.get_all("Program Enrollment",filters={'student': student, 'program': document, 'docstatus': 1})
	if master == 'course':
		enrollments = frappe.get_all("Course Enrollment", filters={'student': student, 'course': document})

	if enrollments:
		return enrollments[0].name
	else:
		return None