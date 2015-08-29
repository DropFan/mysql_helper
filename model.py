#! /bin/env python
# -*- coding:utf-8 -*-
# author:Tiger <DropFan@Gmail.com>

from db_mysql import db_mysql
from var_dump import var_dump as dump
from pprint import pprint

class model(object):
    """docstring for model"""

    tableName = ''
    data = {}
    datamodel = {}

    def __init__(self, id, **args):
        super(model, self).__init__()
        # self.arg = arg


    def insert(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def __del__(self):
        pass

class userModel(model):

    tableName = 'user'

    data = {
        'id'        : 1,
        'name'      : str,
        'pass'      : str,
        'email'     : str,
        'reg_time'  : int,
        'last_login': int
    }
    dataModel = {
        'id'        : int,
        'name'      : str,
        'pass'      : str,
        'email'     : str,
        'reg_time'  : int,
        'last_login': int
    }

    def __init__(self, id='', **args):
        super(model, self).__init__()
        if isinstance(id, int):
            self.id = id
            self.data = self.__fetch_by_id()


    def __fetch_by_id(self):
        fields= ', '.join(['`%s`' % k for k in self.data.keys()])
        sql = "SELECT %s FROM `%s` WHERE `id` = '%d'" % (fields, self.tableName, self.id)
        print sql

    def __getattr__(self, key):
        if key in self.data.keys():
            return self.data[key]

    def __setattr__ (self, key, value):
        if key in self.data.keys() and isinstance(value, self.dataModel[key]):
            self.data[key] = value
        # print self.data




def main():
    print 'start main():'
    print '---------------------------------------------'

    print type(['k','a'])
    user = userModel(1)
    print '====='
    print user.data
    print '++++++++++'
    # pprint(user)
    # dump(user)

    user2 = userModel()
    print user
    print user2

    print user.data



    print '---------------------------------------------'
    print 'end main()'
    pass





if __name__ == '__main__':
    main()