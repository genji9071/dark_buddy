# !/usr/bin/env python
# coding=utf-8
from mapper.DarkBuddyCommonMapper import DarkBuddyCommonMapper


def select_by_name(name):
    with DarkBuddyCommonMapper() as mapper:
        sql = "select * from dark_buddy_user_status_property where name = '{0}'".format(name)
        mapper.cursor.execute(sql)
        result = mapper.cursor.fetchall()
        if len(result):
            return result[0]
        else:
            return None


def select_all():
    with DarkBuddyCommonMapper() as mapper:
        sql = "select * from dark_buddy_user_status_property"
        mapper.cursor.execute(sql)
        return mapper.cursor.fetchall()
