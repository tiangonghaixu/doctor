CREATE TABLE `ask_img` (
  `id`          INT(11)           NOT NULL AUTO_INCREMENT
  COMMENT 'id,自增',
  `img_url`     VARCHAR(256)               DEFAULT ''
  COMMENT '图片url',
  `ask_id`      INT(11) DEFAULT 0 NOT NULL
  COMMENT '问题id',
  `sort`        INT(11) DEFAULT 0 NULL
  COMMENT '排序越大越靠前',
  `del_flag`    INT(4)            NOT NULL DEFAULT '0',
  `create_time` TIMESTAMP         NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` TIMESTAMP         NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `ask_id` (`ask_id`) USING BTREE
)
  ENGINE = MyISAM
  DEFAULT CHARSET = utf8
  ROW_FORMAT = DYNAMIC
  COMMENT = 'ASK 的图片表';
