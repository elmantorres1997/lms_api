// Copyright (c) 2020, Wela School System and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sectioning', {

    year_level: function(frm) {
        frappe.call({
            method:"lms_api.lms_api.doctype.sectioning.sectioning.get_students",
            args:{
                "level": frm.doc.year_level,
                "branch": frm.doc.branch ? frm.doc.branch : ""
            },
            callback: function(r){
                frm.clear_table("enrollees");
                r.message.forEach(function (arrayItem) {
                    var enrollee = frm.add_child("enrollees");
                    enrollee.student = arrayItem.name;
                    let fullname = (arrayItem.first_name ? arrayItem.first_name : "" )+ (arrayItem.last_name ? " "+arrayItem.last_name : "");
                    enrollee.student_name = fullname;
                    enrollee.branch = arrayItem.branch;
                });
                frm.refresh_field("enrollees");
            }
        })
    },

    branch: function(frm) {
        if (frm.doc.year_level) {
            frappe.call({
                method:"lms_api.lms_api.doctype.sectioning.sectioning.get_students",
                args:{
                    "level": frm.doc.year_level,
                    "branch": frm.doc.branch
                },
                callback: function(r){
                    frm.clear_table("enrollees");
                    r.message.forEach(function (arrayItem) {
                        var enrollee = frm.add_child("enrollees");
                        enrollee.student = arrayItem.name;
                        let fullname = (arrayItem.first_name ? arrayItem.first_name : "" )+ (arrayItem.last_name ? " "+arrayItem.last_name : "");
                        enrollee.student_name = fullname;
                        enrollee.branch = arrayItem.branch;
                    });
                    frm.refresh_field("enrollees");
                }
            })
        }
    }
});
