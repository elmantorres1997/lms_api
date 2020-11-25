import frappe

@frappe.whitelist()
def video_tool():
    print("hello")
    return frappe.db.get_single_value('Wela Settings', 'video_tool')
