<template>
	<div>
		<div v-if="loading_posts && !posts.length">
			<post-skeleton v-for="index in 5" :key="index"/>
		</div>
		<transition-group name="flip-list">
			<post ref="posts"
				:post="post"
				v-for="(post, index) in posts"
				:key="post.name"
				@delete-post="delete_post(index)"
			/>
		</transition-group>
		<div v-if="!loading_posts && !posts.length" class="no-post-message text-muted">
			{{ __('No posts yet') }}
		</div>
		<div
			v-show="loading_posts && posts.length"
			class="text-center text-muted padding">
			{{ __('Fetching posts...') }}
		</div>
		<div
			v-show="posts.length && !loading_posts && !more_posts_available"
			class="text-center text-muted padding">
			{{ __("No more posts") }}
		</div>
	</div>
</template>
<script>
import Post from './Post.vue';
import PostSkeleton from './PostSkeleton.vue';

export default {
	props: ['post_list_filter'],
	components: {
		Post,
		PostSkeleton
	},
	data() {
		return {
			posts: [],
			more_posts_available: true,
			loading_posts: false,
			load_new: false
		}
	},
	created() {
		frappe.realtime.on('global_pin', () => {
			this.update_posts()
		})
		frappe.realtime.on('add_post', (data) => {
		    let current_user_courses = []
            frappe.call({
                method:"frappe.custom.social_post.get_user_courses",
                async:false,
                callback: function(r){
                    r.message.forEach(function (arrayItem) {
                        current_user_courses.push(arrayItem.course);
                    });
                }
            });
            let match = current_user_courses.includes(data['course']);
		    if (match || data['owner']=="Administrator") {
		        this.add_post(data);
		    }

		})
		this.$root.$on("delete_post", (name)=>{
		    this.delete_post_via_name(name);
		})

		this.$root.$on('load_new_posts', () => {
			this.update_posts()
		})
		window.addEventListener('scroll', this.handle_scroll);
		this.update_posts();
	},
	watch: {
		post_list_filter(old_val, new_val) {
			if (JSON.stringify(old_val) !== JSON.stringify(new_val)){
				this.update_posts()
			}
		}
	},
	methods: {
		get_posts(filters, load_old) {
			return frappe.xcall('frappe.social.doctype.post.post.get_posts', {
				filters,
				limit_start: load_old ? this.posts.length : 0
			})
		},
		update_posts(load_old = false) {
			if (!this.post_list_filter) return
			this.loading_posts = true;

			const filters = Object.assign({}, this.post_list_filter);
			this.get_posts(filters, load_old).then((res) => {
				if (load_old) {
					if (!res.length) {
						this.more_posts_available = false;
					}
					this.posts = this.posts.concat(res);

				} else {
					this.posts = res;
				}
			}).finally(() => {
				this.loading_posts = false;
				this.track_seen()
			});
		},
		handle_scroll: frappe.utils.debounce(function() {
			this.track_seen()
			const screen_bottom = document.documentElement.scrollTop + window.innerHeight === document.documentElement.offsetHeight;
			if (screen_bottom && this.more_posts_available) {
				if (!this.loading_posts) {
					this.update_posts(true);
				}
			}
		}, 500),
		track_seen() {
			const posts = this.$refs.posts || []
			posts.forEach((post_component) => {
				if(!post_component.post.seen
				 && frappe.dom.is_element_in_viewport(post_component.$el, 50)) {
					post_component.update_seen()
				}
			})
		},
		add_post(data) {
		    this.posts.unshift(data);
		},
		delete_post_via_name(name){
		    let self = this;
		    this.posts = this.posts.filter(function(el) { return el.name != name; });
		},
		delete_post(index) {
			this.posts.splice(index, 1);
		},
	},
	destroyed() {
		window.removeEventListener('scroll', this.handle_scroll);
	}
}
</script>
<style lang="less" scoped>
.no-post-message {
	height: 200px;
	text-align: center;
	vertical-align: middle;
	line-height: 200px;
}
.flip-list-move, .flip-list-to {
	transition: transform 0.3s;
}
</style>
