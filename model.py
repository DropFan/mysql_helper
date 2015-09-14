#! /bin/env python
# -*- coding:utf-8 -*-
# author:Tiger <DropFan@Gmail.com>

from mysql_helper import mysql_helper as mdb

__author__ = 'Tiger <DropFan@Gmail.com>'


class model(object):
    """docstring for model"""

    # _data = {}
    dataModel = {}

    # db instance

    # __db = mdb(db_host='localhost', db_port=3306 ,db_user='root', db_pass='123456', db_name='test', read_default_file='/etc/my.cnf', autocommit=True)
    __db = None

    def __init__(self, id=-1, **kwargs):
        super(model, self).__init__()
        # self.arg = arg
        # print 'model'
        # self.tableName = ''
        # self.data = {}
        # self.datamodel = {}
        self.__db = mdb(db_host='localhost',
                        db_port=3306,
                        db_user='root',
                        db_pass='123456',
                        db_name='test',
                        read_default_file='/etc/my.cnf',
                        autocommit=True)
        self.data = {}
        for key in self.dataModel.keys():
            self.data[key] = self.dataModel[key]
        del(self.data['id'])

        if isinstance(id, int) and id != -1:
            self.id = id
            data = self.__fetch_by_id()
            if isinstance(data, dict):
                self.data = data

    def __fetch_by_id(self):
        fields = ', '.join(['`%s`' % k for k in self.dataModel.keys()])
        # sql = "SELECT %s FROM `%s` WHERE `id` = '%d'" % (fields, self.tableName, self.id)
        db = self.__db
        if db.select(self.tableName, fields, where='`id` = %d' % self.id, limit='1'):
            ret = db.fetch_one_dict()
            ret['id'] = int(ret['id'])
        else:
            ret = False
        print 'fetch ', ret
        return ret

    def insert(self):
        print 'insert'
        if 'id' not in self.data.keys():
            db = self.__db
            insert_id = db.insert(self.tableName, self.data)
            return insert_id
        else:
            print 'id ?'
            return False

    def update(self):
        print 'update'
        if 'id' in self.data.keys() and isinstance(self.id, int):
            db = self.__db
            ret = db.update(self.tableName, self.data, where='`id` = %d' % self.id, limit='1')
            return True if ret else False
        else:
            return False

    def delete(self):
        print 'delete'
        if 'id' in self.data.keys() and isinstance(self.id, int):
            db = self.__db
            ret = db.delete(self.tableName, where='`id` = %d' % self.id, limit='1')
            return True if ret else False
        else:
            return False

    # @classmethod
    # def delete_by_id(cls, id):
    # write later...

    @classmethod
    def select(cls, fields='*', **kwargs):
        print 'select'

        if isinstance(fields, tuple) or isinstance(fields, list):
            fields = ', '.join(['`%s`' % x for x in fields])
        else:
            fields = ', '.join(['`%s`' % x for x in cls.dataModel.keys()])

        if 'where' in kwargs and isinstance(kwargs['where'], str):
            where = kwargs['where']
        else:
            where = '1 = 1'

        if 'order' in kwargs and isinstance(kwargs['order'], str):
            order = kwargs['order']
        else:
            order = False

        if 'limit' in kwargs and isinstance(kwargs['limit'], str):
            limit = kwargs['limit']
        else:
            limit = False

        db = cls.__db
        ret = db.select(cls.tableName, fields, where=where, order=order, limit=limit)
        if ret:
            rows = db.fetch_all_dict()
            return rows
        return False

    def __getattr__(self, key):
        print 'get', key

        if key in self.data.keys():
            return self.data[key]
            # super(model, self).__getattribute__(self.data[key])
        else:
            pass

    def __setattr__(self, key, value):
        print 'set k:', key, 'v:', value
        if key in self.dataModel.keys() and isinstance(value, self.dataModel[key]) and key != 'id':
            print 'data[%s]:%s' % (key, value)
            self.data[key] = value
        elif key == 'tableName':
            print 'You can\'t modify this attribute! (%s)' % key
            return None
        else:
            super(model, self).__setattr__(key, value)

# end class model
