import pymysql

from config.DataSoure import host, port_mysql, user_mysql, password_mysql, db_mysql


class DarkBuddyCommonMapper():

    def __init__(self, *lock_table):
        self.conn = None
        self.cursor = None
        self.lock_table = lock_table
        self.connect()



    def connect(self):
        self.conn = pymysql.connect(
            host=host,
            port=port_mysql,
            user=user_mysql,
            passwd=password_mysql,
            db=db_mysql
        )
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 关闭数据库cursor和连接
    def close(self, exception):
        if exception:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.cursor.execute('unlock tables')
        self.cursor.close()
        self.conn.close()

    # 进入with语句自动执行
    def __enter__(self):
        if self.lock_table:
            for table in self.lock_table:
                self.cursor.execute('lock tables {0} write'.format(table))
        return self

    # 退出with语句块自动执行
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close(exc_val)
