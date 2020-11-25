import frappe
import requests
import json
from frappe import _

@frappe.whitelist()
def get_rooms(user):
    #check if student
    print(user)
    print(frappe.get_roles(user))
    school_code = frappe.db.get_single_value('Wela Settings', 'school_code')
    if "Administrator" == user:
        classes = frappe.db.sql("""SELECT DISTINCT `tabProgram Course`.course,`tabProgram`.name
                                                FROM `tabProgram Course`
                                                INNER JOIN `tabProgram`
                                                ON `tabProgram`.name = `tabProgram Course`.parent""")
        print(classes)
        if classes != ():
            strip_names = []
            for class_ in classes:
                strip_names.append(class_[1].title().replace(" ", "") + "-" + class_[0].title().replace(" ", ""))
            return strip_names, frappe.db.get_single_value('Wela Settings', 'video_tool'), school_code
        else:
            return None
    else:
        if 'Student' in frappe.get_roles(user):
            print('is student')
            student_user = frappe.db.sql("""SELECT name FROM `tabStudent` WHERE user=%s""",(frappe.session.user))
            if student_user != ():
                classes = frappe.db.sql("""SELECT `tabCourse Enrollment`.course,`tabProgram Enrollment`.program
                                    FROM `tabCourse Enrollment`
                                    INNER JOIN `tabProgram Enrollment`
                                    ON `tabProgram Enrollment`.name = `tabCourse Enrollment`.program_enrollment
                WHERE `tabCourse Enrollment`.student=%s""",(student_user[0][0]))
                print(classes)
                if classes != ():
                    strip_names = []
                    for class_ in classes:
                        strip_names.append(class_[1].title().replace(" ","")+"-"+class_[0].title().replace(" ",""))
                    return strip_names, frappe.db.get_single_value('Wela Settings', 'video_tool'), school_code
                else:
                    return None
            else:
                return None
        else:
            print("not a student")
            classes = frappe.db.sql("""SELECT DISTINCT `tabProgram Course`.course,`tabProgram`.name
                                            FROM `tabProgram Course`
                                            INNER JOIN `tabProgram`
                                            ON `tabProgram`.name = `tabProgram Course`.parent""")
            print(classes)
            if classes != ():
                strip_names = []
                for class_ in classes:
                    strip_names.append(class_[1].title().replace(" ", "") + "-" + class_[0].title().replace(" ", ""))
                return strip_names, frappe.db.get_single_value('Wela Settings', 'video_tool'), school_code
            else:
                return None

@frappe.whitelist()
def request_meeting(topic):
    topic = ''.join(e for e in topic if e.isalnum())
    school_code = frappe.db.get_single_value('Wela Settings', 'school_code')
    result = checking_meeting(topic)
    if (type(result) is str):
        result = json.loads(result)

    if "statusCode" in result:
        param = str(result['statusCode'])
    else:
        param = "200"
    if param == "404":
        URL = "https://us-central1-silid-production.cloudfunctions.net/requestMeeting"

        data = {
            "topic": topic,
            "user": frappe.session.user,
            "school_code": school_code,
        }

        r = requests.post(url = URL, data=data) 
        return r.text
    else: 
        return json.dumps(result)


@frappe.whitelist()
def checking_meeting(topic):
    topic = ''.join(e for e in topic if e.isalnum())
    school_code = frappe.db.get_single_value('Wela Settings', 'school_code')
    URL = "https://us-central1-silid-production.cloudfunctions.net/requestJoinMeeting"
    
    data = {
        "topic": topic,
        "school_code": school_code,
    }
    r = requests.post(url = URL, data=data) 
    return r.text

@frappe.whitelist()
def check_meeting_status(topic):
    topic = ''.join(e for e in topic if e.isalnum())
    school_code = frappe.db.get_single_value('Wela Settings', 'school_code')
    URL = "https://us-central1-silid-production.cloudfunctions.net/get_room"
    
    data = {
        "topic": topic,
        "school_code": school_code,
    }
    r = requests.post(url = URL, data=data) 
    return r.text

@frappe.whitelist()
def update_meeting_status(topic, status):
    topic = ''.join(e for e in topic if e.isalnum())
    school_code = frappe.db.get_single_value('Wela Settings', 'school_code')
    URL = "https://us-central1-silid-production.cloudfunctions.net/update_room"
    
    data = {
        "topic": topic,
        "school_code": school_code,
        "status": status,
    }
    r = requests.post(url = URL, data=data) 
    return r.text

@frappe.whitelist()
def request_meeting_blue_api(topic):
    topic = ''.join(e for e in topic if e.isalnum())
    response = check_meeting_blue_api(topic)
    if (type(response) is str):
        response = json.loads(response)
    if "FAILED" in response["response"]["returncode"]["_text"]:
        api_res = create_meeting_blue_api(topic)
        if (type(api_res) is str):
            api_res = json.loads(api_res)
        if "SUCCESS" in api_res["response"]["returncode"]["_text"]:
            api_join_res = join_meeting_blue_api(topic)
            return api_join_res
    else:
        api_join_res = join_meeting_blue_api(topic)
        return api_join_res
    # print(response["response"]["returncode"])

def check_meeting_blue_api(topic):
    topic = ''.join(e for e in topic if e.isalnum())
    school_code = frappe.db.get_single_value('Wela Settings', 'school_code')
    api = frappe.db.get_single_value('Wela Settings', 'api')
    if str(api) == "Scalelite 1":
        URL = "https://us-central1-silid-production.cloudfunctions.net/blue_button_api_check_room_1"
    elif str(api) == "Scalelite 2":
        URL = "https://us-central1-silid-production.cloudfunctions.net/blue_button_api_check_room_2"
    elif str(api) == "Scalelite 3":
        URL = "https://us-central1-silid-production.cloudfunctions.net/blue_button_api_check_room_3"
    else:
        URL = "https://us-central1-silid-production.cloudfunctions.net/blue_button_api_check_room_1"
    
    data = {
        "topic": str(school_code) + "_" + str(topic)
    }
    r = requests.post(url = URL, data=data)
    return r.text

def create_meeting_blue_api(topic):
    topic = ''.join(e for e in topic if e.isalnum())
    school_code = frappe.db.get_single_value('Wela Settings', 'school_code')
    api = frappe.db.get_single_value('Wela Settings', 'api')
    if str(api) == "Scalelite 1":
        URL = "https://us-central1-silid-production.cloudfunctions.net/blue_button_api_create_1"
    elif str(api) == "Scalelite 2":
        URL = "https://us-central1-silid-production.cloudfunctions.net/blue_button_api_create_2"
    elif str(api) == "Scalelite 3":
        URL = "https://us-central1-silid-production.cloudfunctions.net/blue_button_api_create_3"
    else:
        URL = "https://us-central1-silid-production.cloudfunctions.net/blue_button_api_create_1"

    data = {
        "topic": str(school_code) + "_" + str(topic)
    }
    r = requests.post(url = URL, data=data)
    return r.text

def join_meeting_blue_api(topic):
    topic = ''.join(e for e in topic if e.isalnum())
    school_code = frappe.db.get_single_value('Wela Settings', 'school_code')
    api = frappe.db.get_single_value('Wela Settings', 'api')
    if str(api) == "Scalelite 1":
        URL = "https://us-central1-silid-production.cloudfunctions.net/blue_button_api_join_1"
    elif str(api) == "Scalelite 2":
        URL = "https://us-central1-silid-production.cloudfunctions.net/blue_button_api_join_2"
    elif str(api) == "Scalelite 3":
        URL = "https://us-central1-silid-production.cloudfunctions.net/blue_button_api_join_3"
    else:
        URL = "https://us-central1-silid-production.cloudfunctions.net/blue_button_api_join_1"

    user = frappe.session.user

    if user == "Administrator":
        password = "moderator"
    elif 'Student' in frappe.get_roles(user):
        password = "attendee"
    else:
        password = "moderator"
    
    data = {
        "topic": str(school_code) + "_" + str(topic),
        "user": user,
        "pass": password
    }
    r = requests.post(url = URL, data=data)
    return r.text


@frappe.whitelist()
def get_recording_meeting_blue_api(topic):
    topic = ''.join(e for e in topic if e.isalnum())
    school_code = frappe.db.get_single_value('Wela Settings', 'school_code')
    api = frappe.db.get_single_value('Wela Settings', 'api')
    if str(api) == "Scalelite 1":
        URL = "https://us-central1-silid-production.cloudfunctions.net/blue_button_api_get_recording_1"
    elif str(api) == "Scalelite 2":
        URL = "https://us-central1-silid-production.cloudfunctions.net/blue_button_api_get_recording_2"
    elif str(api) == "Scalelite 3":
        URL = "https://us-central1-silid-production.cloudfunctions.net/blue_button_api_get_recording_3"
    else:
        URL = "https://us-central1-silid-production.cloudfunctions.net/blue_button_api_get_recording_1"

    # user = frappe.session.user

    data = {
        "topic": str(school_code) + "_" + str(topic),
    }
    r = requests.post(url = URL, data=data)
    return r.text

@frappe.whitelist()
def request_meeting_new(topic,user):
    topic = ''.join(e for e in topic if e.isalnum())
    school_code = frappe.db.get_single_value('Wela Settings', 'school_code')
    result = checking_meeting_new(topic,user)
    print(result)
    if (type(result) is str):
        result = json.loads(result)

    if "statusCode" in result:
        param = str(result['statusCode'])
    else:
        param = "200"
    if param == "404":
        URL = "https://us-central1-silid-production.cloudfunctions.net/requestMeetingNew"

        data = {
            "topic": topic,
            "school_code": school_code,
            "user": user,
        }

        r = requests.post(url = URL, data=data) 
        return r.text
    if param == "403":
        frappe.msgprint(_("Username not found"))
    else: 
        return json.dumps(result)


@frappe.whitelist()
def checking_meeting_new(topic,user):
    topic = ''.join(e for e in topic if e.isalnum())
    school_code = frappe.db.get_single_value('Wela Settings', 'school_code')
    URL = "https://us-central1-silid-production.cloudfunctions.net/requestJoinMeetingNew"
    
    data = {
        "topic": topic,
        "school_code": school_code,
        "user": user,
    }
    r = requests.post(url = URL, data=data) 
    return r.text

@frappe.whitelist()
def checking_recordings_new(topic,user):
    topic = ''.join(e for e in topic if e.isalnum())
    school_code = frappe.db.get_single_value('Wela Settings', 'school_code')
    URL = "https://us-central1-silid-production.cloudfunctions.net/requestMeetingRecordings"
    
    data = {
        "topic": topic,
        "school_code": school_code,
        "user": user,
    }
    r = requests.post(url = URL, data=data) 
    return r.text