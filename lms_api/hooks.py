# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "lms_api"
app_title = "LMS API"
app_publisher = "Wela School System"
app_description = "Silid"
app_icon = "octicon octicon-file-directory"
app_color = "orange"
app_email = "hello@wela.online"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "assets/lms_api/css/custom.css"
app_include_js = "/assets/lms_api/js/notification_service.js"
# app_include_jss = "/assets/lms_api/js/howler.js"
app_include_naive = "/assets/lms_api/js/naive.js"

# include js, css files in header of web template
# web_include_css = "/assets/lms_api/css/lms_api.css"
# web_include_js = "/assets/lms_api/js/lms_api.js"
# web_include_js = "/files/external_api.js"

# include js in page
page_js = {"video-conference" : "public/js/external_api.js"}


# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "lms_api.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "lms_api.install.before_install"
# after_install = "lms_api.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "lms_api.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

#/home/jvfiel/frappe-v11/apps/lms_api/lms_api/silid/__init__.py
doc_events = {
    "User": {
        "validate": "lms_api.silid.user.block_modules_user"
    },
    "Content Silid": {
        "validate": "lms_api.silid.validate_silid",
        # "on_cancel": "method",
        "on_trash": "lms_api.silid.on_trash_silid"
    },
    "Program Enrollment": {
        "after_insert": "lms_api.silid.auto_submit_enrollee"
    },
    "Topic": #/lms_api/silid/__init__.py
        {
            # "before_insert": "lms_api.silid.name_topic",
            "autoname": "lms_api.silid.name_topic",
            # "validate": "lms_api.silid.name_topic"
        },
    "File": {
        "after_insert": "lms_api.silid.attach_f",
    },
    # "Quiz Silid": {
    #     "validate": "lms_api.silid.quiz.create_quiz",
    #     "after_insert": "lms_api.silid.quiz.create_to_do_tasks_enqueue",
    # },
    "Program Enrollment": {
        "autoname": "lms_api.silid.quiz.student_name",
    },
    # "Written Activity": {
    #     "validate": "lms_api.silid.set_program", # lms_api.silid.set_program
    # },
    "Quiz Question": {
        "validate": "lms_api.silid.quiz.shorten_quiz",  # lms_api.silid.set_program
        "before_insert": "lms_api.silid.quiz.shorten_quiz",  # lms_api.silid.set_program
        "autoname": "lms_api.silid.quiz.shorten_quiz",  # lms_api.silid.set_program
        "before_save": "lms_api.silid.quiz.shorten_quiz",  # lms_api.silid.set_program
        "on_trash": "lms_api.silid.quiz.shorten_quiz",  # lms_api.silid.set_program
        "after_delete": "lms_api.silid.quiz.shorten_quiz",  # lms_api.silid.set_program
        #lms_api/silid/quiz.shorten_quiz
    },
    "Course Activity": {
        "after_insert": "lms_api.silid.mark_to_do_done"
    }
}

# Scheduled Tasks
# ---------------

scheduler_events = {
    "cron": {
        "*/5 20,0-5 * * *": [
            "lms_api.lms_api.doctype.schedule_mg.schedule_mg.execute_schedules"
        ],
        # "*/5 18,0-5 * * *": [
        #     "lms_api.patches.sq.execute_all"
        # ],
        "*/5 * * * *": [
            "lms_api.patches.sq.execute_all"
        ],
        "0 12 * * *": [
            "lms_api.silid.social.notification_sender.send"
        ],
        "0 17 * * *": [
            "lms_api.silid.social.notification_sender.send"
        ]
    }
}

# Testing
# -------

# before_tests = "lms_api.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "lms_api.event.get_events"
# }
fixtures = ['Web Page', 'Custom Script','Calendar View', 'Print Format']

