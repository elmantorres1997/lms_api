import frappe

# bench --site khs.silid.co execute lms_api.patches.missing_topic_content.topics
def topics():
    print("Script started")
    quiz_silid = frappe.get_list("Quiz Silid", fields="*")
    count = 0
    for quiz in quiz_silid:
        quiz_infos = frappe.get_all("Quiz", {"content_silid": quiz.name})
        for quiz_info in quiz_infos:
            exist_topic_content = frappe.db.sql(f"SELECT name FROM `tabTopic Content` WHERE content='{quiz_info.name}'")
            if exist_topic_content == ():
                tc = frappe.get_doc({
                    "doctype": "Topic Content",
                    "parent": quiz.topic,
                    "parenttype": "Topic",
                    "parentfield": "topic_content",
                    "content_type": "Quiz",
                    "content": quiz_info.name,
                    "content_title": quiz.quiz_title
                }).insert(ignore_permissions=True)
                frappe.db.commit()
                count +=1
                print(f"Added: {quiz_info.name} - {quiz.quiz_title}")
    print("Total Rows affected:", count)