import frappe

"""Turn On or Turn Off this API"""
turn_on = True

@frappe.whitelist()
def do_transfer(student_email_id, section,school_year):
    """
    This function will transfer Student section.
    1) Cancel Program Enrollment
    2) Create new Program Enrollment
    3) Remove User Permission
    4) Create New User Permission
    """

    """ 1) Cancel Program Enrollment"""

    exists_program = frappe.db.sql("""SELECT name FROM `tabProgram`
                                                                     WHERE program_name=%s""", (section))

    if exists_program == ():
        print("no program")
        return "no program"


    # Get name from Student List
    student_info = frappe.db.sql(f"SELECT name FROM `tabStudent` WHERE student_email_id='{student_email_id}'",as_dict=True)
    print(student_info)
    if student_info == []:
        return  "student not found"
    student = student_info[0]['name']

    # Get old values before deleting
    exists_program = frappe.db.sql(
        f"SELECT name,academic_year,program FROM `tabProgram Enrollment` WHERE student='{student}'",as_dict=True)
    print(exists_program)
    # Delete Program Enrollment
    program_name = ""
    if exists_program != []:
        prog = frappe.get_doc("Program Enrollment",exists_program[0].name)
        prog.cancel()
        frappe.db.commit()
        frappe.db.sql("""delete from `tabCourse Enrollment` where program_enrollment=%s""",exists_program[0].name)
        frappe.db.commit()
        delete = frappe.delete_doc("Program Enrollment", exists_program[0].name)
        frappe.db.commit()

    """ 2) Create new Program Enrollment"""
    # Map from old values but use new Section
    program_doc = frappe.get_doc({
        "doctype": "Program Enrollment",
        "student": student,
        "academic_year": school_year,
        "program": section,
        "enrollment_date": frappe.utils.get_datetime().date(),
        "docstatus": 1
    }).insert(ignore_permissions=True)
    frappe.db.commit()
    program_name = program_doc.name

    print(program_name)
    if program_name:
        """ 3) Remove User Permission """
        # Get old permission
        # exists_permission = frappe.db.sql(
        #     f"SELECT name,for_value FROM `tabUser Permission` WHERE user='{student}' AND for_value='{program_name}'",as_dict=True)
        #
        # if exists_permission != []:
            # Delete Old Permission
        delete = frappe.db.sql(f"DELETE FROM `tabUser Permission` WHERE user='{student_email_id}' AND allow='Program'",as_dict=True)
        frappe.db.commit()
        # else:
        """ Create New User Permission """
        frappe.get_doc({
            "doctype": "User Permission",
            "user": student_email_id,
            "allow": "Program",
            "for_value": section
        }).insert(ignore_permissions=True)
        frappe.db.commit()

@frappe.whitelist()
def transfer(student_email_id, section,school_year):
    if turn_on:
        try:
            do_transfer(student_email_id,section,school_year)
        except Exception as e:
            print(f"An error occured: {e}")