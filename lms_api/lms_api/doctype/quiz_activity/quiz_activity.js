// Copyright (c) 2020, Wela School System and contributors
// For license information, please see license.txt
let titleCase = function(str) {
  str = str.toLowerCase();
  str = str.split(' ');
  for (var i = 0; i < str.length; i++) {
    str[i] = str[i].charAt(0).toUpperCase() + str[i].slice(1);
  }
  return str.join(' ');
}
let max_points = 0;
let passing_average = 0;
frappe.ui.form.on('Quiz Activity', {
    onload: function(frm) {
        frappe.call({
             method: "lms_api.lms_api.doctype.quiz_activity.quiz_activity.get_quiz",
             args: {
                 name: frm.doc.quiz,
             },
             async:false,
             callback(r) {
                 if(r.message) {
                     let quiz_info = r.message;
                     let content_silid = quiz_info.content_silid;
                     frappe.call({
                        method:"lms_api.lms_api.doctype.quiz_activity.quiz_activity.get_quiz_silid",
                        args: {
                            doctype:"Quiz Silid",
                            name: content_silid
                        },
                        async:false,
                        callback:function(resp) {
                            if (resp.message) {
                                let quiz_silid_info = resp.message;
                                let questionsArray = quiz_silid_info;
                                $.each(frm.doc.result, function(idx,row) {
                                    row.question_description = questionsArray[idx].question
                                    row.points_per_item = row.points_per_item || questionsArray[idx].question_points
                                    row.question_type = questionsArray[idx].question_type

                                })
                            }
                        }
                     })

                     cur_frm.set_value("highest_possible_score",quiz_info.max_points);
                    frm.refresh_field("highest_possible_score");
                 }
             }
        });
        if (!frappe.user.has_role("Student") || frappe.session.user == "Administrator"){
            cur_frm.get_field("recalculate_score").$input.css({"width":"150px","font-size":"15px", "font-weight":"bolder"});
            cur_frm.get_field("recalculate_score").$input.addClass("btn-primary");
            if (frappe.user.has_role("Student")  && frappe.session.user != "Administrator"){
                cur_frm.set_df_property("recalculate_score", "hidden", 1);
//                for(let i=0; i<frm.doc.result.length;i++){
//                    let child = frm.doc.result[i];
//                    frappe.meta.get_docfield(child.doctype,"answer", cur_frm.doc.name).hidden = 1;
//                }
//                frm.refresh_field("result");
            }

        }

        let is_partial = false;
	    $.each(frm.doc.result, function(idx,row) {
            if(row.result_silid === "") {
                is_partial = true;
            }
	    });
	    if (!frm.doc.is_result_ready) {
            setTimeout(function(){
	            $(".primary-action").prop("disabled", true);
	        }, 1000)
            $(document).bind('keydown', 'ctrl+s', function(e) {
                e.preventDefault();
                return false;
            });

            for(let i=0; i<frm.doc.result.length;i++){
                let child = frm.doc.result[i];
                frappe.meta.get_docfield(child.doctype,"result_silid", cur_frm.doc.name).read_only = 1;
                frappe.meta.get_docfield(child.doctype,"points_per_item", cur_frm.doc.name).read_only = 1;
            }
            frm.refresh_field("result");
	    } else {
	        frm.toggle_display("is_result_ready_status", false);
            frm.refresh_field("is_result_ready_status");
            for(let i=0; i<frm.doc.result.length;i++){
                let child = frm.doc.result[i];
                frappe.meta.get_docfield(child.doctype,"result_silid", cur_frm.doc.name).read_only = 0;
                frappe.meta.get_docfield(child.doctype,"points_per_item", cur_frm.doc.name).read_only = 0;
            }
            frm.refresh_field("result");
	    }
	    if (is_partial) {
            $(frm.fields_dict.quiz_result_status.wrapper).html('<h1 style="color:blue">This Quiz Result is PARTIAL and to be rechecked by the teacher</h1>')
            cur_frm.set_value("status","Initial");
            frm.toggle_display("quiz_result_status", true);
            frm.refresh_field("quiz_result_status");
            frm.refresh_field("status");
	    } else {
	        frm.toggle_display("quiz_result_status", false);
	        frm.refresh_field("quiz_result_status");
	    }


	    if (cur_frm.doc.result.length==0)
        {
            $(frm.fields_dict.quiz_result_status.wrapper).html('<h1 style="color:blue">This Quiz Result is PARTIAL and to be rechecked by the teacher</h1>')
             frm.toggle_display("quiz_result_status", true);
            frm.refresh_field("quiz_result_status");
        }

	    frm.doc.status = "";
	    frm.refresh_field("status");
	    if (!frm.doc.is_result_ready) {
            setTimeout(function(){
	            $(".primary-action").prop("disabled", true);
	        }, 1000)
            $(frm.fields_dict.is_result_ready_status.wrapper).html('<h3 style="color:blue">The answers below are preview only. The system is evaluating the quiz, try again after 5 minutes.</h3>')
            frm.toggle_display("is_result_ready_status", true);
            frm.refresh_field("is_result_ready_status");

        }
    },
	refresh: function(frm) {
	    if (!frm.doc.is_result_ready) {
	        $(document).bind('keydown', 'ctrl+s', function(e) {
                e.preventDefault();
                return false;
            });
            setTimeout(function(){
	            $(".primary-action").prop("disabled", true);

	        }, 1000)
            $(frm.fields_dict.is_result_ready_status.wrapper).html('<h3 style="color:blue">The answers below are preview only. The system is evaluating the quiz, try again after 5 minutes.</h3>')
            frm.toggle_display("is_result_ready_status", true);
            frm.refresh_field("is_result_ready_status");


        }

        cur_frm.get_field("recalculate_score").$input.css({"width":"150px","font-size":"15px", "font-weight":"bolder"});
        cur_frm.get_field("recalculate_score").$input.addClass("btn-primary");
        if (frappe.user.has_role("Student")   && frappe.session.user != "Administrator"){
            cur_frm.set_df_property("recalculate_score", "hidden", 1);
            frappe.call({
                    "method": "frappe.client.get",
                    args: {
                        doctype: "Wela Settings"
                    },
                    callback: function (data) {
                        let message = data.message
                        const dateToday = new Date()
                        const activityDate = new Date(frm.doc.activity_date)
                        if (message.days_to_hide_quiz_answers) {
                            let unixDate = activityDate.setDate(activityDate.getDate() + message.days_to_hide_quiz_answers)
                            if (new Date(unixDate) > dateToday) {
                                for(let i=0; i<frm.doc.result.length;i++){
                                    let child = frm.doc.result[i];
                                    frappe.meta.get_docfield(child.doctype,"answer", cur_frm.doc.name).hidden = 1;
                                }
                                frm.refresh_field("result");
                            }
                        }
                    }
            });

        }
	    frm.doc.status = "";
	    frm.refresh_field("status");
	    let is_partial = false;
	    $.each(frm.doc.result, function(idx,row) {
            if(row.result_silid === "") {
                is_partial = true;
            }
	    });
	    if (!frm.doc.is_result_ready) {
	        setTimeout(function(){
	            $(".primary-action").prop("disabled", true);
	        }, 1000)
	        $(frm.fields_dict.is_result_ready_status.wrapper).html('<h3 style="color:blue">The answers below are preview only. The system is evaluating the quiz, try again after 5 minutes.</h3>')
            frm.toggle_display("is_result_ready_status", true);
            frm.refresh_field("is_result_ready_status");

            for(let i=0; i<frm.doc.result.length;i++){
                let child = frm.doc.result[i];
                frappe.meta.get_docfield(child.doctype,"result_silid", cur_frm.doc.name).read_only = 1;
                frappe.meta.get_docfield(child.doctype,"points_per_item", cur_frm.doc.name).read_only = 1;
            }
            frm.refresh_field("result");
	    } else {
	        frm.toggle_display("is_result_ready_status", false);
            frm.refresh_field("is_result_ready_status");
            for(let i=0; i<frm.doc.result.length;i++){
                let child = frm.doc.result[i];
                frappe.meta.get_docfield(child.doctype,"result_silid", cur_frm.doc.name).read_only = 0;
                frappe.meta.get_docfield(child.doctype,"points_per_item", cur_frm.doc.name).read_only = 0;
            }
            frm.refresh_field("result");
	    }
	    if (is_partial) {
            $(frm.fields_dict.quiz_result_status.wrapper).html('<h1 style="color:blue">This Quiz Result is PARTIAL and to be rechecked by the teacher</h1>');
            cur_frm.set_value("status","Initial");
            frm.toggle_display("quiz_result_status", true);
            frm.refresh_field("quiz_result_status");
            frm.refresh_field("status");
	    } else {
	        frm.toggle_display("quiz_result_status", false);
	        frm.refresh_field("quiz_result_status");

	    }


	      if (cur_frm.doc.result.length==0)
        {
            $(frm.fields_dict.quiz_result_status.wrapper).html('<h1 style="color:blue">This Quiz Result is PARTIAL and to be rechecked by the teacher</h1>')
             frm.toggle_display("quiz_result_status", true);
            frm.refresh_field("quiz_result_status");
        }

		if (frm.doc.student_name == "" || frm.doc.student_name ==undefined)
		{
		 frappe.call({
                    "method": "frappe.client.get",
                    args: {
                        doctype: "Student",
                        name: frm.doc.student
                    },
                    callback: function (data) {
                        let first_name = data.message.first_name === null ? '' : data.message.first_name;
                        let last_name = data.message.last_name === null ? '' : data.message.last_name;
                        let final_name = first_name+" "+last_name;
                        final_name = titleCase(final_name);
                        cur_frm.set_value("student_name",final_name);
                        frm.save();
            }
            });
		}

	},
	recalculate_score: function(frm) {
	    let score = 0
	    $.each(frm.doc.result, function(idx,row) {
            if(row.question_type=="Enumeration") {
                // Count how many items
                let evaluation_split = []
                try{
                    evaluation_split = row.evaluation_result.split(",")
                } catch(e){
                    if (row.result_silid === "Correct") {
                        let answer_split = row.answer.split(",")
                        $.each(answer_split, function(idx,answer) {
                            score += parseFloat(row.points_per_item);
                        })
                    }
                }

                $.each(evaluation_split, function(ide,evaluation) {
                    if (evaluation.replace(/\s/g, '') === "Correct") {
                        if (row.points_per_item) {
                            score += parseFloat(row.points_per_item);
                        }
                    }
                })

            }
            else if (row.question_type == "Matching Type") {
                // Count how many items
                let evaluation_split = []
                try{
                    evaluation_split = row.evaluation_result.split(",")
                } catch(e){
                    if (row.result_silid === "Correct") {
                        let answer_split = row.answer.split(",")
                        $.each(answer_split, function(idx,answer) {
                            score += parseFloat(row.points_per_item);
                        })
                    }
                }
                $.each(evaluation_split, function(ide,evaluation) {
                    if (evaluation.replace(/\s/g, '') === "Correct") {
                        if (row.points_per_item) {
                            score += parseFloat(row.points_per_item);
                        }

                    }
                })
            }
            else{
                if (row.result_silid === "Correct") {
                    if (row.points_per_item) {
                        score += parseFloat(row.points_per_item);
                    }

                }
            }

	    });
	    frm.doc.score = score;
         frm.refresh_field("score");
	}

});
