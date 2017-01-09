# coding: utf-8

import tornado.ioloop
import tornado.web
import logging

from tornado.web import Application
from tornado.log import enable_pretty_logging
from sns.urls import urls


def main():
    port = 8080
    enable_pretty_logging()
    application = Application(urls, cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=")
    application.listen(port)
    logging.info("listening port: %s" % port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
