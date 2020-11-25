// Copyright (c) 2020, Wela School System and contributors
// For license information, please see license.txt
let topic_filters = function(frm) {
    frm.set_query("topic", function() {
        return {
            filters: []
        }
    });

    if(frm.doc.program && frm.doc.course === undefined) {
        frm.set_query("topic", function() {
            return {
                filters: [
                    ["program", "like", frm.doc.program],
                ]
            }
        });
        frm.doc.topic = undefined;
        frm.refresh_field("topic");
        frm.set_df_property("topic", "hidden", true);
    }
    if(frm.doc.program  === undefined && frm.doc.course) {
        frm.set_query("topic", function() {
            return {
                filters: [
                    ["subject", "like", frm.doc.course]
                ]
            }
        });
        frm.doc.topic = undefined;
        frm.refresh_field("topic");
        frm.set_df_property("topic", "hidden", true);
    }
    if(frm.doc.program && frm.doc.course) {
        frm.set_query("topic", function() {
            return {
                filters: [
                    ["program", "like", frm.doc.program],
                    ["subject", "like", frm.doc.course]
                ]
            }
        });
        frm.doc.topic = undefined;
        frm.refresh_field("topic");
        frm.set_df_property("topic", "hidden", false);
    }
 }
frappe.ui.form.on('Content Silid', {
    refresh: function(frm) {
        if (frm.doc.program === undefined && frm.doc.course === undefined) {
            frm.set_df_property("topic", "hidden", true);
        }
        frm.clear_custom_buttons();
        frm.add_custom_button(__('Add Grade'), function(){
            let d = new frappe.ui.Dialog({
                title: 'Add Student Grade',
                fields: [
                    {
                        label: 'Student',
                        fieldname: 'student',
                        fieldtype: 'Link',
                        options: 'Student',
                        reqd: 1
                    },
                    {
                        label: "Grade",
                        fieldname: "grade",
                        fieldtype: "Float",
                        reqd: 1,

                    }
                ],
                primary_action_label: 'Save',
                primary_action(values) {
                    if (values.grade > frm.doc.highest_possible_score) {
                        frappe.throw(`Grade must be lesser than or equal to ${frm.doc.highest_possible_score} (Highest Possible Score)`)
                    } else {
                        frappe.call({
                            method:"lms_api.lms_api.doctype.content_silid.content_silid.make_grade",
                            args: {
                                student:values.student,
                                grade: values.grade,
                                doc:frm.doc
                            },
                            callback: function(r) {
//                                window.location.reload();
                            }
                        })
                    }
                    d.hide();
                }
            });
            d.show();


        }).addClass("btn-primary");
        frm.add_custom_button(__('Move to another Folder/Topic'), function(){
            let d = new frappe.ui.Dialog({
                title: 'Move to another Topic',
                fields: [
                    {
                        label: 'New Program',
                        fieldname: 'program',
                        fieldtype: 'Link',
                        options: 'Program',
                        default: frm.doc.program,
                        reqd: 1
                    },
                    {
                        label: 'New Subject',
                        fieldname: 'course',
                        fieldtype: 'Link',
                        options: 'Course',
                        default: frm.doc.course,
                        reqd: 1
                    },
                    {
                        label: 'New Topc',
                        fieldname: 'topic',
                        fieldtype: 'Link',
                        options: 'Topic',
                        default: frm.doc.topic,
                        reqd: 1
                    }
                ],
                primary_action_label: 'Save',
                primary_action(values) {
                    console.log(values);
                    frappe.call({
                        method:"lms_api.lms_api.doctype.content_silid.content_silid.move_topic",
                        args: {
                            old_topic:frm.doc.topic,
                            new_topic: values.topic,
                            new_program: values.program || frm.doc.program,
                            new_subject: values.course || frm.doc.course,
                            is_video: frm.doc.is_video,
                            content_title: frm.doc.title,
                            content_name: frm.doc.name
                        },
                        callback: function(r) {
                            window.location.reload();
                        }
                    })
                    d.hide();
                }
            });
            d.show();


        }).addClass("btn-primary");
        frm.add_custom_button(__("Send Text"), function (frm) {
            var d = new frappe.ui.Dialog({
                'fields': [
                    {'fieldname': 'text', 'fieldtype': 'Data', 'label':'Put your message here. 160 characters per text.','length':160}
                ],
                primary_action: function(){
                    d.hide();
                    console.log(d.get_values());
                     frappe.call({
                            method: "lms_api.silid.notifications.custom_text",
                            args: {
                                "msg":d.get_values().text,
                                "program":cur_frm.doc.program
                            },
                            callback: function (r, rt) {
                                console.log(r);
                                msgprint("Message sent!");
                            }
                     });
                }
            });
            d.show();

        });
        frm.add_custom_button(__('Go To Content'), function(){
            let x = frappe.msgprint("Opening content...");
            frappe.call({
                method:"lms_api.lms_api.doctype.content_silid.content_silid.get_content_name",
                args: {
                    topic_content: frm.doc.topic_content
                },
                async:false,
                callback: function(res){
                    x.hide();
                    if (frm.doc.is_video) {
                        window.open(`/lms/content?program=${frm.doc.program}&course=${frm.doc.course}&topic=${frm.doc.topic}&type=Video&content=${res.message}`);
                    } else {
                        window.open(`/lms/content?program=${frm.doc.program}&course=${frm.doc.course}&topic=${frm.doc.topic}&type=Article&content=${res.message}`);
                    }
                }
            })

        });
        frm.add_custom_button(__('Preview Content'), function(){
            let x = frappe.msgprint("Opening content...");
            frappe.call({
                method:"lms_api.lms_api.doctype.content_silid.content_silid.get_content_name",
                args: {
                    topic_content: frm.doc.topic_content
                },
                async:false,
                callback: function(res){
                    x.hide();
                    if (frm.doc.is_video) {
                        window.open(`/lms/preview?program=${frm.doc.program}&course=${frm.doc.course}&topic=${frm.doc.topic}&type=Video&content=${res.message}`);
                    } else {
                        window.open(`/lms/preview?program=${frm.doc.program}&course=${frm.doc.course}&topic=${frm.doc.topic}&type=Article&content=${res.message}`);
                    }
                }
            })
        })

    },
    onload: function(frm) {
        if (frm.doc.program === undefined && frm.doc.course === undefined) {
            frm.set_df_property("topic", "hidden", true);
        }
        if(frm.doc.is_video) {
            frm.set_df_property("provider", "hidden", false);
            frm.set_df_property("url", "hidden", false);
        } else {
            frm.set_df_property("provider", "hidden", true);
            frm.set_df_property("url", "hidden", true);
        }
    },
    program: function(frm){
        topic_filters(frm);
     },
     course: function(frm){
        topic_filters(frm);
     },
    is_video: function(frm){
        if(frm.doc.is_video) {
            frm.set_df_property("provider", "hidden", false);
            frm.set_df_property("url", "hidden", false);
        } else {
            frm.set_df_property("provider", "hidden", true);
            frm.set_df_property("url", "hidden", true);
        }
    },
//    program: function(frm) {
//      frappe.call({
//          method: "lms_api.lms_api.doctype.content_silid.content_silid.get_topics",
//          args: {'program': frm.doc.program},
//          callback: function(r){
//              let optionList = [];
//              r.message.forEach(function (arrayItem) {
//                    optionList.push(arrayItem.name);
//                });
//              frm.set_df_property("topic", "options", optionList );
//          }
//      })
//    }
})