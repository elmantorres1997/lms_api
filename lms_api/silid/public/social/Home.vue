<template>
	<div ref="social" class="social">
	    <img v-if="banner" :src="banner" style="width:100%;height:auto"></img>
        <div class="hidden-lg hidden-sm hidden-md">
            <br>
	        <button @click="post" class="btn btn-primary btn-sm primary-action btn-block">Post</button>
	    </div>
		<keep-alive>
			 <component :is="current_page.component" v-bind="current_page.props"></component>
		</keep-alive>
		<image-viewer :src="preview_image_src" v-if="show_preview"></image-viewer>
	</div>
</template>

<script>

import Wall from './pages/Wall.vue';
import Profile from './pages/Profile.vue';
import UserList from './pages/UserList.vue';
import NotFound from './components/NotFound.vue';
import ImageViewer from './components/ImageViewer.vue';

function get_route_map() {
	return {
		'social/home': {
			'component': Wall,
			'props': {}
		},
		'social/profile/*': {
			'component': Profile,
			'props': {
				'user_id': frappe.get_route()[2],
				'key': frappe.get_route()[2]
			}
		},
		'social/users': {
			'component': UserList,
			'props': {}
		},
		'not_found': {
			'component': NotFound,
		}
	}
}
let student_courses = [];
let get_student_courses = frappe.call({
    method: "frappe.social.doctype.post.post.get_student_courses",
    async: false,
    callback: function(r){
        if (r.message !== undefined) {
            let courses = r.message;
            courses.forEach(function (course){
                student_courses.push(course['course'])
            });
            student_courses.unshift("All");

        }
    }
})
get_student_courses
 let poster = new frappe.ui.Dialog({
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
            poster.disable_primary_action();
            const post = frappe.model.get_new_doc('Post');
            post.content = values.content;
            post.course = values.course;
            frappe.db.insert(post).then((data) => {

                frappe.call({
                    method: "frappe.custom.social_post.add_post",
                    args: { data: data }
                });
                poster.clear();
                poster.hide();
            }).finally(() => {
                poster.enable_primary_action();
            });
		} else {
		    poster.disable_primary_action();
		    student_courses.forEach(function (course){
		        if (course !== "All"){
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
		        }
            });
            poster.clear();
            poster.hide();
            poster.enable_primary_action();
		}
    }
});
export default {
	components: {
		ImageViewer
	},
	data() {
		return {
			current_page: this.get_current_page(),
			show_preview: false,
			preview_image_src: '',
			banner: "",
			wela_settings_obj:[]
		}
	},
	created() {
		this.$root.$on('show_preview', (src) => {
			this.preview_image_src = src;
			this.show_preview = true;
		})

		this.$root.$on('hide_preview', () => {
			this.preview_image_src = '';
			this.show_preview = false;
		})
        $('.page-head').hide();
        $('.page-content').css("margin-top","0px");
		this.update_primary_action(frappe.get_route()[1])
	},
	mounted() {
		frappe.route.on('change', () => {
			if (frappe.get_route()[0] === 'social') {
				this.set_current_page();
				this.update_primary_action(frappe.get_route()[1])
				frappe.utils.scroll_to(0);
				$("body").attr("data-route", frappe.get_route_str());
			}
		});
		frappe.ui.setup_like_popover($(this.$refs.social), '.likes', false);
		frappe.xcall('frappe.social.doctype.custom.wela_settings.get_wela_settings').then(r => {
		    this.wela_settings_obj = r;
		    this.init_banner()
		})
	},
	methods: {
		set_current_page() {
			this.current_page = this.get_current_page();
		},
		init_banner() {
		    let obj = this.wela_settings_obj.find(o => o.field === 'banner');
	        this.banner = obj.value || "";
		},
		post() {
            poster.show();
	    },
		update_primary_action(current_route) {
			if (current_route === 'home') {
				this.$root.page.set_title(__('Social'));
				frappe.breadcrumbs.update();
				this.$root.page.set_primary_action(__('Post'), () => {
					frappe.social.post_dialog.show();
				});
			} else {
				frappe.breadcrumbs.add({
					type: 'Custom',
					label: __('Social Home'),
					route: '#social/home'
				});
				this.$root.page.clear_primary_action();
			}

			if (current_route === 'users') {
				this.$root.page.set_title(__('Leaderboard'));
			}
		},
		get_current_page() {
			const route_map = get_route_map();
			const route = frappe.get_route_str();
			if (route_map[route]) {
				return route_map[route];
			} else {
				return route_map[route.substring(0, route.lastIndexOf('/')) + '/*'] || route_map['not_found']
			}
		},
	}
}
</script>
