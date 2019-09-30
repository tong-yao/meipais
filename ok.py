# -*- coding: utf-8 -*-
# @Time    : 2019/9/25 8:37 下午
# @Site    : 
# @File    : ok.py
# @Software: PyCharm
# -*- coding=utf-8 -*-
# @Time : 2019/7/23 15:25
# @Author : piller
# @File : spider.py
# @Software: PyCharm
"""
    上传评论
"""
import pymysql
import hashlib
import requests,logging

# logging.basicConfig(filename="/var/www/meipais/meipai_log.txt", filemode="a",
#                     format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%Y-%m-%d %H:%M:%S",
#                     level=logging.INFO)
HOST = "47.94.204.15"
PORT = 3306
USER = "lianzhuoxinxi"
PASSWORD = "LIANzhuoxinxi888?"
DATABASE = "spider"
CHARSET = "utf8mb4"
def connect_base_sql():
    db = pymysql.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            db=DATABASE,
            charset=CHARSET,
        )
    return db

conn = connect_base_sql()


def get_video_id_and_ref_id():
    with conn.cursor()as cursor:
        sql = "select video_id_prod, ref_id from spider.video where source = %s"
        args = ["美拍美妆",]
        cursor.execute(sql,args)
        data = cursor.fetchall()
    return data


def get_user(count):
    rand = "wll"
    sc = "e6f9fdda5fa04a3f3a43f28b7c1c6cdd"
    sign = f"count={count}&rand={rand}{sc}"
    print(sign)
    md5 = hashlib.md5()
    md5.update(sign.encode())
    a = md5.hexdigest()
    print(a)
    data = {
        "rand": rand,
        "count": count,
        "sign": f"{a}",
    }
    response = requests.get(url="https://api.qkb.admin.lianzhuoxinxi.com/web/user/get", params=data)
    print(response.content.decode())
    return response.json().get("data")


def up_vv(**kwargs):
    sc = "e6f9fdda5fa04a3f3a43f28b7c1c6cdd"
    c = sorted(kwargs.keys())
    sign = ""
    l = c.__len__()
    print(f"l:{l}")
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


def get_comment():
    data = get_video_id_and_ref_id()
    for video_id, ref_id in data:
        if video_id == 0:
            continue
        with conn.cursor() as cursor:
            sql = "select id, content from spider.comment where ref_id = {}".format(ref_id)
            cursor.execute(sql)
            info = cursor.fetchall()
        print(info)
        if info == ():
            continue
        for id_, comment in info:
            print(id_, comment)
            user_id = get_user(1)[0]
            print(user_id)
            params = up_vv(comment=comment, rand="wll", user_id=user_id, video_id=video_id)
            print("datadata",params)
            response = requests.post("https://api.qkb.admin.lianzhuoxinxi.com/web/video/comment", data=params)
            logging.info(response.content.decode())
            logging.info("还剩{}".format(video_id))
            with conn.cursor() as cursor:
                sql = f"update comment set video_id_prod={video_id},user_id_prod={user_id} where id = {id_}"
                cursor.execute(sql)
            conn.commit()


# ob_url = "https://api.qkb.admin.lianzhuoxinxi.com/web/video/comment"


"""def main():
    # 1, 链接数据库
    conn = base_sql_connect()
    # 2, 查看user_id
    data = __select(conn)
    for subject_id, _ in data:
        if subject_id == "34780":
            continue
        print(f"subject_id, qkb_user_id : {subject_id, _}")
        # 2.1, 查看ref_id
        ref_data = __select_ref_id(conn, subject_id)
        for ref_id, article_id in ref_data:
            print(f"ref_id: {ref_id}, article_id: {article_id}")
            # 3, 查看video_id
            video_id = __select_video_id(conn, ref_id)
            video_id = video_id[0][0]
            print(f"video_id: {video_id}")
            if video_id == 0:
                continue
            # 3.2 查看评论用户的subject_id
            comments = __select_comments(conn, article_id)
            user_ids = {}
            for id_, content, subject_id_comment, qkb_comment_id in comments:
                if qkb_comment_id == 0 or qkb_comment_id == '0':
                    continue
                if subject_id in user_ids.keys():
                    user_id = user_ids.get(subject_id_comment)
                else:
                    user_id = __select_user_id(conn, subject_id_comment)[0][0]
                    user_ids[subject_id_comment] = user_id
                print(f"id_, content, subject_id, user_id, qkb_comment_id: "
                      f"{id_, content, subject_id_comment, user_id, qkb_comment_id}")
                if user_id == 0:
                    continue
                content = re.sub(r'(@|#)[^ ]+( |$)', '', content)
                content = re.sub(r'<[^>]+>', "", content, re.S)
                if "太抖" in content:
                    __update(conn, -1, id_=id_)
                    continue
                if content == "":
                    continue
                # 4, 上传
                rand = "wli_pill"
                sc = "e6f9fdda5fa04a3f3a43f28b7c1c6cdd"
                sign = f"comment={content}&rand={rand}&user_id={user_id}&video_id={video_id}{sc}"
                print(sign)
                md5 = hashlib.md5()
                md5.update(sign.encode())
                a = md5.hexdigest()
                print(a)
                info = {
                    "rand": rand,
                    "user_id": user_id,
                    "video_id": video_id,
                    "comment": content,
                    "sign": a
                }
                print(f"info: {info}")
                response = obs_requests(url=ob_url, methods="POST", data=info)
                print(response.content.decode())
                try:
                    qkb_comment_id = response.json().get("data").get("id")
                except:
                    continue
                __update(conn, qkb_comment_id, id_=id_)"""


if __name__ == '__main__':
    get_comment()