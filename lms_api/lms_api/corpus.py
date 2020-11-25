import frappe
import json
import random
from frappe.utils.password import update_password

def random_word(length):
    return ''.join(random.choice(['A','B','C','D','E','F','G','H','J','K',
                                  'L','M','N','O','P','Q','R','S','T','U',
                          'V','W','X','Y','Z']) for i in range(length))


#bench execute lms_api.lms_api.create_k12_users.create_account_
@frappe.whitelist()
def create_account_(first_name,last_name,id_number,
                   contact_number,url,welcome_text,
                   programs,courses,grade_level,school_year):
    if not frappe.db.exists('User', id_number + "@wela.online"):

        import ast
        print("((( XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX )))")
        print(programs,courses)
        programs = ast.literal_eval(programs)
        courses = ast.literal_eval(courses)
        # x = [n.strip() for n in x]







        user = frappe.get_doc({
            "doctype": "User",
            "first_name": first_name,
            "last_name": last_name,
            "username": id_number,
            "email": id_number + "@wela.online",
            "user_type": "System User",
            "send_welcome_email": 0
        }).insert(ignore_permissions=True)

        user.append('roles', {
            "doctype": "Has Role",
            "role": "Student"
        })

        for d in user.block_modules:
            user.block_modules.remove(d)

        block_mods = ['Desk','Users and Permissions','Integrations','dashboard','Accounts','Buying',
                      'Assets','CRM','HR','Marketplace','Settings','Customization',
                      'Website','Leaderboard','Getting Started','Selling','Stock',
                      'Projects','Support','Quality Management','Help','Program Enrollment Tool',
                      'Quiz Activity']

        for mod in block_mods:
            user.append("block_modules", {
                'module': mod
            })


        user.save()

        frappe.db.commit()

        code = random_word(8)

        # message =  "Your WELA account, username:{0}@wela.online, password: {1}. " \
        #            "Website: {2}".format(id_number, code, url)

        # message = "After done paying. Proceed with your Online Class, log on to {2} , " \
        #           "username:{0}@wela.online, password: {1}. ".format(id_number, code, url)

        message = welcome_text.format(id_number, code, url)





        # send_to_semaphore(contact_number, message)






        # self.send_account_details = 0

        # user.new_password = self.default_code
        # user.save()
        # /home/jvfiel/frappe-v11/apps/frappe/frappe/utils/password.py
        # print("************ UPDATE PASSWORD ************")
        # print(user.name,code)

        if not frappe.db.exists('Year Level', grade_level):
            lvl = frappe.get_doc({
                "doctype": "Year Level",
                "level": grade_level
            }).insert(ignore_permissions=True)
            frappe.db.commit()


        update_password(user.name, code)

        student = frappe.get_doc({
            "doctype": "Student",
            "first_name": first_name,
            "last_name": last_name,
            "student_email_id": id_number + "@wela.online",
            "user": user.name,
            "level":grade_level
            # "note":note,
            # "entrance_exam":entrance_exam
        }).insert(ignore_permissions=True)


        frappe.db.commit()



        # for cours in courses:
        #     exists_program = frappe.db.sql("""SELECT name FROM `tabCourse`
        #                                                                 WHERE course_name=%s""", (cours))
        #
        #     if exists_program == ():
        #         course_doc = frappe.get_doc({
        #             "doctype": "Course",
        #             "course_name": cours
        #         }).insert(ignore_permissions=True)
        #         frappe.db.commit()
        #
        #
        #
        #
        # for prog in programs:
        #     exists_program = frappe.db.sql("""SELECT name FROM `tabProgram`
        #                                                          WHERE program_name=%s""",(prog))
        #
        #     if exists_program == ():
        #         program_doc = frappe.get_doc({
        #             "doctype": "Program",
        #             "program_name": prog,
        #             "is_published":1,
        #             "courses":[{"course":prog,"course_name":prog}]
        #         }).insert(ignore_permissions=True)
        #         frappe.db.commit()




        exists_program = frappe.db.sql("""SELECT name FROM `tabAcademic Year`
                                                                           WHERE academic_year_name=%s""", (school_year))

        if exists_program == ():
            course_doc = frappe.get_doc({
                "doctype": "Academic Year",
                "academic_year_name": school_year
            }).insert(ignore_permissions=True)
            frappe.db.commit()




        # for i,prog in enumerate(programs):
        #     enrollment = frappe.get_doc({
        #         "doctype": "Program Enrollment",
        #         "student": student.name,
        #         "academic_year": school_year,
        #         "program": prog,
        #         "enrollment_date": frappe.utils.get_datetime().date(),
        #         "docstatus": 1
        #     }).insert(ignore_permissions=True)
        #     frappe.db.commit()
        #
        #
        #     course_enrollment = frappe.get_doc({
        #         "doctype": "Course Enrollment",
        #         "student": student.name,
        #         # "academic_year": "2020-21",
        #         "program_enrollment": enrollment.name,
        #         "course": courses[i],
        #         "enrollment_date": frappe.utils.get_datetime().date(),
        #         # "docstatus": 1
        #     }).insert(ignore_permissions=True)



    else:

        user = frappe.get_doc("User", id_number + "@wela.online")

        code = random_word(8)

        # message =  "Your WELA account, username:{0}@wela.online, password: {1}. " \
        #            "Website: {2}".format(id_number, code, url)

        # message = "After done paying. Proceed with your Online Class, log on to {2} , " \
        #           "username:{0}@wela.online, password: {1}. ".format(id_number, code, url)

        message = welcome_text.format(id_number, code, url)

        # send_to_semaphore(contact_number, message)

        # self.send_account_details = 0

        # user.new_password = self.default_code
        # user.save()
        # /home/jvfiel/frappe-v11/apps/frappe/frappe/utils/password.py
        # print("************ UPDATE PASSWORD ************")
        # print(user.name,code)
        update_password(user.name, code)

        user.save()
        # for cours in courses:
        #     print(cours)
        #     if cours:
        #         exists_program = frappe.db.sql("""SELECT name FROM `tabCourse`
        #                                                                     WHERE course_name=%s""", (cours))
        #
        #         if exists_program == ():
        #             course_doc = frappe.get_doc({
        #                 "doctype": "Course",
        #                 "course_name": cours
        #             }).insert(ignore_permissions=True)
        #             frappe.db.commit()
        #
        #
        #
        #
        # for prog in programs:
        #     exists_program = frappe.db.sql("""SELECT name FROM `tabProgram`
        #                                                          WHERE program_name=%s""",(prog))
        #
        #     if exists_program == ():
        #         program_doc = frappe.get_doc({
        #             "doctype": "Program",
        #             "program_name": prog,
        #             "is_published":1,
        #             "courses":[{"course":prog,"course_name":prog}]
        #         }).insert(ignore_permissions=True)
        #         frappe.db.commit()
        #
        #
        #
        #
        # exists_program = frappe.db.sql("""SELECT name FROM `tabAcademic Year`
        #                                                                    WHERE academic_year_name=%s""", (school_year))
        #
        # if exists_program == ():
        #     course_doc = frappe.get_doc({
        #         "doctype": "Academic Year",
        #         "academic_year_name": school_year
        #     }).insert(ignore_permissions=True)
        #     frappe.db.commit()
        #     print('school year created!')
        # else:
        #     print('exists sy')
        #     print(exists_program)
        #
        # # student = frappe.get_doc({
        # #     "doctype": "Student",
        # #     "first_name": first_name,
        # #     "last_name": last_name,
        # #     "student_email_id": id_number + "@wela.online",
        # #     "user": user.name,
        # #     "grade_level": grade_level,
        # #     # "note":note,
        # #     # "entrance_exam":entrance_exam
        # # }).insert(ignore_permissions=True)
        #
        # student_sql = frappe.db.sql("""select name from `tabStudent` where student_email_id=%s""",(id_number + "@wela.online"))
        #
        #
        # print(school_year)
        # if student_sql != ():
        #     student = frappe.get_doc("Student",student_sql[0][0])
        #
        #     for i,prog in enumerate(programs):
        #
        #         try:
        #             enrollment = frappe.get_doc({
        #                 "doctype": "Program Enrollment",
        #                 "student": student.name,
        #                 "academic_year": school_year,
        #                 "program": prog,
        #                 "enrollment_date": frappe.utils.get_datetime().date(),
        #                 "docstatus": 1
        #             }).insert(ignore_permissions=True)
        #             frappe.db.commit()
        #
        #
        #             course_enrollment = frappe.get_doc({
        #                 "doctype": "Course Enrollment",
        #                 "student": student.name,
        #                 # "academic_year": "2020-21",
        #                 "program_enrollment": enrollment.name,
        #                 "course": courses[i],
        #                 "enrollment_date": frappe.utils.get_datetime().date(),
        #                 # "docstatus": 1
        #             }).insert(ignore_permissions=True)
        #         except:
        #             pass


    return user.name,code









