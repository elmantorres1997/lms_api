// Copyright (c) 2020, Wela School System and contributors
// For license information, please see license.txt

frappe.ui.form.on('Video Conference Rooms', {
	onload: async function(frm, cdt, cdn) {
		// if (! await frappe.db.get_single_value('Wela Settings', 'enable_zoom')) {
		// 	if (cur_frm.doc.video_conference_tool == "Zoom") {
		// 		cur_frm.set_df_property('video_conference_tool', 'options', ['BigBlueButton', 'Jitsi']);
		// 		cur_frm.set_value('video_conference_tool', "BigBlueButton")
		// 	} else {
		// 		cur_frm.set_df_property('video_conference_tool', 'options', ['BigBlueButton', 'Jitsi']);
		// 	}
		// }
		var zoom = await frappe.db.get_single_value('Wela Settings', 'enable_zoom')
		var bbb  = await frappe.db.get_single_value('Wela Settings', 'enable_bigbluebutton')
		var meet  = await frappe.db.get_single_value('Wela Settings', 'enable_meet')

		if (!zoom && !bbb && !meet) {
			cur_frm.set_df_property('video_conference_tool', 'options', ['Jitsi'])
			cur_frm.set_value('video_conference_tool', "Jitsi")
		} else if (!zoom && !bbb && meet)  {
			cur_frm.set_df_property('video_conference_tool', 'options', ['Meet', 'Jitsi']);
			if (cur_frm.doc.video_conference_tool != "Meet" && cur_frm.doc.video_conference_tool != "Jitsi") {
				cur_frm.set_value('video_conference_tool', "Meet")
			}
		} else if (!zoom && bbb && !meet) {
			cur_frm.set_df_property('video_conference_tool', 'options', ['BigBlueButton', 'Jitsi']);
			if (cur_frm.doc.video_conference_tool != "BigBlueButton" && cur_frm.doc.video_conference_tool != "Jitsi") {
				cur_frm.set_value('video_conference_tool', "BigBlueButton")
			}
		} else if (!zoom && bbb && meet) {
			cur_frm.set_df_property('video_conference_tool', 'options', ['BigBlueButton', 'Jitsi', 'Meet']);
			if (cur_frm.doc.video_conference_tool != "BigBlueButton" && cur_frm.doc.video_conference_tool != "Jitsi" && cur_frm.doc.video_conference_tool != "Meet") {
				cur_frm.set_value('video_conference_tool', "BigBlueButton")
			}
		} else if (zoom && !bbb && !meet) {
			cur_frm.set_df_property('video_conference_tool', 'options', ['Zoom', 'Jitsi']);
			if (cur_frm.doc.video_conference_tool != "Zoom" && cur_frm.doc.video_conference_tool != "Jitsi") {
				cur_frm.set_value('video_conference_tool', "Zoom")
			}
		} else if (zoom && !bbb && meet) {
			cur_frm.set_df_property('video_conference_tool', 'options', ['Zoom', 'Jitsi', 'Meet']);
			if (cur_frm.doc.video_conference_tool != "Zoom" && cur_frm.doc.video_conference_tool != "Jitsi" && cur_frm.doc.video_conference_tool != "Meet") {
				cur_frm.set_value('video_conference_tool', "Zoom")
			}
		} else if (zoom && bbb && !meet) {
			cur_frm.set_df_property('video_conference_tool', 'options', ['Zoom', 'Jitsi', 'BigBlueButton']);
			if (cur_frm.doc.video_conference_tool != "Zoom" && cur_frm.doc.video_conference_tool != "Jitsi" && cur_frm.doc.video_conference_tool != "BigBlueButton") {
				cur_frm.set_value('video_conference_tool', "BigBlueButton")
			}
		}
		try {
			if (cur_frm.doc.video_conference_tool == "Zoom" && frm.doc.zoom_username) {
				frappe.call({
					method: "lms_api.lms_api.page.video_conference.checking_recordings_new",
					args: {
							"topic": frm.doc.room_name || "",
							"user": frm.doc.zoom_username
					},
					callback: function(r) {
						var child = locals[cdt][cdn];
						// console.log(JSON.parse(r.message))
						if(r.message) {
							const res = JSON.parse(r.message)
							// console.log(res)
							if (res.meetings.length > 0){
								// if (Array.isArray(res.response.recordings.recording)) {
								res.meetings.map(meeting => {
								var newrow = frm.add_child("recordings");
								newrow.filename = meeting.topic
								newrow.date_and_time = new Date(meeting.start_time)
								newrow.url = meeting.share_url
								})
								// }
								//  else {
								// 	// child.recordings.push({filename: res.response.recordings.recording.recordID._text, date_and_time: "2020-07-29 15:23:12"})
								// 		var newrow = frm.add_child("recordings");
								// 		newrow.filename = res.response.recordings.recording.recordID._text
								// 		newrow.date_and_time = new Date(Number(res.response.recordings.recording.startTime._text))
								// 		newrow.url = res.response.recordings.recording.playback.format.url._text
			
								// 	// console.log(newrow)
								// 	// newrow.view_recording = `<a target="_blank"  href="${res.response.recordings.recording.playback.format.url._text}">Link</a>`
								// 	// newrow.view_recording = frm.cscript.chec
								// }
							}
						}
						frm.refresh_field("recordings");
					}
				})
			}
		} catch(e) {
			console.log("error")
		}
		
		frm.cscript.view_recording = function(doc, cdt, cdn){
			window.open(cur_frm.selected_doc.url);
		}
		frm.cscript.join_room_as_host = function(doc, dt, dn){
			if (frm.doc.zoom_username) {
				frappe.call({
					method: "lms_api.lms_api.page.video_conference.request_meeting_new",
					args: {
							"topic": frm.doc.room_name,
							"user": frm.doc.zoom_username,
					},
					callback: function(r) {
						// console.log(r.message)
						console.log("host")
						if(r.message) {
							const res = JSON.parse(r.message)
							// console.log(res)
							let url = res.start_url
							// if (/Mobi/i.test(navigator.userAgent)) {
							// 	url = res.start_url
							// } else {
							// 	url = `https://video.wela.online/index.html?meeting_number=${res.id}&meeting_pwd=${res.encrypted_password}&display_name=${frappe.session.user}&role=1`
							// }
							window.open(url)
						} else {
							msgprint(__("Can't start video tool"))
						}
					}
				})
			} else {
				msgprint(__("Zoom username must not be empty."))
			}
		}
		frm.cscript.join_room_as_attendee = function(doc, dt, dn) {
			if (frm.doc.zoom_username) {
				frappe.call({
					method: "lms_api.lms_api.page.video_conference.request_meeting_new",
					args: {
							"topic": frm.doc.room_name,
							"user": frm.doc.zoom_username,
					},
					callback: function(r) {
						console.log("attendee")
						if(r.message) {
							const res = JSON.parse(r.message)
							// console.log(res)
							let url = res.join_url
							// console.log(url)
							// if (/Mobi/i.test(navigator.userAgent)) {
							// 	url = res.join_url
							// } else {
							// 	url = `https://video.wela.online/index.html?meeting_number=${res.id}&meeting_pwd=${res.encrypted_password}&display_name=${frappe.session.user}&role=0`
							// }
							window.open(url)
						} else {
							msgprint(__("Can't start video tool"))
						}
					}
				})
			} else {
				msgprint(__("Zoom username must not be empty."))
			}
		}
		frm.cscript.join_room = function(doc, dt, dn){
			if (doc.video_conference_tool) {
				// if(doc.video_conference_tool === "Zoom"){
				// 	frappe.call({
				// 		method: "lms_api.lms_api.page.video_conference.request_meeting",
				// 		args: {
				// 				"topic": frm.doc.room_name
				// 		},
				// 		callback: function(r) {
				// 			// console.log(r.message)
				// 			if(r.message) {
				// 				const res = JSON.parse(r.message)
				// 				const role = frappe.user.has_role("Student")
				// 				let url = ""
				// 				if (role) {
				// 					if (frappe.session.user === "Administrator") {
				// 						if (/Mobi/i.test(navigator.userAgent)) {
				// 							url = res.start_url
				// 						} else {
				// 							url = `https://video.wela.online/index.html?meeting_number=${res.id}&meeting_pwd=${res.encrypted_password}&display_name=${frappe.session.user}&role=1`
				// 						}
				// 						window.open(url)
				// 					} else {
				// 						if (/Mobi/i.test(navigator.userAgent)) {
				// 							url = res.join_url
				// 						} else {
				// 							url = `https://video.wela.online/index.html?meeting_number=${res.id}&meeting_pwd=${res.encrypted_password}&display_name=${frappe.session.user}&role=0`
				// 						}
				// 						window.open(url)
				// 					}
				// 				}
				// 				else {
				// 					if (/Mobi/i.test(navigator.userAgent)) {
				// 						url = res.start_url
				// 					} else {
				// 						url = `https://video.wela.online/index.html?meeting_number=${res.id}&meeting_pwd=${res.encrypted_password}&display_name=${frappe.session.user}&role=1`
				// 					}
				// 					window.open(url)
				// 				}
				// 			} else {
				// 				msgprint(__("Can't start video tool"))
				// 			}
				// 		}
				// 	})
				// } else 
				if (doc.video_conference_tool === "Jitsi") {
					frappe.call({
						method: "lms_api.lms_api.page.video_conference.check_meeting_status",
						args: {
								"topic": frm.doc.room_name
						},
						callback: function(r) {
							// console.log(r.message)
							const role = frappe.user.has_role("Student")
							const domain = 'chat.wela.online';
							const options = {
								roomName: frm.doc.room_name,
								width: "100%",
								height: 700,
								parentNode: document.querySelector('#meet'),
								userInfo: {
									email: frappe.session.user,
									displayName: frappe.session.user_fullname
								}
							};
							if (role) {
								const width = "100%"
								if (frappe.session.user === "Administrator") {
									const url = `https://chat.wela.online/${frm.doc.room_name}#userInfo.email=%22${frappe.session.user}%22&userInfo.displayName=%22${frappe.session.user_fullname}%22`
									window.open(url)
									frappe.call({
										method: "lms_api.lms_api.page.video_conference.update_meeting_status",
										args: {
												"topic": frm.doc.room_name,
												"status": true
										},
									})
								} else {
									if (r.message) {
										const res = JSON.parse(r.message)
										if (res.status === false) {
											msgprint(__("Class has not started yet."))
										} else {
											const url = `https://chat.wela.online/${frm.doc.room_name}#userInfo.email=%22${frappe.session.user}%22&userInfo.displayName=%22${frappe.session.user_fullname}%22`
											window.open(url)
										}
									} else {
										msgprint(__("Class has not started yet."))
									}
								}
							}
							else {
								const url = `https://chat.wela.online/${frm.doc.room_name}#userInfo.email=%22${frappe.session.user}%22&userInfo.displayName=%22${frappe.session.user_fullname}%22`
								window.open(url)
								frappe.call({
									method: "lms_api.lms_api.page.video_conference.update_meeting_status",
									args: {
											"topic": frm.doc.room_name,
											"status": true
									},
								})
							}
						}
					})
					
				} else if (doc.video_conference_tool === "BigBlueButton") {
					frappe.call({
						method: "lms_api.lms_api.page.video_conference.request_meeting_blue_api",
						args: {
								"topic": frm.doc.room_name
						},
						callback: function(r) {
							// console.log(r.message)
							if(r.message) {
								window.open(r.message)
							} else {
								msgprint(__("Can't start video tool"))
							}
						}
					})
				} else if (doc.video_conference_tool === "Meet") {
					if (doc.meet_url) {
						window.open(doc.meet_url)
					} else {
						msgprint(__("Meet URL must not be empty."))
					}
				}else {
					msgprint(__("Video tool not valid."))
				}
			} else {
				msgprint(__("No video tool found. Configure video tool settings."));
			}
		}
	}
});