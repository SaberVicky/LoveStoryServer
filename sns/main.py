# coding: utf-8

import tornado.ioloop
import tornado.web

from tornado.web import Application
from sns.urls import urls


def main():
    application = Application(urls)
    application.listen(8080)
    print "开启服务器"
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
