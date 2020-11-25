from __future__ import unicode_literals
import erpnext.education.utils as utils
import frappe
from datetime import date
no_cache = 1

def get_context(context):
	try:
		course = frappe.form_dict['course']
		program = frappe.form_dict['program']
		topic = frappe.form_dict['topic']
	except KeyError:
		frappe.local.flags.redirect_location = '/lms'
		raise frappe.Redirect

	context.program = program
	context.course = course
	context.topic = frappe.get_doc("Topic", topic)
	context.contents = get_contents(context.topic, course, program)
	context.has_access =  utils.allowed_program_access(program)


def get_contents(topic, course, program):
	student = utils.get_current_student()
	if student:
		course_enrollment = utils.get_or_create_course_enrollment(course, program)
	contents = topic.get_contents()
	progress = []
	if contents:
		for content in contents:
			content_data = frappe.get_doc(content.doctype, content.name).as_dict()
			publish_date = content_data.publish_date if content_data.publish_date is not None else date.today()
			if content.doctype in ('Article', 'Video'):
				if student:
					status = utils.check_content_completion(content.name, content.doctype, course_enrollment.name)
				else:
					status = True
				progress.append({'content': content, 'content_type': content.doctype, 'completed': status, 'publish_date': publish_date })
			elif content.doctype == 'Quiz':
				if student:
					status, score, result, max_points = check_quiz_completion(content, course_enrollment.name)
				else:
					status = False
					score = None
					result = None
					max_points = None
				progress.append({'content': content, 'content_type': content.doctype, 'completed': status, 'score': score, 'result': result, 'max_points':max_points , 'publish_date': publish_date})

	return progress

def check_quiz_completion(quiz, enrollment_name):
	attempts = frappe.get_all("Quiz Activity", filters={'enrollment': enrollment_name, 'quiz': quiz.name},
                              fields=["name", "activity_date", "score", "status", "quiz"])
	if (len(attempts) > 0):
		status = True
	else:
		status = False
	score = None
	result = None
	max_points = None
	if attempts:
		if quiz.grading_basis == 'Last Highest Score':
			attempts = sorted(attempts, key=lambda i: int(i.score), reverse=True)
		score = attempts[0]['score']
		result = attempts[0]['status']
		quiz_info = frappe.get_doc("Quiz", attempts[0]['quiz'])
		max_points = quiz_info.max_points
		if result == 'Pass':
			status = True
	return status, score, result, max_points