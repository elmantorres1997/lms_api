from __future__ import unicode_literals
import erpnext.education.utils as utils
import frappe

no_cache = 1


def get_context(context):
	context.education_settings = frappe.get_single("Education Settings")
	if not context.education_settings.enable_lms:
		frappe.local.flags.redirect_location = '/'
		raise frappe.Redirect
	context.featured_programs = get_portal_programs()


def get_featured_programs():
	return utils.get_portal_programs()

def get_portal_programs():
	roles = frappe.get_roles(frappe.session.user)
	portal_programs = []
	if "Student" in roles and frappe.session.user != "Administrator" :
		student = frappe.db.sql("""select name from `tabStudent` where user=%s""", (frappe.session.user))
		if student != ():
			enrolled = frappe.db.sql("""select program from `tabProgram Enrollment` where student=%s and docstatus=1""",
									 (student[0][0]))
			if enrolled != ():
				# portal_programs = [{'program': program, 'has_access': allowed_program_access(program.name)}]
				for enroll in enrolled:
					portal_programs.append({'program': frappe.get_doc("Program", enroll[0]),
											'has_access': 1})
	else:
		# This is for the Teachers
		is_restricted = 0
		# Try catch to catch error if settings is not yet migrated
		try:
			wela_settings = frappe.get_doc("Wela Settings")
			is_restricted = wela_settings.restrict_teacher_assignment
		except:
			pass

		if frappe.session.user != "Administrator" and is_restricted:
			assigned_subjects = frappe.db.sql(
				f"SELECT distinct course FROM `tabCourses` JOIN `tabTeacher Assignment` ON `tabCourses`.parent=`tabTeacher Assignment`.name "
				f"WHERE `tabCourses`.parent LIKE '%{frappe.session.user}%' "
				f"AND `tabTeacher Assignment`.docstatus=1 ", as_dict=1
			)
			published_programs = []
			published_courses = []
			subject_list = []
			for subject in assigned_subjects:
				if subject['course'] not in subject_list:
					subject_list.append(subject['course'])

			published_courses.append(frappe.get_all("Program Course", fields=['distinct parent','name'],filters=[["course", "in", tuple(subject_list)]], group_by="parent"))

			for programs in published_courses:
				for program in programs:
					if program['parent'] not in published_programs:
						published_programs.append(program['parent'])
			portal_programs = [{'program': frappe.get_doc("Program", program), 'has_access': 1} for program in published_programs]

		# This is for the Admin
		else:
			published_programs = frappe.get_all("Program", filters={"is_published": True})
			if not published_programs:
				return None

			portal_programs = [{'program': frappe.get_doc("Program", program), 'has_access': 1} for program in published_programs]
			# portal_programs = [{'program': program, 'has_access': utils.allowed_program_access(program.name)} for program in
			# 				   program_list if utils.allowed_program_access(program.name) or program.allow_self_enroll]

	return portal_programs
