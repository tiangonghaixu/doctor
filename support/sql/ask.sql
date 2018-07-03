CREATE TABLE `ask` (
  `id`          INT(11)           NOT NULL AUTO_INCREMENT
  COMMENT '问题id,自增',
  `title`       VARCHAR(256)               DEFAULT ''
  COMMENT '问题title',
  `content`     VARCHAR(2048)              DEFAULT ''
  COMMENT '问题内容',
  `user_id`     INT(11) DEFAULT 0 NOT NULL
  COMMENT '提问用户id',
  `like_num`    INT(11)                    DEFAULT 0
  COMMENT '点赞数，做冗余处理',
  `comment_num` INT(11)                    DEFAULT 0
  COMMENT '评论数，做冗余处理',
  `follow_num`  INT(11)                    DEFAULT 0
  COMMENT '关注数，做冗余处理',
  `keep_num`    INT(11)                    DEFAULT 0
  COMMENT '收藏数，做冗余处理',
  `sort`        INT(11) DEFAULT 0 NULL
  COMMENT '排序越大越靠前',
  `del_flag`    INT(4)            NOT NULL DEFAULT '0',
  `create_time` TIMESTAMP         NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` TIMESTAMP         NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`) USING BTREE
)
  ENGINE = MyISAM
  DEFAULT CHARSET = utf8
  ROW_FORMAT = DYNAMIC
  COMMENT = 'ASK 表';

