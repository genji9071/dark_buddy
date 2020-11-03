from mapper.DarkBuddyCommonMapper import DarkBuddyCommonMapper


def select_all():
    with DarkBuddyCommonMapper() as mapper:
        mapper.cursor.execute("select * from dark_buddy_dark_spy_words where status = 0")
        total_words = mapper.cursor.fetchall()
        return total_words
