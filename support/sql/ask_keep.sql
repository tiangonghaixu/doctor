CREATE TABLE `ask_keep` (
  `id`          BIGINT(20)         NOT NULL AUTO_INCREMENT
  COMMENT '问题收藏id,自增',
  `ask_id`      INT(11) DEFAULT 0  NOT NULL
  COMMENT '问题id',
  `user_id`     INT(11) DEFAULT 0  NOT NULL
  COMMENT '用户id',
  `del_flag`    INT(4)             NOT NULL DEFAULT '0',
  `create_time` TIMESTAMP          NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` TIMESTAMP          NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`) USING BTREE,
  KEY `ask_id` (`ask_id`) USING BTREE
)
  ENGINE = MyISAM
  DEFAULT CHARSET = utf8
  ROW_FORMAT = DYNAMIC
  COMMENT = 'ASK收藏表';