#! /usr/bin/env python2
# -*- coding:utf-8 -*-
# author: Tiger <DropFan@Gmail.com>

from model import model


class userModel(model):
    """
        user model extends model
    """

    tableName = 'user'

    dataModel = {
        'id': int,
        'name': str,
        'pass': str,
        'email': str,
        'reg_time': int,
        'last_login': int
    }

    def __init__(self, id=-1, **kwargs):
        # self.data = {
        #     'id'        : int,
        #     'name'      : str,
        #     'pass'      : str,
        #     'email'     : str,
        #     'reg_time'  : int,
        #     'last_login': int
        # }
        super(userModel, self).__init__(id)
        # print self.data
