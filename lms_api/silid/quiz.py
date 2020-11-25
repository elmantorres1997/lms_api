import frappe
import re
import json
from frappe.model.rename_doc import rename_doc
from frappe.utils.background_jobs import enqueue
#bench --site staging-hcm.silid.co execute lms_api.silid.quiz.test_create --kwargs "{'title':'avengers Q'}"
def test_create(title):
    quiz = {
        "doctype": "Quiz Silid",
        "quiz_title": title,
        "items": [
            {
                "question":"Two cars collide head on. At every moment during collision, the magnitude of the force the first car exerts on the second is exactly equal to the magnitude of the force the second car exerts on the first. This is an example of ________.",
                "choice_1":"answer A",
                "correct_1":1,
                "choice_2": "answer B",
                "correct_12": 0
            }
        ],  # quiz_question,
        "passing_score": 1.0,
        "max_attempts": 1,
        "program":"TEST1",
        "topic":"BTS",
        "course":"TEST4",
        "grading_basis": "Latest Highest Score",
        "classwork_category": "Written Work"
    }

    frappe.get_doc(quiz).insert(ignore_permissions=True)

def escape(text):
    if text:
        return text.replace("'","\\'")
    return text

def create_quiz(doc):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if regex.search(doc.quiz_title) == None:
        pass

    else:
        frappe.throw('Unable to Save. Please remove special character')

    quiz_erpnext = frappe.db.sql("""SELECT name FROM `tabQuiz` WHERE content_silid=%s""", (doc.name), as_dict=1)
    for quiz_ in quiz_erpnext:
        time_limit = frappe.get_all("Time Limit",fields=['name'],filters={'quiz_code': quiz_['name']})
        if len(time_limit) > 0:
            frappe.throw('A student has taken the quiz already. Cannot resave quiz. If you wish to change the date click "set new publish date and deadline" button.')
            break

    # This is okay to make sure topic_content is not doubled
    #frappe.db.sql("""DELETE FROM `tabTopic Content` WHERE name=%s""", (doc.topic_content))  # remove from child table
    #frappe.db.commit()




    frappe.db.commit()
    print("creating a question.")


    quiz_question = []
    questions = []
    total_points = []
    for q in doc.items:
        question = {
            "doctype":"Question",
            "question": q.question,
            "options": [],
            "question_image": q.question_image,
            "type_of_question": q.question_type,
            "points": (q.question_points if q.question_points else 1)
        }
        no_q = 10
        no_q_choices = 6
        q_dict = q.as_dict()

        if q.question_type == "Enumeration":
            for i in range(1,no_q+1):
                if q_dict['enum_ans_'+str(i)]:
                    total_points.append(q.question_points if q.question_points else 1)

        elif q.question_type == "Matching Type":
            for i in range(1,no_q+1):
                if q_dict['matching_left_' + str(i)] and q_dict['matching_right_' + str(i)]:
                    total_points.append(q.question_points if q.question_points else 1)

        else:
            total_points.append(q.question_points if q.question_points else 1)

        options = []

        if q.question_type == "Identification":
            options.append({
                "option": q_dict["correct"],
                "is_correct": True,
                "image": None,
            })
        if q.question_type == "Essay":
            options.append({
                "option": "Essay",
                "is_correct": True,
                "image": None,
            })
        elif q.question_type == "True or False":
            options.append({
                "option": q_dict["select_tf"],
                "is_correct": True,
                "image": None,
            })
        elif q.question_type == "Fill in the Blank":
            options.append({
                "option": q_dict["fnb_answer_1"],
                "is_correct": True,
                "image": None,
            })
        elif q.question_type == "Enumeration":
            for i in range(1,no_q+1):
                if q_dict['enum_ans_'+str(i)]:
                    options.append(
                            {
                                "option":q_dict['enum_ans_'+str(i)],
                                "is_correct": True,
                                "image": None
                            }
                    )
        elif q.question_type == "Matching Type":
            for i in range(1,no_q+1):
                if q_dict['matching_left_' + str(i)] and q_dict['matching_right_' + str(i)]:
                    options.append(
                            {
                                "option": json.dumps({
                                    q_dict['matching_left_' + str(i)]: q_dict['matching_right_' + str(i)]
                                }),
                                "is_correct": True,
                                "image": None
                            }
                    )
        elif q.question_type == "Multiple Choice":
            for i in range(1,no_q_choices+1):
                if q_dict['choice_'+str(i)]:
                    options.append(
                            {
                                "option":q_dict['choice_'+str(i)],
                                "is_correct":q_dict['correct_'+str(i)],
                                "image":q_dict['image_'+str(i)]
                            }
                    )

        question['options'] = options

        question_doc = frappe.get_doc(question)
        question_doc.insert(ignore_permissions=True)
        frappe.db.commit()
        questions.append(question_doc)


        quiz_question.append({
            "question_link":question_doc.name,
            "question":q.question[:100]
        })


    # quiz_question = [{
    #     "question_link":"",#question
    #     "question":""
    # }]
    quiz = {
        "doctype":"Quiz",

        "title": doc.quiz_title,
        "check_exam_permit": doc.check_exam_permit,
        "question": quiz_question,  # quiz_question,
        "passing_score": doc.passing_score,
        "max_attempts": doc.max_attempts,
        "content_silid":doc.name,
        "classwork_category":doc.classwork_category,
        "subject": doc.course,
        "grading_basis": "Latest Highest Score",
        "time_limit":doc.time_limit,
        "shuffle_question": doc.shuffle_question,
        "publish_date": doc.publish_date,
        "deadline": doc.deadline,
        "quarter":doc.quarter,
        "school_year":doc.school_year,
        "max_points": sum(total_points),
        "topic": doc.topic,
        "program": doc.program
    }
    quiz_info = None
    if len(quiz_erpnext)==0:
        quiz_info = frappe.get_doc(quiz)
        quiz_info.insert(ignore_permissions=True)
        frappe.db.commit()
    else:
        # Replace child table only
        for quiz_erp in quiz_erpnext:
            quiz_info = frappe.get_doc("Quiz", quiz_erp['name'])
            quiz_info.title = doc.quiz_title
            quiz_info.check_exam_permit = doc.check_exam_permit
            quiz_info.passing_score = doc.passing_score
            quiz_info.max_attempts = doc.max_attempts
            quiz_info.classwork_category = doc.classwork_category
            quiz_info.subject = doc.course
            quiz_info.time_limit = doc.time_limit
            quiz_info.shuffle_question = doc.shuffle_question
            quiz_info.publish_date = doc.publish_date
            quiz_info.deadline = doc.deadline
            quiz_info.quarter = doc.quarter
            quiz_info.school_year = doc.school_year
            quiz_info.max_points = sum(total_points)
            quiz_info.topic = doc.topic
            quiz_info.program = doc.program

            quiz_info.question = []
            for question in quiz_question:
                quiz_info.append("question", question)

            quiz_info.save(ignore_permissions=True)
            frappe.db.commit()

    if not doc.course:
        frappe.throw("Please set course.")


    exists_topic_in_course = frappe.db.sql("""SELECT Count(*)
                 FROM `tabCourse Topic` WHERE parent=%s AND topic=%s""", (doc.course, doc.topic))

    if exists_topic_in_course[0][0] == 0:
        ct = frappe.get_doc({
            "doctype": "Course Topic",
            "parent": doc.course,
            "parenttype": "Course",
            "parentfield": "topics",
            "topic": doc.topic,
        }).insert(ignore_permissions=True)
        frappe.db.commit()

    # if quiz_erpnext:
    #     for quiz_erp in quiz_erpnext:
    #         rename_doc("Quiz",quiz_erp['name'], quiz_.name ,merge=True, ignore_permissions=True)
    #         frappe.db.commit()
    #
    #
    tc_infos = frappe.db.sql(f"SELECT name FROM `tabTopic Content` WHERE content='{escape(quiz_info.name)}'", as_dict=1)
    for tc_info in tc_infos:
        tc = frappe.get_doc("Topic Content", tc_info['name'])
        tc.content_title = doc.quiz_title
        tc.save(ignore_permissions=True)
        frappe.db.commit()



    quiz_erpnext_ = frappe.db.sql("""SELECT name 
                                    FROM `tabTopic Content` WHERE parent=%s and
                                            content=%s""", (doc.topic, quiz_info.name), as_dict=1)

    if len(quiz_erpnext_) == 0:
        tc = frappe.get_doc({
            "doctype": "Topic Content",
            "parent": doc.topic,
            "parenttype": "Topic",
            "parentfield": "topic_content",
            "content_type": "Quiz",
            "content": quiz_info.name,
            "content_title": doc.quiz_title
        }).insert(ignore_permissions=True)
        frappe.db.commit()

        doc.topic_content = tc.name

def create_to_do_tasks_enqueue(doc):
    create_to_do_tasks(doc)


def create_to_do_tasks(doc):
    course_enrollments = frappe.get_all("Course Enrollment", fields=['student'], filters={"course": doc.course})
    to_exist_already = frappe.get_all("To Do Tasks", fields=['name'], filters={"content_id": doc.name, "program": doc.program})
    if len(to_exist_already) == 0:
        for enrollment in course_enrollments:
            student_info = frappe.get_doc("Student", enrollment['student'])

            to_do = {
                "doctype": "To Do Tasks",
                "status": "To Do",
                "program": doc.program,
                "course": doc.course,
                "topic": doc.topic,
                "classwork_category": doc.classwork_category,
                "task_type": "Quiz",
                "task_doctype": "Quiz Silid",
                "title": doc.quiz_title,
                "content_id": doc.name,
                "publish_date": doc.publish_date,
                "deadline": doc.deadline,
                "owner": student_info.user or student_info.student_email_id
            }
            to_do_ = frappe.get_doc(to_do)
            to_do_.insert(ignore_permissions=True)
            frappe.db.commit()

def student_name(doc,method):
    doc.name = (doc.student_name or doc.student ) + '/' +doc.program


def shorten_quiz(doc,method):
    doc.question = doc.question[:140]
