# coding=utf-8
from common import errcode
from dao.news.news_category_dao import NewsCategoryDao
from handlers.base.base_handler import BaseHandler


class GetNewsCategoriesHandler(BaseHandler):
    methods = ['POST']

    def __init__(self):
        expect_request_para = {
            "common_param": {},
        }
        need_para = (
            "common_param",
        )
        super(GetNewsCategoriesHandler, self).__init__(expect_request_para, need_para)

    def _process_imp(self):
        categories = NewsCategoryDao.get_all()

        self.ret_code = errcode.NO_ERROR
        self.ret_msg = 'ok'
        self.ret_data = {"categories": categories}

        return
