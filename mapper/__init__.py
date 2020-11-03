import mapper.DarkBuddyMessageRecord as mapper_message_record
import mapper.DarkBuddyUser as mapper_user
import mapper.DarkBuddyUserStatus as mapper_user_status
import mapper.DarkBuddyUserStatusProperty as mapper_user_status_property
from config import db

db.generate_mapping()