from __future__ import unicode_literals
import erpnext.education.utils as utils
import frappe
from datetime import date

no_cache = 1

def get_context(context):
	# Load Query Parameters

	try:
		program = frappe.form_dict['program']
		content = frappe.form_dict['content']
		content_type = frappe.form_dict['type']
		course = frappe.form_dict['course']
		topic = frappe.form_dict['topic']
	except KeyError:
		frappe.local.flags.redirect_location = '/lms'
		raise frappe.Redirect


	# Check if user has access to the content
	has_program_access = utils.allowed_program_access(program)
	has_content_access = allowed_content_access(program, content, content_type)

	if frappe.session.user == "Guest" or not has_program_access or not has_content_access:
		frappe.local.flags.redirect_location = '/lms'
		raise frappe.Redirect

	roles = frappe.get_roles(frappe.session.user)
	block_role = ["Student"]
	if bool(set(block_role).intersection(roles)) and frappe.session.user !="Administrator":
		frappe.local.flags.redirect_location = '/lms'
		raise frappe.Redirect


	# Set context for content to be displayer
	context.content = frappe.get_doc(content_type, content).as_dict()
	context.content.publish_date = context.content.publish_date if context.content.publish_date is not None else date.today()
	context.content_type = content_type
	context.program = program
	context.course = course
	context.topic = topic

	topic = frappe.get_doc("Topic", topic)
	content_list = [{'content_type':item.content_type, 'content':item.content} for item in topic.topic_content]

	# Set context for progress numbers
	context.position = content_list.index({'content': content, 'content_type': content_type})
	context.length = len(content_list)

	# Set context for navigation
	context.previous = get_previous_content(content_list, context.position)
	context.next = get_next_content(content_list, context.position)
	context.uploaded_files = []

	# Get uploaded files
	activity_name = context.content.name
	content_type = context.content.doctype
	user = escape(frappe.session.user)
	activity_name = escape(activity_name)

	if content_type == "Article":

		written_activity_info = frappe.db.sql(f"SELECT name from `tabWritten Activity` "
											  f"WHERE activity LIKE '%{activity_name}%' "
											  f"AND student='{user}'", as_dict=1)
		submitted_files = []
		for info in written_activity_info:
			submitted_files = frappe.db.sql(f"SELECT file_name,file_url,creation FROM `tabFile` WHERE owner='{user}' "
											f"AND attached_to_name='{escape(info['name'])}'"
											f" AND attached_to_doctype='Written Activity'", as_dict=1)
		context.uploaded_files = submitted_files

	elif content_type == "Video":
		written_activity_info = frappe.db.sql(f"SELECT name from `tabWritten Activity` "
											  f"WHERE video LIKE '%{activity_name}%' "
											  f"AND student='{user}'", as_dict=1)
		submitted_files = []
		for info in written_activity_info:
			submitted_files = frappe.db.sql(f"SELECT file_name,file_url,creation FROM `tabFile` WHERE owner='{user}' "
											f"AND attached_to_name='{escape(info['name'])}'"
											f" AND attached_to_doctype='Written Activity'", as_dict=1)
		context.uploaded_files = submitted_files
	else:
		context.uploaded_files = []

def escape(text):
	if text:
		return text.replace("'","\\'")
	return text

def get_next_content(content_list, current_index):
	try:
		return content_list[current_index + 1]
	except IndexError:
		return None

def get_previous_content(content_list, current_index):
	if current_index == 0:
		return None
	else:
		return content_list[current_index - 1]

def allowed_content_access(program, content, content_type):
	contents_of_program = frappe.db.sql("""select `tabTopic Content`.content, `tabTopic Content`.content_type
	from `tabCourse Topic`,
		 `tabProgram Course`,
		 `tabTopic Content`
	where `tabCourse Topic`.parent = `tabProgram Course`.course
			and `tabTopic Content`.parent = `tabCourse Topic`.topic
			and `tabProgram Course`.parent = %(program)s""", {'program': program})

	return (content, content_type) in contents_of_program