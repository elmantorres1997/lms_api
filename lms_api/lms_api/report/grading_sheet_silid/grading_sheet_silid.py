# Copyright (c) 2013, Bai Web and Mobile Lab and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.frappeclient import FrappeClient

#lms_api.lms_api.report.grading_sheet_silid.grading_sheet_silid.get_data
def get_data():
    columns, data = [], []

    columns = [
        {"label": "Student", 'width': 100, "fieldname": "student"}
    ]

    program = "Filipino 8 Summer Class 2020"

    acts = frappe.db.sql("""SELECT `tabWritten Activity`.activity FROM `tabWritten Activity`
                               WHERE program=%s
                              """, (program), as_dict=True)
    print(acts)
    for act in acts:
        columns.append({"label": act['activity'], 'width': 100, "fieldname": act['activity']})

    grades = frappe.db.sql("""SELECT `tabUser`.full_name as student, `tabWritten Activity`.activity, `tabWritten Activity`.grade,
               `tabContent Silid`.highest_possible_score, `tabContent Silid`.classwork_category  FROM `tabWritten Activity`
                             INNER JOIN `tabArticle`
                             ON `tabArticle`.name = `tabWritten Activity`.activity
                             INNER JOIN `tabContent Silid`
                              ON `tabArticle`.content_silid = `tabContent Silid`.name
                              INNER JOIN `tabUser` ON `tabUser`.name = `tabWritten Activity`.owner
                              WHERE `tabWritten Activity`.program=%s
                             ORDER BY `tabUser`.full_name
                              """, (program), as_dict=True)

    stud = {}

    current_stud = ""
    print(grades)
    for i, grade in enumerate(grades):

        if i == 0:
            current_stud = grade['student']
            stud.update({"student": grade["student"],
                         grade["activity"]: str(grade["grade"]) + '/' + str(grade['highest_possible_score'])})

        else:
            if current_stud == grade['student']:
                if grade["grade"]:
                    stud.update({grade["activity"]: str(grade["grade"]) + '/' + str(grade['highest_possible_score'])})
                else:
                    stud.update({"student": grade["student"],
                                 grade["activity"]: ""})
            else:
                data.append(stud)
                current_stud = grade['student']
                stud = {}
                if grade["grade"]:
                    stud.update({"student": grade["student"],
                                 grade["activity"]: str(grade["grade"]) + '/' + str(grade['highest_possible_score'])})
                else:
                    stud.update({"student": grade["student"],
                                 grade["activity"]: ""})
            if i == len(grades) - 1:
                data.append(stud)
                stud = {}

    return columns, data


def execute(filters=None):
    columns, data = [], []

    # program_filter = filters['program'].replace("'", "\\'")
    course_filter = filters['course'].replace("'", "\\'")
    quarter_filter = filters['quarter'].replace("'", "\\'")
    raw_score_filter = filters.get("raw_score")
    columns = [
                {"label": "Last Name", 'width': 100, "fieldname": "last_name"},
                {"label": "First Name", 'width': 100, "fieldname": "first_name"},

    ]
    data.append(
        {"first_name": "<b>Highest Possible Score</b>",

         "last_name":"BOYS",

         "student_code":"", "final_grade":0}
    )

    """
    1) Get Master Grade Records according to Filters
    2) Group Each grade by Component
    3) Count Sub totals
    4) Count total
    5) Last Column final grade for Quarter
    """

    """1) Get Master Grade Records according to Filters"""


    master_grade_records = frappe.db.sql(
        f"SELECT tb1.*, tb2.last_name,tb2.first_name,tb2.gender "
        f"FROM `tabMaster Grade` tb1 "
        f"INNER JOIN `tabStudent` tb2 "
        f"ON tb1.student=tb2.name "
        f"WHERE tb1.course='{course_filter}' "
        f"AND tb1.quarter='{quarter_filter}'"
        f"AND tb1.raw_score IS NOT NULL "
        f"ORDER BY tb2.last_name ASC, tb2.first_name ASC", as_dict=1
    )
    classwork_category_weights = frappe.db.sql(f"SELECT * FROM `tabClasswork Category Weight` WHERE parent='{course_filter}' ORDER BY idx ASC", as_dict=1)

    component_collection = []
    for compo in classwork_category_weights:
        component = compo['classwork_category']
        weight = compo['weight']
        #Fill up component collections
        if component not in component_collection:
            component_collection.append({"component": component, "weight": weight})
        # component_collection.sort()

    final_percentage = 0
    final_weight = 0
    for attribute in component_collection:
        component_col = attribute["component"]
        component_weight = attribute['weight']
        records = [x for x in master_grade_records if x["component"] == component_col ]
        total_points_earned = 0
        total_points_earned_obj = {}
        for record in records:

            component = record['component']
            activity_title = record['activity_title']
            activity_name = record['activity_name']
            highest_possible_score = record['highest_possible_score']
            raw_score = record['raw_score']
            student_code = record['student']
            # student_name = record['student_name']
            first_name = record['first_name']
            last_name = record['last_name']
            gender = record['gender']
            # does_column_exist = next((x for x in columns if x['fieldname'] == activity_name), None)
            if not any(d['fieldname'] == activity_name for d in columns):
            # if does_column_exist is None:
                columns.append({
                    "label": activity_title,
                    "width": 130,
                    "fieldname": activity_name
                })
            data[0].update({
                activity_name: f"{highest_possible_score}",
                "gender": "Male",
                f"hps_{activity_name}": { "highest_possible_score": highest_possible_score, "is_counted": 0 }
            })

            if raw_score:
                total_points_earned += float(raw_score)

            total_points_earned_obj.update({
                f"{student_code}_tpe": total_points_earned
            })
            does_exist = next((x for x in data if x['student_code'] == student_code), None)
            if does_exist is not None:
                does_exist.update({
                    activity_name: float(raw_score),
                    "gender": gender,
                    f"raw_score_{activity_name}": { "raw_score": float(raw_score), "is_counted": 0 }
                })
            else:
                # Append Data of student
                data.append({
                    "student_code": student_code,
                    "first_name": first_name.upper(),
                    "last_name": last_name.upper(),
                    "gender": gender,
                    activity_name: float(raw_score),
                    f"raw_score_{activity_name}": { "raw_score": float(raw_score), "is_counted": 0 },

                })
        if not raw_score_filter:
            columns.append({
                "label": "Total",
                "width": 130,
                "fieldname": f"total_{component_col}"
            })
            columns.append({
                "label": f"{component_col} Percentage",
                "width": 130,
                "fieldname": f"percentile_{component_col}"
            })
        high_total = 0

        # highest Possible scores to table
        for attr, value in data[0].items():
            try:
                if "hps" in attr and value['is_counted'] == 0 and "total_" not in attr:
                    high_total += float(value['highest_possible_score'])
                    data[0][attr]['is_counted'] = 1
            except:
                pass

        data[0].update({
            f"total_{component_col}": float(high_total),
            f"percentile_{component_col}":float(component_weight)
        })
        final_weight += component_weight


        for databit in data[1:]:
            total = 0

            for attr, value in databit.items():
                try:
                    if "hps" not in attr and "total_" not in attr and value['is_counted'] == 0:
                        total += float(value['raw_score'])
                        databit[attr]['is_counted'] = 1
                except:
                    pass

            try:
                if total == 0:
                    percentile = 0.0
                else:
                # percentile = float((total / float(data[0][f'total_{component_col}'])) * float(component_weight)) if float(data[0][f'total_{component_col}']) else 0.0
                    percentile = float(((total / float(data[0][f'total_{component_col}'])) * 50 + 50) * float(component_weight/100)) if float(data[0][f'total_{component_col}']) else 0.0
            except:
                percentile = 0.0

            databit.update({
                # f"total_{component_col}": f"{total}",
                f"total_{component_col}": float(total),
                # f"percentile_{component_col}":
                #     "<span style='font-weight:bold';>{:.2f}</span>".format(float(percentile)) if percentile > 75.0 else
                #     "<span style='font-weight:bold';>{:.2f}</span>".format(float(percentile)),

                f"percentile_{component_col}":float(round(percentile,2)),

                f"raw_percentile_{component_col}": float(round(percentile,2))
            })



        data[0].update({
            f"final_grade": float(final_weight),
        })

    if not raw_score_filter:
        columns.append({
            "label": f"Final Percentage",
            "width": 130,
            "fieldname": f"final_grade"
        })

    for databit in data[1:]:
        total = 0
        for attr, value in databit.items():
            try:
                if "raw_percentile" in attr:
                    total += float(value)
            except:
                pass
        databit.update({  "final_grade": round(total,2) })

    if len(data) == 1:
        data.clear()

    boys = []
    girls = []
    for group in data:
        if group['gender'] == "Male":
            boys.append(group)
        else:
            girls.append(group)
    if boys:
        final_data = boys + [{"first_name": "----------------","last_name":"GIRLS"}] + girls
    else:
        final_data = data

    return columns, final_data

@frappe.whitelist()
def send_grades_to_wela(grades):
    from frappe.utils.password import get_decrypted_password
    import json
    json_grades = json.loads(grades)
    params ={
        "grades": json_grades
    }
    wela_settings = frappe.get_doc("Wela Settings")
    wela_api_url = wela_settings.wela_api_url
    wela_api_username = wela_settings.wela_api_username
    wela_api_password = get_decrypted_password("Wela Settings", "Wela Settings", fieldname="wela_api_password")
    if wela_api_url and wela_api_username and wela_api_password:

        conn = FrappeClient(wela_api_url, wela_api_username, wela_api_password)
        lms_user = conn.get_api("wela.grading.doctype.submit_grading_sheet.submit_grades_from_silid", params)
        return lms_user

    else:
        frappe.throw("Please Set API settings on Wela Settings")

# OLD VERSION
# def execute(filters=None):
#     columns, data = [],[]
#
#     columns = [
#         {"label": "Student", 'width': 100, "fieldname": "student"}
#     ]
#     data.append(
#         {"student": "<b>Highest Possible Score</b>"}
#     )
#     classwork_categories = frappe.db.sql(
#         f"SELECT name FROM `tabClasswork Category`", as_dict=1
#     )
#     program = filters.get("program")
#     for category in classwork_categories:
#         category_name = category['name']
#         total_points_earned_obj = {}
#         total_points_earned = 0
#
#         # Get Written Activities by Course and Classwork Category
#         written_activities = frappe.db.sql(
#             f"SELECT "
#             f"`tabCourse Enrollment`.student as student_code, "
#             f"`tabStudent`.student_email_id,"
#             f"`tabStudent`.first_name,"
#             f"`tabStudent`.middle_name,"
#             f"`tabStudent`.last_name,"
#             f"`tabWritten Activity`.`activity` as written_activity_activity,"
#             f"`tabWritten Activity`.`program` as written_activity_program,"
#             f"`tabWritten Activity`.`grade` as written_activty_grade,"
#             f"`tabContent Silid`.`highest_possible_score`,"
#             f"`tabContent Silid`.`classwork_category`"
#             f"FROM `tabCourse Enrollment` "
#             f"JOIN `tabStudent` ON `tabCourse Enrollment`.student=`tabStudent`.name "
#             f"JOIN `tabWritten Activity` ON `tabWritten Activity`.`student`=`tabStudent`.`student_email_id` "
#             f"LEFT JOIN `tabContent Silid` ON `tabContent Silid`.`name`=`tabWritten Activity`.`activity` "
#             f"WHERE `tabContent Silid`.`classwork_category`='{category_name}' "
#             f"AND `tabWritten Activity`.`program`='{program}' "
#             f"GROUP BY `tabWritten Activity`.`activity`"
#             , as_dict=1
#         )
#
#         # Get Quizzes Activities by Course and Worklass Category
#         quiz_activities = frappe.db.sql(
#             f"SELECT "
#             f"`tabCourse Enrollment`.student as student_code, "
#             f"`tabStudent`.student_email_id,"
#             f"`tabStudent`.first_name,"
#             f"`tabStudent`.middle_name,"
#             f"`tabStudent`.last_name,"
#             f"`tabQuiz Activity`.`name` ,"
#             f"`tabQuiz Activity`.`quiz` as quiz_name,"
#             f"`tabQuiz Activity`.`course`,"
#             f"`tabQuiz Activity`.`score`,"
#             f"`tabQuiz`.`max_points`,"
#             f"`tabQuiz`.`classwork_category` as quiz_classwork_category "
#             f"FROM `tabCourse Enrollment` "
#             f"LEFT JOIN `tabStudent` ON `tabCourse Enrollment`.student=`tabStudent`.name "
#             f"LEFT JOIN `tabQuiz Activity` ON `tabCourse Enrollment`.`student`=`tabQuiz Activity`.`student` "
#             f"LEFT JOIN `tabQuiz` ON `tabQuiz`.`name`=`tabQuiz Activity`.`quiz` "
#             f"WHERE `tabQuiz`.`classwork_category`='{category_name}' "
#             f"AND `tabQuiz Activity`.`course`='{program}' "
#             f"GROUP BY `tabCourse Enrollment`.student, quiz"
#             ,as_dict=1
#         )
#
#
#
#         if written_activities:
#             for written_activity in written_activities:
#                 # Append Column name according to written activity
#                 columns.append({
#                     "label": written_activity['written_activity_activity'],
#                     "width": 130,
#                     "fieldname": written_activity['written_activity_activity']
#                 })
#
#                 # Append Highest possible score on first row
#                 data[0].update({
#                     written_activity['written_activity_activity']: f"{written_activity['highest_possible_score']}",
#                     "hps": written_activity['highest_possible_score']
#                 })
#
#                 total_points_earned += float(written_activity['written_activty_grade'])
#
#                 total_points_earned_obj.update({
#                     f"{written_activity['student_code']}_tpe": total_points_earned
#                 })
#
#                 # Append Data of student
#                 full_name = f"{written_activity['first_name'] or ''} {written_activity['middle_name'] or ''} {written_activity['last_name'] or ''}"
#                 data.append({
#                     "student_code": written_activity['student_code'],
#                     "student": full_name,
#                     written_activity['written_activity_activity']: written_activity['written_activty_grade'],
#
#                 })
#
#         if quiz_activities:
#
#             for quiz in quiz_activities:
#
#                 # Append column name according to Quiz Name
#                 columns.append({
#                     "label": quiz['quiz_name'],
#                     "width": 130,
#                     "fieldname": quiz['quiz_name']
#                 })
#
#                 # Append Max Points on first row
#                 data[0].update({
#                     quiz['quiz_name']: quiz['max_points'],
#                     "hps": quiz['max_points']
#                 })
#
#                 # Find existing Object of Student from data and update with Quiz Score
#                 does_exist = next((x for x in data if x== quiz['student_code']), None)
#                 if does_exist is not None:
#                     does_exist.update({
#                         quiz['quiz_name']: quiz['score']
#                     })
#                 else:
#                     full_name = f"{quiz['first_name'] or ''} {quiz['middle_name'] or ''} {quiz['last_name'] or ''}"
#                     data.append({
#                         "student_code": quiz['student_code'],
#                         "student": full_name,
#                         quiz['quiz_name']: quiz['score']
#                     })
#
#         # Count Total and Percentile per Workclass Category
#         if written_activities or quiz_activities:
#             columns.append({
#                 "label": "Total",
#                 "width": 130,
#                 "fieldname": f"total_{category_name}"
#             })
#             columns.append({
#                 "label": f"{category_name} Percentage",
#                 "width": 130,
#                 "fieldname": f"percentile_{category_name}"
#             })
#             for databit in data:
#                 total = 0
#                 for attr, value in databit.items():
#                     try:
#                         total += float(value) if attr != "hps" else 0
#                     except:
#                         pass
#                 percentile = float((total / int(data[0]['hps'])) * 100) if int(data[0]['hps']) else 100.0
#                 databit.update({
#                     f"total_{category_name}": f"{total}",
#                     f"percentile_{category_name}":
#                         f"<span style='color:#006400!important;font-weight:bold';>{percentile}%</span>" if percentile > 75.0 else
#                         f"<span style='color:#c30c0c!important;font-weight:bold';>{percentile}%</span>"
#                 })
#
#     if len(data) == 1:
#         data.clear()
#     return columns, data