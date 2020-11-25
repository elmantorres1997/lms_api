frappe.listview_settings['Master Grade'] = {
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
        if (frappe.user.has_role("Instructor")== true) {
            frappe.call({
                method: "lms_api.lms_api.doctype.quiz_activity.quiz_activity.get_subject_filters_teacher",
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

    }
}