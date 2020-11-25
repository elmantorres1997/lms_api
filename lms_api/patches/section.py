
""" THIS SCRIPT IS TO TRANSFER SECTIONS FROM SILID TO WELA - TCA Request """

import frappe
from frappe.frappeclient import FrappeClient

# bench --site tca.silid.co execute lms_api.patches.section.transfer
def transfer(url, username, password):
    """ begin transfer """

    # url = "https://tca.wela.online/"
    # username = "Administrator"
    # password = "apwzh2KSyqU3ZkKP"

    conn = FrappeClient(url, username, password)

    program_enrollments = frappe.get_all(
        doctype="Program Enrollment",
        fields=['student', 'student_name','program','academic_year','enrollment_date'],
        filters={ "docstatus": 1 }
    )
    len(program_enrollments)
    for enrollment in program_enrollments:
        if "-" in enrollment['program']:


            student = frappe.get_doc("Student",enrollment['student'])
            if student.first_name and student.last_name:
                params = {
                    # "student_name": enrollment['student_name'],
                    "fname": student.first_name,
                    "lname": student.last_name,
                    "academic_year": enrollment['academic_year'],
                    "program": enrollment['program']
                }
                print(params)
                to_wela = conn.get_api("wela.registration.doctype.sectioning.silid_to_wela", params)
            else:
                print("Err ",student.first_name," ", student.last_name)

# bench --site mca.silid.co execute lms_api.patches.section.mca
def mca():
    """ begin transfer """

    url = "https://millennium.wela.online/"
    username = "Administrator"
    password = "HENRMBUX"

    conn = FrappeClient(url, username, password)

    program_enrollments = frappe.get_all(
        doctype="Program Enrollment",
        fields=['student', 'student_name','program','academic_year','enrollment_date'],
        filters={ "docstatus": 1 }
    )
    len(program_enrollments)
    for enrollment in program_enrollments:
        if "-" in enrollment['program']:


            student = frappe.get_doc("Student",enrollment['student'])
            if student.first_name and student.last_name:
                params = {
                    # "student_name": enrollment['student_name'],
                    "fname": student.first_name,
                    "lname": student.last_name,
                    "academic_year": enrollment['academic_year'],
                    "program": enrollment['program']
                }
                print(params)
                to_wela = conn.get_api("wela.registration.doctype.sectioning.silid_to_wela", params)
            else:
                print("Err ",student.first_name," ", student.last_name)