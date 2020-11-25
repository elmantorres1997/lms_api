# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _


def get_data():
    return [
        {
            "module_name": "LMS API",
            "color": "orange",
            "icon": "octicon octicon-file-directory",
            "type": "module",
            "label": _("LMS API")
        },
        {
            "module_name": 'Program',
            "category": "Modules",
            "label": _('Classes or Programs'),
            "icon": "fa fa-graduation-cap",
            "link": "#List/Program/List",
            "doctype": "Program",
            "type": "list"
        },
        {
            "module_name": 'Class',
            "category": "Modules",
            "label": _('Class List'),
            "icon": "fa fa-graduation-cap",
            "link": "#List/Class/List",
            "doctype": "Class",
            "type": "list"
        },
        {
            "module_name": 'Content Silid',
            "category": "Modules",
            "label": _('Add a Content'),
            "icon": "fa fa-file-image-o",
            "link": "#List/Content%20Silid/List",
            "doctype": "Content Silid",
            "type": "list"
        },
        {
            "module_name": 'Quiz Silid',
            "category": "Modules",
            "label": _('Create a Quiz'),
            "icon": "fa fa-check-square-o",
            "link": "#List/Quiz%20Silid/List",
            "doctype": "Quiz Silid",
            "type": "list"
        },
        {
            "module_name": 'Written Activity',
            "category": "Modules",
            "label": _('Written Activity'),
            "icon": "fa fa-pencil-square-o",
            "link": "#List/Written Activity/List",
            "doctype": "Written Activity",
            "type": "list"
        },
        {
            "module_name": 'Quiz Activity',
            "category": "Modules",
            "label": _('Quiz Scores'),
            "icon": "fa fa-check-square-o",
            "link": "#List/Quiz%20Activity/List",
            "doctype": "Quiz Activity",
            "type": "list"
        },
          {
            "module_name": 'File Sharing Silid',
            "category": "Modules",
            "label": _('File Sharing'),
            "icon": "fa fa-check-square-o",
            "link": "#List/File%20Sharing%20Silid/List",
            "doctype": "File Sharing Silid",
            "type": "list"
        },
        {
            "module_name": 'Grading Sheet Silid',
            "category": "Modules",
            "label": _('View Grading Sheet'),
            "icon": "fa fa-check-square-o",
            "link": "#query-report/Grading%20Sheet%20Silid",
            "doctype": "Quiz Activity",
            "type": "query-report"
        },
        {
            "module_name": 'lms',
            "category": "Modules",
            "label": _('Silid Aralan'),
            "icon": "fa fa-home",
            "type": "link",
            "link": "/lms"
        },
        {
            "module_name": 'Program Enrollment Tool',
            "category": "Modules",
            "label": _('Program Enrollment Tool'),
            "icon": "fa fa-users",
            "type": "link",
            "link": "#Form/Program%20Enrollment%20Tool/Program%20Enrollment%20Tool"
        },

        {
            "module_name": "video-conference",
            "category": "Modules",
            "color": "grey",
            "icon": "fa fa-camera",
            "type": "list",
            "link": "#List/Video%20Conference%20Rooms/List",
            "label": _("Video Conference"),
        },
        {
            "module_name": "my-quiz-scores",
            "category": "Modules",
            "color": "grey",
            "icon": "fa fa-check-square-o",
            "type": "list",
            "link": "#List/Quiz%20Activity/List",
            "label": _("My Quiz Scores"),
        },
        {
            "module_name": "pending-tasks",
            "category": "Modules",
            "color": "grey",
            "icon": "fa fa-check-square-o",
            "type": "list",
            "link": "#List/To%20Do%20Tasks/List",
            "label": _("My Pending Tasks"),
        },
        {
            "module_name": "help",
            "category": "Modules",
            "color": "grey",
            "icon": "fa fa-question-circle",
            "type": "list",
            "link": "/how-to-use-silid",
            "label": _("Help"),
        },
        {
            "module_name": "attendance-sheet",
            "category": "Modules",
            "color": "grey",
            "icon": "fa fa-calendar-check-o",
            "type": "list",
            "link": "#query-report/Attendance%20Sheet",
            "label": _("Attendance Sheet"),
        },
        {
            "module_name": "master-grade",
            "category": "Modules",
            "color": "grey",
            "icon": "fa fa-check-square-o",
            "type": "list",
            "link": "#List/Master%20Grade/List",
            "label": _("Master Grade"),
        }

    ]
