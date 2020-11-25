# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import re

class Program(Document):
	def validate(self):
		self.flags.ignore_links = True

	def before_update_after_submit(self):
		self.flags.ignore_links = True

	def get_course_list(self):
		program_course_list = self.courses
		course_list = [frappe.get_doc("Course", program_course.course) for program_course in program_course_list]
		return course_list

	def autoname(self):
		regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
		print(self.program_name)
		program_name=str(self.program_name)
		print(program_name)
		print(regex.search(program_name))
		if regex.search(program_name) is None:
			pass
		else:
			frappe.throw('Unable to Save. Please remove special character '+program_name)