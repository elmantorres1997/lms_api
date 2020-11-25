# -*- coding: utf-8 -*-
# Copyright (c) 2020, Wela School System and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import json

class ContentSilid(Document):
	pass

@frappe.whitelist()
def get_topics(program):
	topics = frappe.get_all('Topic', filters={'program': program})
	return topics

@frappe.whitelist()
def get_content_name(topic_content):
	topic_content = frappe.get_doc("Topic Content", topic_content)
	return topic_content.content

def escape(text):
	if text:
		return text.replace("'","\\'")
	return text

def return_escape(text):
	if text:
		return text.replace("\'","'")
	return text

@frappe.whitelist()
def move_topic(old_topic, new_program, new_subject, new_topic, is_video, content_title, content_name):
	unescaped_new_subject = new_subject
	unescaped_new_topic = new_topic
	old_topic = escape(old_topic)
	new_program = escape(new_program)
	new_subject = escape(new_subject)
	new_topic = escape(new_topic)
	content_title = escape(content_title)
	content_name = escape(content_name)
	frappe.db.sql(f"UPDATE `tabContent Silid` SET program='{new_program}', topic='{new_topic}', course='{new_subject}' WHERE name='{content_name}'")

	# Get info
	topic_info = frappe.db.sql(f"SELECT name,content FROM `tabTopic Content` WHERE parent='{old_topic}' AND content_title='{content_title}'", as_dict=1)
	for info in topic_info:
		info_name = escape(info['content'])

		if int(is_video) == 1:
			content_type = "Video"
			frappe.db.sql(f"UPDATE `tabVideo` SET program='{new_program}', topic='{new_topic}' WHERE name='{info_name}'")
		else:
			content_type = "Article"
			frappe.db.sql(f"UPDATE `tabArticle` SET program='{new_program}', topic='{new_topic}' WHERE name='{info_name}'")

		# Transfer to new
		frappe.db.sql(f"UPDATE `tabTopic Content` SET parent='{return_escape(new_topic)}' WHERE name='{info['name']}'")

	frappe.db.sql(f"UPDATE `tabTo Do Tasks` SET course='{new_subject}',program='{new_program}',topic='{new_topic}' WHERE content_id='{content_name}'")
	frappe.db.commit()

	exists_topic_in_course = frappe.db.sql("""SELECT Count(*)
			              FROM `tabCourse Topic` WHERE parent=%s AND topic=%s""", (unescaped_new_subject, unescaped_new_topic))
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
def make_grade(student,grade,doc):
	doc = json.loads(doc)
	student_info = frappe.get_doc("Student", student)
	if doc["is_video"]:
		code = get_content_name(doc['topic_content'])
		params = {
			"doctype": "Written Activity",
			"student": student_info.user,
			"grade": grade,
			"highest_possible_score": doc['highest_possible_score'],
			"title": doc['title'],
			"quarter": doc['quarter'],
			"school_year": doc['school_year'],
			"program": doc['program'],
			"subject": doc['course'],
			"topic": doc['topic'],
			"video":code,
			"owner": student_info.user
		}
	else:
		code = get_content_name(doc['topic_content'])
		params = {
			"doctype": "Written Activity",
			"student": student_info.user,
			"grade": grade,
			"highest_possible_score": doc['highest_possible_score'],
			"title": doc['title'],
			"quarter": doc['quarter'],
			"school_year": doc['school_year'],
			"program": doc['program'],
			"subject": doc['course'],
			"topic": doc['topic'],
			"activity": code,
			"owner": student_info.user
		}
	written_activity = frappe.get_doc(params)
	written_activity.insert(ignore_permissions=True)
	frappe.db.commit()
	return True