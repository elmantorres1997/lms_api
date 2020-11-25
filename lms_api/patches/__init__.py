import frappe
import  json
import datetime
import re


#bench execute lms_api.lms_api.patches.test_json
def test_json():


 #    s = """
 #
 # {'quiz_response': '{"QUESTION-205183":"8b3c6ec117","QUESTION-205184":"927c6b2f02","QUESTION-205185":"1c251c935c","QUESTION-205186":"f828d1d499","QUESTION-205187":"9a21101419","QUESTION-205188":"2a00f017e1","QUESTION-205189":"c22205c279","QUESTION-205190":"ac3a12cd8d","QUESTION-205191":"afef2475bb","QUESTION-205192":"043e8df02e","QUESTION-205193":"Economics","QUESTION-205194":"T","QUESTION-205195":"T","QUESTION-205196":"T","QUESTION-205197":"Water Resource","QUESTION-205198":"Wind","QUESTION-205199":"T","QUESTION-205200":"Capital","QUESTION-205201":"Water","QUESTION-205202":"T","QUESTION-205203":"Human Resources","QUESTION-205204":"People using force for commercial sex act.","QUESTION-205205":"being aware of your doings, and what is wrong and right.","QUESTION-205206":"Capital","QUESTION-205207":"Outdated jeepneys that are old and rusty are changed into modernized vehicles","QUESTION-205208":"Making all jeepneys modernized for our public transport.","QUESTION-205209":"Capital","QUESTION-205210":"People are using fake money to pay for goods.","QUESTION-205211":"Should use real money to pay for their needs.","QUESTION-205212":"Natural","QUESTION-205213":"Climate change causes damage to our environment","QUESTION-205214":"Be aware of your surroundings and clean your environment properly.","QUESTION-205215":"Capital","QUESTION-205216":"Unstable internet connection.","QUESTION-205217":"Find a more stable internet source that has good signal.","QUESTION-205218":"NE","QUESTION-205219":"PE","QUESTION-205220":"NE","QUESTION-205221":"PE","QUESTION-205222":"NE","QUESTION-205223":"PE","QUESTION-205224":"PE","QUESTION-205225":"NE","QUESTION-205226":"PE","QUESTION-205227":"NE","QUESTION-205228":" Covid-19 has affected the resources of the Philippines. Which the specific resource of Human has been affected a lot, Humans have been sick for days, weeks, and months. So, we need to help them get better.\\nIn Natural Recources, it has healed our environment because people rarely go out. This helps not causing a lot of damage to our environment. Reduced energy demand.\\nCapital Resources have created a huge impact to our society. People have created machines to help us with our needs. But it can also lead to unemployment for the people who have worked before in the factories and etc.\\n\\n\\n"}', 'quiz_name': '0d256c3d9a', 'course': 'Social Studies 9 – Prudence A', 'program': 'Grade 9 – Prudence A'}
 #    """

    s = """
    
{'quiz_response': '{"QUESTION-205183":"8b3c6ec117","QUESTION-205184":"927c6b2f02","QUESTION-205185":"1c251c935c","QUESTION-205186":"f828d1d499","QUESTION-205187":"9a21101419","QUESTION-205188":"2a00f017e1","QUESTION-205189":"c22205c279","QUESTION-205190":"ac3a12cd8d","QUESTION-205191":"afef2475bb","QUESTION-205192":"043e8df02e","QUESTION-205193":"Economics","QUESTION-205194":"T","QUESTION-205195":"T","QUESTION-205196":"T","QUESTION-205197":"Water Resource","QUESTION-205198":"Wind","QUESTION-205199":"T","QUESTION-205200":"Capital","QUESTION-205201":"Water","QUESTION-205202":"T","QUESTION-205203":"Human Resources","QUESTION-205204":"People using force for commercial sex act.","QUESTION-205205":"being aware of your doings, and what is wrong and right.","QUESTION-205206":"Capital","QUESTION-205207":"Outdated jeepneys that are old and rusty are changed into modernized vehicles","QUESTION-205208":"Making all jeepneys modernized for our public transport.","QUESTION-205209":"Capital","QUESTION-205210":"People are using fake money to pay for goods.","QUESTION-205211":"Should use real money to pay for their needs.","QUESTION-205212":"Natural","QUESTION-205213":"Climate change causes damage to our environment","QUESTION-205214":"Be aware of your surroundings and clean your environment properly.","QUESTION-205215":"Capital","QUESTION-205216":"Unstable internet connection.","QUESTION-205217":"Find a more stable internet source that has good signal.","QUESTION-205218":"NE","QUESTION-205219":"PE","QUESTION-205220":"NE","QUESTION-205221":"PE","QUESTION-205222":"NE","QUESTION-205223":"PE","QUESTION-205224":"PE","QUESTION-205225":"NE","QUESTION-205226":"PE","QUESTION-205227":"NE","QUESTION-205228":" Covid-19 has affected the resources of the Philippines. Which the specific resource of Human has been affected a lot, Humans have been sick for days, weeks, and months. So, we need to help them get better.\\nIn Natural Recources, it has healed our environment because people rarely go out. This helps not causing a lot of damage to our environment. Reduced energy demand.\\nCapital Resources have created a huge impact to our society. People have created machines to help us with our needs. But it can also lead to unemployment for the people who have worked before in the factories and etc.\\n\\n\\n"}', 'quiz_name': '9b56914fdd', 'course': 'Social Studies 9 – Prudence A', 'program': 'Grade 9 – Prudence A','student':'abaoathenajanelle@wela.online'} 
    """



    s = s.replace('"','\ "'.replace(" ",""))
    #
    # print(str)
    #
    s = s.replace("'",'"')
    #
    #
    # print(str)

    print(s)

    loaded = json.loads(s)


    print(loaded['student'], loaded['quiz_response'])


def clean_(str):

    print(str)

    str = str.replace('"', '\ "'.replace(" ", ""))
    print("==============")

    print(str)

    str = str.replace("'", '"')
    print("================")

    print(str)

    loaded = json.loads(str)


    return loaded




def test_json2():
    stop_time = datetime.datetime.now() + datetime.timedelta(minutes=4)
    all = frappe.db.sql("SELECT * FROM `tabScheduled Quizzes` WHERE checked=0 limit 1",as_dict=1)
    total = len(all)
    print("Total:", total)



    for sh in all:

        loaded = ""
        data = sh['data']
        quiz_name = sh['quiz']
        # loaded = json.loads(data)
        try:
            loaded = json.loads(data)
        except Exception as e:
            # frappe.log_error(frappe.get_traceback())
            try:
                loaded = clean_(data)
            except Exception as e:
                frappe.log_error(frappe.get_traceback())

        if loaded:
            print(loaded['student'], loaded['quiz_response'])