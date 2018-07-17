# coding=utf-8
from common import errcode
from dao.user.user_status_dao import UserStatusDao
from handlers.base.base_handler import BaseHandler


class UserReportStatusHandler(BaseHandler):
    methods = ['POST']

    def __init__(self):
        expect_request_para = {
            "longitude": 118.78,
            "latitude": 32.04,
            "ip": "0.0.0.0",
            "open_push": 1,
            "province": "",
            "city": "",
            "area": "",
            "common_param": None,
        }
        need_para = (
            "longitude",
            "latitude",
            "common_param",
        )
        super(UserReportStatusHandler, self).__init__(expect_request_para, need_para)

    def _process_imp(self):
        UserStatusDao.insert(self.common_param["user_id"],
                             self.common_param["cuid"],
                             self.para_map["longitude"],
                             self.para_map["latitude"],
                             self.para_map["open_push"],
                             self.para_map["ip"],
                             self.para_map["province"],
                             self.para_map["city"],
                             self.para_map["area"],
                             )

        self.ret_code = errcode.NO_ERROR
        self.ret_msg = 'ok'
        return
