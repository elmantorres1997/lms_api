import frappe
from lms_api.silid.quiz import create_quiz,create_to_do_tasks_enqueue


@frappe.whitelist()
def apply_quiz(docname):
    #     "validate": "lms_api.silid.quiz.create_quiz",
    #     "after_insert": "lms_api.silid.quiz.create_to_do_tasks_enqueue",

    doc = frappe.get_doc("Quiz Silid",docname)

    create_quiz(doc)
    create_to_do_tasks_enqueue(doc)

    pass