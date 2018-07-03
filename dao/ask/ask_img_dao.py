# coding=utf-8
from dao.base.base_dao import BaseDao
from support.db.mysql_db import doctor_conn


class AskImgDao(BaseDao):
    db_name = "doctor"
    table_name = "ask_img"

    @classmethod
    def get_by_askid(cls, ask_id):
        """
        根据ask_id获取图片列表

        :return:
        """
        sql = "select img_url from {db}.{table} where del_flag=0 and ask_id={ask_id} order by sort desc ". \
            format(db=cls.db_name,
                   table=cls.table_name,
                   ask_id=ask_id)

        item_list = doctor_conn.fetchall(sql)
        return item_list
