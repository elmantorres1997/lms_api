import frappe

#bench --site all execute lms_api.patches.indexing.index_pending_task
def index_pending_task():
    try:
        frappe.db.sql(f"CREATE INDEX idx_student_docstatus ON `tabProgram Enrollment` (student,docstatus) ")
    except Exception as e:
        print(e)
    try:
        frappe.db.sql(f"CREATE INDEX idx_program ON `tabQuiz Silid` (program) ")
    except Exception as e:
        print(e)
    try:

        frappe.db.sql(f"CREATE INDEX idx_content ON `tabQuiz` (content_silid,deadline) ")
    except Exception as e:
        print(e)
    try:
        frappe.db.sql(f"CREATE INDEX idx_quiz_student ON `tabQuiz Activity` (quiz,student)")
    except Exception as e:
        print(e)
    try:
        frappe.db.sql(f"CREATE INDEX idx_program ON `tabContent Silid` (program)")
    except Exception as e:
        print(e)

    try:
        frappe.db.sql(f"CREATE INDEX idx_topic ON `tabContent Silid` (topic)")
    except Exception as e:
        print(e)
    try:
        frappe.db.sql(f"CREATE INDEX idx_content ON `tabTopic Content` (content)")
    except Exception as e:
        print(e)

    frappe.db.commit()
    print("Indexing complete")


#bench --site all execute lms_api.patches.indexing.to_do_task
def to_do_task():
    try:
        frappe.db.sql(f"CREATE INDEX idx_status_owner ON `tabTo Do Tasks` (status,owner) ")
    except Exception as e:
        print(e)