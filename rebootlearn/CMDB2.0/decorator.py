#!/usr/bin/env python
#coding:utf-8
def my_hello(fn):
    def hello1(name):
        print '123'
        fn(name)
        print '456'
    return hello1
@my_hello
def hello(name):
    print 'hello '+name
hello('sunfan')
