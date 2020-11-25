import frappe

#lms_api.patches.topic_content.update_names
def update_names():
    for content in frappe.db.sql("""select name,content_type,content from `tabTopic Content`"""):
        print(content)

        try:
            doc = frappe.get_doc(content[1],content[2])

            frappe.db.sql("""update `tabTopic Content` set content_title=%s where name=%s""",(doc.title,content[0]))

        except:
            print("err")
            pass