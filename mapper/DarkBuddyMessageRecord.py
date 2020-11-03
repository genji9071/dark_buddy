# !/usr/bin/env python
# coding=utf-8

from mapper.DarkBuddyCommonMapper import DarkBuddyCommonMapper


def insert_message_record(message_record):
    with DarkBuddyCommonMapper() as mapper:
        sql = "insert into `dark_buddy_message_record` (`user_id`, `message`, `create_time`) VALUES ({0}, '{1}', now())".format(
            message_record['user_id'], message_record['message'])
        mapper.cursor.execute(sql)


def select_word_frequency():
    with DarkBuddyCommonMapper() as mapper:
        sql = """select message, count(message) as `count` from dark_buddy_message_record where message not like '**%' and message not like '%:%' and message not like '开启%' group by message order by count(message) desc limit 300"""
        return mapper.cursor.execute(sql).fetchall()
