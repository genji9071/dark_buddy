from mapper.DarkBuddyCommonMapper import DarkBuddyCommonMapper


def select_by_user_id(user_id):
    with DarkBuddyCommonMapper() as mapper:
        mapper.cursor.execute(
            "select * from dark_buddy_sweet_talk where user_id = {0}".format(user_id))
        records = mapper.cursor.fetchall()
        return records
