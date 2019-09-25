# -*- coding: utf-8 -*-
# @Time    : 2019/9/25 3:21 下午
# @Site    : 
# @File    : ud_test.py
# @Software: PyCharm
import hashlib
import uuid

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

# lis = []
# def getimgurl():
#     if len(lis) < 5:
#         try:
# with conn.cursor() as cursor:
#     sql = "select image_path from video_copy1 limit {}, {}".format(int((page - 1) * row), row)
#     cursor.execute(sql)
#     cc = cursor.fetchall()
    #             page = page + 1
    #             for b, in cc:
    #                 lis.insert(0, b)
    #     except Exception as e:
    #         print(e)
    # return lis.pop()

# def getsize():
#     if len(lis) < 5:
#         try:
# with conn.cursor() as cursor:
#     sql = "select size from video_copy1 limit {},{}".format(int((page - 1) * row),row)
#     cursor.execute(sql)
#     cc = cursor.fetchall()
    #             page = page + 1
    #             for b, in cc:
    #                 lis.insert(0,b)
    #     except Exception as e:
    #         print(e)
    # return lis.pop
with conn.cursor() as cursor:
    sql = "select video_path from video_copy1"
    cursor.execute(sql)
    cc = cursor.fetchall()
for b, in cc:
    print(type(b))

# for i in range(105000):
#     image_url = getimgurl()
#
#     rands = uuid.uuid4()
#     rand = str(rands)
#
#     size =
#
#     title =

    # video_url =
    #
    # user_id =
    #
    # sc = "e6f9fdda5fa04a3f3a43f28b7c1c6cdd"
    #
    # miyao = "cover_img=" + image_url + "&" + "rand=" + rand + "&" + "size=" + size + "&" + "title=" + title + "&" + "url=" + video_url + "&" + "user_id=" + user_id + sc
    # print(miyao)
    # md5 = hashlib.md5()
    # md5.update(str(miyao).encode())
    # namename = md5.hexdigest()
    #
    # print()

    # response = requests.post('https://api.qkb-test.admin.lianzhuoxinxi.com/web/video/add',data = {
    #         "rand": rand,
    #         "url": video_url,
    #         "cover_img": image_url,
    #         "size": size,
    #         "title": title,
    #         "user_id": user_id,
    #         "sign": namename,
    #     })