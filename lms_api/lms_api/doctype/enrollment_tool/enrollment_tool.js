// Copyright (c) 2020, Wela School System and contributors
// For license information, please see license.txt

frappe.ui.form.on('Enrollment Tool', {
    refresh: function(frm) {
        frappe.call({
            method:"get_programs",
            doc:frm.doc,
            freeze: true,
            freeze_message: "Collecting Programs",
            callback: function(r) {
                console.log(r)
                if (r.message) {
                    frm.set_df_property('program', 'options', r.message)
//                    frm.set_query("program", function(){
//                        return {
//                            filters: [
//                                ["name", "in", r.message],
//                            ]
//                        }
//                    })
                }
            }
        })
    },
	 program: function(frm) {
        frappe.call({
            method:"get_students",
            doc:frm.doc,
            callback: function(r) {
				if(r.message) {
					frm.set_value("students", r.message);
				}
			}
        })
	 },
	 add_students: function(frm) {
	    frappe.confirm(
            'Do you want to proceed?',
            function(){
                frappe.call({
                    method:"enroll_students",
                    doc:frm.doc,
                    freeze:true,
                    freeze_message:"Crunching Data",
                    async: false,
                    callback: function(r) {
                        if(r.message) {
                            let newStudentsList = []
                            frm.doc.students.forEach(function(item) {
                                let params = {
                                    student: item.student,
                                    student_name: item.student_name
                                }
                                newStudentsList.push(params)

                            })
                            let newArray = [...newStudentsList,...r.message].filter((v,i,a)=>a.findIndex(t=>(t.student === v.student))===i)
                            frm.set_value("students", newArray);
                            frm.set_value('select_student', '')
                            frm.set_value('school_year', '')
                            frm.doc.select_student = [];
                            frm.doc.select_student.length = 0;
                            frm.refresh_field("select_student");
                        }
                    }
                })
                window.close();
            },
            function(){
                show_alert('Cancelled')
            }
        )

	 }
});
