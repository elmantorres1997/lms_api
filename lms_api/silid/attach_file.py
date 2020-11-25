import frappe, json
from frappe.utils.file_manager_old import save_file

@frappe.whitelist()
def attach_file_to_project_(work,title,student):


    if getattr(frappe, "uploaded_file", None):
        with open(frappe.uploaded_file, "rb") as upfile:
            fcontent = upfile.read()
    else:
        fcontent = frappe.local.uploaded_file

    fname = frappe.local.uploaded_filename

    filedata =fcontent


    # sql_check_grade = frappe.db.sql(
    #     """Select grade,name from `tabWritten Activity` WHERE activity = '{0}' AND owner = '{1}'""".format(title,
    #                                                                                                        student))
    #
    # if sql_check_grade != ():
    #     if sql_check_grade[0][0] > 0:
    #         frappe.msgprint('Unable to Save. Grade Already Added')
    #     else:
    #         # no grade update work
    #         written_data = frappe.get_doc("Written Activity", sql_check_grade[0][1])

    # else:
        # Get Quarter and School Year

    written = {
        "doctype": "Written Activity",
        "activity": work,
        # "upload": file_name,
        # "student": student
    }

    written_data = frappe.get_doc(written)

    written_data.insert(ignore_permissions=True)

    if filedata:
        fd_json = json.loads(filedata)
        fd_list = list(fd_json["files_data"])

        for fd in fd_list:
            filedoc = save_file(fd["filename"], fd["dataurl"],
                                "Written Activity", written_data.name, decode=True, is_private=0)

            frappe.db.commit()

            written_data.upload = filedoc.file_url

            written_data.save(ignore_permissions=True)

            frappe.db.commit()

@frappe.whitelist()
def attach_url_to_project(filedata, work,title,work_title, student,doctype, course, topic,program, fileUrl):


    if doctype == "Article":
        work = work.replace("'", "\\'")
        work_title = work_title.replace("'", "\\'")
        check_existing = frappe.get_list("Written Activity", fields=["name"],
                                         filters={"activity": work, "title": work_title, "subject": course})

        if check_existing:
            written_data = frappe.get_doc("Written Activity", check_existing[0]['name'])

        else:
            written = {
                "doctype": "Written Activity",
                "activity": work,
                "title": work_title,
                "subject": course,
                "topic": topic,
                "program": program,
                # "upload": file_name,
                "student": student
            }
            written_data = frappe.get_doc(written)
            written_data.insert(ignore_permissions=True)
            frappe.db.commit()
    else:
        work = work.replace("'", "\\'")
        work_title = work_title.replace("'", "\\'")
        check_existing = frappe.get_list("Written Activity", fields=["name"],
                                         filters={"video": work, "title": work_title, "subject": course})
        if check_existing:
            written_data = frappe.get_doc("Written Activity", check_existing[0]['name'])

        else:
            written = {
                "doctype": "Written Activity",
                "video": work,
                "title": work_title,
                "subject": course,
                "topic": topic,
                "program": program,
                # "upload": file_name,
                "student": student
            }

            written_data = frappe.get_doc(written)
            written_data.insert(ignore_permissions=True)

            frappe.db.commit()

    written_data.alternative_uploads =  fileUrl

    if doctype == "Article":
        article_info = frappe.get_doc("Article", work)
        written_data.quarter = article_info.quarter
        written_data.school_year = article_info.school_year
        written_data.title = work_title
        written_data.subject = course
        written_data.student = student
        written_data.save(ignore_permissions=True)

        frappe.db.commit()

    else:
        article_info = frappe.get_doc("Video", work)
        written_data.quarter = article_info.quarter
        written_data.school_year = article_info.school_year
        written_data.subject = course
        written_data.title = work_title
        written_data.student = student
        written_data.save(ignore_permissions=True)

        frappe.db.commit()


@frappe.whitelist()
def attach_file_to_project(filedata, work,title,work_title, student,doctype, course, topic,program, fileUrl):
    # sql_check_grade = frappe.db.sql(
    #     """Select grade,name from `tabWritten Activity` WHERE activity = %s AND owner = %s""",(title, student))
    #
    # if sql_check_grade != ():
    #     if sql_check_grade[0][0] > 0:
    #         frappe.msgprint('Unable to Save. Grade Already Added')
    #     else:
    #         #no grade update work
    #         written_data = frappe.get_doc("Written Activity",sql_check_grade[0][1])
    #
    # else:

    if doctype == "Article":
        work = work.replace("'","\\'")
        work_title = work_title.replace("'","\\'")
        check_existing = frappe.get_list("Written Activity", fields=["name"] , filters={"activity": work, "title": work_title, "subject":course })


        if check_existing:
            written_data = frappe.get_doc("Written Activity", check_existing[0]['name'])

        else:
            written = {
                "doctype": "Written Activity",
                "activity": work,
                "title":work_title,
                "subject": course,
                "topic": topic,
                "program":program,
                # "upload": file_name,
                "student": student
            }
            written_data = frappe.get_doc(written)
            written_data.insert(ignore_permissions=True)
            frappe.db.commit()
    else:
        work = work.replace("'", "\\'")
        work_title = work_title.replace("'", "\\'")
        check_existing = frappe.get_list("Written Activity", fields=["name"] , filters={"video": work, "title": work_title, "subject":course })
        if check_existing:
            written_data = frappe.get_doc("Written Activity", check_existing[0]['name'])

        else:
            written = {
                "doctype": "Written Activity",
                "video": work,
                "title": work_title,
                "subject": course,
                "topic": topic,
                "program": program,
                # "upload": file_name,
                "student": student
            }

            written_data = frappe.get_doc(written)
            written_data.insert(ignore_permissions=True)

            frappe.db.commit()

    written_data.uploads = fileUrl #written_data.uploads + fileUrl if written_data.uploads else fileUrl
    # if filedata:
    #     fd_json = json.loads(filedata)
    #     fd_list = list(fd_json["files_data"])
    #     for fd in fd_list:
    #         try:
    #             filedoc = save_file(fname=fd["filename"], content=fd["dataurl"],dt="Written Activity", dn=written_data.name, decode=True, is_private=1)
    #             frappe.db.commit()
    #             written_data.upload = filedoc.file_url
    #         except:
    #             if check_existing:
    #                 pass
    #             else:
    #                 frappe.delete_doc("Written Activity", written_data.name,ignore_permissions=True)
    #                 frappe.db.commit()
    #
    #             frappe.throw("File upload was not successful")



    if doctype == "Article":
        article_info = frappe.get_doc("Article", work)
        written_data.quarter = article_info.quarter
        written_data.school_year = article_info.school_year
        written_data.title = work_title
        written_data.subject = course
        written_data.student = student
        written_data.save(ignore_permissions=True)

        frappe.db.commit()

    else:
        article_info = frappe.get_doc("Video", work)
        written_data.quarter = article_info.quarter
        written_data.school_year = article_info.school_year
        written_data.subject = course
        written_data.title = work_title
        written_data.student = student
        written_data.save(ignore_permissions=True)

        frappe.db.commit()

@frappe.whitelist()
def attach_file_to_project_old(filedata, work,title,work_title, student,doctype, course):
    sql_check_grade = frappe.db.sql(
        """Select grade,name from `tabWritten Activity` WHERE activity = %s AND owner = %s""",(title, student))

    if sql_check_grade != ():
        if sql_check_grade[0][0] > 0:
            frappe.msgprint('Unable to Save. Grade Already Added')
        else:
            #no grade update work
            written_data = frappe.get_doc("Written Activity",sql_check_grade[0][1])

    else:

        if doctype == "Article":
            work = work.replace("'","\\'")
            work_title = work_title.replace("'","\\'")
            course = course.replace("'","\\'")
            check_existing = frappe.get_list("Written Activity", fields=["name"] , filters={"activity": work, "title": work_title, "subject":course })


            if check_existing:
                written_data = frappe.get_doc("Written Activity", check_existing[0]['name'])
            else:
                written = {
                    "doctype": "Written Activity",
                    "activity": work,
                    "title":work_title,
                    "subject": course,
                    # "upload": file_name,
                    "student": student
                }
                written_data = frappe.get_doc(written)
                written_data.insert(ignore_permissions=True)
                frappe.db.commit()
        else:
            work = work.replace("'", "\\'")
            work_title = work_title.replace("'", "\\'")
            course = course.replace("'", "\\'")
            check_existing = frappe.get_list("Written Activity", fields=["name"] , filters={"video": work, "title": work_title, "subject":course })
            if check_existing:
                written_data = frappe.get_doc("Written Activity", check_existing[0]['name'])
            else:
                written = {
                    "doctype": "Written Activity",
                    "video": work,
                    "title": work_title,
                    "subject": course,
                    # "upload": file_name,
                    "student": student
                }

                written_data = frappe.get_doc(written)
                written_data.insert(ignore_permissions=True)

                frappe.db.commit()

    if filedata:
        fd_json = json.loads(filedata)
        fd_list = list(fd_json["files_data"])
        for fd in fd_list:
          filedoc = save_file(fname=fd["filename"], content=fd["dataurl"],
              dt="Written Activity", dn=written_data.name, decode=True, is_private=1)

          frappe.db.commit()

          written_data.upload = filedoc.file_url

    if doctype == "Article":
        article_info = frappe.get_doc("Article", work)
        written_data.quarter = article_info.quarter
        written_data.school_year = article_info.school_year

        written_data.save(ignore_permissions=True)

        frappe.db.commit()

    else:
        article_info = frappe.get_doc("Video", work)
        written_data.quarter = article_info.quarter
        written_data.school_year = article_info.school_year

        written_data.save(ignore_permissions=True)

        frappe.db.commit()


#bench --site holycrossofmintal.silid.co execute lms_api.silid.attach_file.fix_files
#bench --site staging-hcm.silid.co execute lms_api.silid.attach_file.fix_files
def fix_files():
    for upload in frappe.db.sql("""SELECT name,upload FROM `tabWritten Activity`"""):
        file_upload = frappe.db.sql("""SELECT name,file_name,file_url,modified FROM `tabFile` WHERE file_url=%s ORDER BY modified DESC""",(upload[1]))
        if file_upload != ():
            frappe.db.sql("""UPDATE `tabFile` SET attached_to_name = %s WHERE name = %s""",(upload[0],file_upload[0][0]))
            frappe.db.commit()
