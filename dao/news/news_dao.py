# coding=utf-8
from dao.base.base_dao import BaseDao
from support.db.mysql_db import doctor_conn


class NewsDao(BaseDao):
    db_name = "doctor"
    table_name = "news"

    @classmethod
    def get_by_category(cls, category_id, page_num, page_size):
        """
        根据分类获取news
        :param category_id:
        :param page_num:
        :param page_size:
        :return:
        """
        sql = """
              select id, title, content, author_id, comment_num, follow_num, keep_num, like_num,
              UNIX_TIMESTAMP(create_time) as create_time, UNIX_TIMESTAMP(update_time) as update_time from {db}.{tbl}
              where id in
              (select id from {db}.{category_map_tbl} where category_id={category_id}) limit {offset}, {page_size}
            """.format(db=cls.db_name,
                       tbl=cls.table_name,
                       category_map_tbl="news_category_map",
                       category_id=category_id,
                       offset=(int(page_num) - 1) * page_size,
                       page_size=page_size

                       )
        items = doctor_conn.fetchall(sql)
        return items
