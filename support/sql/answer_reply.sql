CREATE TABLE `answer_reply` (
  `id`          BIGINT(20)        NOT NULL AUTO_INCREMENT
  COMMENT '回答id,自增',
  `ask_id`      INT(11) DEFAULT 0 NOT NULL
  COMMENT '问题id',
  `answer_id`   INT(11) DEFAULT 0 NOT NULL
  COMMENT '回答id',
  `user_id`     INT(11) DEFAULT 0 NOT NULL
  COMMENT '用户id',
  `user_name`   INT(11)                    DEFAULT 0
  COMMENT '用户名字，冗余处理',
  `content`     VARCHAR(256)               DEFAULT ''
  COMMENT '回复内容',
  `del_flag`    INT(4)            NOT NULL DEFAULT '0',
  `create_time` TIMESTAMP         NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` TIMESTAMP         NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`) USING BTREE,
  KEY `ask_id` (`ask_id`) USING BTREE,
  KEY `answer_id` (`answer_id`) USING BTREE
)
  ENGINE = MyISAM
  DEFAULT CHARSET = utf8
  ROW_FORMAT = DYNAMIC
  COMMENT = 'Answer回复表';

