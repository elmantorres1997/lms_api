// Copyright (c) 2016, Wela School System and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sectioning Status"] = {
	"filters": [
        {
            "fieldname": "status",
            "label": __("Status"),
            "fieldtype": "Select",
            "options": ["","Sectioned", "Unsectioned"],
            "default": "",
            "reqd": 1
        },
	]
};
