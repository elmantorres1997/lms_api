import frappe
import phonenumbers
from frappe.utils.background_jobs import enqueue
from frappe.frappeclient import FrappeClient
deadline_reminder = "Hi {0}, kamusta? You have an Activity on DUE. Open na sa {1} :) This is an automated SMS. Do not reply."
new_content_msg = "Hi {0}, kamusta? Your teacher added a NEW Activity. Open na sa {1} :) This is an automated SMS. Do not reply."

def wrong_number(number):
    invalid_number = 0
    if number:
        formatted_number = ""
        try:
            phone = phonenumbers.parse(number, "PH")
            if len(str(phone.national_number)) > 10 or len(str(phone.national_number)) < 10:
                # frappe.throw("Wrong Mobile Number format for Mother, should be 63 + 10 digits")
                invalid_number = 1
        except:
            invalid_number = 1
    return invalid_number

def send_sms(mobile_number, message,prio=0):

    if not wrong_number(mobile_number):
        # print "SENDING NOW"

        sms = frappe.get_doc({"doctype": "Memo",
                              "mobile_number": mobile_number,
                              "message": message,
                              "priority":prio
                              })
        sms.insert(ignore_permissions=True)

    else:
        error_msg = "Wrong Number."
        # frappe.get_doc({"doctype": "Wela Error Log",
        #                 "name": id_generator(),
        #                 "method": "SMS Error",
        #                 "error": "{'error_msg':'" + error_msg +
        #                          "','student':'" + name +
        #                          "','number':'" + mobile_number +
        #                          ",'id':'" + id_generator() + "'}"}).insert(ignore_permissions=True)

#lms_api.silid.notifications.clear_dates
def clear_dates():#for debugging
    frappe.db.sql("""UPDATE `tabContent Silid`
               SET remind_deadline=NULL, remind_new=NULL """)



#lms_api.silid.notifications.deadlines
@frappe.whitelist()
def publish_dates():



    date_today = frappe.utils.get_datetime().date()
    print(date_today)
    contents = frappe.db.sql("""SELECT program,article_number,title,name
                            FROM `tabContent Silid`
                            WHERE publish_date <= %s
                            AND publish_date != '' AND publish_date is not NULL
                            AND (remind_new is NULL OR remind_new ='') """,(date_today),as_dict=True)

    messages = []
    print(contents)
    if contents != ():
        for content in contents:
            students = frappe.db.sql("""SELECT `tabStudent`.first_name,
                              `tabStudent`.student_mobile_number
                              FROM `tabProgram Enrollment`
                              INNER JOIN `tabStudent` ON `tabStudent`.name = `tabProgram Enrollment`.student
                               WHERE program=%s""",(content['program']),as_dict=True)

            for student in students:
                print(content['title'])
                new_content_msg = "Hi {0}, kamusta? Your teacher added a NEW Activity. Open na sa {1} :) This is an automated SMS. Do not reply."
                message = new_content_msg.format(student.first_name,frappe.utils.get_url())


                if message not in messages:
                    print(message)
                    messages.append(message)
                    if student['student_mobile_number']:
                        try:
                            send_sms(student['student_mobile_number'],message)
                        except:
                            print("error sms")
                    else:
                        print("mobile no not specified")


            frappe.db.sql("""UPDATE `tabContent Silid`
                SET remind_new=%s WHERE name=%s""",(date_today,content['name']))

            """

            send text messages

            """
            frappe.db.commit()







@frappe.whitelist()
def deadlines():

    date_today = frappe.utils.get_datetime().date()
    print(date_today)
    contents = frappe.db.sql("""SELECT program,article_number,title,name
                            FROM `tabContent Silid`
                            WHERE deadline <= %s
                            AND deadline != ''
                            AND (remind_deadline is NULL OR remind_deadline ='') """, (date_today),
                             as_dict=True)

    messages = []
    print(contents)
    if contents != ():
        for content in contents:
            students = frappe.db.sql("""SELECT `tabStudent`.first_name,
                              `tabStudent`.student_mobile_number
                              FROM `tabProgram Enrollment`
                              INNER JOIN `tabStudent` ON `tabStudent`.name = `tabProgram Enrollment`.student
                               WHERE program=%s""", (content['program']), as_dict=True)

            for student in students:
                print(content['title'])
                deadline_reminder = "Hi {0}, kamusta? You have an Activity on DUE. Open na sa {1} :) This is an automated SMS. Do not reply."
                message = deadline_reminder.format(student.first_name, frappe.utils.get_url())

                if message not in messages:
                    print(message)
                    messages.append(message)
                    if student['student_mobile_number']:
                        try:
                            send_sms(student['student_mobile_number'], message)
                        except:
                            print("error sms")
                    else:
                        print("mobile no not specified")

            frappe.db.sql("""UPDATE `tabContent Silid`
                SET remind_deadline=%s WHERE name=%s""", (date_today, content['name']))

            """

            send text messages

            """
            frappe.db.commit()


# def new_content(name,program):
#
#     date_today = frappe.utils.get_datetime().date()
#
#     messages = []
#     students = frappe.db.sql("""SELECT `tabStudent`.first_name,
#                       `tabStudent`.student_mobile_number
#                       FROM `tabProgram Enrollment`
#                       INNER JOIN `tabStudent` ON `tabStudent`.name = `tabProgram Enrollment`.student
#                        WHERE program=%s""",(program),as_dict=True)
#
#     for student in students:
#         # print(content['title'])
#         message = deadline_reminder.format(student.first_name,frappe.utils.get_url())
#
#
#         if message not in messages:
#             print(message)
#             messages.append(message)
#             if student['student_mobile_number']:
#                 try:
#                     send_sms(student['student_mobile_number'],message)
#                 except:
#                     print("error sms")
#             else:
#                 print("mobile no not specified")
#
#
#     frappe.db.sql("""UPDATE `tabContent Silid`
#         SET remind_deadline=%s WHERE name=%s""",(date_today,name))
#
#     """
#
#     send text messages
#
#     """
#     frappe.db.commit()


def check_up():
    pass


@frappe.whitelist()
def custom_text(msg,program):
    enqueue("lms_api.silid.notifications.custom_text_", queue='long', msg=msg,program=program)
    # custom_text_(msg=msg, program=program)
    """

    send text messages

    """
    # frappe.db.commit()
    return "Success!"

@frappe.whitelist()
def custom_text_(msg,program):
    students = frappe.db.sql("""SELECT `tabStudent`.first_name,
                             `tabStudent`.student_mobile_number
                             FROM `tabProgram Enrollment`
                             INNER JOIN `tabStudent` ON `tabStudent`.name = `tabProgram Enrollment`.student
                              WHERE program=%s""", (program), as_dict=True)
    wela_setting = frappe.get_doc("Wela Settings")
    if wela_setting.content_text_service == "Memo":
        for student in students:
            if student['student_mobile_number']:
                try:
                    send_sms(student['student_mobile_number'], msg)
                except:
                    print("error sms")
            else:
                print("mobile no not specified")
    else:
        conn = FrappeClient("https://wela.tailerp.com", "gsmbox@wela.online", "hbTcTdFtBag9RV4Y")
        for student in students:
            params = {
                "mobile_number": student['student_mobile_number'],
                "message": msg
            }

            lms_user = conn.get_api("gsmbox.gsmbox.doctype.memo.add_memo", params)