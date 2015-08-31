#! /bin/env python
# -*- coding:utf-8 -*-
# author:Tiger <DropFan@Gmail.com>

from pysql import pysql as mdb


class model(object):
    """docstring for model"""

    # _data = {}
    dataModel = {}

    def __init__(self, id=-1, **kwargs):
        super(model, self).__init__()
        # self.arg = arg
        # print 'model'
        # self.tableName = ''
        # self.data = {}
        # self.datamodel = {}
        self.data = {}

        if isinstance(id, int) and id != -1:
            self.id = id
            self.data = self.__fetch_by_id()
        else:
            for key in self.dataModel.keys():
                self.data[key] =  self.dataModel[key]
            del(self.data['id'])



    def __fetch_by_id(self):
        fields= ', '.join(['`%s`' % k for k in self.dataModel.keys()])
        # sql = "SELECT %s FROM `%s` WHERE `id` = '%d'" % (fields, self.tableName, self.id)
        db = mdb(db_host='localhost', db_user='root', db_pass='123456', db_name='test')

        db.select(self.tableName, fields, where='`id` = %d' % self.id)
        data = db.fetch_one_dict()
        print 'fetch ',data
        return data

    def insert(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    # def __getattr__(self, key):
    #     print 'get',key

    #     if key in self.data.keys():
    #         super(model, self).__getattribute__(self.data[key])
    #     else:
    #         super(model, self).__getattribute__(key)


    # def __setattr__ (self, key, value):
    #     print 'set k:',key,'v:',value
    #     if key in self.data.keys() and isinstance(value, self.dataModel[key]):
    #         print 'data[%s]:%s' %(key,value)
    #         self.data[key] = value
    #         super(model, self).__setattr__(key, value)
    #     else:
    #         super(model, self).__setattr__(key, value)
