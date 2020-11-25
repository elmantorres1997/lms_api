frappe.provide('wela.late_students_graph');

frappe.pages['video-conference'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: '',
		single_column: true
	});
	console.log(window.location.pathname)
	console.log("Hello World");
	console.log(frappe.session.user)
	// console.log(frappe.get_roles(frappe.session.user));
	page.hide_actions_menu();
	// wrapper.append('<iframe src="http://map.brooky.io/brooky-map/"></iframe>');

	wrapper.latestudentsgraph = new wela.late_students_graph.LateStudentsGraph(wrapper);
	window.cur_pos = wrapper.latestudentsgraph;

};


wela.late_students_graph.LateStudentsGraph = class PointOfSale {
	
	constructor(wrapper) {
		this.wrapper = $(wrapper).find('.layout-main-section');
		this.page = wrapper.page;

		const assets = [
		];

		frappe.require(assets, () => {
			this.make();
		});
	}

	make() {
		this.prepare_dom();
		var x = document.getElementsByClassName("page-head");
		console.log(x);
		// x.parentNode.removeChild();
		// console.log(x.parentNode);
		x[0].remove();
	}

	prepare_dom() {
		// this.wrapper.append('<iframe src="https://meet.wela.online/" width="100%" height="720px" allowfullscreen></iframe>');
		this.wrapper.append('<div row="class" id="meet"></div>');
		var x = document.getElementsByClassName("layout-main-section")
		const div_ = document.createElement("div")
		div_.setAttribute("class", "myDiv")
		div_.setAttribute("id", "myDiv")
		const h5_ = document.createElement("h4")
		h5_.setAttribute("class", "myH5")
		h5_.innerText = "NOTE: Make sure to allow camera, microphone and pop-up in your browser"
		h5_.style.color = "red"
		x[0].appendChild(h5_)
		x[0].appendChild(div_)
		document.getElementById("myDiv").innerHTML += '<br><h2>Available Rooms:</h2><br>'
		
		var wrapper_ = this.wrapper

		frappe.call({
			method: "lms_api.lms_api.page.video_conference.get_rooms",
			args: {
					"user": frappe.session.user
			},
			callback: function(r, rt) {
				console.log(r);
				console.log(r.message[1])
				console.log(r.message[2])
				if(r.message) {
                    if(r.message[1] === "Zoom"){
						for (var i=0;i<r.message[0].length;i++) {
							document.getElementById("myDiv").innerHTML += '<div class="row">' +
								'<div class="col-xs-12">' +
								'<button id="'+r.message[0][i]+'" type="button" class="btn btn-primary"' +
								' onclick="join_my_class_zoom(this.id)">Join '+r.message[0][i]+'</button></div></div><br>'
							// div_.append('<div class="row">' +
							// 	'<div class="col-xs-12">' +
							// 	'<button id="'+r.message[0][i]+'" type="button" class="btn btn-primary"' +
							// 	' onclick="join_my_class_zoom(this.id)">Join '+r.message[0][i]+'</button></div></div><br>');
						}
					} else if(r.message[1] === "Jitsi") {
						for (var i=0;i<r.message[0].length;i++) {
							document.getElementById("myDiv").innerHTML += '<div class="row">' +
								'<div class="col-xs-12">' +
								'<button id="'+r.message[0][i]+'" type="button" class="btn btn-primary"' +
								' onclick="join_my_class_jitsi(this.id)">Join '+r.message[0][i]+'</button></div></div><br>'
							// div_.append('<div class="row">' +
							// 	'<div class="col-xs-12">' +
							// 	'<button id="'+r.message[0][i]+'" type="button" class="btn btn-primary"' +
							// 	' onclick="join_my_class_jitsi(this.id)">Join '+r.message[0][i]+'</button></div></div><br>');
						}
					} else if(r.message[1] === "BigBlueButton") {
						for (var i=0;i<r.message[0].length;i++) {
							// document.getElementById("myDiv").innerHTML += '<div class="row">' +
							// 	'<div class="col-xs-12">' +
							// 	'<button id="'+r.message[0][i]+'" type="button" class="btn btn-primary"' +
							// 	' onclick="join_my_class_bigblue(this.id)">Join '+r.message[0][i]+'</button></div></div><br>'
							document.getElementById("myDiv").innerHTML += '<div class="row">' +
								'<div class="col-xs-12">' +
								'<button id="'+r.message[0][i]+'" type="button" class="btn btn-primary"' +
								' onclick="join_my_class_bigblue(this.id)">Join '+r.message[0][i]+'</button></div></div><br>'
							// div_.append('<div class="row">' +
							// 	'<div class="col-xs-12">' +
							// 	'<button id="'+r.message[0][i]+'" type="button" class="btn btn-primary"' +
							// 	' onclick="join_my_class_jitsi(this.id)">Join '+r.message[0][i]+'</button></div></div><br>');
						}
					}
				}
			}
		});
		console.log(wrapper_)
	}


};


function join_my_class_zoom(room) {
	document.getElementById(room).disabled = true

	var x = document.getElementsByClassName("layout-main-section")
	const div_ = document.createElement("div")
	div_.setAttribute("class", "loading-label-div")
	div_.setAttribute("id", "loading-label-div")
	div_.style.flex = 1
	div_.style.textAlign = "center"
	div_.style.marginTop = "5%"

	const h4_1 = document.createElement("h4")
	h4_1.setAttribute("class", "loading-label-h4")
	h4_1.setAttribute("id", "loading-label-h4")
	h4_1.innerText = "Loading video conference tool, please wait..."
	h4_1.style.margin = "16px"
	div_.appendChild(h4_1)


	// const role = frappe.user.has_role("Student")

	// if (role) {
	// 	if (frappe.session.user === "Administrator") {
	// 		div_.appendChild(button_1)
	// 		div_.appendChild(h4_2)
	// 		div_.appendChild(button_2)
	// 		div_.appendChild(h4_1)
	// 	} else {
	// 		con_role = 0
	// 	}
	// }
	// else {
	// 	div_.appendChild(button_1)
	// 	div_.appendChild(h4_2)
	// 	div_.appendChild(button_2)
	// 	div_.appendChild(h4_1)
	// }

	// const h4_ = document.createElement("h4")
	// h4_.setAttribute("class", "loading-label-h4")
	// h4_.setAttribute("id", "loading-label-h4")
	// h4_.innerText = "Loading video conference tool, please wait..."

	x[0].appendChild(div_)

	document.getElementById("myDiv").style.display = "none"

	frappe.call({
		method: "lms_api.lms_api.page.video_conference.request_meeting",
		args: {
				"topic": room
		},
		callback: function(r) {
			console.log(r.message)
			if(r.message) {
				// console.log(r.message)
				document.getElementById("loading-label-h4").innerText = ""
				const res = JSON.parse(r.message)
				const role = frappe.user.has_role("Student")
				var con_role = null

				const div_ = document.getElementById("loading-label-div")

				const h4_2 = document.createElement("h4")
				h4_2.setAttribute("class", "or-label-h4")
				h4_2.setAttribute("id", "or-label-h4")
				h4_2.innerText = "OR"

				const button_1 = document.createElement("button")
				button_1.innerHTML = "Join as Host"; 
				button_1.setAttribute("id", "btn_host_start_vid")
				button_1.setAttribute("class", "btn btn-primary")
				button_1.onclick = function () {
					document.getElementById("btn_host_start_vid").disabled = true
					document.getElementById("btn_attendee_start_vid").disabled = true
					if (/Mobi/i.test(navigator.userAgent)) {
						url = res.start_url
					} else {
						url = `https://video.wela.online/index.html?meeting_number=${res.id}&meeting_pwd=${res.encrypted_password}&display_name=${frappe.session.user}&role=1`
					}
					window.open(url)
					document.getElementById("loading-label-h4").innerText = "Video tool started. Please allow pop-up if no new window appeared."
				};
				
				const button_2 = document.createElement("button")
				button_2.innerHTML = "Join as Attendee"; 
				button_2.setAttribute("id", "btn_attendee_start_vid")
				button_2.setAttribute("class", "btn btn-primary")
				button_2.onclick = function () {
					document.getElementById("btn_host_start_vid").disabled = true
					document.getElementById("btn_attendee_start_vid").disabled = true
					if (/Mobi/i.test(navigator.userAgent)) {
						url = res.join_url
					} else {
						url = `https://video.wela.online/index.html?meeting_number=${res.id}&meeting_pwd=${res.encrypted_password}&display_name=${frappe.session.user}&role=0`
					}
					window.open(url)
					document.getElementById("loading-label-h4").innerText = "Video tool started. Please allow pop-up if no new window appeared."
				};
				
				// var url = ""

				// if (role) {
				// 	if (frappe.session.user === "Administrator") {
				// 		con_role = 1
				// 	} else {
				// 		con_role = 0
				// 	}
				// }
				// else {
				// 	con_role = 1
				// }

				// if (/Mobi/i.test(navigator.userAgent)) {
				// 	if(con_role === 1) {
				// 		url = res.start_url
				// 	} else {
				// 		url = res.join_url
				// 	}
				// } else {
				// 	url = `https://video.wela.online/index.html?meeting_number=${res.id}&meeting_pwd=${res.encrypted_password}&display_name=${frappe.session.user}&role=${con_role}`
				// }

				if (role) {
					if (frappe.session.user === "Administrator") {
						div_.appendChild(button_1)
						div_.appendChild(h4_2)
						div_.appendChild(button_2)
						
					} else {
						if (/Mobi/i.test(navigator.userAgent)) {
							url = res.join_url
						} else {
							url = `https://video.wela.online/index.html?meeting_number=${res.id}&meeting_pwd=${res.encrypted_password}&display_name=${frappe.session.user}&role=0`
						}
						window.open(url)
						document.getElementById("loading-label-h4").innerText = "Video tool started. Please allow pop-up if no new window appeared."
					}
				}
				else {
					div_.appendChild(button_1)
					div_.appendChild(h4_2)
					div_.appendChild(button_2)
				}


				// window.open(url)
				
			}
		}
	});
}

function join_my_class_jitsi(room) {
	document.getElementById(room).disabled = true
	var x = document.getElementsByClassName("layout-main-section")
	const div_ = document.createElement("div")
	div_.setAttribute("class", "loading-label-div")
	div_.setAttribute("id", "loading-label-div")
	div_.style.flex = 1
	div_.style.textAlign = "center"
	div_.style.marginTop = "5%"
	const h4_ = document.createElement("h4")
	h4_.setAttribute("class", "loading-label-h4")
	h4_.setAttribute("id", "loading-label-h4")
	h4_.innerText = "Loading video conference tool, please wait..."
	div_.appendChild(h4_)
	x[0].appendChild(div_)

	document.getElementById("myDiv").style.display = "none"
	frappe.call({
		method: "lms_api.lms_api.page.video_conference.check_meeting_status",
		args: {
				"topic": room
		},
		callback: function(r) {
			console.log(r.message)
			const role = frappe.user.has_role("Student")
			const domain = 'chat.wela.online';
			const options = {
				roomName: room,
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
					const url = `https://chat.wela.online/${room}#userInfo.email=%22${frappe.session.user}%22&userInfo.displayName=%22${frappe.session.user_fullname}%22`
					window.open(url)
					// const api = new JitsiMeetExternalAPI(domain, options);
					// console.log(api)
					// api.on("readyToClose", function() {
					// 	console.log("CLOSED")
					// 	frappe.call({
					// 		method: "lms_api.lms_api.page.video_conference.update_meeting_status",
					// 		args: {
					// 				"topic": room,
					// 				"status": false
					// 		},
					// 	})
					// })
					frappe.call({
						method: "lms_api.lms_api.page.video_conference.update_meeting_status",
						args: {
								"topic": room,
								"status": true
						},
					})
				} else {
					if (r.message) {
						const res = JSON.parse(r.message)
						if (res.status === false) {
							const h5_ = document.createElement("h5")
							h5_.innerText = "Class has not started yet"
							document.querySelector('#meet').appendChild(h5_)
						} else {
							// https://chat.wela.online/BachelorOfScienceInComputerEngineering-MechanicsOfDeformableBodies#jitsi_meet_external_api_id=0&userInfo.email=%22teststud%40wela.online%22&userInfo.displayName=%22testing%20testung%22
							const url = `https://chat.wela.online/${room}#userInfo.email=%22${frappe.session.user}%22&userInfo.displayName=%22${frappe.session.user_fullname}%22`
							window.open(url)
							// const api = new JitsiMeetExternalAPI(domain, options);
							// console.log(api)
						}
					} else {
						const h1_ = document.createElement("h1")
						h1_.innerText = "Class has not started yet"
						document.querySelector('#meet').appendChild(h1_)
					}
				}
			}
			else {
				const url = `https://chat.wela.online/${room}#userInfo.email=%22${frappe.session.user}%22&userInfo.displayName=%22${frappe.session.user_fullname}%22`
				window.open(url)
				// const api = new JitsiMeetExternalAPI(domain, options);
				// api.on("readyToClose", function() {
				// 	console.log("CLOSED")
				// 	frappe.call({
				// 		method: "lms_api.lms_api.page.video_conference.update_meeting_status",
				// 		args: {
				// 				"topic": room,
				// 				"status": false
				// 		},
				// 	})
				// })
				frappe.call({
					method: "lms_api.lms_api.page.video_conference.update_meeting_status",
					args: {
							"topic": room,
							"status": true
					},
				})
			}
			document.getElementById("loading-label-h4").innerText = "Video tool started. Please allow pop-up if no new window appeared."
		}
	})
}

function join_my_class_bigblue(room) {
	// document.getElementById(room).disabled = true

	var x = document.getElementsByClassName("layout-main-section")

	const div_ = document.createElement("div")
	div_.setAttribute("class", "loading-label-div")
	div_.setAttribute("id", "loading-label-div")
	div_.style.flex = 1
	div_.style.textAlign = "center"
	// div_.style.marginTop = "5%"

	const h4_ = document.createElement("h4")
	h4_.setAttribute("class", "loading-label-h4")
	h4_.setAttribute("id", "loading-label-h4")
	// h4_.innerText = "Loading video conference tool, please wait..."

	const button_ = document.createElement("button")
	button_.innerHTML = "Start Video Conference"; 
	button_.setAttribute("id", "btn_start_vid")
	button_.setAttribute("class", "btn btn-primary")
	button_.onclick = function () {
		document.getElementById("loading-label-h4").innerText = "Loading video conference tool, please wait..."
		document.getElementById("btn_start_vid").disabled = true
		start_tool(room);
	};

	const button_1 = document.createElement("button")
	button_1.innerHTML = "Back"; 
	button_1.setAttribute("id", "btn_start_vid2")
	button_1.setAttribute("class", "btn btn-secondary")
	button_1.onclick = function () {
		document.getElementById("myDiv").style.display = "block"

		var element = document.getElementById("loading-label-div")
		element.parentNode.removeChild(element)
		
		var element2 = document.getElementById("btn_start_vid2")
		element2.parentNode.removeChild(element2)

		var element3 = document.getElementById("loading-label-div3")
		element3.parentNode.removeChild(element3)
	};

	x[0].appendChild(button_1)
	div_.appendChild(button_)
	div_.appendChild(h4_)
	x[0].appendChild(div_)


	const div3_ = document.createElement("div")
	div3_.setAttribute("class", "row")
	div3_.setAttribute("id", "loading-label-div3")
	div3_.style.flex = 1
	div3_.style.display = "block"
	div3_.style.margin = "8px"

	const title_prev_ = document.createElement("h4")
	title_prev_.setAttribute("class", "loading-label-h4")
	title_prev_.setAttribute("id", "loading-label-h44")
	title_prev_.innerText = "Previous Recordings"

	div3_.appendChild(title_prev_)
	x[0].appendChild(div3_)

	document.getElementById("myDiv").style.display = "none"

	frappe.call({
		method: "lms_api.lms_api.page.video_conference.get_recording_meeting_blue_api",
		args: {
				"topic": room
		},
		callback: function(r) {
			// console.log(r.message)
			if(r.message) {
				const res = JSON.parse(r.message)
				if (res.response.recordings.recording){
					if (Array.isArray(res.response.recordings.recording)) {
						res.response.recordings.recording.map(get_url)
					} else {
						get_url(res.response.recordings.recording)
					}
				}
				// console.log(result)
			// 	window.open(r.message)
			// 	document.getElementById("loading-label-h4").innerText = "Video tool started. Please allow pop-up if no new window appeared."
			}
		}
	})
}

function get_url(param) {
	console.log(new Date(Number(param.startTime._text)))
	const div_ = document.createElement("div")
	div_.setAttribute("class", "column")
	div_.setAttribute("id", "loading-label-div2")
	div_.style.flex = 1
	div_.style.textAlign = "start"
	div_.style.margin = "8px"
	div_.style.display = "inline-block"

	const a_ = document.createElement("a")
	a_.title = new Date(Number(param.startTime._text))
	a_.href = param.playback.format.url._text
	a_.target = "_blank"
	a_.style.color = "blue"
	a_.style.flex = 1
	a_.style.textAlign = "center"
	a_.style.alignItems = "center"
	a_.style.justifyItems = "center"
	a_.style.display = "grid"


	var title = document.createElement("label")
	var current_datetime = new Date(Number(param.startTime._text))
	var formatted_date = current_datetime.getFullYear() + "-" + (current_datetime.getMonth() + 1) + "-" + current_datetime.getDate() + " " + current_datetime.getHours() + ":" + current_datetime.getMinutes() + ":" + current_datetime.getSeconds()
	title.innerText = String(formatted_date) + " Recording"
	// var link = document.createTextNode(String(new Date(Number(param.startTime._text))) + " Recording"); 
	var img = document.createElement('img'); 
	img.src = param.playback.format.preview.images.image[0]._text
	// img.src = "/assets/lms_api/img/allow_popup.png"
	a_.appendChild(img);  
	a_.appendChild(title);  

	div_.appendChild(a_)
	document.getElementById("loading-label-div3").appendChild(div_)
}

function start_tool(room) {
	frappe.call({
		method: "lms_api.lms_api.page.video_conference.request_meeting_blue_api",
		args: {
				"topic": room
		},
		callback: function(r) {
			console.log(r.message)
			if(r.message) {
				window.open(r.message)
				document.getElementById("loading-label-h4").innerText = "Video tool started. Please allow pop-up if no new window appeared."
				var img = document.createElement('img'); 
				img.src = "/assets/lms_api/img/allow_popup.png"
				document.getElementById("loading-label-div").appendChild(img)
			} else {
				document.getElementById("btn_start_vid").disabled = false
			}
		}
	})
}
