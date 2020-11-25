


frappe.ui.form.on('Quiz Activity', {

	refresh(frm) {
		// your code here
		if (frm.doc.student_name === "" || frm.doc.student_name ===undefined)
		{
		 frappe.call({
                    "method": "frappe.client.get",
                    args: {
                        doctype: "Student",
                        name: frm.doc.student
                    },
                    callback: function (data) {
                        cur_frm.set_value("student_name",data.message.first_name + " "+data.message.last_name);
                        frm.save();
            }
            });
		}
	},
onload: function(frm){

	if (frappe.user.has_role('Student')) { // if student
			//view grades

			if(cur_frm.doc.program)
			{
				var hide_answers = 0;
				var exclude_ = ['grade 7','grade 8','grade 9','grade 10','grade 11','grade 12']
				for (var i =0;i<exclude_.length;i++)
				{

					var lower_ = cur_frm.doc.program.toLowerCase();
					if(lower_.includes(exclude_[i]))
					{
						hide_answers =1;
						break;
					}
				}

				cur_frm.set_df_property("result", "hidden", hide_answers);

			}

	}
}


});