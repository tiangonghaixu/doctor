# URL请求
```
http://47.106.101.39/v1/ask/get_list
```

# 方法:
```
POST
```

# 参数：
```
page_num: int, 页面数，默认是1
page_size, int, 每一页item数，默认是10
```

# 返回：
```
{
    "data": [
        {
            "comment_num": 2000,
            "content": "啊，长得太帅导致生活总被人打扰怎么办？",
            "create_time": "Tue, 03 Jul 2018 09:45:17 GMT",
            "del_flag": 0,
            "follow_num": 300,
            "id": 1,
            "imgs": [
                {
                    "img_url": "http://images2.vnstory.xyz/vnstory/34/d2/34d2f4a1b16978f9087b51533d198af1.jpeg"
                },
                {
                    "img_url": "http://images2.vnstory.xyz/vnstory/34/d2/34d2f4a1b16978f9087b51533d198af1.jpeg"
                }
            ],
            "keep_num": 4000,
            "like_num": 1000,
            "sort": 0,
            "title": "测试问题1",
            "update_time": "Tue, 03 Jul 2018 09:45:17 GMT",
            "user": {
                "avatar": "http://images2.vnstory.xyz/vnstory/62/cb/62cb0ce19962cb50bfb0262586807e1d.jpeg",
                "id": 1,
                "sex": 1,
                "user_name": "国哥"
            },
            "user_id": 1
        },
        {
            "comment_num": 666,
            "content": "学习总是进步神速怎么办？感觉和别人格格不入！！！",
            "create_time": "Tue, 03 Jul 2018 09:45:17 GMT",
            "del_flag": 0,
            "follow_num": 322,
            "id": 2,
            "imgs": [
                {
                    "img_url": "http://images.vnstory.xyz/vnstory/rs/z_/rsz_f14fbbe242ccac7438a6bb680304419f.jpg"
                },
                {
                    "img_url": "http://images.vnstory.xyz/vnstory/d1/25/d12574500cab167c4a51a43bfbd09306.jpg"
                }
            ],
            "keep_num": 900,
            "like_num": 888,
            "sort": 0,
            "title": "测试问题2",
            "update_time": "Tue, 03 Jul 2018 10:04:30 GMT",
            "user": {
                "avatar": "http://images.vnstory.xyz/vnstory/aa/61/aa61d0bfa92e85f128e0ec561e0a8385.jpg",
                "id": 2,
                "sex": 2,
                "user_name": "伟大的维多利亚少年"
            },
            "user_id": 2
        }
    ],
    "msg": "ok",
    "ret": 0
}
```



