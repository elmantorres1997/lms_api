frappe.listview_settings['Written Activity'] = {
    onload:function(listview){
        listview.filter_area.filter_list.clear_filters();
        $("input.input-with-feedback.form-control.input-sm").val("")
        if (frappe.user.has_role('Student') == true && frappe.user.name != 'Administrator') {
                $("div.filter-list").hide()
                $("ul.list-group-by").hide()
                $("ul.sidebar-stat").hide()
                $("li.list-link").hide()
                $("li.list-link").hide()
        }
        if (frappe.user.has_role('Student') == true) {
            frappe.call({
                method: "lms_api.lms_api.doctype.written_activity.written_activity.get_subject_filters",
                async:true,
                callback: function(r){
                    console.log(r)
                    r.message.forEach(function (item, index) {
                      listview.page.add_sidebar_item(__(item.subject), function () {
                            var assign_filter = listview.filter_area.filter_list.get_filter("subject");
                            assign_filter && assign_filter.remove(true);
                            listview.filter_area.filter_list.add_filter(listview.doctype, "subject", '=', item.subject);
                             listview.refresh();
                        });
                    });

                }
            })
        }
        if (frappe.user.has_role('Instructor') == true) {
            frappe.call({
                method: "lms_api.lms_api.doctype.written_activity.written_activity.get_subject_filters_teacher",
                async:true,
                callback: function(r){
                    console.log(r)
                    r.message.forEach(function (item, index) {
                      listview.page.add_sidebar_item(__(item.subject), function () {
                            var assign_filter = listview.filter_area.filter_list.get_filter("subject");
                            assign_filter && assign_filter.remove(true);
                            listview.filter_area.filter_list.add_filter(listview.doctype, "subject", '=', item.subject);
                             listview.refresh();
                        });
                    });

                }
            })
        }

    }

}