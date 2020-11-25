import frappe

#bench --site all execute lms_api.patches.fix_classwork.fix
def fix():

    condition = " REGEXP 'grade 1-|grade 2|grade 3|grade 4|grade 5|grade 6'"
    condition2 = "Formative Assessment (FA)"
    condition3 = "Summative Assessment (SA)"
    classwork = "Written Work"
    print("This will replace FA and SA to Written Work from Grade 1 to Grade 6")
    input("Highly recommended to backup before proceeding. Press any key to continue... ")

    # update Quiz
    frappe.db.sql(f"UPDATE `tabQuiz` SET classwork_category='{classwork}' WHERE program {condition} "
                  f"AND (classwork_category='{condition2}' OR classwork_category='{condition3}') ")

    # update article
    frappe.db.sql(f"UPDATE `tabArticle` SET classwork_category='{classwork}' WHERE program {condition} "
                  f"AND (classwork_category='{condition2}' OR classwork_category='{condition3}') ")

    # update Video
    frappe.db.sql(f"UPDATE `tabVideo` SET classwork_category='{classwork}' WHERE program {condition} "
                  f"AND (classwork_category='{condition2}' OR classwork_category='{condition3}') ")

    # Master Grade
    frappe.db.sql(f"UPDATE `tabMaster Grade` SET component='{classwork}' WHERE program {condition} "
                  f"AND (component='{condition2}' OR component='{condition3}') ")
    frappe.db.commit()

    print("Process done.")