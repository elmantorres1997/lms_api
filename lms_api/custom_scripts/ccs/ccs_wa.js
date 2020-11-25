


frappe.ui.form.on('Written Activity', {

	student_1(frm) {
		// your code here
		if (frm.doc.student_name === "" || frm.doc.student_name ===undefined)
		{
		 frappe.call({
                    "method": "frappe.client.get",
                    args: {
                        doctype: "Student",
                        name: frm.doc.student_1
                    },
                    callback: function (data) {
                        cur_frm.set_value("student",data.message.user);
                        // frm.save();
						cur_frm.refresh_field("student");
            }
            });
		}
	}

});