#-*- coding:utf-8 -*-
import tornado.ioloop
import tornado.web
import json
import MySQLdb
import os
import time

class GetPublishHandler(tornado.web.RequestHandler):
    def get(self):
        account = self.get_argument('user_account', None)
        db = MySQLdb.connect("127.0.0.1","root","sl2887729","test")
        db.set_character_set('utf8')
        db.set_character_set('utf8')
        cursor = db.cursor()
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        sql = "select * from T_Publish_Text where user_account = '%s' order by id desc limit 10" % account
        cursor.execute(sql)
        outResult = ()
        i = 0
        for data in cur.fetchall():
            out_content = data[2]
            out_time = data[3]
            result = {
                time : out_time,
                content: out_content
            }
            outResult[i] = result
            i++


        db.commit()
        db.close()
        self.write(json.dumps(outResult))

class PublishHandler(tornado.web.RequestHandler):
    def get(self):

        text = self.get_argument('publish_text', None)
        account = self.get_argument('user_account', None)
        publishtime = time.time()

        db = MySQLdb.connect("127.0.0.1","root","sl2887729","test")
        db.set_character_set('utf8')
        db.set_character_set('utf8')
        cursor = db.cursor()
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        sql = "INSERT INTO T_Publish_Text(user_account, publish_content, publish_time) VALUES ('%s', '%s', '%s')"  % (account, text, publishtime)
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

        db = MySQLdb.connect("127.0.0.1","root","sl2887729","test")
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

        db = MySQLdb.connect("127.0.0.1","root","sl2887729","test")
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
        

application = tornado.web.Application([
    (r"/publish", PublishHandler),
    (r"/register", RegisterHandler),
    (r"/login", LoginHandler),
    (r"/get_publish", GetPublishHandler),
])


if __name__ == "__main__":
    application.listen(80)
    print "开启服务器"
    tornado.ioloop.IOLoop.instance().start()
