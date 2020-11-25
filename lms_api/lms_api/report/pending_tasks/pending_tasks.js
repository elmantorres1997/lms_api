// Copyright (c) 2016, Wela School System and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Pending Tasks"] = {
	"filters": [
         {
            "fieldname": "type",
            "label": __("Activity Type"),
            "fieldtype": "Select",
            "options": ["All", "Quiz", "Content"],
            "default": "All",
            "reqd": 1
        },
        {
            "fieldname": "classwork_category",
            "label": __("Classwork Category"),
            "fieldtype": "Link",
            "options": "Classwork Category"
        },
        {
            "fieldname": "page",
            "label": __("Page"),
            "fieldtype": "Int",
            "default": 1,
            "reqd": 1
        }
	],
		onload: function(report) {


	    report.page.add_inner_button(__("1st Page"), function() {


		    frappe.query_report.set_filter_value("page",1);
		    frappe.query_report.refresh();

				});





		report.page.add_inner_button(__("Prev Page"), function() {

		    var now_page = frappe.query_report.get_filter_value("page");

		    now_page -= 1
			if (now_page<1)
				now_page = 1;
			console.log(now_page);
		    frappe.query_report.set_filter_value("page",now_page);
		    frappe.query_report.refresh();

				});

		report.page.add_inner_button(__("Next Page"), function() {

		    var now_page = frappe.query_report.get_filter_value("page");

		    now_page += 1
			console.log(now_page);
		    frappe.query_report.set_filter_value("page",now_page);
		    frappe.query_report.refresh();

				});

	}
};
