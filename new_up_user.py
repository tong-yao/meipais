# -*- coding: utf-8 -*-
# @Time    : 2019/9/27 3:36 下午
# @Site    : 
# @File    : new_up_user.py
# @Software: PyCharm
import hashlib

import pymysql
import requests,logging

logging.basicConfig(filename="/var/www/meipais/meipai_log.txt", filemode="a",
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%Y-%m-%d %H:%M:%S",
                    level=logging.INFO)

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
def get_user(count):
    rand = "wll"
    sc = "e6f9fdda5fa04a3f3a43f28b7c1c6cdd"
    sign = f"count={count}&rand={rand}{sc}"
    md5 = hashlib.md5()
    md5.update(sign.encode())
    a = md5.hexdigest()
    data = {
        "rand": rand,
        "count": count,
        "sign": f"{a}",
    }
    response = requests.get(url="https://api.qkb-test.admin.lianzhuoxinxi.com/web/user/get", params=data)
    # print(response.content.decode())
    return response.json().get("data")

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
    sql = "select `old_app_id` from video where source = %s group by old_app_id"
    args = ["美拍美妆",]
    cursor.execute(sql,args)
    cc = cursor.fetchall()


ccs = [i[0] for i in cc]
# print(ccs)

video_user = get_user(len(cc))
dic = {}
for i in range(len(cc)):
    dic[video_user[i]]=[ccs[i]]

# for i,j in dic.items():
#     print(i,j)
with conn.cursor()as cursor:
    try:
        for i,j in dic.items():
            sql = "update spider.video set old_app_id={} where old_app_id = {}".format(i,j[0])
            cursor.execute(sql)
            print("chenggong")
            conn.commit()
            print(2)
            logging.info(i,j)
    except Exception as e:
        print(e)
