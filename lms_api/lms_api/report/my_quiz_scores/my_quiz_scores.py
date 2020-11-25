# Copyright (c) 2013, Wela School System and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe.service import *
import frappe

def execute(filters=None):
	columns, data = [], []

	columns = [
		{
			"label": "Quiz Name",
			'width': 250,
			"fieldname": "quiz_title"
		},
		{
			"label": "Score",
			'width': 100,
			"fieldname": "score"
		},
		{
			"label": "Number of items",
			'width': 150,
			"fieldname": "number_of_items"
		},
		# {
		# 	"label": "Score Percentage",
		# 	'width': 125,
		# 	"fieldname": "percentage"
		# },
		{
			"label": "Date",
			'width': 125,
			"fieldname": "modified"
		},
		{
			"label": "Teacher Remarks",
			'width': 200,
			"fieldname": "remarks"
		}
		# {
		# 	"label": "Passing Percentage",
		# 	'width': 100,
		# 	"fieldname": "passing_percentage"
		# },
		# {
		# 	"label": "Status",
		# 	'width': 100,
		# 	"fieldname": "status"
		# },

	]
	filters = filters.update({ '`tabQuiz Activity`.owner': frappe.session.user })
	scores = execute_query("GET_STUDENT_SCORES", filters=filters, as_dict=1, order_by="`tabQuiz Activity`.modified DESC")
	for score in scores:
		percentage = round(( int(score['score']) / int(score['max_points'])) * 100) if int(score['max_points']) else 0
		status = f"<span style='color:#006400!important;font-weight:bold';>{score['status']}ed</span>" if score['status'] =="Pass" else \
			f"<span style='color:#c30c0c!important;font-weight:bold';>{score['status']}ed</span>"
		obj = {
			"quiz_title": score['quiz_title'],
			"score": f"{score['score']}",
			"number_of_items": f"{score['max_points']}",
			"percentage": f"{percentage}%",
			"modified": score['modified'].strftime("%B %d, %Y"),
			"passing_percentage": f"{score['passing_score']}%",
			"status": status,
			"quiz_name": score['quiz_name'],
			"remarks": score['remarks']
		}
		# This will show only the latest attempt
		# find =next((x for x in data if x['quiz_name'] == obj['quiz_name']), None)
		# if not find:
		data.append(obj)

	return columns, data
