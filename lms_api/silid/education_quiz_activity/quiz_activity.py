# -*- coding: utf-8 -*-
# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class QuizActivity(Document):
	pass
	# def validate(self):
	# 	score = 0
	# 	for i in self.result:
	# 		if i.quiz_result == "Correct":
	# 			score += 1

	# 	self.score = round(score / len(self.result) * 100)
	# 	question = frappe.get_doc('Quiz', self.quiz)
	# 	if round(score / len(self.result) * 100) >= question.passing_score:
	# 		self.status = "Pass"
	# 	else:
	# 		self.status = "Fail"
