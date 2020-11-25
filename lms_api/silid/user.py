import frappe

def block_modules_user(doc,method):
    print("setup user icons...")

    #     users = frappe.db.sql("""SELECT DISTINCT `tabUser`.name FROM `tabUser`
    # INNER JOIN `tabHas Role` ON `tabHas Role`.parent=`tabUser`.name
    #       WHERE `tabHas Role`.role!='Student' AND `tabHas Role`.parentfield='roles'""")
    #
    #     for i, user in enumerate(users):
    #         print(user)

            # user = frappe.get_doc("User", user[0])
    # user = doc.name
    # if user == "Administrator":
    # frappe.db.sql("""DELETE FROM `tabBlock Module` WHERE parent=%s""",(doc.name))
    # frappe.db.commit()

    # for mods in doc.block_modules:
    doc.block_modules = []

    # for d in user.block_modules:
    #     user.block_modules.remove(d)
    instructor = ["Written Activity","Grading Sheet Silid","Program Enrollment Tool",
                  "Content Silid","Quiz Silid","Quiz Activity","Class"]
    # registrar_ = ["Applicants","Enrollees","Enrollee Customer","School Tuition Plan",
    #              "School General Ledger","Accounts Receivable WSS",
    #             "Daily Payment Report","Remind Billing"]
    # coordinator_ = ["Generate SF5","Conduct Sheet","Submit Attendance","Specialized Combine Grades",
    #                 "Spreadsheets","Spreadsheets SHS",
    #                 "Combine Subject Grade","Submit Grades","Submit Grades SHS"]

    not_allowed_modules = []

    if 'Instructor' not in frappe.get_roles(doc.name):
        not_allowed_modules += instructor
    else:
        print('is teacher or coor')
    print(frappe.get_roles(frappe.session.user))
    print(not_allowed_modules)

    block_mods = ["Accounts",
                  "Agriculture",
                  "Assets",
                  "Attendance",
                  "Attendance Summary",
                  "Buying",
                  "Chapter",
                  "Clinical Procedure",
                  "Contacts",
                  "Core",
                  "Course",
                  "Course Schedule",
                  "CRM",
                  "Crop",
                  "Crop Cycle",
                  "Customer",
                  "Daily Attendance",
                  "Data Import",
                  "Desk",
                  "Disciplinary Notes",
                  "Disease",
                  "Donor",
                  "Education",
                  "Email Inbox",
                  "Employee",
                  "Fees",
                  "Fertilizer",
                  "File Manager",
                  "Generate SF5",
                  "Grading",
                  "Grant Application",
                  "Gsmbox",
                  "Healthcare",
                  "Healthcare Practitioner",
                  "Hotels",
                  "HR"
                  "Hub",
                  "ID Management",
                  "Inpatient Record",
                  "Instructor",
                  "Integrations",
                  "Issue",
                  "Lab Test",
                  "Lead",
                  "Leaderboard",
                  "Learn",
                  "Library",
                  "Location",
                  "Maintenance",
                  "Manufturing",
                  "Master Grading Report",
                  "Mastersheets SHS",
                  "Member",
                  "Non Profit",
                  "Patient",
                  "Patient Appointment",
                  "Patient Encounter",
                  "Plant Analysis",
                  "POS",
                  "Profit and Loss Statement",
                  "Program",
                  "Project",
                  "Projects",
                  "Registration",
                  "Restaurant",
                  "Room",
                  "Selling",
                  "Setup",
                  "Soil Analysis",
                  "Soil Texture",
                  "Stock",
                  "Student",
                  "Student Applicant",
                  "Student Attendance Report",
                  "Student Attendance Tool",
                  "Supplier",
                  "Support",
                  "Vital Signs",
                  "Volunteer",
                  "Water Analysis",
                  "Weather",
                  "Website",
                  "Quality Management",
                  "HR",
                  #"Social", #temp
                  "Settings",
                  "Customization",
                  "Users and Permissions",
                  "dashboard",
                  "Marketplace",
                  "Getting Started",
                  "Help",
                  # "Silid Aralan" # temp
                  # "lms" #temp
                  ]

    block_mods += not_allowed_modules

    for mod in block_mods:
        doc.append("block_modules", {
            'module': mod
        })

    # user.save()
    # if i % 100:
    frappe.db.commit()


#bench execute lms_api.silid.user.update_users
def update_users():
    for user in frappe.db.sql("""select name from `tabUser`"""):
        doc = frappe.get_doc("User",user[0])
        doc.save()
        # frappe.db.sql("""DELETE FROM `tabBlock Module` WHERE parent=%s""", (doc.name))
        # # for d in user.block_modules:
        # #     user.block_modules.remove(d)
        # instructor = ["Written Activity", "Grading Sheet Silid", "Program Enrollment Tool",
        #               "Content Silid", "Quiz Silid", "Quiz Activity"]
        # # registrar_ = ["Applicants","Enrollees","Enrollee Customer","School Tuition Plan",
        # #              "School General Ledger","Accounts Receivable WSS",
        # #             "Daily Payment Report","Remind Billing"]
        # # coordinator_ = ["Generate SF5","Conduct Sheet","Submit Attendance","Specialized Combine Grades",
        # #                 "Spreadsheets","Spreadsheets SHS",
        # #                 "Combine Subject Grade","Submit Grades","Submit Grades SHS"]
        #
        # not_allowed_modules = []
        #
        # if 'Instructor' not in frappe.get_roles(doc.name):
        #     not_allowed_modules += instructor
        # else:
        #     print('is teacher or coor')
        # print(frappe.get_roles(frappe.session.user))
        # print(not_allowed_modules)
        #
        # block_mods = ["Accounts",
        #               "Agriculture",
        #               "Assets",
        #               "Attendance",
        #               "Attendance Summary",
        #               "Buying",
        #               "Chapter",
        #               "Clinical Procedure",
        #               "Contacts",
        #               "Core",
        #               "Course",
        #               "Course Schedule",
        #               "CRM",
        #               "Crop",
        #               "Crop Cycle",
        #               "Customer",
        #               "Daily Attendance",
        #               "Data Import",
        #               "Desk",
        #               "Disciplinary Notes",
        #               "Disease",
        #               "Donor",
        #               "Education",
        #               "Email Inbox",
        #               "Employee",
        #               "Fees",
        #               "Fertilizer",
        #               "File Manager",
        #               "Generate SF5",
        #               "Grading",
        #               "Grant Application",
        #               "Gsmbox",
        #               "Healthcare",
        #               "Healthcare Practitioner",
        #               "Hotels",
        #               "HR"
        #               "Hub",
        #               "ID Management",
        #               "Inpatient Record",
        #               "Instructor",
        #               "Integrations",
        #               "Issue",
        #               "Lab Test",
        #               "Lead",
        #               "Leaderboard",
        #               "Learn",
        #               "Library",
        #               "Location",
        #               "Maintenance",
        #               "Manufturing",
        #               "Master Grading Report",
        #               "Mastersheets SHS",
        #               "Member",
        #               "Non Profit",
        #               "Patient",
        #               "Patient Appointment",
        #               "Patient Encounter",
        #               "Plant Analysis",
        #               "POS",
        #               "Profit and Loss Statement",
        #               "Program",
        #               "Project",
        #               "Projects",
        #               "Registration",
        #               "Restaurant",
        #               "Room",
        #               "Selling",
        #               "Setup",
        #               "Soil Analysis",
        #               "Soil Texture",
        #               "Stock",
        #               "Student",
        #               "Student Applicant",
        #               "Student Attendance Report",
        #               "Student Attendance Tool",
        #               "Supplier",
        #               "Support",
        #               "Vital Signs",
        #               "Volunteer",
        #               "Water Analysis",
        #               "Weather",
        #               "Website",
        #               "Quality Management",
        #               "HR",
        #               #   "Social",
        #               "Settings",
        #               "Customization",
        #               "Users and Permissions",
        #               "dashboard",
        #               "Marketplace",
        #               "Getting Started",
        #               "Help"
        #               ]
        #
        # block_mods += not_allowed_modules
        #
        # for mod in block_mods:
        #     doc.append("block_modules", {
        #         'module': mod
        #     })
        #
        # user.save()
        # # if i % 100:
        # frappe.db.commit()
