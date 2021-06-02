#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 日志包

import logging


class Logger:

    def __init__(self):
        # create logger
        logger = logging.getLogger('console')
        logger.setLevel(logging.DEBUG)

        # create console handler and set level
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)

        # log format
        _format = '%(asctime)s  %(levelname)s %(process)d --- [%(threadName)+15s] module.%(module)-20s : %(message)s'
        formatter = logging.Formatter(_format, datefmt='%Y-%m-%d %H:%M:%S.000')

        # set formatter
        handler.setFormatter(formatter)

        # set handler
        logger.addHandler(handler)
        self.logger = logger


log = Logger().logger
