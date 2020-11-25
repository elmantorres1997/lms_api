import frappe

@frappe.whitelist()
def download(filename, is_private):

    #/private/files/Grade 3 Mapagmahal Class Schedule.pdf


    frappe.response.filename = filename
    # public_path = frappe.get_site_path("public", "files")
    # private_path = frappe.get_site_path("private", "files")
    # if is_private == "true":
    #     filepath = private_path + f"/{filename}"
    # else:
    #     filepath = public_path + f"/{filename}"
    filepath = frappe.utils.get_bench_path() + "/sites/"+frappe.local.site
    # filepath = frappe.utils.get_files_path(is_private=is_private) + f"/{filename}"

    if is_private == "true":
        # filepath = filepath + f"/private/files/{filename}"
        filepath = filepath + f"{filename}"
    else:
        filepath = filepath + f"/public/{filename}"

    with open(filepath, "r+b") as fileobj:
        filedata = fileobj.read()
    frappe.response.filecontent = filedata
    frappe.response.type = "download"
    return frappe.response