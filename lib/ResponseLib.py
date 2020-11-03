#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 响应通用异常
class ResponseLib:
    def __init__(self):
        self.ERROR_CODE = {
            "code": "1",
            "message": "",
            "result": None
        }
        self.SUCCESS_CODE = {
            "code": "0",
            "message": "success",
            "result": None
        }


response_lib = ResponseLib()
