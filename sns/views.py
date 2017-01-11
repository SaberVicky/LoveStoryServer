#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Chunyang Guo
#
# Copyright (C) 2016 Zhihu Inc.

from __future__ import absolute_import

import json
import time
import tornado.web
import MySQLdb
import uuid 
from sns import wrapper

from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config

db_password = "sl2887729"

qiniu_access_key = 'pY-VZRw7ynreklOFs-KuHWzpxGFIg8rssrSkpcwV'
qiniu_secret_key = 'lESmFWIsNz9s4bt2Y7XV47blCb4e65lsOo9qzJPf'
qiniu_bucket_name = 'lovestory'
qiniu_img_url = 'http://ojae83ylm.bkt.clouddn.com/'

# class BaseHandler(tornado.web.RequestHandler):
#     def get_current_user(self):
#         user_id = self.get_secure_cookie("user_id")
#         # 这里去数据库查询用户
#         return None

#     def login(self, user_id):
#         self.set_secure_cookie("user_id", str(user_id))

#     def get_login_url(self):
#         return '/login'


class RequestQiNiuParams(tornado.web.RequestHandler):
    def get(self):
        q = Auth(qiniu_access_key, qiniu_secret_key)
        bucket = qiniu_bucket_name
        key = uuid.uuid1().hex + '.png' 
        token = q.upload_token(bucket, key, 3600)
        img_url = qiniu_img_url + key
        result = {
            'ret' : 1,
            'token' : token,
            'key' : key,
            'bucket' : bucket,
            'img_url' : img_url 
        }
        self.write(json.dumps(result))


class GetPublishHandler(tornado.web.RequestHandler):
    # @wrapper.check_logi
    def get(self):

        account = self.get_argument('user_account', None)

        db = MySQLdb.connect("127.0.0.1","root",db_password,"test")
        db.set_character_set('utf8')
        db.set_character_set('utf8')
        cursor = db.cursor()
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        sql = "select * from T_Publish where user_account = '%s' order by id desc limit 10" % account
        cursor.execute(sql)
        outResult = []
        i = 0
        for dbData in cursor.fetchall():
            out_content = dbData[2]
            out_time = dbData[3]
            out_img_url = dbData[4]
            result = {
                "time" : out_time,
                "content" : out_content,
                "img_url" : out_img_url
            }
            outResult.append(result)
            i = i + 1


        db.commit()
        db.close()
        self.write(json.dumps({"data": outResult}))


class PublishHandler(tornado.web.RequestHandler):
    def get(self):

        text = self.get_argument('publish_text', None)
        account = self.get_argument('user_account', None)
        img_url = self.get_argument('img_url', None)
        publishtime = time.time()

        db = MySQLdb.connect("127.0.0.1","root",db_password,"test")
        db.set_character_set('utf8')
        db.set_character_set('utf8')
        cursor = db.cursor()
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        sql = "INSERT INTO T_Publish(user_account, publish_content, publish_time, publish_img_url) VALUES ('%s', '%s', '%s', '%s')"  % (account, text, publishtime, img_url)
        cursor.execute(sql)
        db.commit()
        db.close()

        result = {
            "ret" : 1,
            "msg" : "发布成功"
        }
        self.write(json.dumps(result))


class LoginHandler(tornado.web.RequestHandler):
    def post(self):
        a = self.get_argument('user_account', None)
        b = self.get_argument('user_password', None)

        db = MySQLdb.connect("127.0.0.1","root",db_password,"test")
        cursor = db.cursor();
        sql1 = "select count(*) from T_User where user_account = '%s' and user_password = '%s'" % (a, b)
        cursor.execute(sql1)
        count = cursor.fetchone()[0]
        db.commit()
        db.close()


        if count == 1:
            result = {
            "ret" : 1,
            "msg" : "登录成功"
            }
        else:
            result = {
            "ret" : 0,
            "msg" : "登录失败"
            }

        self.write(json.dumps(result))


class RegisterHandler(tornado.web.RequestHandler):
    def post(self):
        a = self.get_argument('user_account', None)
        b = self.get_argument('user_password', None)

        db = MySQLdb.connect("127.0.0.1","root",db_password,"test")
        cursor = db.cursor();
        sql1 = "select count(*) from T_User where user_account = '%s'" % a
        cursor.execute(sql1)
        count = cursor.fetchone()[0]
        if count > 0:
            result = {
            "ret" : 0,
            "count" : count,
            "msg" : "该账号已经被注册"
            }
        else:
            result = {
            "ret" : 1,
            "count" : count,
            "msg" : "注册成功"
            }
            sql = "INSERT INTO T_User(user_account, user_password) VALUES ('%s', '%s')"  % (a, b)
            cursor.execute(sql)

        db.commit()
        db.close()
        self.write(json.dumps(result))