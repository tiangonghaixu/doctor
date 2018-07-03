# coding=utf-8
from common import errcode
from dao.ask.ask_dao import AskDao
from dao.ask.ask_img_dao import AskImgDao
from dao.user.user_dao import UserDao
from handlers.base.base_handler import BaseHandler


class GetAskListHandler(BaseHandler):
    methods = ['POST']

    def __init__(self):
        expect_request_para = {
            "page_num": None,
            "page_size": None,
            "common_param": {},
        }
        need_para = (
            "page_num",
            "page_size",
            "common_param",
        )
        super(GetAskListHandler, self).__init__(expect_request_para, need_para)

    def _process_imp(self):
        asks = AskDao.get_by_page(self.para_map["page_num"], self.para_map["page_size"])

        for ask in asks:
            # 获取问题的提问用户
            user = UserDao.get_by_id(ask["user_id"])
            ask["user"] = user

            # 获取问题的图片
            ask_imgs = AskImgDao.get_by_askid(ask["id"])
            ask["imgs"] = ask_imgs

        self.ret_code = errcode.NO_ERROR
        self.ret_msg = 'ok'
        self.ret_data = asks

        return
