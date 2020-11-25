// Copyright (c) 2016, Wela School System and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Attendance Sheet Instructor"] = {
	"filters": [
        {
            "fieldname": "activity_type",
            "label": __("Log Type"),
            "fieldtype": "Select",
            "options": ["Login", "Logout"],
            "default": "Login"
        },
        {
            "fieldname": "date_range",
            "label": __("Date"),
            "fieldtype": "Date Range",
            "reqd": 1
        }
	]
};
