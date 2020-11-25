from __future__ import unicode_literals
import erpnext.education.utils as utils
import frappe
from frappe import _

no_cache = 1

def get_context(context):
	try:
		program = frappe.form_dict['program']
	except KeyError:
		frappe.local.flags.redirect_location = '/lms'
		raise frappe.Redirect

	context.education_settings = frappe.get_single("Education Settings")
	context.program = get_program(program)
	is_strict = 0
	try:
		wela_settings = frappe.get_doc("Wela Settings")
		is_strict = wela_settings.restrict_subject_assignment
	except:
		pass
	roles = frappe.get_roles(frappe.session.user)
	if is_strict and frappe.session.user != "Administrator" and "Student" not in roles and "Instructor" in roles:
		allowed_courses = []
		assigned_courses = []
		user_assigned_courses = frappe.db.sql(f"SELECT course FROM tabCourses WHERE parent LIKE '%{frappe.session.user}%' AND docstatus LIKE '1'", as_dict=1)
		for course in user_assigned_courses:
			assigned_courses.append(course['course'])

		for course in context.program.courses:
			if course.course in assigned_courses:
				allowed_courses.append(course.course)

		if len(allowed_courses)==1:
			tuple_list = str(tuple(allowed_courses))
			tuple_list = tuple_list.replace(",","")
		else:
			tuple_list = str(tuple(allowed_courses))
		if len(allowed_courses) > 0:
			context.courses = frappe.db.sql(f"SELECT name,course_name,description,hero_image from `tabCourse` WHERE name in {tuple_list}",as_dict=1)
		else:
			context.courses = []
	else:
		allowed_courses = []
		for course in context.program.courses:
			if course.course not in allowed_courses:
				allowed_courses.append(course.course)
		if len(allowed_courses)==1:
			tuple_list = str(tuple(allowed_courses))
			tuple_list = tuple_list.replace(",","")
		else:
			tuple_list = str(tuple(allowed_courses))

		if len(allowed_courses) > 0:
			context.courses = frappe.db.sql(f"SELECT name,course_name,description,hero_image FROM `tabCourse` WHERE name in {tuple_list}",as_dict=1)
		else:
			context.courses = []

	context.has_access = utils.allowed_program_access(program)
	context.progress = get_course_progress(context.courses, context.program)

def get_program(program_name):
	try:
		return frappe.get_doc('Program', program_name)
	except frappe.DoesNotExistError:
		frappe.throw(_("Program {0} does not exist.".format(program_name)))

# def get_course_progress(courses, program):
# 	progress = {course.name: utils.get_course_progress(course, program) for course in courses}
# 	return progress


def get_course_progress(courses, program):
	progress = {course['name']: {'completed': False, 'started': True} for course in courses}
	return progress