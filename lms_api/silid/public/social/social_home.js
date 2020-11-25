import Home from './Home.vue';
frappe.provide('frappe.social');

frappe.social.Home = class SocialHome {
	constructor({ parent }) {
		this.$parent = $(parent);
		this.page = parent.page;
		this.setup_header();
		this.make_body();
	}
	make_body() {
		this.$social_container = this.$parent.find('.layout-main');
		new Vue({
			el: this.$social_container[0],
			render: h => h(Home),
			data: {
				'page': this.page
			}
		});
	}
	setup_header() {
		this.page.set_title(__('Social'));
	}
};
let student_courses = [];
let get_student_courses = frappe.call({
    method: "frappe.social.doctype.post.post.get_student_courses",
    async: false,
    callback: function(r){
        if (r.message !== undefined) {
            let courses = r.message;
            try {

                courses.forEach(function (course){
                    student_courses.push(course['course'])
                });
                student_courses.unshift("All");
            } catch(e) {
                frappe.set_route("/")
            }

        }
    }
})
get_student_courses

frappe.social.post_dialog = new frappe.ui.Dialog({
	title: __('Create Post'),
	fields: [
	    {
		    fieldtype: "Select",
		    fieldname: "course",
		    label: __("Course"),
		    options: student_courses,
		    hidden: frappe.session.user === 'Administrator',
		    reqd: frappe.session.user !== 'Administrator'
		},
		{
			fieldtype: "Text Editor",
			fieldname: "content",
			label: __("Content"),
			reqd: 1
		}

	],
	primary_action_label: __('Post'),
	primary_action: (values) => {
	    if (values.course !== "All"){
            frappe.social.post_dialog.disable_primary_action();
            const post = frappe.model.get_new_doc('Post');
            post.content = values.content;
            post.course = values.course;
            frappe.db.insert(post).then((data) => {

                frappe.call({
                    method: "frappe.custom.social_post.add_post",
                    args: { data: data }
                });
                frappe.social.post_dialog.clear();
                frappe.social.post_dialog.hide();
            }).finally(() => {
                frappe.social.post_dialog.enable_primary_action();
            });
		} else {
		    frappe.social.post_dialog.disable_primary_action();
		    student_courses.forEach(function (course){
                const post = frappe.model.get_new_doc('Post');
                post.content = values.content;
                post.course = course;
                frappe.db.insert(post).then((data) => {
                    frappe.call({
                        method: "frappe.custom.social_post.add_post",
                        async:false,
                        args: { data: data }
                    });
                }).finally(() => {});
            });
            frappe.social.post_dialog.clear();
            frappe.social.post_dialog.hide();
            frappe.social.post_dialog.enable_primary_action();
		}
	}
});

frappe.social.is_home_page = () => {
	return frappe.get_route()[0] === 'social' && frappe.get_route()[1] === 'home';
};

frappe.social.is_profile_page = (user) => {
	return frappe.get_route()[0] === 'social'
		&& frappe.get_route()[1] === 'profile'
		&& (user ? frappe.get_route()[2] === user : true);
};

frappe.social.is_session_user_page = () => {
	return frappe.social.is_profile_page() && frappe.get_route()[2] === frappe.session.user;
};

frappe.provide('frappe.app_updates');

frappe.utils.make_event_emitter(frappe.app_updates);
