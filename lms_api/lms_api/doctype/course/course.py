# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from datetime import datetime as dt

class Course(Document):
	def validate(self):
		self.course_name = self.course_name.replace("&", "and")
		self.validate_assessment_criteria()

	def autoname(self):
		self.name = self.course_name.replace("&", "and")

	def validate_assessment_criteria(self):
		if self.assessment_criteria:
			total_weightage = 0
			for criteria in self.assessment_criteria:
				total_weightage += criteria.weightage or 0
			if total_weightage != 100:
				frappe.throw(_("Total Weightage of all Assessment Criteria must be 100%"))

	def get_topics(self):
		topic_data= []
		wela_setting = frappe.get_doc("Wela Settings")
		filter_date = wela_setting.topic_date
		if filter_date:
			filter_date = dt.strptime(filter_date, "%Y-%m-%d")
		for topic in self.topics:
			topic_doc = frappe.get_doc("Topic", topic.topic)
			if filter_date:

				if topic_doc.topic_content and (topic_doc.creation >= filter_date):
					topic_data.append(topic_doc)
			else:
				if topic_doc.topic_content:
					topic_data.append(topic_doc)

		# topics_list = []
		# for topic in self.topics:
		# 	if topic.topic not in topics_list:
		# 		topics_list.append(topic.topic)
		#
		# if len(topics_list) == 1:
		# 	tuple_string = str(tuple(topics_list))
		# 	tuple_string = tuple_string.replace(",","")
		# else:
		# 	tuple_string = str(tuple(topics_list))
		# if len(topics_list) > 0:
		# 	topic_data = frappe.db.sql(f"SELECT name,hero_image,topic_name FROM `tabTopic` WHERE name in {tuple_string} ORDER BY topic_name asc",as_dict=1)
		# else:
		# 	topic_data = []

		return topic_data