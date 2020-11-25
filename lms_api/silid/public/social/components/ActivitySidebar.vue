<template>
	<div>
	    <button @click="post" class="btn btn-primary btn-sm primary-action btn-block">Post</button>
	    <br><br>
		<div class="muted-title">{{ __('Upcoming Events') }}</div>
		<div class="event" v-for="event in events" :key="event.name">
			<span class="bold">{{ get_time(event.starts_on) }}</span>
			<a @click="open_event(event)"> {{ event.subject }}</a>
		</div>
		<div class="event" v-if="!events.length">
			{{ __('No Upcoming Events') }}
		</div>
		<div class="muted-title">{{ __('Chat') }}</div>
		<a @click="open_chat">
			{{ __('Open Chat') }}
		</a>
		<br><br>
		<div class="about container-fluid" v-if="about" v-html="about"></div>

	</div>
</template>
<script>
let student_courses = [];
let get_student_courses = frappe.call({
    method: "frappe.social.doctype.post.post.get_student_courses",
    async: false,
    callback: function(r){
        if (r.message !== undefined) {
            console.log(r.message);
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
	data() {
		return {
			'events': [],
			wela_settings_obj: [],
			about:"",
		}
	},
	mounted() {
	    frappe.xcall('frappe.social.doctype.custom.wela_settings.get_wela_settings').then(r => {
		    this.wela_settings_obj = r;
		    this.init_about()
		})
	},
	created() {
		this.get_events().then((events) => {
			this.events = events
		})
	},
	methods: {
	    init_about() {
	        let obj = this.wela_settings_obj.find(o => o.field === 'about');
	        this.about = obj.value;
	    },
	    post() {
            poster.show();
	    },
		get_events() {
			const today = frappe.datetime.now_date();
			return frappe.xcall('frappe.desk.doctype.event.event.get_events', {
				start: today,
				end: today
			})
		},
		open_chat() {
			setTimeout(frappe.chat.widget.toggle);
		},
		get_time(timestamp) {
			return frappe.datetime.get_time(timestamp)
		},
		open_event(event) {
			frappe.set_route('Form', 'Event', event.name);
		}
	}
}
</script>
<style lang="less" scoped>
.about {
    background-color: #f6f6f6;
    padding:10px;
}
</style>