# !/usr/bin/env python
# coding=utf-8

from mapper.DarkBuddyCommonMapper import DarkBuddyCommonMapper


def select_by_statusId_and_userId(status_id, user_id):
    with DarkBuddyCommonMapper() as mapper:
        sql = "select * from dark_buddy_user_status where status_id = {0} and user_id = {1}".format(status_id, user_id)
        mapper.cursor.execute(sql)
        result = mapper.cursor.fetchall()
        if len(result):
            return result[0]
        else:
            return None


def select_by_statusCode_and_userId(status_code, user_id):
    with DarkBuddyCommonMapper() as mapper:
        sql = "select * from dark_buddy_user_status where status_code = '{0}' and user_id = {1}".format(status_code,
                                                                                                        user_id)
        mapper.cursor.execute(sql)
        result = mapper.cursor.fetchall()
        if len(result):
            return result[0]
        else:
            return None


def insert_user_status(user_status):
    with DarkBuddyCommonMapper() as mapper:
        sql = "insert into `dark_buddy_user_status` (`user_id`, `status_id`, `status_code`, `value`, `create_time`, `update_time`) VALUES ({0}, {1}, '{2}', '{3}', now(), now())".format(
            user_status['user_id'], user_status['status_id'], user_status['status_code'], str(user_status['value']))
        mapper.cursor.execute(sql)


def update_user_status(user_status):
    founded = select_by_statusId_and_userId(user_status['status_id'], user_status['user_id'])
    if not founded:
        return insert_user_status(user_status)
    if user_status.get('value'):
        founded['value'] = str(user_status['value'])
    with DarkBuddyCommonMapper() as mapper:
        sql = "update `dark_buddy_user_status` set `value`='{0}', `update_time`=now() where status_id = {1} and user_id = {2}".format(
            founded['value'], founded['status_id'], founded['user_id'])
        mapper.cursor.execute(sql)
    return founded
