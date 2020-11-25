# -*- coding: utf-8 -*-
# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from datetime import datetime
import json
from xml.sax import saxutils as su
from lms_api.lms_api.doctype.quiz_activity.quiz_activity import quiz_to_master_grade

class Quiz(Document):
	def validate(self):
		today = datetime.now()
		if self.passing_score > 100:
			frappe.throw(_("Passing Score value should be between 0 and 100"))
		frappe.db.sql(f"UPDATE `tabMaster Grade` SET component='{self.classwork_category}',"
					  f"highest_possible_score='{self.max_points}',"
					  f"activity_title='{self.title}',"
					  f"activity_name='{self.name}',"
					  f"course='{self.subject}'"
					  f"  WHERE activity_name='{self.name}' OR activity_title='{self.name}'")
		frappe.db.commit()
		

	def allowed_attempt(self, enrollment, quiz_name):
		if self.max_attempts ==  0:
			return True

		try:
			if len(frappe.get_all("Quiz Activity", {'enrollment': enrollment.name, 'quiz': quiz_name})) >= self.max_attempts:
				frappe.msgprint(_("Maximum attempts for this quiz reached!"))
				return False
			else:
				return True
		except Exception as e:
			return False


	def evaluate(self, response_dict, quiz_name):
		try:

			# print("/////")
			# print(response_dict)

			# ques_list = [ques.question_link for ques in self.question]

			def getList(dict):
				return dict.keys()

			ques_list = getList(response_dict)

			if len(ques_list) == 1:
				ques_list_tuple_temp = str(tuple(ques_list))
				ques_list_tuple = ques_list_tuple_temp.replace(",","")
			else:
				ques_list_tuple = str(tuple(ques_list))

			questions = frappe.db.sql(f"SELECT name,type_of_question, points FROM `tabQuestion` WHERE name in {ques_list_tuple}",as_dict=1)







			answers = {}
			for q in questions:
				query = frappe.get_all("Options", fields=['`tabOptions`.name', '`tabOptions`.option', '`tabOptions`.is_correct',
														  '`tabOptions`.image'],
									   filters={'parent': q['name']},order_by="idx asc")
				option_ans = get_answer(q['name'],query, q['type_of_question'])
				answers.update({
					q['name']:option_ans
				})
			question_type = {q['name']: q['type_of_question'] for q in questions}
			points = {q['name']: q['points'] for q in questions}

			total_points = self.max_points
			if total_points == 0:
				raise Exception("No max points")
			result = {}
			score = 0
			for key in answers:
				try:
					if isinstance(response_dict[key], list):
						if question_type[key] == "Matching Type":
							is_correct = compate_list_matching([ clean_text(x) for x in response_dict[key]], [clean_text(x) for x in answers[key]])
						elif question_type[key] == "Enumeration":
							if len(response_dict[key]) > 0:
								is_correct = compate_list_enumeration([clean_text(x) for x in response_dict[key]], [clean_text(x) for x in answers[key]])
							else:
								temp_ans = []
								for _ in answers[key]:
									temp_ans.append(False)
								is_correct = temp_ans
						elif question_type[key] == "Essay":
							is_correct = "Essay"
						else:
							is_correct = compare_list_elementwise([clean_text(x) for x in response_dict[key]], [clean_text(x) for x in answers[key]])
					else:
						if question_type[key] == "Essay":
							is_correct = "Essay"
						else:
							is_correct = ( clean_text(response_dict[key]) == clean_text(answers[key]))
				except Exception as e:
					is_correct = False

				result[key] = is_correct
				item_points = points[key] if points[key] else 1 # if quiz creator forgot to input question_points default points is 1

				if type(is_correct) == list:
					for ans in is_correct:
						score += item_points if ans==True else 0 # if answer is correct increment with item_points else increment with 0
				else:
					score += item_points if is_correct==True else 0 # if answer is correct increment with item_points else increment with 0

			average = round((float(score) / float(total_points)) * 100)
			if average >= self.passing_score:
				status = "Pass"
			else:
				status = "Fail"
			return result, score, status
		except Exception as e:
			frappe.log_error(frappe.get_traceback())
			pass

	def get_questions(self):
		return [frappe.get_doc('Question', question.question_link) for question in self.question]

	def get_publish_date(self):
		return self.publish_date

	def get_deadline_date(self):
		return self.deadline

def clean_text(text):
	if text:
		text_first_layer = text.lower().replace("&","and").replace("&amp;","and").replace(" ","")
		text = su.unescape(text_first_layer)
		return text

	return text

def get_answer(name,options,type_of_question):
	# options = self.options
	if type_of_question == "Identification" or type_of_question == "True or False" or type_of_question == "Fill in the Blank" or type_of_question == "Enumeration":
		answers = [item['option'] for item in options if item['is_correct'] == True]
	elif type_of_question == "Matching Type":
		answers = [list(json.loads(item['option']).values())[0] for item in options if item['is_correct'] == True]
	else:
		answers = [item['name'] for item in options if item['is_correct'] == True]
	if len(answers) == 0:
		frappe.throw(_("No correct answer is set for {0}".format(name)))
		return None
	elif len(answers) == 1:
		return answers[0]
	else:
		return answers


def compare_list_elementwise(*args):
	try:
		if all(len(args[0]) == len(_arg) for _arg in args[1:]):
			return all(all([element in (item) for element in args[0]]) for item in args[1:])
		else:
			return False
	except TypeError:
		frappe.throw(_("Compare List function takes on list arguments"))

def compate_list_matching(resp, ans):
	result = []
	try:
		for i in range(0, len(ans)):
			if resp[i] == ans[i]:
				result.append(True)
			else:
				result.append(False)
		return result
	except TypeError:
		frappe.throw(_("Compare List function takes on list arguments"))

def compate_list_enumeration(resp, ans):
	result = []
	try:
		for r in resp:
			if r in ans:
				result.append(True)
				ans.remove(r)
			else:
				result.append(False)
		return result
	except TypeError:
		frappe.throw(_("Compare List function takes on list arguments"))


@frappe.whitelist()
def carry_over(docname):
	all_qa = frappe.db.sql(f"SELECT name FROM `tabQuiz Activity` WHERE quiz='{docname}'", as_dict=1)
	for qa in all_qa:
		quiz_activity = frappe.get_doc("Quiz Activity", qa['name'])
		quiz_to_master_grade(quiz_activity)
