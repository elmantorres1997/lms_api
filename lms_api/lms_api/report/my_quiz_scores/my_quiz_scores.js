// Copyright (c) 2016, Wela School System and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["My Quiz Scores"] = {
	"filters": [
        {
            "fieldname": "`tabQuiz Activity`.quiz",
            "label": __("Quiz Name"),
            "fieldtype": "Data",
            "reqd": 0
        },
	]
};
