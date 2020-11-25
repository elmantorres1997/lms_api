
import frappe

#bench --site ccs.silid.co execute path.to.script
@frappe.whitelist()
def amend_written_activity():
    # Patch for maam Sam
    need_to_amend = ['cdf16ccd7d', '837de77c69', 'd61594028e']
    try:
        for activity in need_to_amend:
            frappe.db.sql(
                f"UPDATE `tabWritten Activity` set program='Grade 8R - M' WHERE activity='{activity}'"
            )
    except:
        pass
