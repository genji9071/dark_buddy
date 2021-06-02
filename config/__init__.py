# coding=utf-8
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone, timedelta

from redis import Redis

from config.DataSoure import host, port_mysql, user_mysql, password_mysql, db_mysql, password_redis, port_redis

# 机器人部署时的ip地址，或者域名
public_ip = 'www.darkbuddy.cn'

# 统一使用一个线程池，核数根据实际情况调节
dark_show_hand_thread_pool = ThreadPoolExecutor(max_workers=8)


# redis实例
redis = Redis(host, port_redis, password=password_redis)

# 当前时间实例
tzutc_8 = timezone(timedelta(hours=8))
now_date = datetime.utcnow().astimezone(tzutc_8)
