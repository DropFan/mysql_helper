#! /bin/env python
# -*- coding:utf-8 -*-
# author:Tiger <DropFan@Gmail.com>


# import config
from mysql_helper import mysql_helper as mdb
from config import mysql_config as db_config

__author__ = 'Tiger <DropFan@Gmail.com>'


class model(object):
    """docstring for model

    Attributes:
        data (dict): fields in table
        dataModel (dict): fields in table but values are its type
        id (int): id (primary key in table)
    """

    # sub_class should set this attribute.
    # tableName = ''

    # _data = {}
    dataModel = {}

    # db instance
    # __db = mdb(db_host=db_config['db_host'],
    #            db_port=db_config['db_port'],
    #            db_user=db_config['db_user'],
    #            db_pass=db_config['db_pass'],
    #            db_name=db_config['db_name'],
    #            autocommit=True)

    def __init__(self, id=-1, **kwargs):
        """construct method

        Args:
            id (int, optional): primary key in table
            **kwargs: other fields in table
        """
        super(model, self).__init__()
        # self.arg = arg
        # print 'model'
        # self.tableName = ''
        # self.data = {}
        # self.datamodel = {}
        self.data = self.init_data()
        self.__db = model.getDB()

        if isinstance(id, int) and id != -1:
            self.id = id
            data = self.__fetch_by_id()
            if isinstance(data, dict):
                self.data = data

    def __fetch_by_id(self):
        fields = self.dataModel.keys()
        # sql = "SELECT %s FROM `%s` WHERE `id` = '%d'" % (fields, self.tableName, self.id)
        db = self.__db
        if db.select(self.tableName, fields, where='`id` = %d' % self.id, limit='1'):
            ret = db.fetch_one_dict()
            for k in self.dataModel.keys():
                if self.dataModel[k] == int:
                    ret[k] = int(ret[k])
                elif self.dataModel[k] == str:
                    ret[k] = str(ret[k])
        else:
            ret = False
        print 'fetch ', ret
        return ret

    def init_data(self):
        data = {}
        for k in self.dataModel.keys():
            if self.dataModel[k] == int:
                data[k] = 0
            elif self.dataModel[k] == float:
                data[k] = 0.0
            elif self.dataModel[k] == str:
                data[k] = ''
            else:
                data[k] = None
        return data

    def insert(self):
        print 'model->insert'
        if 'id' not in self.data.keys():
            db = self.__db
            insert_id = db.insert(self.tableName, self.data)
            return insert_id
        else:
            print 'id ?'
            return False

    def update(self):
        print 'model->update'
        if 'id' in self.data.keys() and isinstance(self.id, int):
            db = self.__db
            ret = db.update(self.tableName, self.data, where='`id` = %d' % self.id, limit='')
            return True if ret else False
        else:
            return False

    def delete(self):
        print 'model->delete'
        if 'id' in self.data.keys() and isinstance(self.id, int):
            db = self.__db
            ret = db.delete(self.tableName, where='`id` = %d' % self.id, limit='')
            return True if ret else False
        else:
            return False

    # @classmethod
    # def delete_by_id(cls, id):
    # write later...

    @classmethod
    def select(cls, fields='*', **kwargs):
        print 'model->select'

        ret = False
        if isinstance(fields, tuple) or isinstance(fields, list):
            fields = fields
        else:
            fields = cls.dataModel.keys()

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

        db = model.getDB()
        ret = db.select(cls.tableName, fields, where=where, order=order, limit=limit)
        if ret:
            rows = db.fetch_all_dict()
            ret = rows
        del db
        return ret

    @staticmethod
    def getDB():
        db = mdb(db_host=db_config['db_host'],
                 db_port=db_config['db_port'],
                 db_user=db_config['db_user'],
                 db_pass=db_config['db_pass'],
                 db_name=db_config['db_name'],
                 autocommit=True)
        return db

    def __getattr__(self, key):
        print 'model->get', key
        if key == 'data':
            self.data = self.init_data()
        elif key in self.data.keys():
            return self.data[key]
            # super(model, self).__getattribute__(self.data[key])
        else:
            super(model, self).__getattribute__(key)

    def __setattr__(self, key, value):
        print 'model->set k:', key, 'v:', value
        if key in self.dataModel.keys() and isinstance(value, self.dataModel[key]) and key != 'id':
            print 'data[%s]:%s' % (key, value)
            if self.dataModel[key] == int:
                value = int(value)
            elif self.dataModel[key] == float:
                value = float(value)
            elif self.dataModel[key] == str:
                value = str(value)
            self.data[key] = value
        elif key == 'tableName' or key == 'dataModel':
            print 'You can\'t modify this attribute! (%s)' % key
            return None
        else:
            super(model, self).__setattr__(key, value)

# end class model
