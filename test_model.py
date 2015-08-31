#! /bin/env python
# -*- coding:utf-8 -*-
# author: Tiger <DropFan@Gmail.com>

from usermodel import userModel
from var_dump import var_dump as dump
from pprint import pprint
# from time import *
import time,datetime

def main():
    print 'this is test function.'
    print 'start main():'
    print '-'*80

    user = userModel(1)
    print '====='
    # print user.data
    print '++++++++++'
    # pprint(user)
    # dump(user)

    u = userModel()
    print user
    print u
    # user2.id=123
    # user.id=2

    # print user.data
    # pprint(user.data)
    # pprint(user2.data)
    print '-'*80
    print 'end main()'
    print '-'*80

    print u.name
    u.data={
        # 'id':199,
        'name':'hello',
        'pass':'xxxxxx',
        'email':'hello@python.org',
        'reg_time':time.time(),
        'last_login':time.time()
    }
    print u.name
    print '-'*80
    pprint(user.data)
    print '-'*80
    pprint(u.data)
    print '-'*80
    rows = userModel.select(where='`id` > 12345', order='`id` desc', limit='0,2')
    pprint(rows)
    print '='*80
    x = userModel(12368)
    print x.data
    print x.delete()



if __name__ == '__main__':
    main()