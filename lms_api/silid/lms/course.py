from __future__ import unicode_literals
import erpnext.education.utils as utils
import frappe

no_cache = 1

def get_context(context):
	try:
		program = frappe.form_dict['program']
		course_name = frappe.form_dict['name']
	except KeyError:
		frappe.local.flags.redirect_location = '/lms'
		raise frappe.Redirect

	context.education_settings = frappe.get_single("Education Settings")
	course = frappe.get_doc('Course', course_name)
	context.program = program
	context.course = course
	context.topics = course.get_topics()

	# Change content title of topics with random names (e.g. 1a1badd051 ) Exactly 10 characters else don't change


	context.has_access =  utils.allowed_program_access(context.program)
	context.progress = get_topic_progress(context.topics, course, context.program)

	for topics in context.topics:
		for topic in topics.topic_content:
			try:
				if len(str(topic.content)) == 10:
					content_info = frappe.get_doc(topic.content_type, topic.content)
					topic.content = content_info.title
					topic.name = content_info.name
					topic.linker = content_info.name
				else:
					content_info = frappe.get_doc(topic.content_type, topic.content)
					topic.linker = content_info.title
			except:
				pass

def get_topic_progress(topics, course, program):
	progress = {topic.name: utils.get_topic_progress(topic, course.name, program) for topic in topics}

	return progress