// Copyright (c) 2020, Wela School System and contributors
// For license information, please see license.txt

frappe.ui.form.on('Written Activity', {
	 onload: function(frm) {
	    if (!frappe.user.has_role("Student") || frappe.session.user == "Administrator"){
            if (frm.doc.activity) {
                frappe.call({
                    method: "frappe.client.get",
                    args:{
                        doctype:"Article",
                        name: frm.doc.activity
                    },
                    async:false,
                    callback:function(r) {
                        let art_info = r.message;
                        if (parseInt(frm.doc.highest_possible_score) === 0) {
                            cur_frm.set_value("highest_possible_score",art_info.highest_possible_score);
                            frm.refresh_field("highest_possible_score");
                        }
                    }
                });
            }
            if (frm.doc.video) {
                frappe.call({
                    method: "frappe.client.get",
                    args:{
                        doctype:"Video",
                        name: frm.doc.video
                    },
                    async:false,
                    callback:function(r) {
                        let art_info = r.message;
                        if (parseInt(frm.doc.highest_possible_score) === 0) {
                            cur_frm.set_value("highest_possible_score",art_info.highest_possible_score);
                            frm.refresh_field("highest_possible_score");
                        }
                    }
                });
            }
	    }

	 },
	 refresh: function(frm) {
//	    if (!frappe.user.has_role("Student") || frappe.session.user == "Administrator"){
//	        frm.add_custom_button(__('Save to Master Grade'), function(){
//                // This will save the document to master grade immediately
//                frappe.call({
//                    method:"lms_api.lms_api.doctype.written_activity.written_activity.written_to_master_grade",
//                    args:{
//                        self: frm.doc
//                    },
//                    callback: function(r){
//                        console.log("Done");
//                    }
//                })
//            }).addClass("btn-primary");
//        }
	 }
});
