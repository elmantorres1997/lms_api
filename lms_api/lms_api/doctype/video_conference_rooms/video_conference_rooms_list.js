frappe.listview_settings['Video Conference Rooms'] = {
    onload: function(listview) {
        // console.log(listview)
        // console.log(listview.filter_area.filter_list)
        // console.log("helo")
        if(listview.filter_area.filter_list){
            listview.filter_area.filter_list.clear_filters();
        }

        $("div.page-form.flex").hide()
        $("div.filter-list").hide()
        $("input.input-with-feedback.form-control.input-sm").val("")
    }
}

