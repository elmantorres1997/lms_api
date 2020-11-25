// Copyright (c) 2016, Bai Web and Mobile Lab and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["College Score Sheet"] = {
	"filters": [
         {
            "fieldname": "program",
            "label": __("Grade Level and Section"),
            "fieldtype": "Link",
            "options": "Program",
            "reqd": 1
        },
        {
            "fieldname": "course",
            "label": __("Subject"),
            "fieldtype": "Link",
            "options": "Course",
            "reqd": 1
        },
        {
            "fieldname": "quarter",
            "label": __("Quarter"),
            "fieldtype": "Link",
            "options": "Quarter",
            "reqd": 1
        }
	],
	onload: function(report){
        $("button:contains('Refresh')").prop("disabled",true)
        report.page.add_inner_button(__("Refresh Grades"), function() {
            $("button:contains('Refresh Grades')").prop("disabled",true)
            try{
                frappe.query_report.refresh();
            }catch(e) {console.log(e)}
		    setTimeout(function(){
		        $("button:contains('Refresh Grades')").prop("disabled",false)
            }, 3000);
        }).addClass("btn-primary");
	}
}