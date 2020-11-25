
#cd apps/lms_api &&

dir=$(pwd)
apps_dir=$(dirname "$dir")
project_dir=$(dirname "$apps_dir")

#git pull &&

cp -v -r $apps_dir/lms_api/lms_api/silid/lms $apps_dir/erpnext/erpnext/www/ &&
cp -v $apps_dir/lms_api/lms_api/silid/quiz.js $apps_dir/erpnext/erpnext/public/js/education/lms/quiz.js &&

cp -v -r $apps_dir/lms_api/lms_api/lms_api/doctype/article $apps_dir/erpnext/erpnext/education/doctype/ &&
cp -v -r $apps_dir/lms_api/lms_api/lms_api/doctype/topic $apps_dir/erpnext/erpnext/education/doctype/ &&
cp -v -r $apps_dir/lms_api/lms_api/lms_api/doctype/video $apps_dir/erpnext/erpnext/education/doctype/ &&
cp -v -r $apps_dir/lms_api/lms_api/lms_api/doctype/topic_content $apps_dir/erpnext/erpnext/education/doctype/ &&
cp -v -r $apps_dir/lms_api/lms_api/lms_api/doctype/program $apps_dir/erpnext/erpnext/education/doctype/ &&
cp -v -r $apps_dir/lms_api/lms_api/lms_api/doctype/quiz_silid $apps_dir/erpnext/erpnext/education/doctype/ &&
cp -v -r $apps_dir/lms_api/lms_api/lms_api/doctype/quiz_activity $apps_dir/erpnext/erpnext/education/doctype/ &&
cp -v -r $apps_dir/lms_api/lms_api/lms_api/doctype/activity_log $apps_dir/frappe/frappe/core/doctype/ &&
cp -v -r $apps_dir/lms_api/lms_api/lms_api/doctype/quiz $apps_dir/erpnext/erpnext/education/doctype/ &&
cp -v -r $apps_dir/lms_api/lms_api/lms_api/doctype/quiz_question $apps_dir/erpnext/erpnext/education/doctype/ &&
cp -v -r $apps_dir/lms_api/lms_api/lms_api/doctype/quiz_result $apps_dir/erpnext/erpnext/education/doctype/ &&
cp -v -r $apps_dir/lms_api/lms_api/lms_api/doctype/course_enrollment $apps_dir/erpnext/erpnext/education/doctype/ &&

cp -v $apps_dir/lms_api/lms_api/silid/education_quiz/utils.py $apps_dir/erpnext/erpnext/education/utils.py &&
cp -v $apps_dir/lms_api/lms_api/silid/chat.js $apps_dir/frappe/frappe/public/js/frappe/chat.js &&
cp -v -r $apps_dir/lms_api/lms_api/silid/misc $apps_dir/frappe/frappe/public/js/frappe/ &&
cp -v -r $apps_dir/lms_api/lms_api/silid/chat $apps_dir/frappe/frappe/ &&
cp -v $apps_dir/lms_api/lms_api/silid/file.py $apps_dir/frappe/frappe/core/doctype/file/file.py &&
cp -v $apps_dir/lms_api/lms_api/silid/education_question/question.py $apps_dir/erpnext/erpnext/education/doctype/question/question.py &&
#cp -v $apps_dir/lms_api/lms_api/silid/education_course_enrollment/course_enrollment.py $apps_dir/erpnext/erpnext/education/doctype/course_enrollment/course_enrollment.py &&
cp -v $apps_dir/lms_api/lms_api/silid/frappe-web-b4.css $project_dir/sites/assets/css/frappe-web-b4.css &&

# This is removed because we transferred Quiz doctype to LMS API. So edit quiz.py on apps/lms_api/lms_api/lms_api/doctype/quiz/quiz.py
#cp -v $apps_dir/lms_api/lms_api/silid/quiz_dir/quiz.py $apps_dir/erpnext/erpnext/education/doctype/quiz/quiz.py &&


cp -v -r $apps_dir/lms_api/lms_api/silid/service $apps_dir/frappe/frappe/ &&

cp -v -r $apps_dir/lms_api/lms_api/silid/public/social $apps_dir/frappe/frappe/public/js/frappe &&
cp -v -r $apps_dir/lms_api/lms_api/silid/public/ui $apps_dir/frappe/frappe/public/js/frappe &&

cp -v -r $apps_dir/lms_api/lms_api/silid/social $apps_dir/frappe/frappe/ &&
cp -v -r $apps_dir/lms_api/lms_api/silid/custom $apps_dir/frappe/frappe/ &&
cp -v -r $apps_dir/lms_api/lms_api/public/js/ui/toolbar $apps_dir/frappe/frappe/public/js/frappe/ui/ &&
cp -v -r $apps_dir/lms_api/lms_api/silid/www $apps_dir/frappe/frappe/ &&
cp -v -r $apps_dir/lms_api/lms_api/silid/templates $apps_dir/frappe/frappe/ &&
cp -v -r $apps_dir/lms_api/lms_api/silid/desk_module/config $apps_dir/frappe/frappe/ &&
cp -v $apps_dir/lms_api/lms_api/silid/sessions.py $apps_dir/frappe/frappe/ &&
cp -v $apps_dir/lms_api/lms_api/silid/moduleview.py $apps_dir/frappe/frappe/desk/ &&
cp -v $apps_dir/lms_api/lms_api/silid/auth.py $apps_dir/frappe/frappe/ &&
cp -v $apps_dir/lms_api/lms_api/silid/file_manager.py $apps_dir/frappe/frappe/utils/ &&
cp -v $apps_dir/lms_api/lms_api/silid/file_manager_old.py $apps_dir/frappe/frappe/utils/ &&
cp -v -r $apps_dir/lms_api/lms_api/silid/desk/* $apps_dir/frappe/frappe/desk/doctype/ &&
cp -v $apps_dir/lms_api/lms_api/silid/utils.py $apps_dir/frappe/frappe/desk/form/ &&
cp -v $apps_dir/lms_api/lms_api/silid/html_utils.py $apps_dir/frappe/frappe/utils/ &&

cd ../.. &&
bench setup requirements --python &&
bench build &&
bench --site all clear-cache &&
bench restart
