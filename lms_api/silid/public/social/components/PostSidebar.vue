<template>
	<div class="flex flex-column">
		<!-- <a class="leaderboard-link"
			@click.prevent="go_to_user_list()">
			{{ __('Leaderboards') }}
		</a> -->
		<div ref="banner" class="banner">
            <div
                class="user-avatar"
                v-html="user_avatar">
            </div>
        </div>
        <!-- <div class="banner" v-html="user_avatar" @click="goto_profile(current_user)"></div> -->
		<div class="user-details"></div>
		<div class="user-details">
		    <h3>{{ user.fullname }}</h3>
			<p><a @click="view_energy_point_list(user)" class="text-muted">
				{{ __("Energy Points") }}: {{ energy_points }}</a></p>
			<p>{{ user.bio }}</p>
			<div class="location" v-if="user.location">
				<span class="text-muted">
					<i class="fa fa-map-marker">&nbsp;</i>
					{{ user.location }}
				</span>
			</div>
			<div class="interest" v-if="user.interest">
				<span class="text-muted">
					<i class="fa fa-puzzle-piece">&nbsp;</i>
					{{ user.interest }}
				</span>
			</div>
		</div>
		<div class="links" v-if="menus.length">
			<div class="muted-title">
				{{ __('Menu') }}
			</div>
			<div class="flex flex-column">
				<a class="route-link"
					@click.prevent="goto_route(freq.route)"
					v-for="freq in menus"
					:key="freq.route">
					{{ freq.label }}
				</a>
			</div>
		</div>
		<div class="links" v-if="frequently_visited_list.length">
			<div class="muted-title">
				{{ __('Frequently Visited Links') }}
			</div>
			<div class="flex flex-column">
				<a class="route-link"
					@click.prevent="goto_list(route_obj.route)"
					v-for="route_obj in frequently_visited_list"
					:key="route_obj.route">
					{{ get_label(route_obj.route) }}
				</a>
			</div>
		</div>
	</div>
</template>
<script>
export default {
	data() {
		return {
		    energy_points: 0,
		    user: frappe.user_info(frappe.session.user),
		    menus: [],
			frequently_visited_list: [],
			current_user:"",
			user_avatar: frappe.avatar(this.current_user, 'avatar-xl'),
		}
	},
	mounted() {
	    frappe.xcall('frappe.social.doctype.energy_point_log.energy_point_log.get_user_energy_and_review_points', {user: frappe.session.user}).then(r => {
			this.energy_points = r.message ? r[this.user_id].energy_points : 0;
		});

	},
	created() {

		this.set_frequently_visited_list()
		this.set_menus()
		this.current_user = frappe.session.user;

	},
	methods: {

		goto_route(route) {
		    let url = window.location.origin+route;
		    window.location.href = url;
		    //this.$router.push(route);
			//frappe.set_route(route);
		},
		goto_list(route){
		    frappe.set_route(route);
		},
		set_menus() {
		    this.menus = [
		        {
                    label: "Dashboard",
                    route: "/desk#"
		        },
		        {
		            label: "Silid Aralan",
		            route: "/lms"
		        },
		        {
		            label: "Video Conference",
		            route: "/desk#video-conference"
		        }
		    ]
		},
		set_frequently_visited_list() {

			frappe.xcall('frappe.social.doctype.post.post.frequently_visited_links')
				.then(data => {
					this.frequently_visited_list = data;
            })
		},
		get_label(route) {
			return frappe.utils.get_route_label(route);
		},
		go_to_profile_page() {
			frappe.set_route('social', 'profile', frappe.session.user)
		},
		go_to_user_list() {
			frappe.set_route('social', 'users')
		}
	}
}
</script>
<style lang="less" scoped>
.route-link {
	margin: 0px 10px 10px 0;
	text-transform: capitalize;
}
.leaderboard-link {
	.route-link;
	margin-bottom: 15px;
}
.stats {
	min-height: 150px
}
.user-details {
    min-height:150px;
}
.banner {
	.user-avatar {
		position: relative;
		/deep/ .avatar {
			left: 0px;
			width: 150px;
			height: 150px;
			border-radius: 4px;
			background: white;
			position: absolute !important;
		}
	}
	.editable-image {
		/deep/ .avatar {
			cursor: pointer;
			:hover {
				opacity: 0.9;
			}
		}
	}
}
.user-details {
	.user-avatar {
		/deep/.avatar-xl {
			height: 150px;
			width: 150px;
		}
	}
	.user_name {
		display: block;
		margin-top: 10px;
		font-size: 2rem;
		font-weight: 600
	}
}
</style>

