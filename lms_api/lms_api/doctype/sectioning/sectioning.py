# -*- coding: utf-8 -*-
# Copyright (c) 2020, Wela School System and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils.background_jobs import enqueue

class Sectioning(Document):
	def on_submit(self):
		enqueue_process(self.program, self.academic_year,self.remove_permission, self.enrollees)
	def on_cancel(self):
		enqueue_process_remove(self.program, self.enrollees)


@frappe.whitelist()
def enqueue_process_remove(self_program,self_enrollees):
	enqueue("lms_api.lms_api.doctype.sectioning.sectioning.remove_permission_",
			queue='long', self_program=self_program, self_enrollees=self_enrollees)
	frappe.msgprint("Sectioning is now enqueue")

@frappe.whitelist()
def enqueue_process(self_program, self_academic_year,self_remove_permission, self_enrollees):
	enqueue("lms_api.lms_api.doctype.sectioning.sectioning.start_process",
			queue='long', self_program=self_program, self_academic_year=self_academic_year,
			self_remove_permission=self_remove_permission, self_enrollees=self_enrollees)
	frappe.msgprint("Sectioning is now enqueue")

#bench --site testccs.silid.co execute lms_api.lms_api.doctype.sectioning.sectioning.test_start_process --kwargs '{"docname":"Grade 10S - P-SY2020-2021-6"}'
def test_start_process(docname):
	self = frappe.get_doc("Sectioning",docname)
	start_process(self.program, self.academic_year,self.remove_permission, self.enrollees)

def start_process(self_program, self_academic_year,self_remove_permission, self_enrollees):
	# courses = [self_program]
	programs = [self_program]
	school_year = self_academic_year

	# if self_remove_permission:
		# This will remove any old permission
		# remove_old_permission(self_program, self_enrollees)

	for student in self_enrollees:
		if student.section_check:

			# for course in courses:
			# 	try:
			# 		exists_program = frappe.db.sql(f"SELECT name FROM `tabCourse` WHERE course_name='{course}'")
			#
			# 		if exists_program == ():
			# 			frappe.get_doc({
			# 				"doctype": "Course",
			# 				"course_name": course
			# 			}).insert(ignore_permissions=True)
			# 			frappe.db.commit()
			# 	except Exception as e:
			# 		print(e)

			for program in programs:
				# try:

				submitted_ = frappe.db.sql(f"SELECT name,docstatus FROM `tabProgram Enrollment` "
											   f"WHERE program=%s AND student=%s AND docstatus=1 order by creation DESC LIMIT 1",
											   (program, student.student))

				if submitted_ != ():
					continue


				exists_program = frappe.db.sql(f"SELECT name,docstatus FROM `tabProgram Enrollment` "
											   f"WHERE program=%s AND student=%s order by creation DESC LIMIT 1",
											   (program,student.student))
				print(exists_program)
				if exists_program == ():
					frappe.get_doc({
						"doctype": "Program Enrollment",
						"student": student.student,
						"academic_year": school_year,
						"program": program,
						"enrollment_date": frappe.utils.get_datetime().date(),
						"docstatus": 1
					}).insert(ignore_permissions=True)
					frappe.db.commit()
				else:
					print(exists_program)
					for exists in exists_program:
						print(exists)
						if exists[1] == 2:
							course_es = frappe.db.sql(f"SELECT name FROM `tabCourse Enrollment` "
													  f"WHERE `tabCourse Enrollment`.program_enrollment=%s "
													  f"AND `tabCourse Enrollment`.student=%s",
													  (exists[0], student.student), as_dict=True)
							print(course_es)
							for course_e in course_es:
								try:
									course_enrollment = frappe.get_doc("Course Enrollment", course_e['name'])
									course_enrollment.delete()
									frappe.db.commit()
								except Exception as e:
									print(e)
									# pass
							# doc = frappe.get_doc("Program Enrollment",exists[0]).delete()
							doc = frappe.get_doc("Program Enrollment",exists[0])
							new_doc = frappe.copy_doc(doc)
							new_doc.amended_from = exists[0]
							new_doc.submit()
							frappe.db.commit()
							# break
						elif exists[0] == 0:
							doc = frappe.get_doc("Program Enrollment", exists[0])
							doc.submit()
							frappe.db.commit()
					# try:
					# 	frappe.db.sql(f"UPDATE `tabProgram Enrollment` SET docstatus=1 "
					# 				  f"WHERE program=%s AND student=%s",(program,student.student))
					# 	frappe.db.commit()
					# except:
					# 	pass

				# except Exception as e:
				# 	print(e)
				# try:
				get_student = frappe.db.sql(f"SELECT user FROM `tabStudent` WHERE name=%s", (student.student), as_dict=1)
				exists_permission = frappe.db.sql(f"SELECT name FROM `tabUser Permission` "
												  f"WHERE user=%s AND for_value=%s",
												  (get_student[0]['user'],program))
				if exists_permission == ():
					frappe.get_doc({
						"doctype": "User Permission",
						"user": get_student[0]['user'],
						"allow": "Program",
						"for_value": program
					}).insert(ignore_permissions=True)
					frappe.db.commit()
				# except Exception as e:
				# 	print(e)


#bench --site testccs.silid.co execute lms_api.lms_api.doctype.sectioning.sectioning.test_remove_permission_ --kwargs '{"docname":"Grade 10S - P-SY2020-2021-6"}'
def test_remove_permission_(docname):
	self = frappe.get_doc("Sectioning",docname)
	remove_permission_(self.program, self.enrollees)

@frappe.whitelist()
def remove_permission_(self_program, self_enrollees):
	# def on_cancel(self):
	programs = [self_program]
	for student in self_enrollees:
		for program in programs:
			# try:
			program_es = frappe.db.sql(f"SELECT name FROM `tabProgram Enrollment` "
									  f"WHERE `tabProgram Enrollment`.student=%s "
									  f"AND `tabProgram Enrollment`.program=%s",(student.student,program),as_dict=1)
			for program_e in program_es:

				# Course Enrollment is not Submittable so delete immediately
				course_es = frappe.db.sql(f"SELECT name FROM `tabCourse Enrollment` "
										  f"WHERE `tabCourse Enrollment`.program_enrollment=%s "
										  f"AND `tabCourse Enrollment`.student=%s",(program_e['name'],student.student),as_dict=True)
				for course_e in course_es:
					try:
						course_enrollment = frappe.get_doc("Course Enrollment", course_e['name'])
						course_enrollment.delete()
						frappe.db.commit()
					except Exception as e:
						print(e)




				program_enrollment = frappe.get_doc("Program Enrollment", program_e['name'])
				try:
					if program_enrollment.docstatus==1:
						program_enrollment.cancel()
					# program_enrollment.delete()
				except Exception as e:
					print(e)
					pass


			get_student = frappe.db.sql(f"SELECT user FROM `tabStudent` WHERE name=%s ",(student.student))
			permission_es = frappe.db.sql(f"select name FROM `tabUser Permission` "
										 f"WHERE `tabUser Permission`.user=%s "
										 f"AND allow='Program' AND for_value=%s",
										  (get_student[0][0],program), as_dict=1)
			for permission_e in permission_es:
				try:
					permission = frappe.get_doc("User Permission", permission_e['name'])
					# permission.cancel()
					permission.delete()
				except:
					pass


@frappe.whitelist()
def remove_old_permission(self_program, self_enrollees):
	# def on_cancel(self):
	# programs = [self_program]



	for student in self_enrollees:
			# try:
			program_es = frappe.db.sql(f"SELECT name FROM `tabProgram Enrollment` "
									  f"WHERE `tabProgram Enrollment`.student=%s "
									  f"AND `tabProgram Enrollment`.program!=%s",(student.student,self_program),as_dict=1)

			for program_e in program_es:

				# Course Enrollment is not Submittable so delete immediately
				course_es = frappe.db.sql(f"SELECT name FROM `tabCourse Enrollment` "
										  f"WHERE `tabCourse Enrollment`.program_enrollment=%s "
										  f"AND `tabCourse Enrollment`.student=%s",(program_e['name'],student.student),as_dict=True)
				for course_e in course_es:
					try:
						course_enrollment = frappe.get_doc("Course Enrollment", course_e['name'])
						course_enrollment.delete()
						frappe.db.commit()
					except:
						pass




				program_enrollment = frappe.get_doc("Program Enrollment", program_e['name'])
				try:
					if program_enrollment.docstatus==1:
						program_enrollment.cancel()
					program_enrollment.delete()
				except:
					pass


			get_student = frappe.db.sql(f"SELECT user FROM `tabStudent` WHERE name=%s ",(student.student))
			permission_es = frappe.db.sql(f"select name FROM `tabUser Permission` "
										 f"WHERE `tabUser Permission`.user=%s "
										 f"AND allow='Program' AND for_value!=%s",
										  (get_student[0][0],self_program), as_dict=1)
			for permission_e in permission_es:
				try:
					permission = frappe.get_doc("User Permission", permission_e['name'])
					# permission.cancel()
					permission.delete()
				except:
					pass



@frappe.whitelist()
def get_students(level,branch=""):
	if branch:

		students  = frappe.db.sql(
			f"SELECT name,first_name,last_name,branch FROM `tabStudent`"
			f"WHERE `tabStudent`.level='{level}' AND `tabStudent`.branch='{branch}'",
			as_dict=1
		)
	else:
		students  = frappe.db.sql(
			f"SELECT name,first_name,last_name,branch FROM `tabStudent`"
			f"WHERE `tabStudent`.level='{level}'",
			as_dict=1
		)
	return students
