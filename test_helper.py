#! /usr/bin/env python2
# -*- coding:utf-8 -*-
# author: Tiger <DropFan@Gmail.com>


from mysql_helper import mysql_helper as mdb

import datetime,time

config = {
        'db_host'   : 'localhost',
        'db_port'   : 3306,
        'db_user'   : 'root',
        'db_pass'   : '123456',
        'db_name'   : 'test',
        'charset'   : 'utf8'
    }

db = mdb()
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
