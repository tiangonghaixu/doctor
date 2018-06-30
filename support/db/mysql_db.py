# coding: utf8
import threading

import MySQLdb
import MySQLdb.cursors

from common import config
from common import constant
from common import mylog
from myutil import config_tool

logger = mylog.logger


class DBConnection(object):
    def __init__(self, dbs_read, dbs_write=None):
        # logger.debug("will create db instance, callstack:%s", detailtrace())
        print "will create db instance, callstack:>>>>>>>>>", dbs_read, dbs_write

        self.db_source_read = dbs_read
        self.db_source_write = dbs_write
        self.cf_read = config_tool.get_db_conf(self.db_source_read)
        self.cf_write = config_tool.get_db_conf(self.db_source_write)

        try:  # 读连接
            self.lock_obj_read = threading.Lock()
            self.conn_read = MySQLdb.connect(host=self.cf_read['host'], port=self.cf_read['port'],
                                             user=self.cf_read['user'], passwd=self.cf_read['password'],
                                             charset=self.cf_read['charset'], cursorclass=MySQLdb.cursors.DictCursor)
            self.conn_read.autocommit(1)
        except MySQLdb.Error, ex:
            logger.error(ex, exc_info=1)
            self.conn_read = None
            logger.error("connect db conn_read(%s) Error %d: %s", str(self.cf_read), ex.args[0], ex.args[1])
            raise Exception("DBConnection init failed because of read conn.")
        try:  # 同步写连接
            self.lock_obj_write = threading.Lock()
            self.conn_write = MySQLdb.connect(host=self.cf_write['host'], port=self.cf_write['port'],
                                              user=self.cf_write['user'], passwd=self.cf_write['password'],
                                              charset=self.cf_write['charset'], cursorclass=MySQLdb.cursors.DictCursor)
            self.conn_write.autocommit(1)
        except MySQLdb.Error, ex:
            logger.error(ex, exc_info=1)
            self.conn_write = None
            if self.conn_read:  # 注意释放读连接
                self.conn_read.close()
            logger.error("connect db conn_write(%s) Error %d: %s", str(self.cf_write), ex.args[0], ex.args[1])
            raise Exception("DBConnection init failed  because of write conn.")

        print "create db instance ok....."

    def __del__(self):
        if self.conn_read is not None:
            self.conn_read.close()
            self.conn_read = None
        if self.conn_write is not None:
            self.conn_write.close()
            self.conn_write = None
        if self.conn_write_async is not None:
            self.conn_write_async.close()
            self.conn_write_async = None

    def reconnect_db(self, _type):
        """
        重新连接db
        :param _type:
        :return:
        """
        if _type != constant.CONN_READ and _type != constant.CONN_WRITE:
            return False
        if _type == constant.CONN_READ:
            try:
                if self.conn_read is not None:
                    self.conn_read.close()
                self.conn_read = MySQLdb.connect(host=self.cf_read['host'], port=self.cf_read['port'],
                                                 user=self.cf_read['user'], passwd=self.cf_read['password'],
                                                 charset=self.cf_read['charset'],
                                                 cursorclass=MySQLdb.cursors.DictCursor)
            except MySQLdb.Error, e:
                logger.error("reconnect db conn_read(%s) Error %d: %s", str(self.cf_read), e.args[0], e.args[1])
                self.conn_read = None
            return self.conn_read is not None
        elif _type == constant.CONN_WRITE:
            try:
                if self.conn_write is not None:
                    self.conn_write.close()
                self.conn_write = MySQLdb.connect(host=self.cf_write['host'], port=self.cf_write['port'],
                                                  user=self.cf_write['user'], passwd=self.cf_write['password'],
                                                  charset=self.cf_write['charset'],
                                                  cursorclass=MySQLdb.cursors.DictCursor)
            except MySQLdb.Error, e:
                logger.error("reconnect db conn_write(%s) Error %d: %s", str(self.cf_write), e.args[0], e.args[1])
                self.conn_write = None
            return self.conn_write is not None

    def is_connect_living(self, _type):
        """
        判断连接是否存活...
        :param _type:
        :return:
        """
        try:
            if _type == constant.CONN_READ:
                self.conn_read.ping(True)
                return True
            elif _type == constant.CONN_WRITE:
                self.conn_write.ping(True)
                return True
            else:
                return False
        except Exception, ex:
            logger.error(ex, exc_info=1)
            logger.error("is_connect_living judge failed. _type:%s" % _type)
            return False

    def fetchone(self, sql, *args):
        """
        只返回一个数据item

        遇到异常：
            我们先抓住异常后，关掉游标和释放锁，然后再raise，最终不hold住异常
        :param sql:
        :param args:
        :return:
        """
        if sql.split()[0].upper() not in ("SELECT", "SHOW", "EXPLAIN", "DESC"):
            logger.error(
                'only <select> can be called function query(), statement <update> need call function exec_sql()')
            raise Exception(
                'only <select> can be called function query(), statement <update> need call function exec_sql()')

        cursor = None
        try:
            conn_available = True
            sql_result = None
            self.lock_obj_read.acquire()
            if not self.is_connect_living(constant.CONN_READ):
                logger.error("[db_source_read:%s] connect gone away, try to reconnect.", self.db_source_read)
                conn_available = self.reconnect_db(constant.CONN_READ)
            if conn_available:
                if config.SQL_TRACE_ENABLE:
                    logger.debug(sql)

                cursor = self.conn_read.cursor()
                cursor.execute(sql, args)
                items = cursor.fetchall()
                if items:
                    sql_result = items[0]
            return sql_result
        except Exception, e:
            logger.error("[db_source_read:%s] query sql(%s) error:%s", self.db_source_read, str(sql), str(e))
            raise e
        finally:
            if cursor:
                cursor.close()
            self.lock_obj_read.release()

    def fetchall(self, sql, *args):
        """
        返回一个列表

        遇到异常：
            我们先抓住异常，关掉游标和释放锁，然后再raise，最终不hold住异常
        :param sql:
        :param args:
        :return:
        """
        if sql.split()[0].upper() not in ("SELECT", "SHOW", "EXPLAIN", "DESC"):
            logger.error(
                'only <select> can be called function query(), statement <update> need call function exec_sql()')
            raise Exception(
                'only <select> can be called function query(), statement <update> need call function exec_sql()')

        cursor = None
        try:
            sql_result = []
            conn_available = True
            self.lock_obj_read.acquire()
            if not self.is_connect_living(constant.CONN_READ):
                logger.error("[db_source_read:%s] connect gone away, try to reconnect.", self.db_source_read)
                conn_available = self.reconnect_db(constant.CONN_READ)
            if conn_available:
                if config.SQL_TRACE_ENABLE:
                    logger.debug(sql)

                cursor = self.conn_read.cursor()
                cursor.execute(sql, args)
                sql_result = cursor.fetchall()
                sql_result = list(sql_result)
            return sql_result
        except Exception, e:
            logger.error("[db_source_read:%s] query sql(%s) error:%s", self.db_source_read, str(sql), str(e))
            raise e
        finally:
            if cursor:
                cursor.close()
            self.lock_obj_read.release()

    def execute_sql(self, sql):
        """
        执行一条sql： insert、update、delete
        :param sql:
        :return:
        """
        cursor = None
        result = None
        conn_available = True
        try:
            self.lock_obj_write.acquire()
            if not self.is_connect_living(constant.CONN_WRITE):
                logger.error("[db_source_write:%s] connect gone away, try to reconnect", self.db_source_write)
                conn_available = self.reconnect_db(constant.CONN_WRITE)
            if conn_available:
                if config.SQL_TRACE_ENABLE:
                    logger.debug(sql)

                cursor = self.conn_write.cursor()
                cursor.execute(sql)

                if 'update' in sql or 'delete' in sql:  # 如果是单条update，则获取影响的行数
                    result = cursor.rowcount
                elif "insert" in sql:  # 否则，获取最后一次插入的id
                    sql_last_id = "select last_insert_id() as id"
                    cursor.execute(sql_last_id)
                    last_id_result = cursor.fetchall()
                    if len(last_id_result) > 0:
                        result = last_id_result[0]['id']
        except Exception, ex:
            logger.error("sql=%s" % sql)
            logger.error("[db_source_write:%s] exectue error: %s !" % (self.db_source_write, ex), exc_info=1)
            raise
        finally:
            if cursor is not None:
                cursor.close()
            self.lock_obj_write.release()
        return result


doctor_conn = DBConnection(dbs_read='doctor_read', dbs_write='doctor_write')
doctor_user_conn = DBConnection(dbs_read='doctor_user_read', dbs_write='doctor_user_write')

# 斯芬克斯搜索引擎
# doctor_sphinx_conn = DBConnection(dbs_read='doctor_sphinx', dbs_write='doctor_sphinx')
