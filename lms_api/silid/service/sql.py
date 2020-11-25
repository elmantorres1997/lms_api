# -*- coding: utf-8 -*-
# Filter
import frappe
from frappe.service.queries import *


def filter_query(filters=None, sql_query=""):
    if "GROUP BY" in sql_query:
        sql_query += " Having "
    else:
        sql_query += " Where "
    if len(filters) > 0:
        for attribute, value in filters.items():
            value = value.replace("'", "\\'")
            sql_query += f"{attribute} LIKE '%{value}%' AND "
    else:
        sql_query += "1"
    sql_query = sql_query.strip("AND ")
    return sql_query

def filter_array_query(filter_array=None, sql_query=""):
    if "GROUP BY" in sql_query:
        sql_query += " Having "
    else:
        sql_query += " Where "

    for filters in filter_array:
        for attribute, value in filters.items():
            value = value.replace("'","\\'")
            sql_query += f"{attribute} LIKE '%{value}%' OR "

    sql_query = sql_query.strip("OR ")
    print(sql_query)
    return sql_query

def pagination_query(offset, limit, sql_query=""):
    sql_query += f" LIMIT {offset},{limit} "
    return sql_query

def limit_query(limit, sql_query=""):
    sql_query += f" LIMIT {limit} "
    return sql_query

def group_by_query(field_name, sql_query=""):
    sql_query += f" GROUP BY {field_name} "
    return sql_query

def order_by_query(order_by, sql_query=""):
    sql_query += f" ORDER BY {order_by} "
    return sql_query

def execute_query(query_name, filters=None, filter_arrays=None, group_by=None, as_dict=None, limit=None, offset=None, order_by=None):
    base_query = get_query(query_name)

    if filter_arrays is not None and len(filter_arrays) != 0:
        base_query = filter_array_query(filter_arrays, base_query)
    if filters is not None and len(filters) !=0:
        base_query = filter_query(filters, base_query)
    if group_by is not None:
        base_query = group_by_query(group_by, base_query)
    if order_by is not None:
        base_query = order_by_query(order_by, base_query)
    if limit is not None and offset is None:
        base_query = limit_query(limit, base_query)
    if offset is not None and limit is not None:
        base_query = pagination_query(offset, limit, base_query)


    print(base_query)
    if as_dict is not None:
        return frappe.db.sql(base_query, as_dict=as_dict)

    return frappe.db.sql(base_query)