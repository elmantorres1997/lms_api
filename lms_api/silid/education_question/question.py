# -*- coding: utf-8 -*-
# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
import json

class Question(Document):

	def validate(self):
		# print("+++++++++++++++++++++++++++++++++++++++++")
		self.check_at_least_one_option()
		self.check_minimum_one_correct_answer()
		self.set_question_type()

	def check_at_least_one_option(self):
		if self.type_of_question == "Enumeration":
			if len(self.options) < 2:
				frappe.throw(_("Enumeration must have at least 2 answers. Use identification instead"))
			else:
				pass

		elif self.type_of_question == "Multiple Choice":
			if len(self.options) <= 1:
				frappe.throw(_("A question must have more than one options"))
			else:
				pass
		elif self.type_of_question == "Identification"  or self.type_of_question == "Fill in the Blank":
			answer = ""
			for opt in self.options:
				answer+=str(opt.option)
			if answer == "":
				frappe.throw(_("A Question must have a answer"))
			else:
				pass

	def check_minimum_one_correct_answer(self):
		if self.type_of_question != "Essay":
			correct_options = [option.is_correct for option in self.options]
			if bool(sum(correct_options)):
				pass
			else:
				frappe.throw(_("A qustion must have at least one correct options"))

	def set_question_type(self):
		correct_options = [option for option in self.options if option.is_correct]
		if len(correct_options) > 1:
			self.question_type = "Multiple Correct Answer"
		else:
			self.question_type = "Single Correct Answer"

	def get_answer(self):
		options = self.options
		if self.type_of_question == "Identification" or self.type_of_question == "True or False" or self.type_of_question == "Fill in the Blank" or self.type_of_question == "Enumeration":
			answers = [item.option for item in options if item.is_correct == True]
		elif self.type_of_question == "Matching Type":
			answers = [list(json.loads(item.option).values())[0] for item in options if item.is_correct == True]
		else:
			answers = [item.name for item in options if item.is_correct == True]
		if len(answers) == 0:
			frappe.throw(_("No correct answer is set for {0}".format(self.name)))
			return None
		elif len(answers) == 1:
			return answers[0]
		else:
			return answers