import frappe
import os
from lms_api.lms_api.doctype.quiz_activity.quiz_activity import quiz_to_master_grade
from lms_api.lms_api.doctype.written_activity.written_activity import written_to_master_grade
base_path = os.path.dirname(os.path.realpath(__file__))

def escape(text):
    if text:
        return text.replace("'","\\'")
    return text

def quiz_worker(quiz):
    try:
        student_info = frappe.get_doc("Student",quiz['student'])
        quiz_info = frappe.get_doc("Quiz", quiz['quiz'])
        quiz_silid_info = None
        try:
            quiz_silid_info = frappe.get_doc("Quiz Silid", quiz_info.content_silid)

            quiz_info.program = quiz_info.program or quiz_silid_info.program
            quiz_info.topic = quiz_info.topic or quiz_silid_info.topic
            quiz_info.classwork_category = quiz_info.classwork_category or quiz_silid_info.classwork_category
            quiz_info.subject = quiz_info.subject or quiz_silid_info.course
            quiz_info.quarter = quiz_info.quarter or quiz_silid_info.quarter
            quiz_info.school_year = quiz_info.school_year or quiz_silid_info.school_year
            quiz_info.title = quiz_info.title or quiz_silid_info.quiz_title
            quiz_info.save()
            frappe.db.commit()

        except:
            # Quiz Silid not found
            pass
        docu = frappe.get_doc("Quiz Activity", quiz['name'])
        if quiz_silid_info is not None:
            docu.course = docu.course or quiz_silid_info.course
            docu.program =docu.program or quiz_silid_info.program
            docu.topic = docu.topic or quiz_silid_info.topic
            docu.quarter = docu.quarter or quiz_silid_info.quarter
            docu.school_year = docu.school_year or quiz_silid_info.school_year

        else:
            docu.program = docu.program or quiz_info.program
            docu.topic = docu.topic or quiz_info.topic
            docu.quarter = docu.quarter or quiz_info.quarter
            docu.school_year =docu.school_year or quiz_info.school_year

        docu.student_name = docu.student_name or (student_info.first_name + " " + student_info.last_name if docu.student_name == "" else docu.student_name)


        docu.quiz_title = quiz_info.title
        docu.highest_possible_score = quiz_info.max_points

        docu.save()
        frappe.db.commit()
    except Exception as e:
        pass

def written_worker(activity):
    try:
        student_info = frappe.get_doc("User", activity['student'])
        docu = frappe.get_doc("Written Activity",activity['name'])

        if activity['activity']:
            # Type is activity
            article_info = frappe.get_doc("Article", activity['activity'])
            content_silid_info = None
            try:
                content_silid_info = frappe.get_doc("Content Silid",article_info.content_silid)
                if content_silid_info.classwork_category:
                    article_info.classwork_category = content_silid_info.classwork_category
                if content_silid_info.highest_possible_score:
                    article_info.highest_possible_score = content_silid_info.highest_possible_score
                article_info.save()
                frappe.db.commit()

            except:
                pass
            if content_silid_info is not None:
                docu.program = docu.program or article_info.program or content_silid_info.program
                docu.subject = docu.subject or content_silid_info.course
                docu.title = docu.title or article_info.title or content_silid_info.title
                docu.student_name = docu.student_name or student_info.full_name
                docu.quarter = docu.quarter or article_info.quarter or content_silid_info.quarter
                docu.school_year = docu.school_year or article_info.school_year or content_silid_info.school_year
            else:
                docu.program = docu.program or article_info.program
                docu.title = docu.title or article_info.title
                docu.student_name = docu.student_name or student_info.full_name
                docu.quarter = docu.quarter or article_info.quarter
                docu.school_year = docu.school_year or article_info.school_year

        if activity['video']:
            # Type is Video
            video_info = frappe.get_doc("Video", activity['video'])
            content_silid_info = None
            try:
                content_silid_info = frappe.get_doc("Content Silid", video_info.content_silid)
                if content_silid_info.classwork_category:
                    video_info.classwork_category = content_silid_info.classwork_category
                if content_silid_info.highest_possible_score:
                    video_info.highest_possible_score = content_silid_info.highest_possible_score
                video_info.save()
                frappe.db.commit()

            except:
                pass
            if content_silid_info is not None:
                docu.program = docu.program or video_info.program or content_silid_info.program
                docu.subject = docu.subject or content_silid_info.course
                docu.title = docu.title or video_info.title or content_silid_info.title
                docu.student_name = docu.student_name or student_info.full_name
                docu.quarter = docu.quarter or video_info.quarter or content_silid_info.quarter
                docu.school_year = docu.school_year or video_info.school_year or content_silid_info.school_year
            else:
                docu.program = docu.program or video_info.program
                docu.title = docu.title or video_info.title
                docu.student_name = docu.student_name or student_info.full_name
                docu.quarter = docu.quarter or video_info.quarter
                docu.school_year = docu.school_year or video_info.school_year
        docu.save()

        frappe.db.commit()

    except Exception as e:
        pass

def schedule_mg_worker(schedule):
    try:
        if schedule['activity_type'] == "Quiz Activity":
            activity = frappe.get_doc("Quiz Activity", schedule['activity_name'])
            quiz_to_master_grade(activity)

        else:
            activity = frappe.get_doc("Written Activity", schedule['activity_name'])
            written_to_master_grade(activity)
        frappe.db.sql(f"DELETE FROM `tabSchedule MG` WHERE name='{schedule['name']}'")
        frappe.db.commit()
    except Exception as e:
        pass

def direct_to_mg_qa(act):
    try:
        activity = frappe.get_doc("Quiz Activity", act['name'])
        quiz_to_master_grade(activity)
    except Exception as e:
        pass

def direct_to_mg_wa(act):
    try:
        activity = frappe.get_doc("Written Activity", act['name'])
        written_to_master_grade(activity)
    except Exception as e:
        pass



def worker_quiz_master_grade(docu):
    print()

def worker_written_master_grade(docu):
    print()
