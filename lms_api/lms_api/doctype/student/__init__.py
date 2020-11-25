import frappe


@frappe.whitelist()
def update_student_info(first_name, middle_name, last_name, date_of_birth, gender, address_line_1, nationality, city,
                        state, student_mobile_number, student_email):
    # full_name
    try:
        student_id = get_student_user_fullname(first_name, last_name)
        student = frappe.get_doc("Student", student_id)
        student.first_name = clean_name(first_name) if len(student.first_name) <= 3 else student.first_name
        student.middle_name = student.middle_name or clean_name(middle_name)
        student.last_name = student.last_name or clean_name(last_name)
        student.date_of_birth = student.date_of_birth or date_of_birth
        student.gender = student.gender or gender
        student.address_line_1 = student.address_line_1 or address_line_1
        student.nationality = student.nationality or nationality
        student.city = student.city or city
        student.state = student.state or state
        student.student_mobile_number = student.student_mobile_number or number_fix(student_mobile_number)
        student.student_alt_email = student_email
        student.save(ignore_permissions=True)
        frappe.db.commit()
    except Exception as e:
        pass

    # Initials
    try:
        student_id = get_student_initials(first_name, last_name)
        student = frappe.get_doc("Student", student_id)
        student.first_name = clean_name(first_name) if len(student.first_name) <= 3 else student.first_name
        student.middle_name = student.middle_name or clean_name(middle_name)
        student.last_name = student.last_name or clean_name(last_name)
        student.date_of_birth = student.date_of_birth or date_of_birth
        student.gender = student.gender or gender
        student.address_line_1 = student.address_line_1 or address_line_1
        student.nationality = student.nationality or nationality
        student.city = student.city or city
        student.state = student.state or state
        student.student_mobile_number = student.student_mobile_number or number_fix(student_mobile_number)
        student.student_alt_email = student_email
        student.save(ignore_permissions=True)
        frappe.db.commit()
        return "Success"
    except Exception as e:
        return "No Student Found"


def get_student_user_fullname(first_name, last_name):
    student_email = user_full(first_name, last_name)
    student_info = frappe.get_all("Student", {"user": student_email}, ["name"])
    if student_info:
        return student_info[0].name
    else:
        raise Exception("No Student Found")


def get_student_initials(first_name, last_name):
    student_email = user_initial(first_name, last_name)
    student_info = frappe.get_all("Student", {"user": student_email}, ["name"])
    if len(student_info) == 1:
        return student_info[0].name
    else:
        raise Exception(f"Two Students with same Initials")


def user_full(first_name, last_name):
    first_name_ = first_name
    if first_name:
        first_name_ = clean_email(first_name_)
    last_name_ = last_name
    if last_name:
        last_name_ = clean_email(last_name_)
    name_ = last_name_.replace(" ", "") + first_name_.replace(" ", "") + "@wela.online"
    return name_.lower()


def user_initial(first_name, last_name):
    first_name_ = first_name
    if first_name:
        first_name_ = clean_email(first_name_)
        first_name_ = get_initials(first_name_)
    last_name_ = last_name
    if last_name:
        last_name_ = clean_email(last_name_)
    name_ = last_name_.replace(" ", "") + first_name_.replace(" ", "") + "@wela.online"
    return name_.lower()


def get_initials(first_name):
    if first_name:
        return "".join([i[0] for i in first_name.split()])
    return first_name


def clean_name(text):
    if text:
        return text.strip().replace("ñ", "n").replace("Ñ", "N").replace(",", "").replace(".", "").replace("'",
                                                                                                          "").title()
    return text


def clean_email(text):
    if text:
        return text.strip().replace("ñ", "n").replace("Ñ", "N").replace(",", "").replace(".", "")
    return text


def number_fix(student_mobile_number):
    if student_mobile_number:
        if student_mobile_number[0] == "0":
            return "63" + student_mobile_number[1:]

    return student_mobile_number
