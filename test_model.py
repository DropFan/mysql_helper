#! /bin/env python
# -*- coding:utf-8 -*-
# author: Tiger <DropFan@Gmail.com>

from usermodel import userModel
from var_dump import var_dump as dump
from pprint import pprint

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

    user2 = userModel(2)
    print user
    print user2
    # user2.id=123
    # user.id=2

    # print user.data
    # pprint(user.data)
    # pprint(user2.data)
    print '-'*80
    print 'end main()'
    a = userModel()
    b = userModel()
    # print a.tid, b.tid
    a.data['id'] = 1
    b.data['id'] = 2
    print a.data
    print b.data
    print '-'*80
    pprint(user.data)
    pprint(user2.data)




if __name__ == '__main__':
    main()