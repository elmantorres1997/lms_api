# Copyright (c) 2013, Wela School System and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []

	columns = [
		{
			"label": "Title",
			'width': 200,
			"fieldname": "activity_name"
		},
		{
			"label": "Subject",
			'width': 120,
			"fieldname": "subject"
		},
		{
			"label": "Classwork Category",
			'width': 120,
			"fieldname": "classwork"
		},
		# {
		# 	"label": "Type",
		# 	'width': 120,
		# 	"fieldname": "type"
		# },
		{
			"label": "Publish Date",
			'width': 150,
			"fieldname": "publish_date"
		},
		{
			"label": "Deadline",
			'width': 150,
			"fieldname": "deadline"
		},
		{
			"label": "Activity Link",
			'width': 175,
			"fieldname": "act_link"
		}
	]
	student_info = frappe.db.sql(f"SELECT name FROM `tabStudent` where user='{frappe.session.user}'",as_dict=1)
	student_name = student_info[0]['name'].replace("'","\\'")
	program_list = frappe.db.sql(
		f"SELECT program FROM `tabProgram Enrollment` WHERE student='{student_name}' AND docstatus=1",as_dict=1
	)

	for program in program_list:

		# Quiz Silid
		classwork_filter = ""
		if filters.get('classwork_category'):
			classwork_filter = f" AND `tabQuiz Silid`.classwork_category='{escape(filters['classwork_category'])}' "

		if filters['type'] == "All" or filters['type'] == "Quiz":
			quiz_silid = frappe.db.sql(f"SELECT name,topic,course FROM `tabQuiz Silid` WHERE program='{program['program']}' "
									   f" AND (`tabQuiz Silid`.publish_date > '2020-09-06' "
										  f"		AND `tabQuiz Silid`.publish_date <= NOW()) " + classwork_filter
									   ,
									   as_dict=1)
			for quiz_content in quiz_silid:
				topic_name = quiz_content['topic'].replace("'", "\\'")
				topic_content_exist = frappe.db.sql(f"SELECT content FROM `tabTopic Content` WHERE parent='{topic_name}'",as_dict=1)
				quiz_info = frappe.db.sql(f"SELECT name,title,publish_date,deadline,classwork_category "
										  f"	FROM `tabQuiz` "
										  f" WHERE content_silid='{quiz_content['name']}' "
										  f" AND deadline >=NOW()", as_dict=1)
				for quiz in quiz_info:
					quiz_name = quiz['name'].replace("'", "\\'")
					is_exist = frappe.db.sql(f"SELECT name FROM `tabQuiz Activity` WHERE quiz='{quiz_name}' "
											 f"AND student='{student_name}'", as_dict=1)

					if len(is_exist):
						pass
					else:
						topic_exist = next((x for x in topic_content_exist if x['content'] == quiz_name), False)

						if topic_exist:
							link_html = f'<a style="color:blue" href="/lms/content?program={program["program"]}&course={quiz_content["course"]}&topic={quiz_content["topic"]}&type=Quiz&content={quiz_name}">Go to Link</a>'
							obj = {
								"activity_name": quiz['title'],
								"type": "Quiz",
								"subject": quiz_content["course"],
								"classwork": quiz['classwork_category'],
								"publish_date": quiz['publish_date'].strftime('%b %d, %Y %I:%M:%p') if quiz['publish_date'] else "",
								"deadline": quiz['deadline'].strftime('%b %d, %Y %I:%M:%p') if quiz['deadline'] else "",
								"act_link": link_html
							}
							data.append(obj)
		# Content Silid
		content_silid = []
		if filters['type'] == "All" or filters['type'] == "Content":



			# show_only = filters['show_only'].replace("First ","")
			#
			# show_only = int(show_only)

			"""
			OFFSET 10 ROWS 
			FETCH NEXT 10 ROWS ONLY;
			Ref: https://www.sqlservertutorial.net/sql-server-basics/sql-server-offset-fetch/
			"""

			offset_ = ""

			if filters['page'] == 1:
				offset_ = "	LIMIT 10"
			else:
				skip = ( filters['page'] ) * 10
				# offset_ = f" OFFSET {skip} FETCH NEXT 10 ROWS ONLY;"
				offset_ = f" LIMIT {skip},10 "




			# content_silid = frappe.db.sql(f"SELECT "
			# 							  f"`tabContent Silid`.name as content_silid_name,"
			# 							  f"`tabContent Silid`.is_video,"
			# 							  f"`tabContent Silid`.course,"
			# 							  f"`tabContent Silid`.topic,"
			# 							  f"`tabContent Silid`.highest_possible_score,"
			# 							  f"`tabContent Silid`.deadline as content_deadline,"
			# 							  f"`tabContent Silid`.publish_date as content_publish_date,"
			# 							  f"`tabTopic Content`.content as topic_content"
			# 							  f" FROM `tabContent Silid`"
			# 							  f" LEFT JOIN `tabTopic` ON `tabContent Silid`.topic=`tabTopic`.name"
			# 							  f" LEFT JOIN `tabTopic Content` ON `tabTopic`.name=`tabTopic Content`.parent"
			# 							  f" WHERE `tabContent Silid`.program='{escape(program['program'])}'"
			#
			# 							  f" AND (`tabContent Silid`.publish_date > '2020-09-06' "
			# 							  f"		AND `tabContent Silid`.publish_date <= NOW())"
			# 							  f"	ORDER BY content_publish_date,content_deadline " + offset_
			# 							  , as_dict=1)
			classwork_filter = ""
			if filters.get('classwork_category'):

				classwork_filter = f"AND ((`tabArticle`.classwork_category='{escape(filters['classwork_category'])}' ) OR (`tabVideo`.classwork_category='{escape(filters['classwork_category'])}')) "
			content_silid = frappe.db.sql(f"SELECT "
										  f" `tabTopic Content`.content,"
										  f" `tabTopic`.name as topic,"
										  f" `tabTopic`.subject as course, "
										  
										  
										  	   f"`tabVideo`.name as video_name,"
										  f"`tabVideo`.title as video_title,"
										  f"`tabVideo`.deadline as video_deadline,"
										  f"`tabVideo`.publish_date as video_publish_date,"
										  f"`tabVideo`.classwork_category as video_classwork,"
										  
										  f"`tabArticle`.name as article_name,"
										  f"`tabArticle`.title as article_title,"
										  f"`tabArticle`.deadline as article_deadline,"
										  f"`tabArticle`.publish_date as article_publish_date, "
										  f"`tabArticle`.classwork_category as article_classwork, "
										  
										  
										  f"`tabTopic`.program from `tabTopic Content`"
									
										  
										  f" INNER JOIN `tabTopic` ON `tabTopic`.name=`tabTopic Content`.parent"
										  f" LEFT JOIN `tabVideo` ON `tabVideo`.name=`tabTopic Content`.content"
										  f" LEFT JOIN `tabArticle` ON `tabArticle`.name=`tabTopic Content`.content"
										  f" WHERE `tabTopic`.program='{escape(program['program'])}'"
										  f" AND `tabTopic`.subject != '' "
				
										  f" AND ((`tabArticle`.publish_date > '2020-09-06' "
										  f"		AND `tabArticle`.publish_date <= NOW()) "
										  f" OR (`tabVideo`.publish_date > '2020-09-06' "
										  f" AND `tabVideo`.publish_date <= NOW()) ) " + classwork_filter +
										  f"	ORDER BY article_publish_date,video_publish_date " + offset_
										  , as_dict=1)

		for content in content_silid:
			if content['video_name']:

				completed = check_content_completion(content['video_name'], "Video", student_name)
				if not completed and content["video_name"]:
					link_html = f'<a style="color:blue" href="/lms/content?program={program["program"]}&course={content["course"]}&topic={content["topic"]}&type=Video&content={content["video_name"]}">Go to Link</a>'
					obj = {
						"activity_name": content['video_title'],
						"type": "Video",
						"subject": content['course'],
						"classwork":content['video_classwork'],
						# "publish_date": content_['video_publish_date'].strftime('%b %d, %Y %I:%M:%p') if content_['video_publish_date'] else "",
						"publish_date": content['video_publish_date'].strftime('%b %d, %Y %I:%M:%p') if content['video_publish_date'] else "",
						# "deadline": content_['video_deadline'].strftime('%b %d, %Y %I:%M:%p') if content_['video_deadline'] else "",
						"deadline": content['video_deadline'].strftime('%b %d, %Y %I:%M:%p') if content['video_deadline'] else "",
						"act_link": link_html
					}
					data.append(obj)
			else:
				completed = check_content_completion(content['article_name'], "Article", student_name)
				if not completed and content["article_name"]:
					link_html = f'<a style="color:blue"  href="/lms/content?program={program["program"]}&course={content["course"]}&topic={content["topic"]}&type=Article&content={content["article_name"]}">Go to Link</a>'
					obj = {
						"activity_name": content['article_title'],
						"type": "Article",
						"subject": content['course'],
						"classwork": content['article_classwork'],
						"publish_date": content['article_publish_date'].strftime('%b %d, %Y %I:%M:%p') if content['article_publish_date'] else "" ,
						"deadline": content['article_deadline'].strftime('%b %d, %Y %I:%M:%p') if content['article_deadline'] else "",
						"act_link": link_html
					}
					data.append(obj)

	data_sorted = sorted(data, key=lambda i: i['publish_date'], reverse=False)

	return columns, data_sorted

def check_content_completion(content_name, content_type, student):
	activity = frappe.get_all("Course Activity", filters={'student': student, 'content_type': content_type,
                                                          'content': content_name})
	if activity:
		return True
	else:
		return False

def escape(text):
	return text.replace("'","\\'")