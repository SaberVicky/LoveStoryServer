#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Chunyang Guo
#
# Copyright (C) 2016 Zhihu Inc.

from __future__ import absolute_import

from sns import error_code


def check_login(func):
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            return self.write({'errcode': error_code.UNLOGIN, "msg": "unlogin"})
    return wrapper
