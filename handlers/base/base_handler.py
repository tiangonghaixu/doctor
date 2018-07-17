# coding:utf-8
import json
import pickle
import time

from flask import jsonify
from flask import request
from flask.views import MethodView

from common import errcode
from common.mylog import logger
from support.redis.redis_helper import redis_conn, celery_broker_redis_conn


class BaseHandler(MethodView):
    def __init__(self, expect_request_para, need_para):
        """
        # 这是每个请求的公共参数如net、version
        "common_param": {
            "client": "android_7.0",
            "cuid": "ffffffff-f5c5-8962-ffff-ffff8a0d869e",
            "did": "479f4826-472d-4913-866d-e94cfc68418c",
            "flavor": "main",
            "network": 1,
            "utc": 1524299337188,
            "version": "1.4.4"
        }

        :param expect_request_para:
        :param need_para:
        """
        super(BaseHandler, self).__init__()

        t = time.time()
        self.trace_id = self.__class__.__name__ + str(int(round(t * 1000)))
        self.ret_data = {}
        self.ret_code = errcode.NO_ERROR
        self.ret_msg = "ok"
        self.ret_user_msg = None
        self.parse_from_body = True
        self.para_map = {}
        self.expected_para = expect_request_para
        self.required_para = need_para
        self.common_param = {}
        self.os = ""  # android 或者ios
        self.flavor = ""  # 渠道
        self.version = ""  # 版本

    def _handle_request(self, request):
        body = {}
        if self.parse_from_body:
            try:
                body = json.loads(request.data)

                # 统一打印下请求参数
                for key, value in body.iteritems():
                    if key == "common_param":
                        self.common_param = value
                        self.os = self.common_param["client"].split("_")[0]
                        self.app_version = self.common_param["app_version"]
                logger.debug(body)
            except Exception, ex:
                logger.error("[%s] request.body not json str, ex: %s", self.trace_id, ex, exc_info=1)
                self.ret_code = errcode.JSON_BODY_DECODE_ERROR
                self.ret_msg = "request.body not json str"
                return False

        return self._parse_parameters(request, body)

    def _parse_parameters(self, request, body):
        for key, default_value in self.expected_para.iteritems():
            value = body.get(key, default_value)
            if isinstance(value, unicode):
                value = value.encode("utf-8")
            self.para_map[key] = value
        if request.cookies:
            for key, default_value in self.expected_para.iteritems():
                value = request.cookies.get(key, default_value)
                if value != default_value:
                    self.para_map[key] = value
        return self._check_parameters()

    def _check_parameters(self):
        for key in self.required_para:
            if self.para_map[key] is None:
                logger.error("request param is blank：%s" % key)
                self.ret_code = errcode.PARAM_REQUIRED_IS_BLANK
                self.ret_msg = "request param is blank"
                return False
        return True

    def _return_map(self):
        ret_map = {
            "ret": self.ret_code,
            "msg": self.ret_msg
        }
        if self.ret_data:
            ret_map["data"] = self.ret_data
        else:
            ret_map["data"] = {}
        if self.ret_user_msg:
            ret_map["user_msg"] = self.ret_user_msg
        return ret_map

    def _construct_cache_key(self):
        """
        子类可返回具体key, 过期时间
        :return: (key, expire_seconds)
        """
        return None, None

    def _try_read_cache(self):
        """
        尝试从缓存获取数据
        :return:
        """
        # 如果redis挂了，则直接返回False
        if not redis_conn.readable():
            return False

        cache_key, expire_seconds = self._construct_cache_key()
        if cache_key:
            cache_str = redis_conn.get(cache_key)
            if cache_str:
                logger.info("走缓存, key=%s" % cache_key)
                self.ret_code = errcode.NO_ERROR
                self.ret_msg = "ok."
                self.ret_data = pickle.loads(cache_str)
                return True

        return False

    def _try_write_cache(self):
        """
        尝试写返回数据到缓存中...
        :return:
        """
        # 如果redis挂了，则直接返回False
        if not redis_conn.writeable():
            return False

        key, expire_seconds = self._construct_cache_key()
        if key:
            logger.info("设置redis,key=%s, 过期时间=%ss" % (key, expire_seconds))
            redis_conn.set(key, pickle.dumps(self.ret_data))
            redis_conn.expire(key, expire_seconds)
        return True

    def _process_imp(self):
        logger.critical("need implement!!")
        pass

    def _handle_return(self):
        ret_map = self._return_map()
        logger.debug("[%s ###### END] 返回值: code=%s, msg=%s", self.trace_id, ret_map['ret'], ret_map['msg'])
        return jsonify(ret_map)

    def _stat(self):
        """
        每个接口自己实现相关的统计代码
        :return:
        """
        pass

    def _version_control(self):
        """
        每个接口实现自己的版本控制
        :return:
        """
        pass

    def post(self):
        self.request = request
        logger.debug("[%s ###### START]", self.trace_id)

        ret = self._handle_request(self.request)
        if ret is False:
            return self._handle_return()

        # 统计，先判断redis_broker存在否
        # 否则强行调用会导致程序block住
        if celery_broker_redis_conn.writeable():
            self._stat()

        # 读到cache就直接返回
        # if self._try_read_cache():
        #     return self._handle_return()

        # 在最上层处理异常
        try:
            self._version_control()
            self._process_imp()
        except Exception, ex:
            logger.error(ex, exc_info=1)
            self.ret_code = errcode.DB_OPERATION_ERROR
            self.ret_msg = "operation error"

        # # 尝试写 redis 缓存
        # self._try_write_cache()

        return self._handle_return()

    def _output_error(self, name):
        logger.error("不正确的参数：%s=%s" % (name, self.para_map[name]))
        self.ret_code = errcode.PARAMETER_ERROR
        self.ret_msg = "invalid parameter: %s" % name
