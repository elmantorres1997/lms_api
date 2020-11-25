try:
    from tqdm import *
    from contextlib import closing
    import sys
    import frappe
except:
    print("Run: bench setup requirements --python")
    exit()

from multiprocessing import Pool
from lms_api.patches.workers import *
import time

# bench --site all execute lms_api.patches.master_grade.fix_quiz
def fix_quiz(multi=False):
    """ This will fix quiz activity list """

    print("Fixing Quiz Activity List")


    all_quiz_activity = frappe.db.sql(f"SELECT name,quiz,student FROM `tabQuiz Activity` "
                                      f"WHERE DATE(creation) < '2020-09-01' ",as_dict=1)

    if multi:
        pool = Pool(os.cpu_count()-1)
        with closing(pool) as p:
            for _ in tqdm(p.imap_unordered(quiz_worker, all_quiz_activity), total=len(all_quiz_activity)):
               pass
    else:
        for quiz in all_quiz_activity:
            quiz_worker(quiz)



# bench --site all execute lms_api.patches.master_grade.fix_written
def fix_written(multi=False):
    """ This will fix written activity list """

    print("Fixing Written Activity List")


    all_written_activity = frappe.db.sql(f"SELECT name,video,activity,student FROM `tabWritten Activity` WHERE DATE(creation) < '2020-09-01'", as_dict=1)

    if multi:
        pool = Pool(os.cpu_count()-1)
        with closing(pool) as p:
            for _ in tqdm(p.imap_unordered(written_worker, all_written_activity), total=len(all_written_activity)):
                pass
    else:
        for written in all_written_activity:
            written_worker(written)


def execute_schedules(multi=False):
    """ This will execute all Scheduled Master Grade """

    print("Executing Scheduled Master Grade")

    schedules = frappe.db.sql("SELECT name,activity_type,activity_name FROM `tabSchedule MG` WHERE 1", as_dict=1)
    
    if multi:
        pool = Pool(os.cpu_count() - 1)
        with closing(pool) as p:
            for _ in tqdm(p.imap_unordered(schedule_mg_worker, schedules), total=len(schedules)):
                pass
    else:
        for schedule in schedules:
            schedule_mg_worker(schedule)

# bench --site all execute lms_api.patches.master_grade.to_master_grade
def to_master_grade(multi=False):
    """ This will will resave Quiz Activity and Written Activity to QA """

    print("Resaving all Quiz Activity and Written Activity to Master Grade")

    all_quiz_activity = frappe.db.sql(f"SELECT name FROM `tabQuiz Activity` "
                                      f"WHERE DATE(creation) > '2020-08-31'", as_dict=1) # After August 31, 2020

    print("Starting Quiz Activity")
    try:
        if multi:
            pool = Pool(os.cpu_count()-1)
            with closing(pool) as p:
                for _ in tqdm(p.imap_unordered(direct_to_mg_qa, all_quiz_activity), total=len(all_quiz_activity)):
                    pass
        else:
            total = len(all_quiz_activity)
            count = 0
            for act in all_quiz_activity:
                direct_to_mg_qa(act)
                count += 1
                sys.stdout.write('\r')
                sys.stdout.write(f"Progress: {count}/{total}")
                sys.stdout.flush()
    except Exception as e:
        print(e)



    all_written_activity = frappe.db.sql(
        f"SELECT name,video,activity,student FROM `tabWritten Activity` WHERE DATE(creation) > '2020-08-31'", as_dict=1)
    print("Starting Written Activity")
    try:
        if multi:
            pool = Pool(os.cpu_count() - 1)
            with closing(pool) as p:
                for _ in tqdm(p.imap_unordered(direct_to_mg_wa, all_written_activity), total=len(all_written_activity)):
                    pass
        else:
            total = len(all_written_activity)
            count = 0
            for act in all_written_activity:
                direct_to_mg_wa(act)
                count += 1
                sys.stdout.write('\r')
                sys.stdout.write(f"Progress: {count}/{total}")
                sys.stdout.flush()

    except Exception as e:
        print(e)

# bench --site all execute lms_api.patches.master_grade.remove_edu
def remove_edu():
    import os
    import time
    db_name = frappe.conf.get("db_name")
    print("Creating backup of Master Grade. Enter MySQL password")
    os.system(f'mysqldump -u root -p {db_name} "tabMaster Grade" > dumpit.sql')
    time.sleep(10)
    print("Please check sites folder if backup was success.")
    input("Press any key to continue...")
    frappe.db.sql(f"DELETE FROM `tabMaster Grade` WHERE `tabMaster Grade`.`activity_name` LIKE '%EDU-%'")
    frappe.db.commit()
    print("Operation successful")

def escape(text):
    if text:
        return text.replace("'","\\'")
    return text

# bench --site all execute lms_api.patches.master_grade.fix_subjects
def fix_subjects():
    no_subjects = frappe.db.sql(f"SELECT name,activity_name,activity_type FROM `tabMaster Grade` WHERE course is NULL OR course=''", as_dict=1)
    total = len(no_subjects)
    count = 0
    for act in no_subjects:
        # get subject
        if act['activity_type'] == "Quiz Activity":
            try:
                quiz_list = frappe.get_doc("Quiz", act['activity_name'])
                quiz_silid = frappe.get_doc("Quiz Silid", quiz_list.content_silid)
                frappe.db.sql(f"UPDATE `tabMaster Grade` SET course='{escape(quiz_silid.course)}' WHERE name='{act['name']}'")
                frappe.db.commit()
            except:
                pass
        else:
            # test Article
            try:
                article = frappe.get_doc("Article", act['activity_name'])
                content_silid = frappe.get_doc("Content Silid", article.content_silid)
                frappe.db.sql(f"UPDATE `tabMaster Grade` SET course='{escape(content_silid.course)}' WHERE name='{act['name']}'")
                frappe.db.commit()
            except:
                # video
                try:
                    video = frappe.get_doc("Video", act['activity_name'])
                    content_silid = frappe.get_doc("Content Silid", video.content_silid)
                    frappe.db.sql(f"UPDATE `tabMaster Grade` SET course='{escape(content_silid.course)}' WHERE name='{act['name']}'")
                    frappe.db.commit()
                except:
                    pass

        count+=1
        sys.stdout.write('\r')
        sys.stdout.write(f"Progress: {count}/{total}")
        sys.stdout.flush()


# bench --site all execute lms_api.patches.master_grade.execute_all
def execute_all(multi=False):
    """ Start script in ordered manner to avoid errors """

    print("Executing All Scripts available")

    try:
        fix_quiz(multi)
    except:
        time.sleep(3)
        pass
    try:
        fix_written(multi)
    except:
        time.sleep(3)
        pass

    try:
        execute_schedules(multi)
    except:
        time.sleep(3)
        pass
