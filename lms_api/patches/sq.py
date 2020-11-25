import frappe
import json
import datetime


def clean_(str):

    str = str.replace('"', '\ "'.replace(" ", ""))

    # print(str)

    str = str.replace("'", '"')

    # print(str)

    loaded = json.loads(str)

    return loaded

# bench --site all execute lms_api.patches.sq.execute_all
def execute_all(multi=False):
    stop_time = datetime.datetime.now() + datetime.timedelta(minutes=4)
    all = frappe.db.sql("SELECT * FROM `tabScheduled Quizzes` WHERE checked=0 LIMIT 45",as_dict=1)
    total = len(all)
    print("Total:", total)



    for sh in all:

        loaded = ""
        data = sh['data']
        quiz_name = sh['quiz']
        # loaded = json.loads(data)
        try:
            loaded = json.loads(data)
        except Exception as e:
            # frappe.log_error(frappe.get_traceback())
            try:
                loaded = clean_(data)
            except Exception as e:
                frappe.log_error(frappe.get_traceback())

        if loaded:
            try:
                evaluate(loaded['student'], loaded['quiz_response'],
                         quiz_name,loaded['course'],
                         loaded['program'], loaded['quiz_activity_name'])
                mark_as_checked(sh['name'])
            except Exception as e:
                frappe.log_error(frappe.get_traceback())

        if datetime.datetime.now() > stop_time:
            exit()




def execute_all2(multi=False):
    stop_time = datetime.datetime.now() + datetime.timedelta(minutes=4)
    all = frappe.db.sql("SELECT * FROM `tabScheduled Quizzes` WHERE checked=0",as_dict=1)
    total = len(all)
    print("Total:", total)



    for sh in all:

        loaded = ""
        data = sh['data']
        quiz_name = sh['quiz']
        # loaded = json.loads(data)
        try:
            loaded = json.loads(data)
        except Exception as e:
            # frappe.log_error(frappe.get_traceback())
            try:
                loaded = clean_(data)
            except Exception as e:
                frappe.log_error(frappe.get_traceback())

        if loaded:
            try:
                evaluate(loaded['student'], loaded['quiz_response'],
                         quiz_name,loaded['course'],
                         loaded['program'], loaded['quiz_activity_name'])
                mark_as_checked(sh['name'])
            except Exception as e:
                frappe.log_error(frappe.get_traceback())

        if datetime.datetime.now() > stop_time:
            exit()



def mark_as_checked(name):
    doc = frappe.get_doc("Scheduled Quizzes", name)
    doc.checked = 1
    doc.save(ignore_permissions=True)
    frappe.db.commit()

def evaluate(student_email, quiz_response, quiz_name, course, program,activity_name):
    student = get_student(student_email)
    if student:
        quiz_response = json.loads(quiz_response)
        quiz = frappe.get_doc("Quiz", quiz_name)
        result, score, status = quiz.evaluate(quiz_response, quiz_name)
        add_quiz_activity(quiz_name, quiz_response, result, score, status,activity_name, student_email)
        return {'result': result, 'score': score, 'status': status}


def get_student(student_email):
    student_id = frappe.get_all("Student", {"student_email_id": student_email}, ["name"])[0].name
    return frappe.get_doc("Student", student_id)

def get_or_create_course_enrollment(student,course, program):
    course_enrollment = get_enrollment("course", course, student.name)
    if not course_enrollment:
        program_enrollment = get_enrollment('program', program, student.name)
        if not program_enrollment:
            return
        return student.enroll_in_course(course_name=course, program_enrollment=get_enrollment('program', program, student.name))
    else:
        return frappe.get_doc('Course Enrollment', course_enrollment)

def get_enrollment(master, document, student):

    if master == 'program':
        enrollments = frappe.get_all("Program Enrollment",
                                     filters={'student': student, 'program': document, 'docstatus': 1})
    if master == 'course':
        enrollments = frappe.get_all("Course Enrollment", filters={'student': student, 'course': document})

    if enrollments:
        return enrollments[0].name
    else:
        return None



def add_quiz_activity(quiz_name, quiz_response, answers, score, status, activity_name, student_email):
    try:
        result = {}
        # v is either True, False, "Essay" or [list of True and False]
        for k, v in answers.items():
            if isinstance(v, list):
                if sum(v) == len(v):
                    result.update({
                        k: 'Correct'
                    })
                else:
                    result.update({
                        k: 'Wrong'
                    })
            elif v == True:
                result.update({
                    k: 'Correct'
                })
            elif v == False:
                result.update({
                    k: 'Wrong'
                })
            else:
                result.update({
                    k: 'Essay'
                })
        result_data = []

        for key in answers:
            item = {}
            item['question'] = key
            if result[key] != "Essay":
                item['result_silid'] = result[key]
                item['quiz_result'] = result[key]
            else:
                item['quiz_result'] = 'Correct'

            if type(answers[key]) == list:
                item['evaluation_result'] = ", ".join(
                    'Correct' if is_correct else 'Wrong' for is_correct in answers[key])
            else:
                item['evaluation_result'] = result[key]

            selected_option = ""
            try:
                if not quiz_response[key]:
                    item['selected_option'] = "Unattempted"
                elif isinstance(quiz_response[key], list):
                    try:
                        item['selected_option'] = ', '.join(
                            frappe.get_value('Options', res, 'option') for res in quiz_response[key])
                        selected_option = item['selected_option']
                    except:
                        selected_option = ', '.join(quiz_response[key])
                        item['selected_option'] = ', '.join(quiz_response[key])
                else:
                    item['selected_option'] = frappe.get_value('Options', quiz_response[key], 'option')
                    selected_option = item['selected_option']
                    if not item['selected_option']:
                        item['selected_option'] = quiz_response[key]
            except:
                item['selected_option'] = "Unattempted"

            item['answer'] = selected_option or quiz_response[key]
            if type(item) == dict:
                result_data.append(item)

        quiz_activity = frappe.get_doc("Quiz Activity", activity_name)

        quiz_activity.score = score
        quiz_activity.status = status
        quiz_activity.result = []
        quiz_activity.is_result_ready = 1
        for res in result_data:
            quiz_activity.append("result", res)
        quiz_activity.owner = student_email
        quiz_activity.save(ignore_permissions=True, ignore_version=True)
        frappe.db.commit()


    except Exception as e:
        print(e)
        frappe.log_error(frappe.get_traceback())