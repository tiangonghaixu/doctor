# coding=utf-8
from dao.base.base_dao import BaseDao
from support.db.mysql_db import doctor_conn


class NewsCategoryDao(BaseDao):
    db_name = "doctor"
    table_name = "news_category"

    @classmethod
    def get_all(cls):
        """
        获取全部分类列表
        :return:
        """
        sql = "select id,`name` from {db}.{tbl} where del_flag=0 order by sort desc".format(db=cls.db_name,
                                                                                            tbl=cls.table_name)
        items = doctor_conn.fetchall(sql)
        return items
