// Copyright (c) 2016, Wela School System and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Attendance Sheet"] = {
	"filters": [
        {
            "fieldname": "program",
            "label": __("Program"),
            "fieldtype": "Link",
            "options": "Program",
            "reqd": 1
        },
        {
            "fieldname": "activity_type",
            "label": __("Log Type"),
            "fieldtype": "Select",
            "options": ["Login", "Logout"],
            "default": "Login"
        },
        {
            "fieldname": "date_sect",
            "label": __("Date"),
            "fieldtype": "Date",
            "reqd": 1
        }

	]
};
