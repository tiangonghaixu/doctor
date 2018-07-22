# coding=utf-8
from common import errcode
from common.mylog import logger
from dao.news.news_dao import NewsDao
from dao.news.news_img_dao import NewsImgDao
from dao.user.user_dao import UserDao
from handlers.base.base_handler import BaseHandler


class GetNewsByCategoryHandler(BaseHandler):
    methods = ['POST']

    def __init__(self):
        expect_request_para = {
            "category_id": None,
            "page_num": None,
            "page_size": None,
            "common_param": {},
        }
        need_para = (
            "category_id",
            "page_num",
            "page_size",
            "common_param",
        )
        super(GetNewsByCategoryHandler, self).__init__(expect_request_para, need_para)

    def _process_imp(self):
        news = NewsDao.get_by_category(self.para_map["category_id"],
                                       self.para_map["page_num"],
                                       self.para_map["page_size"])

        for new in news:
            # 图片
            imgs = NewsImgDao.get_by_news_id(new["id"])
            new["imgs"] = imgs

            # 作者
            author = UserDao.get_by_id(new["author_id"])
            logger.error("author= %s" % author)
            new["author"] = author if author else {}
            del new["author_id"]

        self.ret_code = errcode.NO_ERROR
        self.ret_msg = 'ok'
        self.ret_data = {"news": news}
        return
