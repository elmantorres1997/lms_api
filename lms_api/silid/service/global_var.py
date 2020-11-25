# import frappe
# import os
#
# if not os.path.exists('csrf'):
#     os.makedirs('csrf')
#
# def get_stored_csrf(user):
#     user = user.replace("@", "").replace(".", "")
#     filename = f"csrf/{user}_csrf.txt"
#     try:
#         f = open(filename, "r")
#         return f.read()
#     except:
#         f = open(filename, "w+")
#         return ""
#
# def change_store_csrf(user,new_csrf):
#     user = user.replace("@", "").replace(".", "")
#     filename = f"csrf/{user}_csrf.txt"
#     with open(filename, 'w') as filetowrite:
#         filetowrite.write(new_csrf)