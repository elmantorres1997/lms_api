# -*- coding: utf-8 -*-
# Copyright (c) 2020, Wela School System and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class EnrollSilid(Document):
    def validate(self):
        courses = [self.program]
        programs = [self.program]
        school_year = self.academic_year
        for enrollee in self.enrollees:
            student = enrollee
            for cours in courses:
                exists_program = frappe.db.sql("""SELECT name FROM `tabCourse`
		                                                                    WHERE course_name=%s""", (cours))

                if exists_program == ():
                    course_doc = frappe.get_doc({
                        "doctype": "Course",
                        "course_name": cours
                    }).insert(ignore_permissions=True)
                    frappe.db.commit()

            for prog in programs:
                exists_program = frappe.db.sql("""SELECT name FROM `tabProgram`
		                                                             WHERE program_name=%s""", (prog))

                if exists_program == ():
                    program_doc = frappe.get_doc({
                        "doctype": "Program",
                        "program_name": prog,
                        "is_published": 1,
                        "courses": [{"course": prog, "course_name": prog}]
                    }).insert(ignore_permissions=True)
                    frappe.db.commit()

            exists_program = frappe.db.sql("""SELECT Count(*) FROM `tabAcademic Year`
		                                                                       WHERE academic_year_name=%s""",
                                           (school_year))

            if exists_program == ():
                course_doc = frappe.get_doc({
                    "doctype": "Academic Year",
                    "academic_year_name": school_year
                }).insert(ignore_permissions=True)
                frappe.db.commit()

            for i, prog in enumerate(programs):
                enrollment = frappe.get_doc({
                    "doctype": "Program Enrollment",
                    "student": student.student,
                    "academic_year": school_year,
                    "program": prog,
                    "enrollment_date": frappe.utils.get_datetime().date(),
                    "docstatus": 1
                }).insert(ignore_permissions=True)
                frappe.db.commit()

                course_enrollment = frappe.get_doc({
                    "doctype": "Course Enrollment",
                    "student": student.student,
                    # "academic_year": "2020-21",
                    "program_enrollment": enrollment.name,
                    "course": courses[i],
                    "enrollment_date": frappe.utils.get_datetime().date(),
                    # "docstatus": 1
                }).insert(ignore_permissions=True)
