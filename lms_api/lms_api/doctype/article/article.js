// Copyright (c) 2020, Wela School System and contributors
// For license information, please see license.txt

frappe.ui.form.on('Article', {
	refresh: function(frm) {
        if (!frappe.user.has_role("Student") || frappe.session.user == "Administrator"){
	        frm.add_custom_button(__('Save to Master Grade'), function(){
                    let d = new frappe.ui.Dialog({
                    title: 'Confirm',
                    fields: [
                        {
                            label: "Message",
                            fieldname: "warn",
                            fieldtype: "HTML Editor",
                            default: "<b style='color:red;font-size:20px;'>This will updated all linked Written Activities info to Master Grade</b>",
                            read_only:1
                        }
                    ],
                    primary_action_label: 'Confirm',
                    primary_action(values) {
                        frappe.call({
                            method:"lms_api.lms_api.doctype.article.article.carry_over",
                            args: {
                                docname:frm.doc.name
                            },
                            async:false,
                            callback: function(r) {
                                frappe.msgprint("Written Activities are being sent to master grade")
                            }
                        })
                        d.hide();
                    }
                });
                d.show();

            }).addClass("btn-primary");
        }
    }
});
