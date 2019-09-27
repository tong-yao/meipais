# -*- coding: utf-8 -*-
# @Time    : 2019/9/27 4:22 下午
# @Site    : 
# @File    : upup.py
# @Software: PyCharm
import hashlib

import pymysql
import requests

HOST = "47.94.204.15"
PORT = 3306
USER = "lianzhuoxinxi"
PASSWORD = "LIANzhuoxinxi888?"
DATABASE = "spider"
CHARSET = "utf8mb4"

def connect_mysql():
    db = pymysql.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        db=DATABASE,
        charset=CHARSET,
    )
    return db

conn = connect_mysql()

sc = "e6f9fdda5fa04a3f3a43f28b7c1c6cdd"

def up_vv(**kwargs):
    c = sorted(kwargs.keys())
    sign = ""
    l = c.__len__()
    # print(f"l:{l}")
    for num, i in enumerate(c):
        sign += f"{i}={kwargs[i]}"
        if num <= l - 2:
            sign += "&"
    sign += sc
    md5 = hashlib.md5()
    md5.update(sign.encode())
    a = md5.hexdigest()

    params = kwargs
    params["sign"] = a
    return params

with conn.cursor() as cursor:
    sql = "select `id`, `image_path`,`video_path`,`size`,`title`,`old_app_id` from video where video_id_test=0 and source = %s"
    args = ["美拍美妆", ]
    cursor.execute(sql,args)
    data = cursor.fetchall()

for id_, i, v, s, title, old_app_id in data:
    i = i.replace("/home/oss","https://c3.123qkk.com")
    v = v.replace("/home/oss","https://c3.123qkk.com")
    data = up_vv(cover_img=i, rand="zyn", size=s,
             title=title, url=v,
             user_id=old_app_id)
    print(data)
    response = requests.post('https://api.qkb-test.admin.lianzhuoxinxi.com/web/video/add',data =data)
    print(response.content.decode())
    try:
        video_id = response.json().get("data").get("id")
    except AttributeError:
        continue
    print(video_id)
    with conn.cursor() as cursor:
        sql = f"update video set video_id_test={video_id} where id = {id_}"
        cursor.execute(sql)
    conn.commit()
