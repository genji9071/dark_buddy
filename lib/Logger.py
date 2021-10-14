#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 日志包

import logging


class Logger:

    def __init__(self):
        # create logger
        self.logger = logging.getLogger('console')
        self.engineio_server = logging.getLogger('engineio.server')
        self.engineio_server.setLevel('ERROR')


logger_instance = Logger()
log = logger_instance.logger
socketio_log = logger_instance.engineio_server
