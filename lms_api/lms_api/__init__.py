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


    code = random_word(8)

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

        # code = random_word(8)

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
        #
        # code = random_word(8)
        message = welcome_text.format(id_number, code, url)


        user = frappe.get_doc("User", id_number + "@wela.online")
        update_password(user.name, code)

        send_to_semaphore(contact_number, message)

        user.save()



    return user.name






def test_create_account_college():
    data = {'first_name': 'MA. CRISTINA', 'last_name': 'ACEDERA', 'id_number': 'ACEDERAMACRISTINA',
     'contact_number': '639383844997', 'url': 'https://mmc.silid.co/',
     'welcome_text': 'Online Class account log on to {2} , username:{0}@wela.online, password: {1}',
     'school_year': '2019-20 Summer',
     'programs': "['FL 2/FOREIGN LANGUAGE 2/SY2020-2021-BSCRIM 2-A', 'GEC 108/ETHICS/SY2020-2021-BSCRIM 2-A', 'FORENSIC 1/FORENSIC PHOTOGRAPHY/SY2020-2021-BSCRIM 2-C', 'GEC 103/THE CONTEMPORARY WORLD,/SY2020-2021-BSCRIM 1-B', '*ELECT 2/SOCIAL SCIENCE AND PHILOSOPHY/SY2020-2021-BSCRIM 1-OCT', 'FORENSIC 2/PERSONAL IDENTIFICATION TECHNIQUES/SY2020-2021-BSCRIM 2-A']",
     'courses': "['FL 2/FOREIGN LANGUAGE 2/SY2020-2021-BSCRIM 2-A', 'GEC 108/ETHICS/SY2020-2021-BSCRIM 2-A', 'FORENSIC 1/FORENSIC PHOTOGRAPHY/SY2020-2021-BSCRIM 2-C', 'GEC 103/THE CONTEMPORARY WORLD,/SY2020-2021-BSCRIM 1-B', '*ELECT 2/SOCIAL SCIENCE AND PHILOSOPHY/SY2020-2021-BSCRIM 1-OCT', 'FORENSIC 2/PERSONAL IDENTIFICATION TECHNIQUES/SY2020-2021-BSCRIM 2-A']",
     'grade_level': '2nd Year'}

    create_account_college(first_name=data['first_name'],
                           last_name=data['last_name'],
                           id_number=data['id_number'],
                           contact_number=data['contact_number'],
                           url=data['url'],
                           welcome_text=data['welcome_text'],
                           programs=data['programs'],
                           courses=data['courses'],
                           grade_level=data['grade_level'],
                           school_year=data['school_year'])


@frappe.whitelist()
def create_account_college(first_name,last_name,id_number,
                   contact_number,url,welcome_text,
                   programs,courses,grade_level,school_year,reset_pass=0):


    code = random_word(8)


    import ast
    print("((( XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX )))")
    print(programs, courses)
    programs = ast.literal_eval(programs)
    courses = ast.literal_eval(courses)
    # x = [n.strip() for n in x]

    programs_ = []

    # courses_ = []

    for prog in programs:
        cours = prog
        cours = cours.replace("/", " ")
        cours = cours.replace("-", " ")
        cours = cours.replace("&", "and")
        cours = cours.replace("*", "")
        cours = cours.replace(":", "")
        cours = cours.replace(",", "")
        cours = cours.replace(".", "")

        # program does not allow special characters
        prog = prog.replace("/", " ")
        prog = prog.replace("-", " ")
        prog = prog.replace("&", "and")
        prog = prog.replace("(", "")
        prog = prog.replace(")", "")
        prog = prog.replace("*", "")
        prog = prog.replace(":", "")
        prog = prog.replace(",", "")
        prog = prog.replace(".", "")

        programs_.append({"program":prog,"course":cours})



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

        # code = random_word(8)

        # message =  "Your WELA account, username:{0}@wela.online, password: {1}. " \
        #            "Website: {2}".format(id_number, code, url)

        # message = "After done paying. Proceed with your Online Class, log on to {2} , " \
        #           "username:{0}@wela.online, password: {1}. ".format(id_number, code, url)

        # message = welcome_text.format(id_number, code, url)





        # send_to_semaphore(contact_number, message)
        update_password(user.name, code)

        user.save()

        frappe.db.commit()



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



        for cours in programs_:

            exists_program = frappe.db.sql("""SELECT name FROM `tabCourse`
                                                                        WHERE course_name=%s""", (cours['course']))

            if exists_program == ():
                course_doc = frappe.get_doc({
                    "doctype": "Course",
                    "course_name": cours['course']
                }).insert(ignore_permissions=True)
                frappe.db.commit()




        for prog in programs_:

            exists_program = frappe.db.sql("""SELECT name FROM `tabProgram`
                                                                 WHERE program_name=%s""",(prog['program']))

            if exists_program == ():
                program_doc = frappe.get_doc({
                    "doctype": "Program",
                    "program_name": prog['program'],
                    "is_published":1,
                    "courses":[{"course":prog['course'],"course_name":prog['course']}]
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




        for i,prog in enumerate(programs_):
            enrollment = frappe.get_doc({
                "doctype": "Program Enrollment",
                "student": student.name,
                "academic_year": school_year,
                "program": prog['program'],
                "enrollment_date": frappe.utils.get_datetime().date(),
                "docstatus": 1
                }).insert(ignore_permissions=True)
            frappe.db.commit()


            course_enrollment = frappe.get_doc({
                "doctype": "Course Enrollment",
                "student": student.name,
                # "academic_year": "2020-21",
                "program_enrollment": enrollment.name,
                "course": prog['course'],
                "enrollment_date": frappe.utils.get_datetime().date(),
                # "docstatus": 1
            }).insert(ignore_permissions=True)



    else:

        user = frappe.get_doc("User", id_number + "@wela.online")

        # import ast
        # print("((( XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX )))")
        # print(programs, courses)
        # programs = ast.literal_eval(programs)
        # courses = ast.literal_eval(courses)

        student_sql = frappe.db.sql("""select name from `tabStudent` where student_email_id=%s""",(id_number + "@wela.online"))


        print(school_year)
        if student_sql != ():
            student = frappe.get_doc("Student",student_sql[0][0])
        else:
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


        # if reset_pass == 1:
        # code = random_word(8)
        # message = welcome_text.format(id_number, code, url)

        # send_to_semaphore(contact_number, message)
        update_password(user.name, code)

        user.save()

        for cours in programs_:

            exists_program = frappe.db.sql("""SELECT name FROM `tabCourse`
                                                                              WHERE course_name=%s""", (cours['course']))

            if exists_program == ():
                course_doc = frappe.get_doc({
                    "doctype": "Course",
                    "course_name": cours['course']
                }).insert(ignore_permissions=True)
                frappe.db.commit()

        for prog in programs_:

            exists_program = frappe.db.sql("""SELECT name FROM `tabProgram`
                                                                 WHERE program_name=%s""",(prog['program']))

            if exists_program == ():
                print(prog)
                program_doc = frappe.get_doc({
                    "doctype": "Program",
                    "program_name": prog['program'],
                    "is_published":1,
                    "courses":[{"course":prog['course'],"course_name":prog['course']}]
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

        for i, prog in enumerate(programs_):

            exists_program = frappe.db.sql("""SELECT name FROM `tabProgram Enrollment`
                                                WHERE program=%s 
                                        and student=%s and docstatus=1""", (prog['program'],student.name))

            if exists_program == ():

                try:
                    enrollment = frappe.get_doc({
                        "doctype": "Program Enrollment",
                        "student": student.name,
                        "academic_year": school_year,
                        "program": prog['program'],
                        "enrollment_date": frappe.utils.get_datetime().date(),
                        "docstatus": 1
                    }).insert(ignore_permissions=True)
                    frappe.db.commit()

                    course_enrollment = frappe.get_doc({
                        "doctype": "Course Enrollment",
                        "student": student.name,
                        # "academic_year": "2020-21",
                        "program_enrollment": enrollment.name,
                        "course": prog['course'],
                        "enrollment_date": frappe.utils.get_datetime().date(),
                        # "docstatus": 1
                    }).insert(ignore_permissions=True)
                except:
                    pass

    from lms_api.lms_api.college import create_rooms_and_permissions

    try:
        create_rooms_and_permissions(user.name)
    except:
        pass

    return user.name, code







#bench --site mmc.silid.co execute lms_api.lms_api.test_create_college_subjects
def test_create_college_subjects():
    programs = ["LEA 1/LAW ENFORCEMENT ORG. & ADM. (INTERAGENCY APPROACH)/SY2020-2021-BSCRIM 1-C"]
    for cours in programs:

        cours = cours.replace("/", " ")
        cours = cours.replace("-", " ")
        cours = cours.replace("&", "and")

        print(cours)
        exists_program = frappe.db.sql("""SELECT name FROM `tabCourse`
                                                                       WHERE course_name=%s""", (cours))

        if exists_program == ():
            course_doc = frappe.get_doc({
                "doctype": "Course",
                "course_name": cours
            }).insert(ignore_permissions=True)
            frappe.db.commit()


@frappe.whitelist()
def create_college_subjects(programs,courses,school_year):
    import ast
    print("((( XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX )))")
    print(programs,courses)
    programs = ast.literal_eval(programs)
    courses = ast.literal_eval(courses)
    # x = [n.strip() for n in x]

    for cours in courses:


        cours = cours.replace("/"," ")
        cours = cours.replace("-"," ")
        cours = cours.replace("&","and")


        print(cours)
        exists_program = frappe.db.sql("""SELECT name FROM `tabCourse`
                                                                    WHERE course_name=%s""", (cours))

        if exists_program == ():
            course_doc = frappe.get_doc({
                "doctype": "Course",
                "course_name": cours
            }).insert(ignore_permissions=True)
            frappe.db.commit()




    for prog in programs:

        cours = prog
        cours = cours.replace("/", " ")
        cours = cours.replace("-", " ")
        cours = cours.replace("&", "and")


        #program does not allow special characters
        prog = prog.replace("/"," ")
        prog = prog.replace("-"," ")
        prog = prog.replace("&", "and")
        prog = prog.replace("(", "")
        prog = prog.replace(")", "")


        exists_program = frappe.db.sql("""SELECT name FROM `tabProgram`
                                                             WHERE program_name=%s""",(prog))

        if exists_program == ():
            program_doc = frappe.get_doc({
                "doctype": "Program",
                "program_name": prog,
                "is_published":1,
                "courses":[{"course":cours,"course_name":cours}]
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

    return True








@frappe.whitelist()
def create_college_subjects_only(programs,courses):
    import ast
    print("((( XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX )))")
    print(programs,courses)
    programs = ast.literal_eval(programs)
    courses = ast.literal_eval(courses)
    # x = [n.strip() for n in x]

    programs_ = []

    for prog in programs:
        cours = prog
        cours = cours.replace("/", " ")
        cours = cours.replace("-", " ")
        cours = cours.replace("&", "and")
        cours = cours.replace("*", "")
        cours = cours.replace(":", "")
        cours = cours.replace(",", "")
        cours = cours.replace(".", "")

        # program does not allow special characters
        prog = prog.replace("/", " ")
        prog = prog.replace("-", " ")
        prog = prog.replace("&", "and")
        prog = prog.replace("(", "")
        prog = prog.replace(")", "")
        prog = prog.replace("*", "")
        prog = prog.replace(":", "")
        prog = prog.replace(",", "")
        prog = prog.replace(".", "")

        programs_.append({"program":prog,"course":cours})

    for cours in programs_:


        # cours = cours.replace("/"," ")
        # cours = cours.replace("-"," ")
        # cours = cours.replace("&","and")
        cours = cours['course']

        print(cours)
        exists_program = frappe.db.sql("""SELECT name FROM `tabCourse`
                                                                    WHERE course_name=%s""", (cours))

        if exists_program == ():
            course_doc = frappe.get_doc({
                "doctype": "Course",
                "course_name": cours
            }).insert(ignore_permissions=True)
            frappe.db.commit()




    for prog in programs_:

        # cours = prog
        # cours = cours.replace("/", " ")
        # cours = cours.replace("-", " ")
        # cours = cours.replace("&", "and")
        #
        #
        # #program does not allow special characters
        # prog = prog.replace("/"," ")
        # prog = prog.replace("-"," ")
        # prog = prog.replace("&", "and")
        # prog = prog.replace("(", "")
        # prog = prog.replace(")", "")
        cours = prog['course']
        prog = prog['program']


        exists_program = frappe.db.sql("""SELECT name FROM `tabProgram`
                                                             WHERE program_name=%s""",(prog))

        if exists_program == ():
            program_doc = frappe.get_doc({
                "doctype": "Program",
                "program_name": prog,
                "is_published":1,
                "courses":[{"course":cours,"course_name":cours}]
            }).insert(ignore_permissions=True)
            frappe.db.commit()


    return True






@frappe.whitelist()
def create_account_college_resend(first_name,last_name,id_number,
                   contact_number,url,welcome_text,
                   programs,courses,grade_level,school_year):
    code = random_word(8)

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