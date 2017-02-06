#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Chunyang Guo
#
# Copyright (C) 2016 Zhihu Inc.

from __future__ import absolute_import

from sns.views import PublishHandler, RegisterHandler, LoginHandler, GetPublishHandler, RequestQiNiuParams, PairHandler, UserInfoHandler, ReplyHandler, GetPeplyHandler

urls = [
    (r"/publish", PublishHandler),
    (r"/register", RegisterHandler),
    (r"/login", LoginHandler),
    (r"/get_publish", GetPublishHandler),
    (r"/request_qiniu_params", RequestQiNiuParams),
    (r"/pair", PairHandler),
    (r"/get_user_info", UserInfoHandler),
    (r"/reply", ReplyHandler),
    (r"/get_reply, GetPeplyHandler")
]


