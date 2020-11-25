import frappe

# bench --site all execute lms_api.patches.quiz_list.all_quiz_list_passing --args {50}
def all_quiz_list_passing(passing=50):
    """ This will change all quizzes in Quiz List passing score according to args """

    print("Script Started")

    frappe.db.sql(f"UPDATE `tabQuiz` SET passing_score={passing} WHERE 1")
    print("Quiz List Done")
    frappe.db.sql(f"UPDATE `tabQuiz Silid` SET passing_score={passing} WHERE 1")
    print("Quiz Silid List Done")


    print(f"All passing_score is now changed to {passing}")

# bench --site all execute lms_api.patches.quiz_list.update_quiz_status
def update_quiz_status():
    """ This will update all quiz status whether pass or fail according to passing_score"""

    print("Script Started")
    total_count = frappe.db.sql(f"SELECT COUNT(*) as total_rows FROM `tabQuiz Activity` WHERE 1",as_dict=1)
    all_quiz_scores = frappe.db.sql(f"SELECT name,quiz,score FROM `tabQuiz Activity` WHERE 1",as_dict=1)
    count = 0
    for quiz_score in all_quiz_scores:
        count+=1
        print(f"Progress: {count}/{total_count[0]['total_rows']}")
        quiz = escape(quiz_score['quiz'])
        quiz_name = escape(quiz_score['name'])
        quiz_infos = frappe.db.sql(f"SELECT passing_score, max_points FROM `tabQuiz` WHERE name='{quiz}'",as_dict=1)
        for quiz_info in quiz_infos:
            try:
                passing_to_float = float(quiz_info['passing_score']) / 100.0
                score_to_pass = float( float(quiz_info['max_points']) * passing_to_float )
                if float(quiz_score['score']) >= score_to_pass:
                    print("Change to Pass")
                    frappe.db.sql(f"UPDATE `tabQuiz Activity` SET status='Pass' WHERE name='{quiz_name}'")
                else:
                    print("Change to Fail")
                    frappe.db.sql(f"UPDATE `tabQuiz Activity` SET status='Fail' WHERE name='{quiz_name}'")
            except Exception as e:
                print(e)
                pass




def escape(text):
    if text:
        return text.replace("'","\\'")
    return text