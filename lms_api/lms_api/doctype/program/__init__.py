import frappe

@frappe.whitelist()
def get_enrolled_students(program):
    return frappe.db.sql("""select A.student,A.student_name,B.user 
                            from `tabProgram Enrollment` as A
                             
                             inner join `tabStudent` as B on A.student=B.name
                             
                             where A.program=%s and A.docstatus=1""",(program))
