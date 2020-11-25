import frappe
import json
import random
from frappe.utils.password import update_password

def random_word(length):
    return ''.join(random.choice(['A','B','C','D','E','F','G','H','J','K',
                                  'L','M','N','O','P','Q','R','S','T','U',
                          'V','W','X','Y','Z']) for i in range(length))


def send_to_semaphore(mobile_number, message):
    import http.client
    data = json.dumps({'apikey': '64229633532ecd99ddada36b000ac85f',
                       'sendername': 'WELA', 'number': mobile_number,
                       'message': message})
    h = http.client.HTTPConnection('api.semaphore.co:80')
    headers = {"Content-type": "application/json", "Accept": "application/json"}

    h.request('POST', '/api/v4/messages', data, headers)
    r = h.getresponse()
    # print r.status, r.reason
    # print("          SEMAPHORE          ")
    # print("          SEMAPHORE          ")
    # print("          SEMAPHORE          ")
    # print("          SEMAPHORE          ")
    # print("          SEMAPHORE          ")
    # print("          SEMAPHORE          ")
    # print("          SEMAPHORE          ")
    # print("          SEMAPHORE          ")
    # print("          SEMAPHORE          ")
    # print("          SEMAPHORE          ")
    # print("          SEMAPHORE          ")
    # print("          SEMAPHORE          ")
    # print("          SEMAPHORE          ")
    # print("          SEMAPHORE          ")
    # print("          SEMAPHORE          ")
    # print("          SEMAPHORE          ")
    # print("          SEMAPHORE          ")
    # print("          SEMAPHORE          ")
    # print("          SEMAPHORE          ")
    # print("          SEMAPHORE          ")
    # print("          SEMAPHORE          ")
    # print("          SEMAPHORE          ")
    # print(r.status,r.reason,message,mobile_number)
    return True

#lms_api.test_user_modules --kwargs  "{'username': '2019-89946@wela.online'}"
def test_user_modules(username):
    user = frappe.get_doc("User", username)
    for d in user.block_modules:
        print(d.module)
    #     user.block_modules.remove(d)
    # user.append("block_modules", {
    #     'module': "Education"
    # })

@frappe.whitelist()
def set_password(email, new_password):
    try:
        user_info = frappe.db.sql(f"SELECT name FROM tabUser WHERE email='{email}'", as_dict=1)
        name = user_info[0]['name']
        update_password(name, new_password)
        return True
    except:
        return False

@frappe.whitelist()
def create_account(first_name,last_name,id_number,
                   contact_number,url,welcome_text,
                   grade_level="",note="",
                   school_year="",entrance_exam=""):
    if not frappe.db.exists('User', id_number + "@wela.online"):
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

        block_mods = ['Desk','Users and Permissions','Integrations',
                      'Social','dashboard','Accounts','Buying',
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

        send_to_semaphore(contact_number, message)
        # self.send_account_details = 0

        # user.new_password = self.default_code
        # user.save()
        # /home/jvfiel/frappe-v11/apps/frappe/frappe/utils/password.py

        # print("************ UPDATE PASSWORD ************")
        # print(user.name,code)
        update_password(user.name, code)

        student = frappe.get_doc({
            "doctype": "Student",
            "first_name": first_name,
            "last_name": last_name,
            "student_email_id": id_number + "@wela.online",
            "user": user.name,
            "grade_level":grade_level,
            "note":note,
            "entrance_exam":entrance_exam
        }).insert(ignore_permissions=True)


        frappe.db.commit()
        if note == "Summer":

            exists_program = frappe.db.sql("""SELECT Count(*) FROM `tabProgram`
                                                        WHERE program_name='Summer Class Applicants'""")

            if exists_program == ():
                program = frappe.get_doc({
                    "doctype": "Program",
                    "program_name": "Summer Class Applicants"
                }).insert(ignore_permissions=True)

            program = frappe.get_doc({
                "doctype": "Program Enrollment",
                "student": student.name,
                "academic_year": "2020 Summer",
                "program": "Summer Class Applicants",
                "enrollment_date": frappe.utils.get_datetime().date(),
                "docstatus":1
            }).insert(ignore_permissions=True)
        elif note == "Exam":

            exists_program = frappe.db.sql("""SELECT Count(*) FROM `tabProgram`
                                                        WHERE program_name='Exam Applicants'""")

            if exists_program == ():
                program = frappe.get_doc({
                    "doctype": "Program",
                    "program_name": "Exam Applicants"
                }).insert(ignore_permissions=True)

            program = frappe.get_doc({
                "doctype": "Program Enrollment",
                "student": student.name,
                "academic_year": "2020",
                "program": "Exam Applicants",
                "enrollment_date": frappe.utils.get_datetime().date(),
                "docstatus": 1
            }).insert(ignore_permissions=True)
        elif note == "Regular":

            exists_program = frappe.db.sql("""SELECT Count(*) FROM `tabProgram`
                                            WHERE program_name='Regular Applicants'""")

            if exists_program == ():
                program = frappe.get_doc({
                    "doctype": "Program",
                    "program_name": "Regular Applicants"
                }).insert(ignore_permissions=True)


            program = frappe.get_doc({
                "doctype": "Program Enrollment",
                "student": student.name,
                "academic_year": "2020",
                "program": "Regular Applicants",
                "enrollment_date": frappe.utils.get_datetime().date(),
                "docstatus": 1
            }).insert(ignore_permissions=True)
        else:
            if note:
                exists_program = frappe.db.sql("""SELECT Count(*) FROM `tabProgram`
                                                WHERE program_name=%s""",(note))

                if exists_program == ():
                    program = frappe.get_doc({
                        "doctype": "Program",
                        "program_name": note
                    }).insert(ignore_permissions=True)


                program = frappe.get_doc({
                    "doctype": "Program Enrollment",
                    "student": student.name,
                    "academic_year": "2020",
                    "program": note,
                    "enrollment_date": frappe.utils.get_datetime().date(),
                    "docstatus": 1
                }).insert(ignore_permissions=True)


    else:
        user = frappe.get_doc("User", id_number + "@wela.online")
    return user.name








    #lms_api.lms_api.create_account_v2 --kwargs '{"first_name":"jj","last_name":"vv","id_number":"vv_jj","contact_number":"09177008340","url":"wela.online","welcome_text":"{0} {1} {2}","programs":["abc"],"courses":["abc"],"grade_level":"Grade 1","school_year":"2020 Summer"}'
@frappe.whitelist()
def create_account_v2(first_name,last_name,id_number,
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

        block_mods = ['Desk','Users and Permissions','Integrations',
                      'Social','dashboard','Accounts','Buying',
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

        send_to_semaphore(contact_number, message)
        # self.send_account_details = 0

        # user.new_password = self.default_code
        # user.save()
        # /home/jvfiel/frappe-v11/apps/frappe/frappe/utils/password.py
        # print("************ UPDATE PASSWORD ************")
        # print(user.name,code)
        update_password(user.name, code)

        student = frappe.get_doc({
            "doctype": "Student",
            "first_name": first_name,
            "last_name": last_name,
            "student_email_id": id_number + "@wela.online",
            "user": user.name,
            "grade_level":grade_level,
            # "note":note,
            # "entrance_exam":entrance_exam
        }).insert(ignore_permissions=True)


        frappe.db.commit()



        for cours in courses:
            exists_program = frappe.db.sql("""SELECT name FROM `tabCourse`
                                                                        WHERE course_name=%s""", (cours))

            if exists_program == ():
                course_doc = frappe.get_doc({
                    "doctype": "Course",
                    "course_name": cours
                }).insert(ignore_permissions=True)
                frappe.db.commit()




        for prog in programs:
            exists_program = frappe.db.sql("""SELECT name FROM `tabProgram`
                                                                 WHERE program_name=%s""",(prog))

            if exists_program == ():
                program_doc = frappe.get_doc({
                    "doctype": "Program",
                    "program_name": prog,
                    "is_published":1,
                    "courses":[{"course":prog,"course_name":prog}]
                }).insert(ignore_permissions=True)
                frappe.db.commit()




        exists_program = frappe.db.sql("""SELECT Count(*) FROM `tabAcademic Year`
                                                                           WHERE academic_year_name=%s""", (school_year))

        if exists_program == ():
            course_doc = frappe.get_doc({
                "doctype": "Academic Year",
                "academic_year_name": school_year
            }).insert(ignore_permissions=True)
            frappe.db.commit()




        for i,prog in enumerate(programs):
            enrollment = frappe.get_doc({
                "doctype": "Program Enrollment",
                "student": student.name,
                "academic_year": school_year,
                "program": prog,
                "enrollment_date": frappe.utils.get_datetime().date(),
                "docstatus": 1
            }).insert(ignore_permissions=True)
            frappe.db.commit()


            course_enrollment = frappe.get_doc({
                "doctype": "Course Enrollment",
                "student": student.name,
                # "academic_year": "2020-21",
                "program_enrollment": enrollment.name,
                "course": courses[i],
                "enrollment_date": frappe.utils.get_datetime().date(),
                # "docstatus": 1
            }).insert(ignore_permissions=True)



    else:

        code = random_word(8)
        message = welcome_text.format(id_number, code, url)


        user = frappe.get_doc("User", id_number + "@wela.online")
        update_password(user.name, code)

        send_to_semaphore(contact_number, message)

        user.save()



    return user.name



@frappe.whitelist()
def update_student_branch_(id_number ,branch):
    student = frappe.db.sql("""select name from `tabStudent` where student_email_id=%s""", (id_number + "@wela.online"))
    if student != ():
        stud = frappe.get_doc("Student", student[0][0])
        stud.branch = branch
        stud.save()
        return True
    return False




@frappe.whitelist()
def create_account_(first_name,last_name,id_number,
                   contact_number,url,welcome_text,
                   programs,courses,grade_level,school_year,branch=""):
    if not frappe.db.exists('User', id_number + "@wela.online"):

        import ast
        programs = ast.literal_eval(programs)
        courses = ast.literal_eval(courses)


        user = frappe.get_doc({
            "doctype": "User",
            "first_name": first_name,
            "last_name": last_name,
            "username": id_number,
            "email": id_number + "@wela.online",
            # "mobile_no":contact_number,
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
        update_password(user.name, code)
        message = welcome_text.format(id_number, code, url)

        send_to_semaphore(contact_number, message)


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



        if branch:
            if not frappe.db.exists('Branch', branch):
                create_branch = frappe.get_doc({
                    "doctype": "Branch",
                    "branch": branch
                }).insert(ignore_permissions=True)
                frappe.db.commit()
            student = frappe.get_doc({
                "doctype": "Student",
                "first_name": first_name,
                "last_name": last_name,
                "student_email_id": id_number + "@wela.online",
                "user": user.name,
                "level":grade_level,
                "student_mobile_number":contact_number,
                "branch": branch
                # "note":note,
                # "entrance_exam":entrance_exam
            }).insert(ignore_permissions=True)
        else:
            student = frappe.get_doc({
                "doctype": "Student",
                "first_name": first_name,
                "last_name": last_name,
                "student_email_id": id_number + "@wela.online",
                "user": user.name,
                "level": grade_level,
                "student_mobile_number": contact_number,
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
        update_password(user.name, code)
        message = welcome_text.format(id_number, code, url)

        send_to_semaphore(contact_number, message)

        # self.send_account_details = 0



        #update student record

        student = frappe.db.sql("""select name from `tabStudent` where student_email_id=%s""",(id_number + "@wela.online"))
        if student != ():
            """
            
                "level":grade_level,
            "student_mobile_number":contact_number
            
            """
            if branch:
                if not frappe.db.exists('Branch', branch):
                    create_branch = frappe.get_doc({
                        "doctype": "Branch",
                        "branch": branch
                    }).insert(ignore_permissions=True)
                    frappe.db.commit()

            stud = frappe.get_doc("Student",student[0][0])
            stud.level = grade_level
            stud.student_mobile_number = contact_number
            if branch:
                stud.branch = branch
            stud.save()

        else:
            try:
                if branch:
                    if not frappe.db.exists('Branch', branch):
                        create_branch = frappe.get_doc({
                            "doctype": "Branch",
                            "branch": branch
                        }).insert(ignore_permissions=True)
                        frappe.db.commit()
                    student = frappe.get_doc({
                        "doctype": "Student",
                        "first_name": first_name,
                        "last_name": last_name,
                        "student_email_id": id_number + "@wela.online",
                        "user": id_number + "@wela.online",
                        "level": grade_level,
                        "student_mobile_number": contact_number,
                        "branch": branch
                    }).insert(ignore_permissions=True)
                else:
                    student = frappe.get_doc({
                        "doctype": "Student",
                        "first_name": first_name,
                        "last_name": last_name,
                        "student_email_id": id_number + "@wela.online",
                        "user": id_number + "@wela.online",
                        "level": grade_level,
                        "student_mobile_number": contact_number,
                    }).insert(ignore_permissions=True)

                frappe.db.commit()
            except:
                pass

        # user.new_password = self.default_code
        # user.save()
        # /home/jvfiel/frappe-v11/apps/frappe/frappe/utils/password.py
        # print("************ UPDATE PASSWORD ************")
        # print(user.name,code)


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


    return user.name


@frappe.whitelist()
def create_account_resend(first_name, last_name, id_number,
                    contact_number, url, welcome_text,
                    programs, courses, grade_level, school_year, branch=""):
    if not frappe.db.exists('User', id_number + "@wela.online"):

        import ast
        print("((( XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX )))")
        print(programs, courses)
        programs = ast.literal_eval(programs)
        courses = ast.literal_eval(courses)
        # x = [n.strip() for n in x]

        user = frappe.get_doc({
            "doctype": "User",
            "first_name": first_name,
            "last_name": last_name,
            "username": id_number,
            "email": id_number + "@wela.online",
            # "mobile_no":contact_number,
            "user_type": "System User",
            "send_welcome_email": 0
        }).insert(ignore_permissions=True)

        user.append('roles', {
            "doctype": "Has Role",
            "role": "Student"
        })

        for d in user.block_modules:
            user.block_modules.remove(d)

        block_mods = ['Desk', 'Users and Permissions', 'Integrations', 'dashboard', 'Accounts', 'Buying',
                      'Assets', 'CRM', 'HR', 'Marketplace', 'Settings', 'Customization',
                      'Website', 'Leaderboard', 'Getting Started', 'Selling', 'Stock',
                      'Projects', 'Support', 'Quality Management', 'Help', 'Program Enrollment Tool',
                      'Quiz Activity']

        for mod in block_mods:
            user.append("block_modules", {
                'module': mod
            })

        user.save()

        frappe.db.commit()

        code = random_word(8)
        message = welcome_text.format(id_number, code, url)

        send_to_semaphore(contact_number, message)
        if not frappe.db.exists('Year Level', grade_level):
            lvl = frappe.get_doc({
                "doctype": "Year Level",
                "level": grade_level
            }).insert(ignore_permissions=True)
            frappe.db.commit()

        update_password(user.name, code)
        if branch:
            if not frappe.db.exists('Branch', branch):
                create_branch = frappe.get_doc({
                    "doctype": "Branch",
                    "branch": branch
                }).insert(ignore_permissions=True)
                frappe.db.commit()
            student = frappe.get_doc({
                "doctype": "Student",
                "first_name": first_name,
                "last_name": last_name,
                "student_email_id": id_number + "@wela.online",
                "user": user.name,
                "level": grade_level,
                "student_mobile_number": contact_number,
                "branch": branch
                # "note":note,
                # "entrance_exam":entrance_exam
            }).insert(ignore_permissions=True)
        else:
            student = frappe.get_doc({
                "doctype": "Student",
                "first_name": first_name,
                "last_name": last_name,
                "student_email_id": id_number + "@wela.online",
                "user": user.name,
                "level": grade_level,
                "student_mobile_number": contact_number,
                # "note":note,
                # "entrance_exam":entrance_exam
            }).insert(ignore_permissions=True)

        frappe.db.commit()

        exists_program = frappe.db.sql("""SELECT name FROM `tabAcademic Year`
                                                                           WHERE academic_year_name=%s""",
                                       (school_year))

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

        student = frappe.db.sql("""select name from `tabStudent` where student_email_id=%s""",
                                (id_number + "@wela.online"))
        if student != ():
            """

                "level":grade_level,
            "student_mobile_number":contact_number

            """
            if branch:
                if not frappe.db.exists('Branch', branch):
                    create_branch = frappe.get_doc({
                        "doctype": "Branch",
                        "branch": branch
                    }).insert(ignore_permissions=True)
                    frappe.db.commit()

            stud = frappe.get_doc("Student", student[0][0])
            stud.level = grade_level
            stud.student_mobile_number = contact_number
            if branch:
                stud.branch = branch
            stud.save()

        else:
            try:
                if branch:
                    if not frappe.db.exists('Branch', branch):
                        create_branch = frappe.get_doc({
                            "doctype": "Branch",
                            "branch": branch
                        }).insert(ignore_permissions=True)
                        frappe.db.commit()
                    student = frappe.get_doc({
                        "doctype": "Student",
                        "first_name": first_name,
                        "last_name": last_name,
                        "student_email_id": id_number + "@wela.online",
                        "user": id_number + "@wela.online",
                        "level": grade_level,
                        "student_mobile_number": contact_number,
                        "branch": branch
                    }).insert(ignore_permissions=True)
                else:
                    student = frappe.get_doc({
                        "doctype": "Student",
                        "first_name": first_name,
                        "last_name": last_name,
                        "student_email_id": id_number + "@wela.online",
                        "user": id_number + "@wela.online",
                        "level": grade_level,
                        "student_mobile_number": contact_number,
                    }).insert(ignore_permissions=True)

                frappe.db.commit()
            except:
                pass

    return user.name







@frappe.whitelist()
def create_account_college_resend(first_name,last_name,id_number,
                   contact_number,url,welcome_text,
                   programs,courses,grade_level,school_year):
    import ast
    programs = ast.literal_eval(programs)
    courses = ast.literal_eval(courses)
    if not frappe.db.exists('User', id_number + "@wela.online"):


        print("((( XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX )))")
        print(programs,courses)

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

        block_mods = ['Desk','Users and Permissions','Integrations',
                      'Social','dashboard','Accounts','Buying',
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





        send_to_semaphore(contact_number, message)






        # self.send_account_details = 0

        # user.new_password = self.default_code
        # user.save()
        # /home/jvfiel/frappe-v11/apps/frappe/frappe/utils/password.py
        # print("************ UPDATE PASSWORD ************")
        # print(user.name,code)
        update_password(user.name, code)

        exists_student = frappe.db.sql("""SELECT name FROM `tabStudent` WHERE student_email_id=%s""", (id_number + "@wela.online"))

        if exists_student == ():
            student = frappe.get_doc({
                "doctype": "Student",
                "first_name": first_name,
                "last_name": last_name,
                "student_email_id": id_number + "@wela.online",
                "user": user.name,
                "grade_level":grade_level,
                # "note":note,
                # "entrance_exam":entrance_exam
            }).insert(ignore_permissions=True)


            frappe.db.commit()
        else:
            student = frappe.get_doc("Student",exists_student[0][0])



        for cours in courses:
            exists_program = frappe.db.sql("""SELECT name FROM `tabCourse`
                                                                        WHERE course_name=%s""", (cours))

            if exists_program == ():
                course_doc = frappe.get_doc({
                    "doctype": "Course",
                    "course_name": cours
                }).insert(ignore_permissions=True)
                frappe.db.commit()




        for prog in programs:
            exists_program = frappe.db.sql("""SELECT name FROM `tabProgram`
                                                                 WHERE program_name=%s""",(prog))

            if exists_program == ():
                program_doc = frappe.get_doc({
                    "doctype": "Program",
                    "program_name": prog,
                    "is_published":1,
                    "courses":[{"course":prog,"course_name":prog}]
                }).insert(ignore_permissions=True)
                frappe.db.commit()




        exists_program = frappe.db.sql("""SELECT name FROM `tabAcademic Year`
                                                                           WHERE academic_year_name=%s""", (school_year))

        if exists_program == ():
            course_doc = frappe.get_doc({
                "doctype": "Academic Year",
                "academic_year_name": school_year
            }).insert(ignore_permissions=True)
            frappe.db.commit()




        for i,prog in enumerate(programs):
            enrollment = frappe.get_doc({
                "doctype": "Program Enrollment",
                "student": student.name,
                "academic_year": school_year,
                "program": prog,
                "enrollment_date": frappe.utils.get_datetime().date(),
                "docstatus": 1
            }).insert(ignore_permissions=True)
            frappe.db.commit()


            course_enrollment = frappe.get_doc({
                "doctype": "Course Enrollment",
                "student": student.name,
                # "academic_year": "2020-21",
                "program_enrollment": enrollment.name,
                "course": courses[i],
                "enrollment_date": frappe.utils.get_datetime().date(),
                # "docstatus": 1
            }).insert(ignore_permissions=True)



    else:

        # code = random_word(8)
        # message = welcome_text.format(id_number, code, url)


        user = frappe.get_doc("User", id_number + "@wela.online")

        code = random_word(8)

        # message =  "Your WELA account, username:{0}@wela.online, password: {1}. " \
        #            "Website: {2}".format(id_number, code, url)

        # message = "After done paying. Proceed with your Online Class, log on to {2} , " \
        #           "username:{0}@wela.online, password: {1}. ".format(id_number, code, url)

        message = welcome_text.format(id_number, code, url)

        send_to_semaphore(contact_number, message)

        # self.send_account_details = 0

        # user.new_password = self.default_code
        # user.save()
        # /home/jvfiel/frappe-v11/apps/frappe/frappe/utils/password.py
        # print("************ UPDATE PASSWORD ************")
        # print(user.name,code)
        update_password(user.name, code)

        exists_student = frappe.db.sql("""SELECT name FROM `tabStudent` WHERE student_email_id=%s""",
                                       (id_number + "@wela.online"))

        if exists_student == ():
            student = frappe.get_doc({
                "doctype": "Student",
                "first_name": first_name,
                "last_name": last_name,
                "student_email_id": id_number + "@wela.online",
                "user": user.name,
                "grade_level": grade_level,
                # "note":note,
                # "entrance_exam":entrance_exam
            }).insert(ignore_permissions=True)

            frappe.db.commit()
        else:
            student = frappe.get_doc("Student", exists_student[0][0])





        for cours in courses:
            exists_program = frappe.db.sql("""SELECT name FROM `tabCourse`
                                                                                WHERE course_name=%s""", (cours))

            if exists_program == ():
                try:
                    course_doc = frappe.get_doc({
                        "doctype": "Course",
                        "course_name": cours
                    }).insert(ignore_permissions=True)

                    frappe.db.commit()
                except:
                    pass


        for prog in programs:
            exists_program = frappe.db.sql("""SELECT name FROM `tabProgram`
                                                                         WHERE program_name=%s""", (prog))

            if exists_program == ():
                try:
                    program_doc = frappe.get_doc({
                        "doctype": "Program",
                        "program_name": prog,
                        "is_published": 1,
                        "courses": [{"course": prog, "course_name": prog}]
                    }).insert(ignore_permissions=True)
                    frappe.db.commit()
                except:
                    pass

        exists_program = frappe.db.sql("""SELECT name FROM `tabAcademic Year`
                                                                                   WHERE academic_year_name=%s""",
                                       (school_year))

        if exists_program == ():
            try:
                course_doc = frappe.get_doc({
                    "doctype": "Academic Year",
                    "academic_year_name": school_year
                }).insert(ignore_permissions=True)
                frappe.db.commit()
            except:
                pass


        for i, prog in enumerate(programs):

            exists_program = frappe.db.sql("""SELECT name FROM `tabProgram Enrollment`
                                              WHERE student=%s and academic_year=%s and program=%s
                                              """,
                                           (student.name,school_year,prog))

            if exists_program == ():
                try:
                    enrollment = frappe.get_doc({
                        "doctype": "Program Enrollment",
                        "student": student.name,
                        "academic_year": school_year,
                        "program": prog,
                        "enrollment_date": frappe.utils.get_datetime().date(),
                        "docstatus": 1
                    }).insert(ignore_permissions=True)
                    frappe.db.commit()
                except:
                    pass
            else:
                enrollment = frappe.get_doc("Program Enrollment",exists_program[0][0])

            try:
                course_enrollment = frappe.get_doc({
                    "doctype": "Course Enrollment",
                    "student": student.name,
                    # "academic_year": "2020-21",
                    "program_enrollment": enrollment.name,
                    "course": courses[i],
                    "enrollment_date": frappe.utils.get_datetime().date(),
                    # "docstatus": 1
                }).insert(ignore_permissions=True)
            except:
                pass


    return user.name