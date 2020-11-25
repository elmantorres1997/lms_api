<template>
	<div>
		<div class="comment-box flex-column">
			<div class="text-muted comment-label">{{ __('Add a comment') }}</div>
			<div ref="comment-section"></div>
			<div class="flex justify-between">
				<div class="text-muted small">
					{{ __("Ctrl+Enter to add comment") }}
				</div>
				<button
					class="btn btn-primary btn-sm"
					@click="create_comment">
					{{ __('Comment') }}
				</button>
			</div>
		</div>
		<div ref="comments" v-if="comments.length" class="comment-list">
			<div class="comment" v-for="comment in comments" :key="comment.name">
				<span
					class="cursor-pointer"
					@click="go_to_profile_page(comment.owner)"
					v-html="get_avatar(comment.owner)">
				</span>
				<span class="content" v-html="comment.content"/>
				<span
					class="text-muted"
					v-html="get_time(comment.creation)">
				</span>
				<span v-if="comment.owner==frappe.session.user"
					class="ml-1 delete-comment-icon" @click="delete_comment(comment.name)"
					>Delete
				</span>
			</div>
		</div>
		<div class="text-center" v-if="can_see_more_comments && (comment_count >= 20)">
		    <a class="text-center bold" href="javascript:;" style="color:blue" @click="get_more_comments" >See more comments</a>
		</div>

	</div>
</template>
<script>
export default {
	props: ['comments', 'post','comment_count'],
	mounted() {
		this.make_comment_section();
		this.make_mentions_clickable(this.$refs['comments']);
	},
	data() {
	    return {
	        start:0,
	        can_see_more_comments: true
	    }
	},
	methods: {
	    delete_comment_via_name(name){
		    let self = this;
		    this.comments = this.comments.filter(function(el) { return el.name != name; });
		},
	    delete_comment(name) {
			frappe.confirm(__("Are you sure you want to delete this comment?"), () => {
				frappe.xcall('frappe.social.doctype.post.post.delete_comment', {
					'comment_name': name
				})
                this.delete_comment_via_name(name);
			})
		},
	    get_more_comments() {
	        if(this.can_see_more_comments) {
	            this.start+=20;
                frappe.db.get_list('Post Comment', {
                fields: ['name', 'content', 'owner', 'creation'],
                order_by: 'creation desc',
                start:this.start,
                limit:20,
                filters: {
                    parent: this.post.name
                },
                }).then(comments => {
                    //this.$root.$emit("see_more_comments", comments);
                    this.comments.push(...comments);
                    if (comments.length < 20) {
                        this.can_see_more_comments = false;
                    }
                })
	        }
	    },
		get_avatar(user) {
			return frappe.avatar(user)
		},
		get_time(timestamp) {
			return comment_when(timestamp, true)
		},
		go_to_profile_page(user) {
			frappe.set_route('social', 'profile', user)
		},
		make_comment_section() {
			this.comment_section = frappe.ui.form.make_control({
				parent: this.$refs['comment-section'],
				only_input: true,
				render_input: true,
				no_wrapper: true,
				mentions: this.get_names_for_mentions(),
				df: {
					fieldtype: 'Comment',
					fieldname: 'comment'
				},
				on_submit: this.create_comment.bind(this)
			});
		},
		create_comment() {
			const message = this.comment_section.get_value().replace('<div><br></div>', '');
			if (!strip_html(message)) return
			frappe.utils.play_sound("click");
			let notificationParams = {
			    document_name: this.post.name,
			    document_type: "Post",
			    subject: `${frappe.session.user} commented on your post in <b>Social</b>`,
			    from_user: frappe.session.user,
			    for_user: this.post.owner,
			    type: "Comment",
			    enable_email_comment:0,
			    email_content: `${frappe.session.user} commented on your post in <b>Social</b>`
			};
			frappe.xcall('frappe.social.doctype.post.post.save_to_notification_log', {
                'params': notificationParams
            })
			this.$emit('create_comment', message);
			this.comment_section.clear();
		},
		get_names_for_mentions() {
			var valid_users = Object.keys(frappe.boot.user_info)
				.filter(user => !["Administrator", "Guest"].includes(user));
			valid_users = valid_users
				.filter(user => frappe.boot.user_info[user].allowed_in_mentions==1);
			return valid_users.map(user => frappe.boot.user_info[user].name);
		},
		make_mentions_clickable(parent_element) {
			Array.from(parent_element.getElementsByClassName('mention'))
				.forEach((mention) => {
					mention.classList.add('cursor-pointer');
					mention.addEventListener('click', () => {
						this.go_to_profile_page(mention.dataset.value)
					})
				});
		}
	}
}
</script>
<style lang="less" scoped>
.comment-box {
	.comment-label {
		margin-bottom: 5px;
	}
	::v-deep .ql-editor {
		background: white;
		border-radius: 4px;
		min-height: 60px !important;
		border: 1px solid #d1d8dd;
	}
	button {
		padding: 2px 5px;
		font-size: 10px;
		align-self: flex-end;
	}
}
.delete-comment-icon {
    color:red;
}
.delete-comment-icon:hover {
    color:red;
    text-decoration: underline;
    cursor: pointer;
}
.ml-1 {
    margin-left:10px;
}
.comment-list {
	margin-top: 10px;
	.comment {
		.comment-input-wrapper {
			margin-top: -6px;
			font-size: 11px;
		}
		display: flex;
		padding: 5px 0;
		.content {
			align-self: center;
			font-size: 12px;
			flex: 1
		}
	}
}
</style>
