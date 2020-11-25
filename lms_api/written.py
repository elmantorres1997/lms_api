
import frappe


@frappe.whitelist()
def create_written_activity(title, name, student, program):
    file_name = '/private/files/'+title

    sql_check_grade = frappe.db.sql("""Select grade from `tabWritten Activity` WHERE activity = '{0}' AND owner = '{1}'""".format(title, student))

    if sql_check_grade:
        if sql_check_grade[0].grade > 0:
            frappe.msgprint('Unable to Save. Grade Already Added')
    else:
        written = {
            "doctype": "Written Activity",
            "activity": name,
            "upload": file_name,
        }
        attachment_doc = frappe.get_doc({
            "doctype": "File",
            "file_name": file_name,
            "file_url": '/private/files/'+title,
            "attached_to_name": title,
            "attached_to_doctype": "Written Activity",
            "old_parent": "Home/Attachments",
            "folder": "Home/Attachments",
            "is_private": 1
        })

        written_data = frappe.get_doc(written)
        written_data.insert(ignore_permissions=True)
        attachment_doc.insert(ignore_permissions=True)

    return 'Success'

