// Copyright (c) 2015, Frappe Technologies and contributors
// For license information, please see license.txt

cur_frm.add_fetch('fee_structure', 'total_amount', 'amount');

frappe.ui.form.on("Program", "refresh", function(frm) {
    if (frm.doc.exam_students.length==0) {
        frappe.call({
            method: "lms_api.lms_api.doctype.program.get_enrolled_students",
            args: {
                "program": frm.doc.name
            },
            callback: function (r) {
                console.log(r);
                for (var i = 0; i < r.message.length; i++) {
                    console.log(r.message[i])
                    var newrow = frm.add_child("exam_students");
                    newrow.student = r.message[i][0]
                    newrow.student_name = r.message[i][1]
                    newrow.username = r.message[i][2]
                    cur_frm.refresh_field("exam_students");
                }
            }
        })

    }
});