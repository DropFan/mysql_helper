#! /usr/env python2
# -*- coding:utf-8 -*-
# author:Tiger <DropFan@Gmail.com>

import MySQLdb
from var_dump import var_dump

__author__ = 'Tiger <DropFan@Gmail.com>'

class pysql(object):
    """
        docstring for db_mysql
        waiting for finish...
    """

    # connect config
    config = {
        'host'      : 'localhost',
        'port'      : 3306,
        'user'      : 'root',
        'pass'      : '123456',
        'db'        : 'test',
        'charset'   : 'utf8'
    }

    # if auto commit() when insert/update/delete
    autocommit = False

    # connect and cursor instance of MySQLdb
    conn = None
    cur  = None

    def __init__(self, config, **args):
        """
            initialize for db_mysql instance
        """

        for k in config.keys():
            if self.config[k]:
                self.config[k] = config[k]
        if 'autocommit' in args and isinstance(args['autocommit'], bool):
            self.autocommit = args['autocommit']
        self.conn = self.connect()
        if self.conn:
            print 'initial connect ok'
            self.cur = self.conn.cursor()
        else:
            print 'initial connect faild. Please try function connect() or check your config'
        print 'mysql initial function done.'


    def connect(self):
        """
            connect to mysql server
        """
        if self.conn:
            return self.conn
        try:
            self.conn = MySQLdb.connect(host=self.config['host'],
                                        port=self.config['port'],
                                        user=self.config['user'],
                                        passwd=self.config['pass'],
                                        db=self.config['db'],
                                        charset=self.config['charset'])
            print 'mysql connect ok'
            self.cur = self.conn.cursor()
            print 'cur ok'
            return self.conn
        except MySQLdb.Error, e:
            print 'mysql error : %s' % e
        except Exception, e:
            print 'connect error :'
            print repr(e)
        return False

    def select_db(self,db):
        if not self.is_connected():
            return False
        try:
            res = self.conn.select_db(db)
            return True
        except Exception, e:
            print 'select_db error : %s' % e
        return False

    def charset(self,charset):
        if not self.is_connected():
            return False
        try:
            self.cur.execute('SET NAMES %s' % charset)
            return True
        except Exception, e:
            print 'change charset error : %s' % e
        return False

    def query(self, sql):
        if not self.is_connected():
            return False
        try:
            res = self.cur.execute(sql)
            return res
        except MySQLdb.Error, e:
            print 'MySQLdb execute error! SQL:%s\nmysql error[%d]:%s' % (sql, e[0], e[1])
        return False

    def insert(self, tablename, data):
        if not self.is_connected():
            return False
        # data = 'INSERT INTO '
        if isinstance(data, dict):
            # generate sql statement
            # fields = []
            # values = []
            # for key in data.keys():
            #     fields.append('`' + key + '`')
            #     values.append('\'' + str(data[key]) + '\'')
            fields = ','.join(['`%s`'% x for x in data.keys()])
            values = ','.join(["'%s'"% x for x in data.values()])
            sql = 'INSERT INTO `%s` (%s) VALUES (%s)'% (tablename, fields, values)
        elif isinstance(data, str):
            sql = 'INSERT INTO `%s` %s'%(tablename, data)
        else:
            print 'Invalid parameter type (data must be dict or string)'
            return False
        print 'INSERT SQL: %s' % sql
        # exit()
        try:
            self.cur.execute(sql)
            insert_id = self.conn.insert_id()
            if self.autocommit:
                self.conn.commit()
            return insert_id
        except MySQLdb.Error, e:
            print 'MySQLdb insert error! SQL:%s\nmysql error[%d]:%s' % (sql, e[0], e[1])
        return False

    def update(self, tablename, data, **args):
        if not self.is_connected():
            return False
        if isinstance(data, dict):
            field = ','.join("`%s`='%s'" % (k,data[k]) for k in data)
            if 'where' in args and isinstance(args['where'], str):
                where = args['where']
            elif 'id' in data.keys():
                where = 'id = %s' % data['id']
            else:
                where = '1'
            if 'limit' in args and isinstance(args['limit'], str):
                limit = 'LIMIT %s' % args['limit']
            else:
                limit = ''
            sql = "UPDATE `%s` SET %s WHERE %s %s" % (tablename, field, where, limit)
        elif isinstance(data, str):
            sql = data
        else:
            print 'Invalid parameter type (data must be dict or string)'
            return False
        print 'UPDATE SQL: %s' % sql
        # exit()
        try:
            res = self.cur.execute(sql)
            # if self.autocommit:
            #     self.conn.commit()
            return self.rowcount()
        except MySQLdb.Error, e:
            print 'MySQLdb update error! SQL:%s\nmysql error[%d]:%s' % (sql, e[0], e[1])
        return False

    def delete(self, tablename, **args):
        if not self.is_connected():
            return False
        if 'where' in args and isinstance(args['where'], str):
            where = args['where']
        else:
            where = '1'
        if 'limit' in args and isinstance(args['limit'], str):
            limit = 'LIMIT %s' % args['limit']
        else:
            limit = ''
        sql = 'DELETE FROM `%s` WHERE %s %s' % (tablename, where, limit)
        print 'DELETE SQL: ', sql
        try:
            res = self.cur.execute(sql)
            if self.autocommit:
                self.conn.commit()
            return self.rowcount()
        except MySQLdb.Error, e:
            print 'MySQLdb delete error! SQL:%s\nmysql error[%d]:%s' % (sql, e[0], e[1])
        return False

    def select(self, tablename, fields,**args):
        if not self.is_connected():
            return False

        if isinstance(fields, tuple) or isinstance(fields, list):
            fields = ', '.join(['`%s`' % x for x in fields])

        if 'where' in args and isinstance(args['where'], str):
            where = args['where']
        else:
            where = '1'

        if 'limit' in args and isinstance(args['limit'], str):
            limit = 'LIMIT %s' % args['limit']
        else:
            limit = ''

        sql = 'SELECT %s FROM `%s` WHERE %s %s' % (fields, tablename, where, limit)
        print 'SELECT SQL: ',sql
        try:
            res = self.cur.execute(sql)
            if self.autocommit:
                self.conn.commit()
            return self.rowcount()
        except MySQLdb.Error, e:
            print 'MySQLdb select error! SQL:%s\nmysql error[%d]:%s' % (sql, e[0], e[1])
        return False

    def rowcount(self):
        return self.cur.rowcount

    def execute(self, sql):
        return self.cur.execute(sql)

    def commit(self):
        return self.conn.commit()

    def rollback(self):
        return self.conn.rollback()

    def fetch_all(self):
        if not self.is_connected():
            return False
        try:
            res = self.cur.fetchall()
            return res
        except MySQLdb.Error, e:
            print 'MySQLdb error : %s' % e
        return False

    def fetch_all_dict(self):
        if not self.is_connected():
            return False
        try:
            res = self.cur.fetchall()
            desc =self.cur.description
            # print 'res',res # debug
            # print 'desc:', desc # debug
            # var_dump(desc) # debug
            dic = []
            for row in res:
                # print 'row', row # debug
                _dic = {}
                for i in range(0,len(row)):
                    _dic[desc[i][0]] = str(row[i])
                dic.append(_dic)
            return dic
        except MySQLdb.Error, e:
            print 'MySQLdb error : %s' % e
        return False

    def fetch_one(self):
        return self.cur.fetchone()

    def fetch_one_dict(self):
        if not self.is_connected():
            return False
        try:
            res = self.cur.fetchone()
            desc = self.cur.description
            dic = {}
            for i in range(0,len(res)):
                dic[desc[i][0]] = str(res[i])
            return dic
        except MySQLdb.Error, e:
            print 'MySQLdb error : %s' % e
        return False

    def close(self):
        if not self.is_connected():
            return False
        try:
            self.cur.close()
            self.conn.close()
        except Exception, e:
            print 'close error :%s' % e

    def is_connected(self):
        if self.conn:
            return True
        else:
            print 'You are not connected to mysql server!'
        return False

    def __del__(self):
        self.close()

# end class

import datetime,time

config = {
        'host'      : 'localhost',
        'port'      : 3306,
        'user'      : 'root',
        'pass'      : '123456',
        'db'        : 'test',
        'charset'   : 'utf8'
    }
db = pysql(config)
# db.autocommit = True
res=db.charset('utf8')

# db.query('show tables')
# db.query('select * from `test`')

print '------------------------'
res = db.select_db('test')
print 'res',res
u={
    # 'id':12345,
    'name':'test',
    'pass':'pass1',
    'email':'ab@test',
    'reg_time':int(time.time()),
    'last_login':int(time.time())
}
x = ['id', 'name', 'pass', 'email', 'reg_time', 'last_login']
# print db.update('user',u,where='`id`>12345',limit='2')
print db.select('user',x,where='`id`>12345',limit='2')
print db.fetch_one()
exit()
# print db.insert('user',u)
print db.commit()

# exit()
print '======='
print db.query('select * from `user`')

# print db.query('select * from `type`')

# r=db.fetch_one_dict()
# print r
