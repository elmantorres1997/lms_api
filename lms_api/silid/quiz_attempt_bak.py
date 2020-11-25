import frappe
import re
import json
from frappe.utils import now
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

def create_quiz(doc,method):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if regex.search(doc.quiz_title) == None:
        pass

    else:
        frappe.throw('Unable to Save. Please remove special character')

    quiz_erpnext = frappe.db.sql("""SELECT name FROM `tabQuiz` WHERE content_silid=%s AND title=%s""", (doc.name, doc.quiz_title), as_dict=1)

    # This is okay to make sure topic_content is not doubled
    frappe.db.sql("""DELETE FROM `tabTopic Content`
                                     WHERE name=%s""", (doc.topic_content))  # remove from child table
    frappe.db.commit()


    if len(quiz_erpnext):
        quiz_erpnext_doc = frappe.get_doc("Quiz",quiz_erpnext[0]['name'])
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
            no_q = 6
            q_dict = q.as_dict()

            if q.question_type == "Enumeration":
                for i in range(1,no_q+1):
                    if q_dict['enum_ans_'+str(i)]:
                        total_points.append(q.question_points if q.question_points else 1)

            elif q.question_type == "Matching Type":
                for i in range(1,no_q):
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
                for i in range(1,no_q):
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
                for i in range(1,no_q+1):
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

        quiz_erpnext_doc.title = doc.quiz_title
        quiz_erpnext_doc.question = quiz_question
        quiz_erpnext_doc.passing_score = doc.passing_score
        quiz_erpnext_doc.max_attempts = doc.max_attempts
        quiz_erpnext_doc.content_silid = doc.name
        quiz_erpnext_doc.classwork_category = doc.classwork_category
        quiz_erpnext_doc.subject = doc.course
        quiz_erpnext_doc.time_limit = doc.time_limit
        quiz_erpnext_doc.publish_date = doc.publish_date
        quiz_erpnext_doc.deadline = doc.deadline
        quiz_erpnext_doc.school_year = doc.school_year
        quiz_erpnext_doc.max_points = sum(total_points)
        quiz_erpnext_doc.topic = doc.topic
        quiz_erpnext_doc.program = doc.program
        quiz_erpnext_doc.save(ignore_permissions=True,ignore_version=True)
        frappe.db.commit()


    else:

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
            no_q = 6
            q_dict = q.as_dict()

            if q.question_type == "Enumeration":
                for i in range(1,no_q+1):
                    if q_dict['enum_ans_'+str(i)]:
                        total_points.append(q.question_points if q.question_points else 1)

            elif q.question_type == "Matching Type":
                for i in range(1,no_q):
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
                for i in range(1,no_q):
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
                for i in range(1,no_q+1):
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
            "question": quiz_question,  # quiz_question,
            "passing_score": doc.passing_score,
            "max_attempts": doc.max_attempts,
            "content_silid":doc.name,
            "classwork_category":doc.classwork_category,
            "subject": doc.course,
            "grading_basis": "Latest Highest Score",
            "time_limit":doc.time_limit,
            "publish_date": doc.publish_date,
            "deadline": doc.deadline,
            "quarter":doc.quarter,
            "school_year":doc.school_year,
            "max_points": sum(total_points),
            "topic": doc.topic,
            "program": doc.program
        }

        quiz_ = frappe.get_doc(quiz)
        quiz_.insert(ignore_permissions=True)
        frappe.db.commit()

    if not doc.course:
        frappe.throw("Please set course.")
    if len(quiz_erpnext):
        tc = frappe.get_doc({
            "doctype": "Topic Content",
            "parent": doc.topic,
            "parenttype": "Topic",
            "parentfield": "topic_content",
            "content_type": "Quiz",
            "content": quiz_erpnext_doc.name,
            "content_title": doc.quiz_title
        }).insert(ignore_permissions=True)
        frappe.db.commit()

        doc.topic_content = tc.name
    else:
        tc = frappe.get_doc({
            "doctype": "Topic Content",
            "parent": doc.topic,
            "parenttype": "Topic",
            "parentfield": "topic_content",
            "content_type": "Quiz",
            "content": quiz_.name,
            "content_title": doc.quiz_title
        }).insert(ignore_permissions=True)
        frappe.db.commit()

        doc.topic_content = tc.name

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


def student_name(doc,method):
    doc.name = (doc.student_name or doc.student ) + '/' +doc.program


def shorten_quiz(doc,method):
    doc.question = doc.question[:140]