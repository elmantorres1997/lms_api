// Copyright (c) 2020, Wela School System and contributors
// For license information, please see license.txt

frappe.ui.form.on('Amend Sectioning', {
	student: function(frm){
	    frappe.call({
	        method: "lms_api.lms_api.doctype.amend_sectioning.amend_sectioning.get_student_name",
	        args: {
	            student: frm.doc.student
	        },
	        async:false,
	        callback: function(r){
	            let first_name = r.message['first_name'] || ""
	            let last_name = r.message['last_name'] || ""
	            let full_name = first_name+" " + last_name
	            frm.set_value("student_name", full_name);
	            frm.refresh_field("student_name");
	        }
	    })
	}
});
