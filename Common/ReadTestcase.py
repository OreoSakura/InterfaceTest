# -*- coding: utf-8 -*-

import xlrd
import os

class ReadTestcase:
    def __int__(self):
        pass

    @classmethod
    # 打开测试用例的文件，获取sheet
    def open_excel(cls):
        global pardir,  casepath
        pardir = os.getcwd()  #入口文件是RunAll.py，所以直接获取该文件的路径即可
        casepath = os.path.join(pardir,  'Testcase',  'TestCase-MVP2.xlsx')
        workbook = xlrd.open_workbook(casepath)
        table = workbook.sheets()[0]
        return table

    @classmethod
    # 获取行号
    def get_nrows(cls, table):
        nrows = table.nrows
        return nrows

    @classmethod
    # 获取用例ID
    def get_id(cls, table, nrows):
        testid = []
        for i in range(nrows):
            testid.append(table.cell(i, 0).value)
        return testid

    @classmethod
    # 获取用例名称name
    def get_name(cls, table, nrows):
        testname = []
        for i in range(nrows):
            testname.append(table.cell(i, 1).value)
        return testname

    @classmethod
    # 获取接口的URL
    def get_url(cls, table, nrows):
        testurl = []
        for i in range(nrows):
            testurl.append(table.cell(i, 2).value + table.cell(i, 3).value)
        return testurl

    @classmethod
    # 获取请求的方法
    def get_method(cls, table, nrows):
        testmethod = []
        for i in range(nrows):
            testmethod.append(table.cell(i, 4).value)
        return testmethod

    @classmethod
    # 获取接口参数data
    def get_data(cls, table, nrows):
        testdata = []
        for i in range(nrows):
            testdata.append(table.cell(i, 5).value)
        return testdata

    @classmethod
    # 获取期望的响应值（验证点）
    def get_pattern(cls, table, nrows):
        testpatten = []
        for i in range(nrows):
            testpatten.append(table.cell(i, 6).value)
        return testpatten

    @classmethod
    # 判断用例是否需要执行
    def get_active(cls, table, nrows):
        caseactive = []
        for i in range(nrows):
            caseactive.append(table.cell(i, 7).value)
        return caseactive
    
