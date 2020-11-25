// Copyright (c) 2016, Bai Web and Mobile Lab and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Grading Sheet Silid"] = {
	"filters": [
//         {
//            "fieldname": "program",
//            "label": __("Grade Level and Section"),
//            "fieldtype": "Link",
//            "options": "Program",
//            "reqd": 1
//        },
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
        },
        {
            "fieldname": "raw_score",
            "label": __("Raw Score Only"),
            "fieldtype": "Check",
            "default": 0
        }
	],
    refresh:function(report) {
        $("button:contains('Refresh')").prop("disabled",true)
        $("button:contains('Refresh')").hide()
    },

	onload: function(report){
        $("button:contains('Refresh')").prop("disabled",true)
        $("button:contains('Refresh')").hide()
        report.page.add_inner_button(__("Refresh Grades"), function() {
            $("button:contains('Refresh Grades')").prop("disabled",true)
            try{
                frappe.query_report.refresh();
            }catch(e) {console.log(e)}
		    setTimeout(function(){
		        $("button:contains('Refresh Grades')").prop("disabled",false)
            }, 3000);


        }).addClass("btn-primary");

        report.page.add_inner_button(__("Preview"), function() {
            $("[data-label=Export]").click();
            setTimeout(function(){
                $('button:contains("Download")').click();
            }, 500)
        }).addClass("btn-primary");

//        report.page.add_inner_button(__("Send Grades to Wela"), function() {
//
//            let d = new frappe.ui.Dialog({
//                title: 'Are you sure?',
//                fields: [
//                    {
//                        label: "Sending Grades to Wela",
//                        fieldname: "warn",
//                        fieldtype: "HTML Editor",
//                        default: "<b style='color:red;font-size:20px;'>Please make sure that all grades are correct. Do you wish to proceed?</b>",
//                        read_only:1
//                    }
//                ],
//                primary_action_label: 'Proceed',
//                primary_action(values) {
//                    try{
//                        const column_row = report.columns.reduce((acc, col) => {
//                            if (!col.hidden) {
//                                acc.push(col.label);
//                            }
//                            return acc;
//                        }, []);
//                        const rows = report.datatable.bodyRenderer.visibleRows;
//                        if (report.raw_data.add_total_row) {
//                            rows.push(report.datatable.bodyRenderer.getTotalRow());
//                        }
//
//                        let data_array = rows.map(row => {
//                            const standard_column_count = report.datatable.datamanager.getStandardColumnCount();
//                            return row
//                                .slice(standard_column_count)
//                                .map((cell, i) => {
//                                    if (true && i===0) {
//                                        cell.content = '   '.repeat(row.meta.indent) + (cell.content || '');
//                                    }
//                                    return cell.content || '';
//                                });
//                        });
//
//                        index_of_student_name = report.columns.indexOf("Student")
//                        index_of_final_grade = report.columns.indexOf("Final Percentage")
//
//                        let regex = /(<([^>]+)>)/ig
//                        let grades_obj = {}
//                        $.each(data_array, function(ide,data) {
//                            grades_obj[data[index_of_student_name]] = (data[index_of_final_grade]).replace(regex,"").replace("%","")
//                        })
//
//                        frappe.call({
//                            method:"lms_api.lms_api.report.grading_sheet_silid.grading_sheet_silid.send_grades_to_wela",
//                            args: {
//                                grades: grades_obj
//                            },
//                            callback:function (r){
//                                console.log(r)
//                                frappe.msgprint(r.message)
//                            }
//                        })
//                    }
//                    catch(e){
//                        frappe.msgprint("No Data Found");
//                    }
//                    d.hide();
//                }
//            });
//
//
//            d.show();
//
//
//        }).addClass("btn-primary");
	}
}