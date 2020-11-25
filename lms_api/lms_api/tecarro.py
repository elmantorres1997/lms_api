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


#bench --site tecarro.silid.co execute lms_api.lms_api.tecarro.create_accounts
def create_accounts():
    students = frappe.db.sql("""select name,program from `tabStudent` 
                                        where program like '%Diploma%' or program like '%Bachelor%' """,as_dict=True)


    print(students)
    for stud in students:
        create_account_(stud.name)



@frappe.whitelist()
def create_account_(name,school_year='SY2020-2021', branch=""):


    student = frappe.get_doc("Student",name)


    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

    print(student.first_name,student.last_name,student.user)

    if student.user:

            user = frappe.get_doc("User", student.user)

    else:
            user = frappe.get_doc({
                "doctype": "User",
                "first_name": student.first_name.strip(),
                "last_name": student.last_name.strip(),
                "username": student.last_name.strip().replace(" ","")+student.first_name.strip().replace(" ","")+"@wela.online",
                "email": student.last_name.strip().replace(" ","")+student.first_name.strip().replace(" ","")+"@wela.online",
                # "mobile_no":contact_number,
                "user_type": "System User",
                "send_welcome_email": 0
            }).insert(ignore_permissions=True)

            frappe.db.commit()

            student.user = user.name
            student.email_id = user.name




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

    update_password(user.name, code)

    welcome_text = "Your WELA account, username:{0}, password: {1}. " \
                   "Website: tecarro.silid.co".format(user.name, code)

    send_to_semaphore(student.student_mobile_number, welcome_text)

    exists_program = frappe.db.sql("""SELECT name FROM `tabAcademic Year`
                                                                       WHERE academic_year_name=%s""",
                                   (school_year))

    if exists_program == ():
        course_doc = frappe.get_doc({
            "doctype": "Academic Year",
            "academic_year_name": school_year
        }).insert(ignore_permissions=True)
        frappe.db.commit()


    try:
        enrollment = frappe.get_doc({
            "doctype": "Program Enrollment",
            "student": student.name,
            "academic_year": school_year,
            "program": student.program,
            "enrollment_date": frappe.utils.get_datetime().date(),
        }).insert(ignore_permissions=True)

        enrollment.submit()
    except Exception as e:
        print(e)
        pass

    return user.name