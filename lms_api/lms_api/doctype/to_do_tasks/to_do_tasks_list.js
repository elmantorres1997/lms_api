/**
 * Created by jvfiel on 11/6/16.
 */
frappe.listview_settings['To Do Tasks'] = {
    get_indicator: function(doc) {
        if(doc.status==="Done"){
            //console.log(doc.status);
			return [__("Done"), "green", "status,=,Done"];
		}
		else if(doc.status==="To Do"){
            //console.log(doc.status);
			return [__("To Do"), "orange", "status,=,To Do"];
		}
    }
    ,onload:function(listview){
        listview.filter_area.filter_list.clear_filters();
        $("input.input-with-feedback.form-control.input-sm").val("")
        if (frappe.user.has_role('Student') == true && frappe.user.name != 'Administrator') {
                $("div.filter-list").hide()
                $("ul.list-group-by").hide()
                // $("ul.sidebar-stat").hide()
                // $("li.list-link").hide()
                // $("li.list-link").hide()
        }
        frappe.call({
            method: "lms_api.lms_api.doctype.to_do_tasks.to_do_tasks.get_subject_filters",
            async:true,
            callback: function(r){
                r.message.forEach(function (item, index) {
                  listview.page.add_sidebar_item(__(item.course), function () {
                        var assign_filter = listview.filter_area.filter_list.get_filter("course");
                        assign_filter && assign_filter.remove(true);
                        listview.filter_area.filter_list.add_filter(listview.doctype, "course", '=', item.course);
                         listview.refresh();
                    });
                });

            }
        })
    }
    // , refresh: function(me) {
    //     console.log("REFRESHED.");
    //     console.log(me.filter_list);
    //     console.log(me.page);
	// 	me.page.add_sidebar_item(__("Overdue"), function() {
	// 		var assign_filter = me.filter_list.get_filter("status");
	// 		assign_filter && assign_filter.remove(true);
    //
	// 		me.filter_list.add_filter(me.doctype, "status", '=', "Overdue");
	// 		me.run();
	// 	});
    //     me.page.add_sidebar_item(__("Borrowed"), function() {
	// 		var assign_filter = me.filter_list.get_filter("status");
	// 		assign_filter && assign_filter.remove(true);
    //
	// 		me.filter_list.add_filter(me.doctype, "status", '=', "Borrowed");
	// 		me.run();
	// 	});
    //     me.page.add_sidebar_item(__("Returned"), function() {
	// 		var assign_filter = me.filter_list.get_filter("status");
	// 		assign_filter && assign_filter.remove(true);
    //
	// 		me.filter_list.add_filter(me.doctype, "status", '=', "Returned");
	// 		me.run();
	// 	});
	// }
};