# coding=utf-8
from dao.base.base_dao import BaseDao
from support.db.mysql_db import doctor_conn


class UserDao(BaseDao):
    db_name = "doctor_user"
    table_name = "user"

    @classmethod
    def get_by_id(cls, user_id):
        """
        根据id获取用户

        :return:
        """

        sql = "select id, user_name, avatar, sex from {db}.{table} where del_flag=0 and id={user_id}". \
            format(db=cls.db_name,
                   table=cls.table_name,
                   user_id=user_id)

        item = doctor_conn.fetchone(sql)
        return item
