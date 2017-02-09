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
        type = self.get_argument('type', None)
        q = Auth(qiniu_access_key, qiniu_secret_key)
        bucket = qiniu_bucket_name    
        key = uuid.uuid1().hex + '.png' 
        if type == 'sound':
            key = uuid.uuid1().hex + '.caf'
        if type == 'video':
            key = uuid.uuid1().hex + '.mov'
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

        sql2 = "select * from T_User where user_account = '%s'" % account
        cursor.execute(sql2)
        data2 = cursor.fetchone()
        coupleAccount = data2[7]
        ownAvator = data2[6]

        sql3 = "select * from T_User where user_account = '%s'" % coupleAccount
        cursor.execute(sql3)
        data3 = cursor.fetchone()
        coupleAvator = data3[6]

        sql = "select * from T_Publish where user_account = '%s' or user_account = '%s'  order by id desc limit 100" % (account, coupleAccount)
        cursor.execute(sql)
        outResult = []
        i = 0
        for dbData in cursor.fetchall():
            out_content = dbData[2]
            out_time = dbData[3]
            account = dbData[1]
            publish_id = dbData[0]
            reply_count = dbData[4]
            avator = ownAvator
            if account == coupleAccount:
                avator = coupleAvator

            result = {
                "publish_id" : publish_id,
                "time" : out_time,
                "content" : out_content,
                "avator" : avator,
                "reply_count": reply_count
            }
            outResult.append(result)
            i = i + 1

        db.commit()
        db.close()
        self.write(json.dumps({"data": outResult}))


class PublishHandler(tornado.web.RequestHandler):
    def get(self):

        text = self.get_argument('publish_text', None)
        print(text)
        account = self.get_argument('user_account', None)
        publishtime = time.time()

        db = MySQLdb.connect("127.0.0.1","root",db_password,"test")
        db.set_character_set('utf8')
        db.set_character_set('utf8')
        cursor = db.cursor()
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        sql = "INSERT INTO T_Publish(user_account, publish_content, publish_time) VALUES ('%s', '%s', '%s')"  % (account, text, publishtime)
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
        sql1 = "select * from T_User where user_account = '%s' and user_password = '%s'" % (a, b)
        cursor.execute(sql1)
        count = 0
        data = cursor.fetchall()
        outResult = {}
        for singleData in data:
            count = count + 1
            outResult = {
                "data" : {
                    "user_id": singleData[0],
                    "user_account": singleData[1],
                    "user_name": singleData[3],
                    "user_birthday": singleData[4],
                    "user_sex": singleData[5],
                    "user_avator": singleData[6],
                    "user_huanXinAccount": singleData[8],
                    "user_huanXinPassword": singleData[9],
                    "user_inviteCode" : singleData[10]
                },
                "ret" : 1,
                "msg" : "登录成功"
            }

        if count == 0:
            outResult = {
            "ret" : 0,
            "msg" : "登录失败"
            }
                    
        db.commit()
        db.close()


       

        self.write(json.dumps(outResult))


class RegisterHandler(tornado.web.RequestHandler):
    def post(self):
        account = self.get_argument('user_account', None)
        password = self.get_argument('user_password', None)
        sex = self.get_argument('user_sex', None)
        birthday = self.get_argument('user_birthday', None)
        huanXinAccount = self.get_argument('user_huanXinAccount', None)
        huanXinPassword = self.get_argument('user_huanXinPassword', None)
        name = self.get_argument('user_name', None)
        avator = self.get_argument('user_avator', None)


        db = MySQLdb.connect("127.0.0.1","root",db_password,"test")
        db.set_character_set('utf8')
        db.set_character_set('utf8')
        cursor = db.cursor();
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        sql1 = "select count(*) from T_User where user_account = '%s'" % account
        cursor.execute(sql1)
        count = cursor.fetchone()[0]
        if count > 0:
            result = {
            "ret" : 0,
            "count" : count,
            "msg" : "该账号已经被注册"
            }
        else:
            sql2 = "select max(user_inviteCode) from T_User"
            cursor.execute(sql2)
            inviteCode = cursor.fetchone()[0]
            inviteCode = inviteCode + 1 
            sql3 =  "select max(id) from T_User"
            cursor.execute(sql3)
            user_id =  cursor.fetchone()[0]
            user_id = user_id + 1
            result = {
            "ret" : 1,
            "count" : count,
            "msg" : "注册成功",
            "inviteCode": inviteCode,
            "user_id" : user_id
            } 

            sql = "INSERT INTO T_User(user_account, user_password, user_sex, user_birthday, user_huanXinAccount, user_huanXinPassword, user_name, user_avator, user_inviteCode) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"  % (account, password, sex, birthday, huanXinAccount, huanXinPassword, name, avator, inviteCode)
            cursor.execute(sql)

        db.commit()
        db.close()
        self.write(json.dumps(result))

class PairHandler(tornado.web.RequestHandler):
    def get(self):
        account = self.get_argument('user_account', None)
        invitedCode = self.get_argument('inviteCode', None)
        db = MySQLdb.connect("127.0.0.1","root",db_password,"test")
        db.set_character_set('utf8')
        db.set_character_set('utf8')
        cursor = db.cursor()
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        sql = "select * from T_User where user_account = '%s'" % account
        cursor.execute(sql)
        data = cursor.fetchone()
        result = {}
        if data == None:
            result = {
                "ret": 0,
                "msg": "邀请码错误"
            }
        else: 
            coupleAccount = data[7]
            if (coupleAccount == "" or coupleAccount == None):
                sql2 = "select * from T_User where user_inviteCode = '%s'" % invitedCode
                cursor.execute(sql2)
                otherData = cursor.fetchone()
                otherAccount = otherData[1]
                otherCoupleAccount = otherData[7]
                otherCoupleName = otherData[3]
                otherCoupleAvator = otherData[6]
                otherInviteCode = otherData[10]
                if (otherCoupleAccount == "" or otherCoupleAccount == None):
                    sql3 = "UPDATE T_User SET couple_account = '%s' WHERE user_account = '%s'" % (otherAccount, account)
                    cursor.execute(sql3)
                    sql4 = "UPDATE T_User SET couple_account = '%s' WHERE user_account = '%s'" % (account, otherAccount)
                    cursor.execute(sql4)
                    result = {
                       "ret": 1,
                       "msg": "绑定成功",
                       "data" : {
                            "couple_account" : otherAccount,
                            "couple_name" : otherCoupleName,
                            "couple_avator": otherCoupleAvator 
                       }
                    }
                else:
                    result = {
                        "ret": 0,
                        "msg": "对方已经绑定伴侣"
                    }

            else:
                result = {
                    "ret": 0,
                    "msg": "您已经绑定伴侣"
                }
        
        db.commit()
        db.close()
        self.write(json.dumps(result))

class UserInfoHandler(tornado.web.RequestHandler):
    def get(self):
        account = self.get_argument('user_account', None)
        db = MySQLdb.connect("127.0.0.1","root",db_password,"test")
        db.set_character_set('utf8')
        db.set_character_set('utf8')
        cursor = db.cursor()
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        sql = "select * from T_User where user_account = '%s'" % account
        cursor.execute(sql)
        data = cursor.fetchone()
        coupleAccount = data[7]
        result =  {}
        if (coupleAccount != None and coupleAccount != ""):
            sql2 = "select * from T_User where user_account = '%s'" % coupleAccount
            cursor.execute(sql2)
            data2 = cursor.fetchone()
            coupleAvator = data2[6]
            coupleName = data2[3]
            result = {
                "ret": 1,
                "couple_account" : coupleAccount,
                "couple_name" : coupleName,
                "couple_avator": coupleAvator
            }
        else:
            result = {
                "ret": 0,
                "msg": "该用户没有关联情侣"
            }
        db.commit()
        db.close()
        self.write(json.dumps(result))

class ReplyHandler(tornado.web.RequestHandler):
    def post(self):
        account = self.get_argument('user_account', None)
        publish_id = self.get_argument('publish_id', None)
        reply_content = self.get_argument('reply_content', None)
        publishtime = time.time()

        db = MySQLdb.connect("127.0.0.1","root",db_password,"test")
        db.set_character_set('utf8')
        db.set_character_set('utf8')
        cursor = db.cursor();
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')



        sql1 = "INSERT INTO T_Reply(publish_id, reply_content, reply_account, reply_time) VALUES ('%s', '%s', '%s', '%s')" % (publish_id, reply_content, account, publishtime)
        cursor.execute(sql1)

        sql2 = "UPDATE T_Publish SET publish_reply_count = publish_reply_count + 1 WHERE id = '%s'" % publish_id
        cursor.execute(sql2)

        db.commit()
        db.close()

        result = {
            "ret" : 1,
            "msg" : "回复成功"
        }
        self.write(json.dumps(result))

class GetPeplyHandler(tornado.web.RequestHandler):
    def get(self):
        publish_id = self.get_argument('publish_id', None)

        db = MySQLdb.connect("127.0.0.1","root",db_password,"test")
        db.set_character_set('utf8')
        db.set_character_set('utf8')
        cursor = db.cursor()
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        sql = "select * from T_Reply where publish_id = '%s' order by id asc limit 100" % publish_id
        cursor.execute(sql)
        outResult = []
        for dbData in cursor.fetchall():
            out_content = dbData[2]
            out_time = dbData[4]
            account = dbData[3]

            result = {
                "time" : out_time,
                "content" : out_content,
                "account" : account
            }
            outResult.append(result)

        db.commit()
        db.close()
        self.write(json.dumps({"data": outResult}))