var last_type = ""


class Quiz {
	constructor(wrapper, options) {
		this.wrapper = wrapper;
		Object.assign(this, options);
		this.questions = []
		this.refresh();
	}

	refresh() {
		this.get_quiz();
	}

	get_quiz() {
		frappe.call('erpnext.education.utils.get_quiz', {
			quiz_name: this.name,
			course: this.course
		}).then(res => {
			this.make(res.message)
		});
	}

	shuffle(array) {
          var currentIndex = array.length, temporaryValue, randomIndex;
          while (0 !== currentIndex) {
            randomIndex = Math.floor(Math.random() * currentIndex);
            currentIndex -= 1;
            temporaryValue = array[currentIndex];
            array[currentIndex] = array[randomIndex];
            array[randomIndex] = temporaryValue;
          }
          return array;
        }

	make(data) {
	    if (data.is_shuffle) {
	        data.questions = this.shuffle(data.questions)
	    }
        data.questions.forEach((question_data, index) => {
            let question_wrapper = document.createElement('div');
            let question = new Question({
                wrapper: question_wrapper,
                index: index + 1,
                ...question_data
            });

                this.questions.push(question)
                this.wrapper.appendChild(question_wrapper);

        })
		if (data.activity.is_complete) {
			this.disable()
			let indicator = 'red'
			let message = 'You are not allowed to attempt the quiz again.'
			if (data.activity.result == 'Pass') {
				indicator = 'green'
				message = 'You have already cleared the quiz.'
			}

			this.set_quiz_footer(message, indicator, data.activity.score)
		}
		else {
			this.make_actions();
		}
	}

	make_actions() {
		const button = document.createElement("button");
		if(last_type == "Essay") {
			button.classList.add("btn", "btn-primary", "mt-15", "mr-2");
		}
		else {
			button.classList.add("btn", "btn-primary", "mt-5", "mr-2");
		}

		button.id = 'submit-button';
		button.innerText = 'Submit';
		button.onclick = () => this.submit();
		this.submit_btn = button
		this.wrapper.appendChild(button);
	}

    cleanResponseObject(responseObj) {
        let cleanObj = {}
        for (let [key, value] of Object.entries(responseObj)) {
            if (value === []) {
                value = null
            }
            cleanObj[key] = value
        }
        return cleanObj
    }


	submit_final() {
	    this.submit_btn.innerText = 'Evaluating..'
		this.submit_btn.disabled = true
		let timeout_counter = 0
		let self = this;
        let timeout_interval = setInterval(function () {
           timeout_counter++;
           if (timeout_counter == 60) {
                clearInterval(timeout_interval);
                self.submit_btn.innerText = 'Submit'
                self.submit_btn.disabled = false
           }
        }, 1000)
		frappe.call({
		    method: 'erpnext.education.utils.evaluate_quiz',
		    args:{
		        'quiz_name': this.name,
                'quiz_response': this.cleanResponseObject(this.get_selected()),
                'course': this.course,
                'program': this.program
		    },
		    callback:function(res) {
    		    clearInterval(timeout_interval);
                var counter = 5;
                let interval = setInterval(function() {
                    self.submit_btn.innerText = "Evaluating... "+counter;
                    counter--;
                    if (counter == 0) {
                        clearInterval(interval);
                        try {
                            if (res.message.hasOwnProperty("error")){
                                self.submit_btn.innerText = 'Submit'
                                self.submit_btn.disabled = false
                                frappe.throw(__(`${res.message.error}`))

                            } else {
                                    self.disable()
                                    self.submit_btn.remove()
                                   if (!res.message) {
                                        frappe.throw(__("Something went wrong while evaluating the quiz."))
                                    }

                                    if (res.message.hasOwnProperty("status")) {
                                        let indicator = 'green'
                                        let message = 'Thank you for submitting your answer. Your teacher will evaluate your answers.'
                                        self.set_quiz_footer(message, indicator, res.message.score)
                                    }
                            }
                        }catch(error) {
                            console.log(error)
                        }
                    }
                }, 1000);
		    },
		    error: function(opts){
		        clearInterval(timeout_interval);
                self.submit_btn.innerText = 'Submit'
                self.submit_btn.disabled = false
		    }
		})
	}

	submit() {
		let responses = this.get_selected()
		let unanswered = []

		let questionNumber = 1
		for (let [key, value] of Object.entries(responses)) {
            if (value === "") {
                unanswered.push(`Question #${questionNumber}`)
            } else if (value === null) {
                unanswered.push(`Question #${questionNumber}`)
            } else if (typeof(value) === "object") {
                value.forEach((respo, index) => {
                    if (respo === "" || respo === "-") {
                        unanswered.push(`Question #${questionNumber} - Row ${index+1}`)
                    }
                })
            } else if (value === []) {
                unanswered.push(`Question #${questionNumber}`)
            }
            questionNumber++;
        }
        let self = this;
        if (unanswered.length > 0) {

            let message = `There are questions you haven't answered yet. Are you sure you want to submit?\n\nUnanswered questions:\n`
            unanswered.forEach((item)=>{
                message += `\n${item}`
            })

            frappe.msgprint({
                title: "Submit Quiz",
                indicator: 'red',
                message: message,
                primary_action: {
                    'label': 'Confirm',
                    action(values) {
                        self.submit_final();
                        this.hide();
                    }
                }
            });
        } else {
            self.submit_final();
        }


	}

	set_quiz_footer(message, indicator, score) {
		const div = document.createElement("div");
		div.classList.add("mt-5");
		div.innerHTML = `<div class="row">
							<div class="col-md-8">
								<h4>${message}</h4>
							</div>
							<div class="col-md-4">
								<a href="${this.next_url}" class="btn btn-primary pull-right">${this.quiz_exit_button}</a>
							</div>
						</div>`

		this.wrapper.appendChild(div)
	}

	disable() {
		this.questions.forEach(que => que.disable())
	}

	get_selected() {
		let que = {}
		this.questions.forEach(question => {
			que[question.name] = question.get_selected()
		})
		return que
	}
}

class Question {
	constructor(opts) {
		Object.assign(this, opts);
		this.make();
	}

	make() {
		let make_enum_input = (wrapper, option, index) => {
			let input_div = document.createElement('div');
			input_div.classList.add('form-check', 'pb-1')
			input_div.style.display = "block"
			input_div.style.position = "relative"

			let input = document.createElement('input');
			input.id = option.name+"_enum";
			input.type = 'text';

			let label = document.createElement('label');
			label.style.marginRight = "1rem"
			label.htmlFor = option.name;
			label.innerText = index + 1;

			input_div.appendChild(label)
			input_div.appendChild(input)

			wrapper.appendChild(input_div)
			return {input: input, ...option}
		}

		let make_matching_select = (name, all_options) => {
			let input = document.createElement('select');
			input.id = name+"_select";
			input.classList.add('form-check-select');
			input.style.flexGrow = 1
			let cleanArray = [];
			all_options.forEach(opt => {
				let values = Object.values(JSON.parse(opt))[0]

				cleanArray.push(values)

			})
			cleanArray = [...new Set(cleanArray)];
			cleanArray.forEach(item => {
			    let options_true = document.createElement('option')
			    options_true.value = item
				let text_node_true = document.createTextNode(item);
				options_true.appendChild(text_node_true)
				input.appendChild(options_true)
			})
			return input
		}

		let make_matching_label = (name, value) => {
			let label = document.createElement('label');
			label.htmlFor = name;
			label.innerText = Object.keys(JSON.parse(value))[0];
			label.style.flexGrow = 1
			label.style.width = "50%"
			return label
		}

		let make_matching_option = (wrapper, option, index, all_options) => {
			let option_div = document.createElement('div')
			option_div.style.display = "flex"
			option_div.style.position = "relative"
			let input = make_matching_select(option.name, all_options);
			let label = make_matching_label(option.name, option.option);
			option_div.appendChild(label);
			option_div.appendChild(input);
			option_div.style.padding = "4px"

			if(option.image) {
				var DOM_img = document.createElement("img");
				DOM_img.src = option.image;
				option_div.appendChild(DOM_img);
			}

			wrapper.appendChild(option_div)
			return {input: input, ...option}
		}
		// this.wrapper.classList.add('row')
		if(this.type_of_question=="Fill in the Blanks")
		{
			let option_list = []
			let options_wrapper = document.createElement('div')
			// options_wrapper.classList.add('ml-2')
			options_wrapper.style.flex = 1
			options_wrapper.style.display = "flex"
			options_wrapper.style.justifyContent  = "start"
			options_wrapper.style.alignItems = "center"
			options_wrapper.style.textAlign = "start"
			options_wrapper.style.position = "relative"
			options_wrapper.style.marginTop = "4rem"

			let label = document.createElement('h5');
			label.innerText = this.index + ".) ";

			options_wrapper.appendChild(label);

			let text_wrapper = document.createElement('div')
			// options_wrapper.classList.add('ml-2')
			text_wrapper.style.flex = 1
			text_wrapper.style.display = "flex"
			text_wrapper.style.justifyContent  = "start"
			text_wrapper.style.alignItems = "center"
			text_wrapper.style.textAlign = "start"
			text_wrapper.style.position = "relative"

			label.appendChild(text_wrapper);

			let question_arr = this.question.split("_")

			let question_1 = document.createElement('h5')
			question_1.innerHTML = question_arr[0] || "";

			let question_2 = document.createElement('h5')
			question_2.innerHTML = question_arr[1] || "";

			let input = document.createElement('input');
			input.id = this.name+"_ident";
			input.type = 'text';
			input.style.marginLeft = "8px"
			input.style.marginRight = "8px"

			if (this.question.indexOf("_") == 5) {
				text_wrapper.appendChild(input)
				text_wrapper.appendChild(question_2)
			} else if (this.question.indexOf("_") == this.question.length -1) {
				text_wrapper.appendChild(question_1)
				text_wrapper.appendChild(input)
			} else {
				text_wrapper.appendChild(question_1)
				text_wrapper.appendChild(input)
				text_wrapper.appendChild(question_2)
			}

			this.answer_obj = input;
			this.options = option_list

			this.wrapper.appendChild(options_wrapper);
			if(this.question_image) {
					var DOM_img = document.createElement("img");
					DOM_img.src = this.question_image;
					this.wrapper.appendChild(DOM_img);
				}
		} else
		{
			this.make_question()
		}

		if(this.type_of_question=="Multiple Choice")
		{
			this.make_options()
		}
		else if(this.type_of_question=="Matching Type") {
			let options_wrapper = document.createElement('div')
			options_wrapper.classList.add('ml-2')
			let option_list = []

			let all_options = []

			this.options.forEach(opt => {
				all_options.push((Object.values(opt)[1]).replace(/&lt;/g,'<').replace(/&gt;/g,'>'))
			})

			// all_options.sort(() => Math.random() - 0.5)
			for(let i = all_options.length - 1; i > 0; i--){
				const j = Math.floor(Math.random() * (i+1))
				const temp = all_options[i]
				all_options[i] = all_options[j]
				all_options[j] = temp
			  }
			all_options.unshift(JSON.stringify({default: "-"}))
			this.options.forEach((opt, index) => {
				option_list.push(make_matching_option(options_wrapper, opt, index, all_options))
			})

			this.options = option_list
			this.wrapper.appendChild(options_wrapper)
		}
		else if(this.type_of_question=="Enumeration")
		{
			let options_wrapper = document.createElement('div')
			options_wrapper.classList.add('ml-2')

			// let option_div = document.createElement('div');
			// option_div.classList.add('form-check', 'pb-1')
			// option_div.style.display = "block"
			// option_div.style.position = "relative"

			let option_list = []
			this.options.forEach((opt, index) => {
				option_list.push(make_enum_input(options_wrapper, opt, index))
			})

			// options_wrapper.appendChild(option_div);
			// this.answer_obj = input;
			this.options = option_list
			this.wrapper.appendChild(options_wrapper)
		}
		else if(this.type_of_question=="True or False")
		{
			let options_wrapper = document.createElement('div')

			options_wrapper.classList.add('ml-2')
			let option_list = []
			// this.options.forEach(opt => option_list.push(make_option(options_wrapper, opt)))

			let input = document.createElement('select');
			input.style.width = '20%';
			input.id = this.name+"_select";
			input.classList.add('form-check-select');

			let options_empty = document.createElement('option')
			options_empty.value = "empty"
			options_empty.classList.add('form-check-select-options-true');

			let text_node_empty = document.createTextNode(" ");
			options_empty.appendChild(text_node_empty)

			input.appendChild(options_empty)

			let options_true = document.createElement('option')
			options_true.value = "True"
			options_true.classList.add('form-check-select-options-true');

			let text_node_true = document.createTextNode("True");
			options_true.appendChild(text_node_true)

			input.appendChild(options_true)

			let options_false = document.createElement('option')
			options_false.value = "False"
			options_false.classList.add('form-check-select-options-false');

			let text_node_false = document.createTextNode("False");
			options_false.appendChild(text_node_false)

			input.appendChild(options_false)
			

			let option_div = document.createElement('div');
			option_div.appendChild(input);
			options_wrapper.appendChild(option_div);
			this.answer_obj = input;
			this.options = option_list
			this.wrapper.appendChild(options_wrapper)
			


		}
		else if(this.type_of_question=="Identification" || this.type_of_question=="Fill in the Blank")
		{
			let options_wrapper = document.createElement('div')
			options_wrapper.classList.add('ml-2')
			let option_list = []
			// this.options.forEach(opt => option_list.push(make_option(options_wrapper, opt)))

			let input = document.createElement('input');
			input.id = this.name+"_ident";
			// input.name = this.name;
			// input.value = value;
			input.type = 'text';
			input.classList.add('form-check-input');
			let option_div = document.createElement('div');
			option_div.classList.add('form-check', 'pb-1')
			option_div.appendChild(input);
			options_wrapper.appendChild(option_div);
			this.answer_obj = input;
			this.options = option_list
			this.wrapper.appendChild(options_wrapper)
		}
		else if (this.type_of_question=="Essay")
		{
			let options_wrapper = document.createElement('div')
			options_wrapper.classList.add('ml-2')
			let option_list = []
			// this.options.forEach(opt => option_list.push(make_option(options_wrapper, opt)))

			let input = document.createElement('textarea');
			input.id = this.name+"_essay";
			input.style.width = '100%';
			input.style.height = '200px';
			input.style.margin = "4px"
			let option_div = document.createElement('div');
			option_div.appendChild(input);
			options_wrapper.appendChild(option_div);
			this.answer_obj = input;
			this.options = option_list
			this.wrapper.appendChild(options_wrapper)
		}
		last_type = this.type_of_question;

	}

	get_selected() {
		let selected = this.options.filter(opt => opt.input.checked)
		if (this.type_of_question=="Multiple Choice")
			{
			if (this.type == 'Single Correct Answer') {
				if (selected[0]) return selected[0].name
			}
			if (this.type == 'Multiple Correct Answer') {
				return selected.map(opt => opt.name)
			}

		}
		else if (this.type_of_question=="Enumeration" || this.type_of_question == "Matching Type") {
			return this.options.map(opt => opt.input.value)
		}
		else{
			return this.answer_obj.value;
		}
		return null
	}

	disable() {
		let selected = this.options.forEach(opt => opt.input.disabled = true)
		var inputs = document.getElementsByTagName("Input");
		var textAreas = document.getElementsByTagName("textarea");
		for (var i = 0; i < inputs.length; i++) {
            inputs[i].disabled = true;
        }
        for (var i = 0; i < textAreas.length; i++) {
            textAreas[i].disabled = true;
        }
	}

	make_question() {
		let question_wrapper = document.createElement('h5');

		if(last_type=="Essay")
		{
			question_wrapper.classList.add('mt-15')
		}
		else if(last_type=="Identification" || last_type=="Fill in the Blank")
		{
			question_wrapper.classList.add('mt-5')
		}
		else {
			question_wrapper.classList.add('mt-3')
		}
		// question_wrapper.classList.add('mt-3');
		// question_wrapper.innerText = this.index + ".) " + this.question;
		question_wrapper.innerHTML = this.index + ".) " + this.question;
		
		this.wrapper.appendChild(question_wrapper);
		if(this.question_image) {
				var DOM_img = document.createElement("img");
				DOM_img.src = this.question_image;
				this.wrapper.appendChild(DOM_img);
			}
	}

	make_options() {
		let make_input = (name, value) => {
			let input = document.createElement('input');
			input.id = name;
			input.name = this.name;
			input.value = value.replace(/&lt;/g,'<').replace(/&gt;/g,'>');
			input.type = 'radio';
			if (this.type == 'Multiple Correct Answer')
				input.type = 'checkbox';
			input.classList.add('form-check-input');
			return input;
		}

		let make_label = function(name, value) {
			let label = document.createElement('label');
			label.classList.add('form-check-label');
			label.htmlFor = name;
			label.innerHTML = value
			return label
		}

		let make_option = function (wrapper, option) {
			let option_div = document.createElement('div')
			option_div.classList.add('form-check', 'pb-1')
			let input = make_input(option.name, option.option.replace(/&lt;/g,'<').replace(/&gt;/g,'>'),option.image);
			let label = make_label(option.name, option.option);
			option_div.appendChild(input);
			option_div.appendChild(label);

			if(option.image) {
				var DOM_img = document.createElement("img");
				DOM_img.src = option.image;
				option_div.appendChild(DOM_img);
			}

			wrapper.appendChild(option_div)
			return {input: input, ...option}
		}

		let options_wrapper = document.createElement('div')
		options_wrapper.classList.add('ml-2')
		
		let option_list = []
		this.options.forEach(opt => option_list.push(make_option(options_wrapper, opt)))

		this.options = option_list
		this.wrapper.appendChild(options_wrapper)
	}
}