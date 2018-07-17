# coding=utf-8
from dao.base.base_dao import BaseDao
from support.db.mysql_db import doctor_user_conn


class UserStatusDao(BaseDao):
    db_name = "doctor_user"
    table_name = "user_status"

    @classmethod
    def insert(cls, user_id, cuid, longitude, latitude, open_push, ip, province, city, area):
        """
        插入用户状态

        :return:
        """
        print type(province)
        print type(city)
        print type(area)

        sql = """
              insert into {db}.{tbl}(user_id, cuid, longitude, latitude, open_push, ip, province, city, area) VALUES (
              '{user_id}', '{cuid}', {longitude}, {latitude}, {open_push}, '{ip}',
              '{province}', '{city}', '{area}') ON DUPLICATE KEY UPDATE longitude={longitude}, latitude={latitude},
              open_push={open_push}, ip='{ip}', province='{province}', city='{city}', area='{area}'
              """.format(db=cls.db_name,
                         tbl=cls.table_name,
                         longitude=longitude,
                         user_id=user_id,
                         cuid=cuid,
                         latitude=latitude,
                         open_push=open_push,
                         ip=ip,
                         province=province,
                         city=city,
                         area=area,
                         )

        doctor_user_conn.execute_sql(sql)
