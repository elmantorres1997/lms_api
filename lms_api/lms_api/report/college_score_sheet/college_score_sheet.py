# Copyright (c) 2013, Wela School System and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
    columns, data = [], []

    program_filter = filters['program'].replace("'", "\\'")
    course_filter = filters['course'].replace("'", "\\'")
    quarter_filter = filters['quarter'].replace("'", "\\'")
    columns = [
                {"label": "Student", 'width': 100, "fieldname": "student"}
    ]
    data.append(
        {"student": "<b>Highest Possible Score</b>","student_code":"", "final_grade":""}
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
        f"SELECT * FROM `tabMaster Grade` "
        f"WHERE program='{program_filter}' "
        f"AND course='{course_filter}' "
        f"AND quarter='{quarter_filter}' ", as_dict=1
    )
    classwork_category_weights = frappe.db.sql(f"SELECT * FROM `tabClasswork Category Weight` WHERE parent='{course_filter}'", as_dict=1)

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
            highest_possible_score = record['highest_possible_score']
            raw_score = record['raw_score']
            student_code = record['student']
            student_name = record['student_name']
            does_column_exist = next((x for x in columns if x['fieldname'] == activity_title), None)
            if does_column_exist is None:
                columns.append({
                    "label": activity_title,
                    "width": 130,
                    "fieldname": activity_title
                })
            data[0].update({
                activity_title: f"{highest_possible_score}",
                f"hps_{activity_title}": { "highest_possible_score": highest_possible_score, "is_counted": 0 }
            })

            if raw_score:
                total_points_earned += float(raw_score)

            total_points_earned_obj.update({
                f"{student_code}_tpe": total_points_earned
            })
            does_exist = next((x for x in data if x['student_code'] == student_code), None)
            if does_exist is not None:
                does_exist.update({
                    activity_title: raw_score,
                    f"raw_score_{activity_title}": { "raw_score": raw_score, "is_counted": 0 }
                })
            else:
                # Append Data of student
                data.append({
                    "student_code": student_code,
                    "student": student_name,
                    activity_title: raw_score,
                    f"raw_score_{activity_title}": { "raw_score": raw_score, "is_counted": 0 },

                })

        columns.append({
            "label": f"{component_col} Total",
            "width": 130,
            "fieldname": f"total_{component_col}"
        })
        # columns.append({
        #     "label": f"{component_col} Percentage",
        #     "width": 130,
        #     "fieldname": f"percentile_{component_col}"
        # })
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
            f"total_{component_col}": f"{high_total}",
            f"percentile_{component_col}":f"<span style='color:#006400!important;font-weight:bold';>{component_weight}%</span>"
        })
        # final_weight += component_weight


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
                percentile = float((total / float(data[0][f'total_{component_col}'])) * float(component_weight)) if float(data[0][f'total_{component_col}']) else 0.0
            except:
                percentile = 0.0

            databit.update({
                f"total_{component_col}": f"{total}",
                f"percentile_{component_col}":
                    "<span style='font-weight:bold';>{:.2f}%</span>".format(percentile) if percentile > 75.0 else
                    "<span style='font-weight:bold';>{:.2f}%</span>".format(percentile),
                f"raw_percentile_{component_col}": percentile
            })
        #
        #
        #
        # data[0].update({
        #     f"final_grade": "<span style='color:#006400!important;font-weight:bold';>{:.2f}%</span>".format(final_weight),
        # })

    # columns.append({
    #     "label": f"Final Percentage",
    #     "width": 130,
    #     "fieldname": f"final_grade"
    # })

    # for databit in data[1:]:
    #     total = 0
    #     for attr, value in databit.items():
    #         try:
    #             if "raw_percentile" in attr:
    #                 total += float(value)
    #         except:
    #             pass
    #     databit.update({
    #         "final_grade":
    #             "<span style='color:#006400!important;font-weight:bold';>{:.2f}%</span>".format(total) if total > 75.0 else
    #             "<span style='color:#e4193f!important;font-weight:bold';>{:.2f}%</span>".format(total)
	#
    #     })

    if len(data) == 1:
        data.clear()

    return columns, data
