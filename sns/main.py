# coding: utf-8

import tornado.ioloop
import tornado.web
import logging

from tornado.web import Application
from tornado.log import enable_pretty_logging
from tornado.wsgi import WSGIAdapter
from sns.urls import urls


def get_application():
    return Application(urls,
                       cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=")


wsgi_application = WSGIAdapter(get_application())


def main():
    port = 8080
    enable_pretty_logging()
    application = get_application()
    application.listen(port)
    logging.info("listening port: %s" % port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
