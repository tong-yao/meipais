# -*- coding: utf-8 -*-
# @Time    : 2019/9/20 2:46 下午
# @Software: PyCharm

import requests, re, json, pymysql, hashlib, os, logging, ffmpeg
from lxml import etree

filePath = '/home/oss/t/a/ceshi_video/'
files = os.listdir(filePath)
logging.basicConfig(filename="/var/www/meipais/meipai_log.txt", filemode="a",
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%Y-%m-%d %H:%M:%S",
                    level=logging.INFO)

while True:
    logging.info("gongzuo")
    response = requests.get(
        "https://api.meipai.com/channels/feed_timeline.json?build=7741&channel=8888&client_id=1089857299&device_id=BFD501B4-8100-43AF-B462-7D8A2527AF91&id=27&idfa=25119624-6F29-4F1C-9B78-938686948775&language=zh-Hans&lat=40.00109870380246&local_time=1569378925029&locale=1&lon=116.3995198266256&model=iPhone7%2C1&network=wifi&os=9.3.3&page=1&resolution=1080%2A1920&sig=7d622b5e198811c3f60c7d11c59d21cb&sigTime=1569378925029&sigVersion=1.3&stat_gid=24844116&version=8.2.12&with_friend_ship=0",
        verify=False)
    a = response.content.decode()
    a = json.loads(a)
    headers = {
        'User-Agent': '"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

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


    db = connect_mysql()

    for i in a:
        video_urls = i["media"]['video']
        comments_url = i["media"]["url"]
        jpg_url = i['media']["cover_pic"]
        caption = i["recommend_caption"]
        logging.info(comments_url)

        if caption:
            id = re.search(".*utm_media_id=(\d+)", comments_url).group(1)

            response = requests.get(video_urls, verify=False)
            jpg_re = requests.get(jpg_url, verify=False)

            c = response.content
            md5 = hashlib.md5()
            md5.update(c)
            video_name = md5.hexdigest()
            files_num = 1
            for i in files:
                if video_name + ".mp4" == i:
                    break
                elif files_num == len(files):
                    files.append(video_name + ".mp4")
                    with open('/home/oss/t/a/ceshi_video/{}.mp4'.format(video_name), "wb") as f:
                        f.write(c)
                    files.append('{}.mp4'.format(video_name))
                    video_path = '/home/oss/t/a/ceshi_video/{}.mp4'.format(video_name)
                    jpg = jpg_re.content
                    md5.update(jpg)
                    jpg_name = md5.hexdigest()
                    with open("/home/oss/t/a/ceshi_jpg/{}.jpg".format(jpg_name), "wb") as f:
                        f.write(jpg)
                    image_path = "/home/oss/t/a/ceshi_jpg/{}.jpg".format(jpg_name)
                    video_data = ffmpeg.probe('/home/oss/t/a/ceshi_video/{}.mp4'.format(video_name))
                    video_duration = video_data.get("format").get("duration")
                    # print("视频时长:{}".format(video_duration))
                    video_size = video_data.get("format").get("size")
                    # print("视频大小:{}".format(video_size))

                    with db.cursor() as cursor:
                        try:
                            sql = "INSERT INTO video_copy1(`source`,`ref_id`,`video_path`,`image_path`,`title`,`size`,`status`,`video_id_test`,`video_id_prod`) values('美拍美妆',{},'{}','{}','{}',{},0,0,0)".format(
                            id, video_path, image_path, caption, video_size)
                            cursor.execute(sql)

                        except Exception as e:
                            print("eeeeeee", e)
                            print(sql)
                        db.commit()

                    try:
                        for i in range(1, 7):
                            response = requests.get(
                            "https://www.meipai.com/medias/comments_timeline?page={}&count=10&id={}".format(i, id),
                            verify=False)
                            r = response.content.decode()
                            c = json.loads(r)
                            if len(c) > 8:
                                for i in c:
                                    if i["content"] == '[图片评论，请下载客户端新版查看]':
                                        continue
                                    elif i["content"].startswith("回复"):
                                        c = re.compile(r"</span>：(.*)")
                                        comments = re.findall(c, i['content'])
                                        for i in comments:
                                            comments = str(i)
                                        with db.cursor() as cursor:
                                            try:
                                                sql = "INSERT INTO comment_copy1(`source`,`ref_id`,`content`,`user_id_test`,`video_id_test`,`user_id_prod`,`video_id_prod`,`status`) values('美拍美妆',{},'{}',0,0,0,0,0)".format(
                                                id, comments)
                                                cursor.execute(sql)
                                            except Exception as e:
                                                print(sql)
                                                print(e)
                                            db.commit()
                                    elif i["content"].startswith("<span"):
                                        c = re.compile(r"</span> (.*)")
                                        comments = re.findall(c, i['content'])
                                        for i in comments:
                                            comments = str(i)
                                        with db.cursor() as cursor:
                                            try:
                                                sql = "INSERT INTO comment_copy1(`source`,`ref_id`,`content`,`user_id_test`,`video_id_test`,`user_id_prod`,`video_id_prod`,`status`) values('美拍美妆',{},'{}',0,0,0,0,0)".format(
                                                id, comments)
                                                cursor.execute(sql)
                                            except Exception as e:
                                                print(sql)
                                                print(e)
                                            db.commit()
                                    else:
                                        comments = str(i['content'])
                                        with db.cursor() as cursor:
                                            try:
                                                sql = "INSERT INTO comment_copy1(`source`,`ref_id`,`content`,`user_id_test`,`video_id_test`,`user_id_prod`,`video_id_prod`,`status`) values('美拍美妆',{},'{}',0,0,0,0,0)".format(
                                                id, comments)
                                                cursor.execute(sql)
                                            except Exception as e:
                                                print(sql)
                                                print(e)
                                            db.commit()
                            else:
                                for i in c:
                                    if i["content"] == '[图片评论，请下载客户端新版查看]':
                                        continue
                                    elif i["content"].startswith("回复"):
                                        c = re.compile(r"</span>：(.*)")
                                        comments = re.findall(c, i['content'])
                                        for i in comments:
                                            comments = str(i)
                                        with db.cursor() as cursor:
                                            try:
                                                sql = "INSERT INTO comment_copy1(`source`,`ref_id`,`content`,`user_id_test`,`video_id_test`,`user_id_prod`,`video_id_prod`,`status`) values('美拍美妆',{},'{}',0,0,0,0,0)".format(
                                                id, comments)
                                                cursor.execute(sql)
                                            except Exception as e:
                                                print(sql)
                                                print(e)
                                            db.commit()
                                    elif i["content"].startswith("<span"):
                                        c = re.compile(r"</span> (.*)")
                                        comments = re.findall(c, i['content'])
                                        for i in comments:
                                            comments = str(i)
                                        with db.cursor() as cursor:
                                            try:
                                                sql = "INSERT INTO comment_copy1(`source`,`ref_id`,`content`,`user_id_test`,`video_id_test`,`user_id_prod`,`video_id_prod`,`status`) values('美拍美妆',{},'{}',0,0,0,0,0)".format(
                                                id, comments)
                                                cursor.execute(sql)
                                            except Exception as e:
                                                print(sql)
                                                print(e)
                                            db.commit()
                                    else:
                                        comments = str(i['content'])
                                        with db.cursor() as cursor:
                                            try:
                                                sql = "INSERT INTO comment_copy1(`source`,`ref_id`,`content`,`user_id_test`,`video_id_test`,`user_id_prod`,`video_id_prod`,`status`) values('美拍美妆',{},'{}',0,0,0,0,0)".format(
                                                id, comments)
                                                cursor.execute(sql)
                                            except Exception as e:
                                                print(sql)
                                                print(e)
                                            db.commit()
                                break

                    except Exception as e:
                        print(e)
                    break

            else:
                files_num += 1
                continue

        else:
            break

# 来源和评论内容
# 视频来源，图片地址，视频地址，标题，视频大小，是否上传，去看吧id
