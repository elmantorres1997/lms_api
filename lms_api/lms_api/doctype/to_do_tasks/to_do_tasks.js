// Copyright (c) 2020, Wela School System and contributors
// For license information, please see license.txt

frappe.ui.form.on('To Do Tasks', {
	 refresh: function(frm) {
        frm.clear_custom_buttons();
        let final_link = ""
        frappe.call({
            method:"lms_api.lms_api.doctype.to_do_tasks.to_do_tasks.get_link",
            args: {
                "content_id": frm.doc.content_id,
                "task_type": frm.doc.task_type
            },
            callback: function(r) {
                final_link = r.message;
            }
        })

        frm.add_custom_button(__('Go To Task'), function(){
            window.open(final_link);
        }).addClass("btn-primary");
	 }
});
