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
frappe.ui.form.on('Quiz Silid', {
     refresh: function(frm) {
        if (frm.doc.program === undefined && frm.doc.course === undefined) {
            frm.set_df_property("topic", "hidden", true);
        }

         if(!cur_frm.doc.name.includes("Quiz Silid"))
         {
             cur_frm.toggle_enable("deadline", 0);
             cur_frm.toggle_enable("publish_date", 0);
         }




        frm.clear_custom_buttons();

        frm.add_custom_button(__('Apply Quiz in Silid'), async function(){

            // console.log("hello world");
            cur_frm.doc.in_silid = "1";
            await cur_frm.save();
            frappe.call({
                    method:"lms_api.lms_api.doctype.quiz_silid.apply_quiz",
                    args: {
                        docname:cur_frm.doc.name
                    },
                    freeze:true,
                    freeze_message:"Applying changes...",
                    callback: function(r) {

                        // msgprint(__("Done applying changes in your Silid."));

                        var d = new frappe.ui.Dialog({
                            'fields': [
                                {'fieldname': 'ht', 'fieldtype': 'HTML'}
                            ]
                        });
                        d.fields_dict.ht.$wrapper.html('Done applying changes in your Silid.');
                        d.show();


                           $(frm.fields_dict.quiz_status.wrapper).html('<h16 style="color:orange"></h16>')

                                cur_frm.toggle_display("quiz_status", true);
                            cur_frm.refresh_field("quiz_status");

                    }
                })



        }).addClass("btn-success");


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
                            method:"lms_api.lms_api.doctype.quiz_silid.quiz_silid.make_grade",
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
                        method:"lms_api.lms_api.doctype.quiz_silid.quiz_silid.move_topic",
                        args: {
                            old_topic:frm.doc.topic,
                            new_topic: values.topic,
                            new_program: values.program || frm.doc.program,
                            new_subject: values.course || frm.doc.course,
                            content_title: frm.doc.quiz_title,
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
        frm.add_custom_button(__('Set New Publish Date and Deadline'), function(){
            let d = new frappe.ui.Dialog({
                title: 'Enter details',
                fields: [
                    {
                        label: "",
                        fieldname: "warn",
                        fieldtype: "HTML Editor",
                        default: "<b style='color:red'>Please double check your entries below before saving</b>",
                        read_only:1
                    },
                    {
                        label: 'New Deadline',
                        fieldname: 'deadline',
                        fieldtype: 'Datetime',
                        description: "<b style='color:red'>Input new deadline above</b>",
                        default: frm.doc.deadline
                    },
                    {
                        label: 'New Publish Date',
                        fieldname: 'publish_date',
                        fieldtype: 'Datetime',
                        description: "<b style='color:red'>Input new publish date above</b>",
                        default: frm.doc.publish_date
                    },
                    {
                        label: "Restart Recorded Time Limit",
                        fieldname: "delete_time_limit",
                        description: "This will restart the time limit for all students in this particular quiz",
                        fieldtype: "Check",
                        default: 0
                    }
                ],
                primary_action_label: 'Save',
                primary_action(values) {
                    frappe.call({
                        method:"lms_api.lms_api.doctype.quiz_silid.quiz_silid.update_publishdate_deadline",
                        args: {
                            docname:frm.doc.name,
                            publish_date: values.publish_date,
                            deadline: values.deadline,
                            delete_time_limit: values.delete_time_limit
                        },
                        async:false,
                        callback: function(r) {
                            window.location.reload();
                        }
                    })
                    d.hide();
                }
            });
            d.show();

        }).addClass("btn-primary");
        frm.add_custom_button(__('Reset Time Limit'), function(){
            let d = new frappe.ui.Dialog({
                title: 'Are you sure?',
                fields: [
                    {
                        label: "Reset Time limit",
                        fieldname: "warn",
                        fieldtype: "HTML Editor",
                        default: "<b style='color:red;font-size:20px;'>Are you sure you want to reset any recorded time limit?</b>",
                        read_only:1
                    }
                ],
                primary_action_label: 'Confirm',
                primary_action(values) {
                    frappe.call({
                        method:"lms_api.lms_api.doctype.quiz_silid.quiz_silid.remove_time_limit",
                        args: {
                            docname:frm.doc.name
                        },
                        async:false,
                        callback: function(r) {
                            frappe.msgprint("Time limit reset successful")
                        }
                    })
                    d.hide();
                }
            });
            d.show();

        }).addClass("btn-danger");


          if(cur_frm.doc.in_silid=="1") {


              frm.add_custom_button(__('Go To Quiz'), function(){
            let x = frappe.msgprint("Opening quiz...");
            frappe.call({
                method:"lms_api.lms_api.doctype.quiz_silid.quiz_silid.get_content_name",
                args: {
                    topic: frm.doc.topic,
                    title: frm.doc.quiz_title
                },
                async:false,
                callback: function(res){

                    if (res.message) {
                        x.hide();
                        window.open(`/lms/content?program=${frm.doc.program}&course=${frm.doc.course}&topic=${frm.doc.topic}&type=Quiz&content=${res.message}`);
                    } else {
                        frappe.msgprint("Cant find quiz. This was caused by manually editing Quiz List.")
                    }
                }
            })

        })
        frm.add_custom_button(__('Preview Quiz'), function(){
            let x = frappe.msgprint("Opening quiz...");
            frappe.call({
                method:"lms_api.lms_api.doctype.quiz_silid.quiz_silid.get_content_name",
                args: {
                    topic: frm.doc.topic,
                    title: frm.doc.quiz_title
                },
                async:false,
                callback: function(res){

                    if (res.message) {
                        x.hide();
                        window.open(`/lms/preview?program=${frm.doc.program}&course=${frm.doc.course}&topic=${frm.doc.topic}&type=Quiz&content=${res.message}`);
                    } else {
                        frappe.msgprint("Cant find quiz. This was caused by manually editing Quiz List.")
                    }
                }
            })

        })

         }


     },
     items_on_form_rendered:function (frm)
     {
       console.log("render()");


         // document.querySelectorAll('[data-fieldname="choice_1"]')[1].style.height='50px';
         // document.querySelectorAll('[data-fieldname="choice_2"]')[1].style.height='50px';
         // document.querySelectorAll('[data-fieldname="choice_3"]')[1].style.height='50px';
         // document.querySelectorAll('[data-fieldname="choice_4"]')[1].style.height='50px';
         // document.querySelectorAll('[data-fieldname="choice_5"]')[1].style.height='50px';
         // document.querySelectorAll('[data-fieldname="choice_6"]')[1].style.height='50px';


     },
     program: function(frm){
        topic_filters(frm);
     },
     course: function(frm){
        topic_filters(frm);
     },


     before_save: function(frm) {
        if (parseInt(frm.doc.max_attempts) > 1) {
            frm.doc.time_limit = 0;
            frm.refresh_field("time_limit");
        }

	    let total_points = [];
	    let no_q = 6;
	    let sum = 0;
        $.each(frm.doc.items, function(idx,q) {
           if (q.question_type === "Enumeration") {
                for (let i = 1; i < no_q+1; i++) {
                  if (q['enum_ans_'+i.toString()]) {
                    total_points.push(q.question_points ? q.question_points : 1)
                  }
                }
           }
           else if(q.question_type === "Matching Type") {
                for (let i = 1; i < no_q; i++) {
                    if (q['matching_left_' + i.toString()] && q['matching_right_' + i.toString()]) {
                        total_points.push(q.question_points ? q.question_points : 1)
                    }
                }
           } else {
                total_points.push(q.question_points ? q.question_points : 1)
           }
            sum = total_points.reduce(function(a, b){
                return parseFloat(a) + parseFloat(b);
            }, 0);

        });
        frm.doc.highest_possible_score = sum;
        frm.refresh_field("highest_possible_score");
	 },
    remind_edit_status:function (frm)
    {
       $(frm.fields_dict.quiz_status.wrapper).html('<h4 style="color:orange">You have edited this quiz. Dont forget to click "Apply Quiz in Silid" once you are finally done.</h4>')

        cur_frm.toggle_display("quiz_status", true);
       cur_frm.refresh_field("quiz_status");

       cur_frm.doc.in_silid = "";
       cur_frm.refresh_field("in_silid");


    },

     onload: function(frm) {
        if (frm.doc.program === undefined && frm.doc.course === undefined) {
            frm.set_df_property("topic", "hidden", true);
        }

         if(cur_frm.doc.in_silid=="1") {


             $(frm.fields_dict.quiz_status.wrapper).html('<h16 style="color:blue"></h16>')

         }
         else
         {



               $(frm.fields_dict.quiz_status.wrapper).html('<h4 style="color:orange">You have edited this quiz. Dont forget to click "Apply Quiz in Silid" once you are finally done.</h4>')
             console.log("not in silid...");


         }
        cur_frm.toggle_display("quiz_status", true);
               cur_frm.refresh_field("quiz_status");




        cur_frm.toolbar.show_title_as_dirty = function() {
            if(this.frm.save_disabled)
                return;

            if(this.frm.doc.__unsaved) {
                this.page.set_indicator(__("Not Saved"), "orange");
                 this.frm.trigger("remind_edit_status");

            }
            else{
                // $(frm.fields_dict.quiz_status.wrapper).html('<h16 style="color:orange"></h16>')
                //     cur_frm.toggle_display("quiz_status", true);
                //    cur_frm.refresh_field("quiz_status");
            }

            $(this.frm.wrapper).attr("data-state", this.frm.doc.__unsaved ? "dirty" : "clean");

	    }


        let total_points = [];
	    let no_q = 6;
	    let sum = 0;
        $.each(frm.doc.items, function(idx,q) {
           if (q.question_type === "Enumeration") {
                for (let i = 1; i < no_q+1; i++) {
                  if (q['enum_ans_'+i.toString()]) {
                    total_points.push(q.question_points ? q.question_points : 1)
                  }
                }
           }
           else if(q.question_type === "Matching Type") {
                for (let i = 1; i < no_q; i++) {
                    if (q['matching_left_' + i.toString()] && q['matching_right_' + i.toString()]) {
                        total_points.push(q.question_points ? q.question_points : 1)
                    }
                }
           } else {
                total_points.push(q.question_points ? q.question_points : 1)
           }
            sum = total_points.reduce(function(a, b){
                return parseFloat(a) + parseFloat(b);
            }, 0);

        });
        frm.doc.highest_possible_score = sum;
        frm.refresh_field("highest_possible_score");
     }

});
