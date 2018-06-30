# coding=utf-8
from common import errcode
from handlers.base.base_handler import BaseHandler
from support.db.mysql_db import doctor_conn
from support.redis.redis_helper import redis_conn


class LoginHandler(BaseHandler):
    methods = ['POST']

    def __init__(self):
        expect_request_para = {
            "phone": "",
            "code": "",
            "common_param": {},
        }
        need_para = (
            "phone",
            "code",
            "common_param",
        )
        super(LoginHandler, self).__init__(expect_request_para, need_para)

    def _process_imp(self):
        redis_item = redis_conn.get("a")
        print redis_item

        db_item = doctor_conn.fetchone("select 1")
        print db_item

        self.ret_code = errcode.NO_ERROR
        self.ret_msg = 'ok'
        self.ret_data = {"msg": "hello world!!!"}

        return
