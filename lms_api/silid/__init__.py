import frappe
import re
from frappe.utils.background_jobs import enqueue
from frappe.model.rename_doc import rename_doc
from datetime import datetime

def update_names():#bench execute lms_api.silid.update_names
    for act in frappe.db.sql("""select name from `tabWritten Activity`"""):
        doc = frappe.get_doc("Written Activity",act[0])
        # if doc.activity:
        #     prog = frappe.db.sql("""SELECT program,content_sild FROM `tabArticle` WHERE name=%s""", (doc.activity))
        # else:
        #     prog = frappe.db.sql("""SELECT program,content_silid FROM `tabVideo` WHERE name=%s""", (doc.video))
        #
        # if prog != ():
        #     if prog[0][0]:
        #         # frappe.db.sql("""UPDATE `tabActivity` SET program = %s WHERE name=%s""",(prog[0][0],doc.activity))
        #         doc.program = prog[0][0]
        #
        #         # content_silid = frappe.db.sql("""select subject from `tabContent Silid` where name=%s""", prog[0][1])
        #         #
        #         # if content_silid != ():
        #         #     doc.course = content_silid[0][0]

        # if doc.owner != "Administrator":
        #     doc.student = doc.owner
        # doc.save()

        try:
            fullname = frappe.db.sql(
                f"SELECT `tabUser`.full_name FROM `tabUser` "
                f"WHERE `tabUser`.email='{doc.owner}'", as_dict=1
            )
            # self.student_name = fullname[0]['full_name']
            frappe.db.sql("""UPDATE `tabWritten Activity` SET student = %s,student_name=%s WHERE name=%s""", (doc.owner,fullname[0]['full_name'], doc.name))

        except:
            frappe.db.sql("""UPDATE `tabWritten Activity` SET student = %s WHERE name=%s""", (doc.owner, doc.name))
            pass



def set_program(doc,method):

    if doc.activity:
        prog = frappe.db.sql("""SELECT program,content_silid FROM `tabArticle` WHERE name=%s""",(doc.activity))
    else:
        prog = frappe.db.sql("""SELECT program,content_silid FROM `tabVideo` WHERE name=%s""",(doc.video))


    if prog != ():
        if prog[0][0]:
            # frappe.db.sql("""UPDATE `tabActivity` SET program = %s WHERE name=%s""",(prog[0][0],doc.activity))
            doc.program = prog[0][0]

            # content_silid = frappe.db.sql("""select subject from `tabContent Silid` where name=%s""", prog[0][1])
            #
            # if content_silid != ():
            #     doc.course = content_silid[0][0]



    if doc.owner != "Administrator":
        doc.student = doc.owner



def auto_submit_enrollee(doc,method):
    doc.insert()



#bench --site staging-hcm.silid.co execute lms_api.silid.test_name_topic --kwargs "{'name':'avengers'}"
def test_name_topic(name):
    tc = frappe.get_doc({
        "doctype": "Topic",
        # "parent": doc.topic,
        # "parenttype": "Topic",
        # "parentfield": "topic_content",
        "topic_name": name,
        "program": "English 10",
    }).insert(ignore_permissions=True)




def name_topic(doc,method):
    # doc.topic_name = doc.topic_name + "/" + doc.program
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if regex.search(doc.topic_name) == None:
        doc.name = doc.topic_name + '-' + doc.program + '-' + doc.subject
        if len(doc.name) > 140:
            # date_today = datetime.today().strftime('-%Y-%m-%d')
            # doc.name = doc.name[:120] + date_today
            doc.name = doc.name[:110] + str(frappe.utils.get_datetime())

    else:
        frappe.throw('Unable to Save. Please remove special character')



def on_trash_silid(doc,method):
    try:
        if doc.is_video == 1:
            video_list = frappe.get_all("Video", fields=['name'], filters={"content_silid": doc.name})
            for video in video_list:
                frappe.db.sql("""DELETE FROM `tabTopic Content` WHERE content=%s""", (video['name']))
                frappe.db.commit()
        else:
            article_list = frappe.get_all("Article", fields=['name'], filters={"content_silid": doc.name})
            for article in article_list:
                frappe.db.sql("""DELETE FROM `tabTopic Content` WHERE content=%s""", (article['name']))
                frappe.db.commit()
    except:
        pass

    to_do_tasks = frappe.get_all("To Do Tasks", fields=['name'], filters={"content_id": doc.name})
    if to_do_tasks:
        enqueue("lms_api.silid.delete_to_do_tasks",
                queue='long', to_do_tasks=to_do_tasks)

def delete_to_do_tasks(to_do_tasks):
    for to_do in to_do_tasks:
        to_do_task = frappe.delete_doc("To Do Tasks", to_do['name'], ignore_permissions=True,force=1)
        frappe.db.commit()

def validate_silid(doc,method):

    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if regex.search(doc.title) == None:
        pass
    else:
        frappe.throw('Unable to Save. Please remove special character')

    # Commented out Deletion of articles and video
    exists = frappe.db.sql("""SELECT name FROM `tabArticle` WHERE content_silid=%s""", doc.name)
    exists_vid = frappe.db.sql("""SELECT name FROM `tabVideo` WHERE content_silid=%s""", doc.name)

    if exists:
        #frappe.db.sql("""DELETE FROM `tabArticle` WHERE content_silid=%s AND title=%s""", (doc.name, doc.title))
        frappe.db.sql("""DELETE FROM `tabTopic Content` WHERE name=%s""", (doc.topic_content))
        frappe.db.commit()

    if exists_vid:
        #frappe.db.sql("""DELETE FROM `tabVideo` WHERE content_silid=%s AND title=%s""", (doc.name, doc.title))
        frappe.db.sql("""DELETE FROM `tabTopic Content` WHERE name=%s""", (doc.topic_content))
        frappe.db.commit()

    # course = frappe.db.sql("""SELECT name,course FROM `tabProgram Course` WHERE parent=%s LIMIT 1""",(doc.program))
    #e setup daan ang course, bale kung unsay program mao rapud dapat ang course


    # if course == ():
    #     frappe.throw("Please setup course")

    # doc.course = course[0][1]
    if not doc.course:
        frappe.throw("Please input subject/course.")
    existing_video_list = []
    existing_article_list = []
    if doc.is_video == 1:
        existing_video_list = frappe.get_all("Video", fields=['name'], filters={"content_silid": doc.name})
        #frappe.db.sql("""DELETE FROM `tabArticle` WHERE content_silid=%s AND title=%s""", (doc.name, doc.title))
        if doc.topic_content:
            frappe.db.sql("""DELETE FROM `tabTopic Content`
                              WHERE name=%s""", (doc.topic_content)) #remove from child table

        frappe.db.commit()
        url = doc.url.strip()
        if doc.provider == "Google Drive":
            temp = url.split("/")
            url = "https://drive.google.com/uc?id=" + temp[5]

        video = frappe.get_doc({
            "doctype": "Video",
            "title": doc.title,
            "provider": doc.provider,
            "url": url,
            "iframe_playposit": doc.iframe_playposit,
            "description": doc.description,
            "publish_date": doc.publish_date,
            "content_silid": doc.name,
            "program":doc.program,
            "course":doc.course,
            "topic":doc.topic,
            "quarter": doc.quarter,
            "school_year": doc.school_year,
            "highest_possible_score": doc.highest_possible_score,
            "classwork_category": doc.classwork_category,
            "deadline":doc.deadline,
        }).insert(ignore_permissions=True)

        frappe.db.commit()

        files = frappe.db.sql("""SELECT name
        FROM `tabFile` WHERE attached_to_name=%s AND attached_to_doctype='Content Silid'""", (doc.name))

        if files != ():

            for f in files:
                file_dict = frappe.get_doc("File", f[0])

                file_dict.update({"attached_to_name": video.name,
                                  "name": "",
                                  "attached_to_doctype": "Video"})
                print("****************************************")
                print("****************************************")
                print("****************************************")
                print(file_dict)
                f = frappe.get_doc(file_dict)

                f.insert(ignore_permissions=True)
                frappe.db.commit()

        tc = frappe.get_doc({
            "doctype": "Topic Content",
            "parent": doc.topic,
            "parenttype": "Topic",
            "parentfield": "topic_content",
            "content_type": "Video",
            "content": video.name,
            "content_title": doc.title
        }).insert(ignore_permissions=True)
        frappe.db.commit()
        doc.topic_content=tc.name
        enqueue("lms_api.silid.merge_content_silid",
                queue='long', doc=doc, existing_video_list=existing_video_list,
                existing_article_list=existing_article_list,
                video=video)
    else:
        existing_article_list = frappe.get_all("Article", fields=['name'], filters={"content_silid": doc.name})
        #frappe.db.sql("""DELETE FROM `tabVideo` WHERE content_silid=%s AND title=%s""", (doc.name, doc.title))
        frappe.db.sql("""DELETE FROM `tabTopic Content`
                                     WHERE name=%s""", (doc.topic_content))


        frappe.db.commit()


        arti = frappe.get_doc({
            "doctype": "Article",
            "title": doc.title,
            # "provider": doc.provider,
            # "url": doc.url,
            "author": doc.author,
            "content": doc.description,
            "publish_date": doc.publish_date,
            "content_silid": doc.name,
            "program": doc.program,
            "course": doc.course,
            "topic": doc.topic,
            "quarter": doc.quarter,
            "school_year": doc.school_year,
            "deadline": doc.deadline,
            "highest_possible_score": doc.highest_possible_score,
            "classwork_category": doc.classwork_category,
            "time_limit": doc.time_limit,
        }).insert(ignore_permissions=True)

        doc.article_number = arti.name

        frappe.db.commit()


        files = frappe.db.sql("""SELECT name
FROM `tabFile` WHERE attached_to_name=%s AND attached_to_doctype='Content Silid'""",(doc.name))

        if files != ():

            for f in files:
                file_dict = frappe.get_doc("File",f[0])

                file_dict.update({"attached_to_name": arti.name,
                                  "name": "",
                                  "attached_to_doctype": "Article"})
                print("****************************************")
                print("****************************************")
                print("****************************************")
                print(file_dict)
                f = frappe.get_doc(file_dict)

                f.insert(ignore_permissions=True)

        tc = frappe.get_doc({
            "doctype": "Topic Content",
            "parent": doc.topic,
            "parenttype": "Topic",
            "parentfield": "topic_content",
            "content_type": "Article",
            "content": arti.name,
            "content_title": doc.title
        }).insert(ignore_permissions=True)
        frappe.db.commit()
        doc.topic_content = tc.name

        enqueue("lms_api.silid.merge_content_silid",
                queue='long', doc=doc, existing_video_list=existing_video_list,
                existing_article_list=existing_article_list,
                arti=arti)

    #ayha na de.lete ang Course Topic if wala na lain Topics sa ana nga Course
    exists_topic_in_course = frappe.db.sql("""SELECT Count(*)
              FROM `tabCourse Topic` WHERE parent=%s AND topic=%s""",(doc.course,doc.topic))
    if exists_topic_in_course[0][0] == 0:
        ct = frappe.get_doc({
            "doctype": "Course Topic",
            "parent": doc.course,
            "parenttype": "Course",
            "parentfield": "topics",
            "topic": doc.topic,
        }).insert(ignore_permissions=True)
        frappe.db.commit()



    # enqueue("lms_api.silid.notifications.new_content", queue='long', name=doc.name,program=doc.program)

    #
    enqueue("lms_api.silid.create_to_do_tasks",
            queue='long', doc=doc)
    # create_to_do_tasks(doc)

def merge_content_silid(doc,existing_video_list,existing_article_list,video=None,arti=None):
    if doc.is_video == 1:
        if existing_video_list:
            for video_hit in existing_video_list:
                rename_doc("Video",video_hit['name'], video.name ,merge=True, ignore_permissions=True)
                frappe.db.commit()
    else:
        if existing_article_list:
            for article_hit in existing_article_list:
                rename_doc("Article", article_hit['name'], arti.name, merge=True, ignore_permissions=True)
                frappe.db.commit()

def create_to_do_tasks(doc):
    course_enrollments = frappe.get_all("Course Enrollment", fields=['student'], filters={"course": doc.course})
    to_exist_already = frappe.get_all("To Do Tasks", fields=['name'],
                                      filters={"content_id": doc.name, "program": doc.program})
    if len(to_exist_already) == 0:
        for enrollment in course_enrollments:
            student_info = frappe.get_doc("Student", enrollment['student'])
            if doc.is_video == 1:
                task_type = "Video"
            else:
                task_type = "Article"
            to_do = {
                "doctype": "To Do Tasks",
                "status": "To Do",
                "program": doc.program,
                "course": doc.course,
                "topic": doc.topic,
                "classwork_category": doc.classwork_category,
                "task_type": task_type,
                "task_doctype": "Content Silid",
                "title": doc.title,
                "content_id": doc.name,
                "publish_date": doc.publish_date,
                "deadline": doc.deadline,
                "owner": student_info.user or student_info.student_email_id
            }
            to_do_ = frappe.get_doc(to_do)
            to_do_.insert(ignore_permissions=True)
            frappe.db.commit()
    else:
        try:
            task_list = []
            if doc.is_video == 1:
                task_type = "Video"
            else:
                task_type = "Article"
            for task in to_exist_already:
                task_list.append(task['name'])
            if doc.deadline is None:
                deadline = "NULL"
            else:
                deadline = f"'{doc.deadline}'"
            if doc.publish_date is None:
                publish_date = "NULL"
            else:
                publish_date = f"'{doc.publish_date}'"
            frappe.db.sql(f"UPDATE `tabTo Do Tasks` "
                          f"SET title='{escape(doc.title)}',"
                          f"publish_date={publish_date},"
                          f"deadline={deadline},"
                          f"task_type='{task_type}',"
                          f"classwork_category='{escape(doc.classwork_category)}',"
                          f"topic='{escape(doc.topic)}',"
                          f"program='{escape(doc.program)}'"
                          f"WHERE name in {str(tuple(task_list))}")

        except Exception as e:
            print(e)
            pass


def escape(text):
    if text:
        return text.replace("'","\\'")
    return text

#bench --site staging-hcm.silid.co execute lms_api.silid.test_add
#bench --site staging-hcm.silid.co execute lms_api.silid.test_add --kwargs "{'title':'avengers'}"
def test_add(title):

    doc = frappe.get_doc({
        "doctype": "Content Silid",
        "program": "English 10",
        "topic": "new topic english 10",
        "title": title,
        "description": title,
    }).insert(ignore_permissions=True)

    frappe.db.commit()


def attach_f(doc,method):
    origin = frappe.form_dict
    file_dict = doc.as_dict()
    if file_dict['attached_to_name'] is None:
        # Video
        print("video")
        file_dict.update({"attached_to_name": origin['docname'],
                          "name": "",
                          "attached_to_doctype": "Video", "is_private": 0})
        f = frappe.get_doc(file_dict)

        f.insert(ignore_permissions=True)
        frappe.db.commit()

    elif doc.attached_to_doctype == "Content Silid" and file_dict['attached_to_name'] is not None:
        print("Article")
        file_dict = doc.as_dict()
        enrollee_name = frappe.db.sql("""SELECT article_number FROM `tabContent Silid` WHERE name=%s"""
                                      ,(file_dict['attached_to_name']))
        if enrollee_name == ():
            return None
        file_dict.update({"attached_to_name":enrollee_name[0][0],
                          "name":"",
                          "attached_to_doctype":"Article", "is_private":0})
        f = frappe.get_doc(file_dict)

        f.insert(ignore_permissions=True)
        frappe.db.commit()

def mark_to_do_done(doc,method):
    enqueue("lms_api.silid.enqueue_mark_to_do_done",
            queue='long', doc=doc)

def enqueue_mark_to_do_done(doc):
    if doc.content_type == "Article":
        content_silid = frappe.get_all("Article", fields=['content_silid'], filters={"name": doc.content}, limit_page_length=1)
    else:
        content_silid = frappe.get_all("Video",fields=['content_silid'], filters={"name":doc.content}, limit_page_length=1)

    if content_silid:
        get_to_dos = frappe.get_all("To Do Tasks", fields=['name'],filters={"content_id": content_silid[0]['content_silid'],"owner":frappe.session.user })
        for to_mark in get_to_dos:
            # to_do = frappe.delete_doc("To Do Tasks", to_mark['name'],ignore_permissions=True,force=1)
            frappe.db.sql("""update `tabTo Do Tasks` set status='Done' where name=%s""",(to_mark['name']))
            # frappe.db.commit()
