import frappe


#bench --site mmc.silid.co execute lms_api.lms_api.college.create_rooms_and_permissions
def create_rooms_and_permissions(user=""):


    if user:
        user = " and user='{0}'".format(user)

    enrollees = frappe.db.sql("""
    
                            select student,course,program,user from 
                            `tabProgram Enrollment` inner join `tabProgram Course` 
                            on `tabProgram Course`.parent=`tabProgram Enrollment`.program  
                            inner join `tabStudent` on `tabStudent`.name = `tabProgram Enrollment`.student where 


`tabStudent`.level is null or `tabStudent`.level not in ('Kinder','Kindergarten','Nursery','Prep 2','Prep 1',
                        'Grade 1','Grade 2','Grade 3','Grade 4','Grade 5','Grade 6','Grade 7','Grade 8','Grade 9',
                        'Grade 10','Grade 11','Grade 12')
  and

`tabProgram Enrollment`.docstatus=1
    
                                    """ + user,as_dict=1)

    # print(enrollees)

    print(len(enrollees))

    for enroll in enrollees:


        print(enroll)

        exists_permission = frappe.db.sql(
            f"SELECT name FROM `tabUser Permission` "
            f"WHERE user=%s AND allow='Course' AND for_value=%s",(enroll['user'],enroll['course']))
        if exists_permission == ():
            try:
                frappe.get_doc({
                    "doctype": "User Permission",
                    "user": enroll['user'],
                    "allow": "Course",
                    "for_value": enroll['course']
                }).insert(ignore_permissions=True)
                frappe.db.commit()
                print('permission created')
            except Exception as e:
                print("errrrr!!!!!!!!!! ",str(e))
        else:
            print('exists permission')

        #check if room exists

        exists_room = frappe.db.sql("""select count(*) from `tabVideo Conference Rooms` 
                                                where subject=%s""",(enroll['course']))

        if exists_room[0][0] == 0:
            try:
                frappe.get_doc({
                    "doctype": "Video Conference Rooms",
                    "room_name": enroll['program'],
                    "subject": enroll['course'],
                    "video_conference_tool": "Meet",
                    "grade_level_and_section": enroll['program']
                }).insert(ignore_permissions=True)
                frappe.db.commit()
                print('room created')
            except:
                print("err!")
                pass
        else:
            print('exists room')

    print(len(enrollees))
