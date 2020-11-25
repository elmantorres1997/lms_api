import frappe
from frappe.service import *
import json
from frappe.utils.background_jobs import enqueue
from frappe.desk.doctype.notification_log.notification_log import make_notification_logs
@frappe.whitelist()
def get_user_courses():
    roles = frappe.get_roles(frappe.session.user)
    if "Administrator" in roles:
        # return None
        return [{"course": "Administrator"}]
    elif "Student" in roles:
        student_name = execute_query("GET_STUDENT_1", as_dict=1, filters={ "student_email_id": frappe.session.user })
        courses = execute_query("GET_COURSES_VIA_STUDENT_ID", as_dict=1, filters={ "student": student_name[0]['name'] })
        return courses
    elif ("LMS User" in roles) or ("Instructor" in roles):
        courses = execute_query("GET_TEACHER_COURSES", as_dict=1, filters={"teacher": frappe.session.user})
        return courses


@frappe.whitelist()
def add_post(data):
    data = json.loads(data)
    data.update({"user_courses":get_user_courses()})
    frappe.publish_realtime(event='add_post', message=data)
    roles = frappe.get_roles(frappe.session.user)
    if ("LMS User" in roles) or ("Instructor" in roles) and "Administrator" not in roles:
        enqueue("frappe.custom.social_post.notify_students_by_course",queue='long', course=data['course'],post_owner=data['owner'],post_name=data['name'])
        # notify_students_by_course(course=data['course'],post_owner=data['owner'],post_name=data['name'])

def escape(text):
    if text:
        return text.replace("'","\\'")
    return text



@frappe.whitelist()
def notify_students_by_course(course,post_owner,post_name):
    # Notify student by course or subject
    course_enrollment = frappe.db.sql(f"SELECT student from `tabCourse Enrollment` WHERE course='{escape(course)}'", as_dict=1)
    student_list = []
    for student in course_enrollment:
        if student['student'] not in student_list:
            student_list.append(student['student'])

    if len(student_list) == 1:
        tuple_string = str(tuple(student_list))
        tuple_string = tuple_string.replace(",","")
    else:
        tuple_string = str(tuple(student_list))

    if len(student_list) > 0:
        student_emails = frappe.db.sql(f"SELECT user from `tabStudent` WHERE name in {tuple_string}", as_dict=1)
        for user in student_emails:
            """let notificationParams = {
			    document_name: this.post.name,
			    document_type: "Post",
			    subject: `${frappe.session.user} commented on your post in <b>Social</b>`,
			    from_user: frappe.session.user,
			    for_user: this.post.owner,
			    type: "Comment",
			    enable_email_comment:0,
			    email_content: `${frappe.session.user} commented on your post in <b>Social</b>`
			};"""

            composition = {
                "document_name": post_name,
                "document_type": "Post",
                "subject": f"{post_owner} has a new post for <b>{course}</b>",
                "from_user": post_owner,
                "for_user": user['user'],
                "type": "Post",
                "enable_email_comment": 0,
                "email_content": f"{post_owner} has a new post for <b>{course}</b>"
            }
            save_to_notification_log(composition)


@frappe.whitelist()
def save_to_notification_log(params):
    recipients = [frappe.db.get_value("User", {"enabled": 1, "name": params['for_user'],"user_type": "System User"})]
    doc = frappe._dict(params)
    make_notification_logs(doc,recipients)
