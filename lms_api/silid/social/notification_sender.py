import frappe
from frappe.service import *
from collections import Counter
import phonenumbers
from frappe.frappeclient import FrappeClient
"""This will Turn Off or Turn On sending of notifications via SMS"""
TURN_ON = True

def gather_list():
    """This function will gather all comments and posts of Students from the 30 minutes"""

    # Get all comments in the past 30 minutes
    comments = execute_query("GET_STUDENT_COMMENTS_FROM_30_MINUTES_AGO", as_dict=1)
    gathered_list = []
    for comment in comments:
        gathered_list.append(comment.post_owner)
    return gathered_list

def compose(gathered_list):
    """This function will compose the message"""
    counter = Counter(gathered_list)
    counted_dict = dict(counter)
    message_list = []
    for key, value in counted_dict.items():
        message_list.append(
            {
                "owner": key,
                "message": f"You have {value} notifications from Silid Social"
            }
        )
    return message_list

def is_correct_number(number):
    if number is not None or number !="":
        phone = phonenumbers.parse(number, "PH")
        if len(str(phone.national_number)) == 10 and str(phone.country_code) == "63":
            return True
        else:
            return False
    return False

def send_list_to_memo(message_list):
    """This function will send the gathered notifications to Memo List"""
    message_priority = 0
    for message in message_list:
        wela_setting = frappe.get_doc("Wela Settings")
        user_info = execute_query("GET_USER_MOBILE_NO", filters={ "name": message['owner'] }, as_dict=1)
        number = user_info[0]['mobile_no']
        if is_correct_number(number):
            try:
                if wela_setting.post_notification_text_service == "Memo":
                    sms = frappe.get_doc(
                        {
                            "doctype": "Memo",
                            "mobile_number": number,
                            "message": message['message'],
                            "priority": message_priority
                        }
                    )
                    sms.insert(ignore_permissions=True)
                elif wela_setting.post_notification_text_service == "Tailerp":
                    try:
                        conn = FrappeClient("https://wela.tailerp.com", "gsmbox@wela.online", "hbTcTdFtBag9RV4Y")
                        params = {
                            "mobile_number": number,
                            "message": message['message']
                        }
                        lms_user = conn.get_api("gsmbox.gsmbox.doctype.memo.add_memo", params)
                    except:
                        sms = frappe.get_doc(
                            {
                                "doctype": "Memo",
                                "mobile_number": number,
                                "message": message['message'],
                                "priority": message_priority
                            }
                        )
                        sms.insert(ignore_permissions=True)
                else:
                    sms = frappe.get_doc(
                        {
                            "doctype": "Memo",
                            "mobile_number": number,
                            "message": message['message'],
                            "priority": message_priority
                        }
                    )
                    sms.insert(ignore_permissions=True)

            except Exception as e:
                print(e)
                pass

@frappe.whitelist()
def send():
    """This is the main function"""
    if TURN_ON:
        gathered_list = gather_list()
        message_list = compose(gathered_list)
        send_list_to_memo(message_list)
