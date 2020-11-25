import frappe

"""UPDATE PROGRAM ENROLLMENT ACCORDING TO USER PERMISSION"""

def patch():
    permissions = frappe.db.sql(f"select * from `tabUser Permission`",as_dict=1)
    for permission in permissions:

        """Get Program Enrollment by Student"""
        email = permission['user']
        if "@wela.online" in email:
            student_info = frappe.db.sql(f"SELECT name FROM `tabStudent` WHERE student_email_id='{email}'", as_dict=1)
            for student in student_info:
                # Check Program Enrollment
                print(student['name'])
                program_enrollment = frappe.db.sql(f"SELECT program FROM `tabProgram Enrollment` WHERE `tabProgram Enrollment`.docstatus=1"
                                                   f" AND `tabProgram Enrollment`.student='{student['name']}' ORDER BY creation DESC LIMIT 1", as_dict=1)
                if program_enrollment[0]['program'] == permission['for_value']:
                    pass
                else:
                    # Set right program
                    frappe.db.sql(f"UPDATE `tabProgram Enrollment` SET program='{permission['for_value']}' WHERE student='{student['name']}'")

