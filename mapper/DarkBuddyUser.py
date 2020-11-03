# !/usr/bin/env python
# coding=utf-8

from mapper.DarkBuddyCommonMapper import DarkBuddyCommonMapper


def select_by_senderId(sender_id):
    with DarkBuddyCommonMapper() as mapper:
        sql = "select * from dark_buddy_user where sender_id = '{0}'".format(sender_id)
        mapper.cursor.execute(sql)
        result = mapper.cursor.fetchall()
        if len(result):
            return result[0]
        else:
            return None


def select_by_name(name):
    with DarkBuddyCommonMapper() as mapper:
        sql = "select * from dark_buddy_user where name = '{0}'".format(name)
        mapper.cursor.execute(sql)
        result = mapper.cursor.fetchall()
        if len(result):
            return result[0]
        else:
            return None


def insert_user(user):
    with DarkBuddyCommonMapper() as mapper:
        sql = "insert into `dark_buddy_user` (`sender_id`, `name`, `create_time`, `update_time`) VALUES ('{0}', '{1}', now(), now())".format(
            user['sender_id'], user['name'])
        mapper.cursor.execute(sql)


def update_user(user):
    founded = select_by_senderId(user['sender_id'])
    if not founded:
        return insert_user(user)
    if user.get('name'):
        founded['name'] = user['name']
    if user.get('status'):
        founded['status'] = user['status']
    with DarkBuddyCommonMapper() as mapper:
        sql = "update `dark_buddy_user` set `name`='{0}', `status`={1}, `update_time`=now() where `sender_id`='{2}'".format(
            user['name'], user['status'], user['sender_id'])
        mapper.cursor.execute(sql)
    return founded
