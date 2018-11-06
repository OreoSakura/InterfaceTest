# -*- coding: utf-8 -*-

import requests
import re
import json
import datetime
import io
import os
import traceback
import sys
from xml.dom import minidom
from Common.ReadTestcase import ReadTestcase
from Common import StartupTeardown
from Common.Log import Log



class CreateTest:
    #将测试数据设置为类对象
    table = ReadTestcase.open_excel()
    nrows = ReadTestcase.get_nrows(table)
    id = ReadTestcase.get_id(table, nrows)
    name = ReadTestcase.get_name(table, nrows)
    url = ReadTestcase.get_url(table, nrows)
    method = ReadTestcase.get_method(table, nrows)
    data = ReadTestcase.get_data(table, nrows)
    pattern = ReadTestcase.get_pattern(table, nrows)

    #初始化日志信息
    log = Log()
    logger = log.get_logger()
    reportpath = log.get_report_path()

    #统计失败用例的编号
    failcaseID = []
    errorcouting = []

    #定义报告的信息类别
    successmsg = '测试通过'
    failmsg = '测试失败，查看日志获取详情。'

    @classmethod
    # 接口函数
    def test_api(self, url, method, data):
        global response
        try:
            #还要添加判断，连接成功才往下走
            if method == 'POST':
                req = requests.post(url = url, data = json.loads(data))
                self.response = req.json()
            if method == 'GET':
                req = requests.get(url = url, params = json.loads(data))
                self.response = req.json()
            return self.response
        except Exception as ex:
            self.logger.error(str(ex))

    @classmethod
    # 正则表达式，判断测试结果
    # def test_result(self,response, pa):  # pa对应Excel中的pattern列
    #     try:
    #         match = re.findall(pa, str(response), re.S)
    #         if match:
    #             self.report = self.successmsg
    #             self.report_log = '用例编号：%s ，' \
    #                               '用例名称：%s，' \
    #                               '测试通过！' % (self.id, self.name)
    #             self.logger.info(self.report_log)
    #         else:
    #             self.report = self.failmsg
    #             self.report_log = '用例编号：%s，' \
    #                               '用例名称：%s，' \
    #                               '测试失败：实际响应数据与用例不符，' \
    #                               '实际响应数据：%s，'\
    #                               '用例数据：%s'% (self.id, self.name, response, self.pattern)
    #             self.logger.info(self.report_log)
    #     except AttributeError:
    #             self.report = self.errormsg
    #             self.logger.error(self.report)
    #     return self.report

    #@classmethod
    # 获取用例执行的时间
    def test_time(cls):
        nowtime = datetime.datetime.now()
        testtime = nowtime.strftime('%Y-%m-%d %H:%M:%S')
        return testtime

    @classmethod
    # 获取本次测试报告的名称
    def test_report(cls):
        nowtime = datetime.datetime.now()
        reporttime = nowtime.strftime('%Y-%m-%d-%H')
        reportname = reporttime+'.html'
        return reportname

    @classmethod
    # 主执行程序
    def test_main(self):
        global testresults
        xml = minidom.Document()
        xml.appendChild(xml.createComment("测试报告"))
        caselist = xml.createElement("caselist")
        xml.appendChild(caselist)

        # 读取测试用例Excel的数据
        for i in range(1, self.nrows):
            testid = self.id[i]
            testname = self.name[i]
            testurl = self.url[i]
            testmethod = self.method[i]
            testdata = self.data[i]
            testpattern = self.pattern[i]

            # 执行测试
            StartupTeardown.startup()
            testresults = CreateTest.test_api(testurl, testmethod, testdata)
            try:
                match = re.findall(str(testpattern), str(testresults), re.S)
                if match:
                    report = self.successmsg
                    report_log = '用例编号：%s ，' \
                                 '用例名称：%s \n' \
                                 '测试通过！' % (self.id[i], self.name[i])
                    self.logger.info(report_log)
                else:
                    report = self.failmsg
                    report_log = '用例编号：%s，' \
                                 '用例名称：%s\n' \
                                 '测试失败：实际响应数据与用例不符 \n' \
                                 '实际响应数据：%s \n' \
                                 '用例数据：%s' % (self.id[i], self.name[i], testresults, self.pattern[i])
                    self.logger.info(report_log)
            except Exception as ex:
                self.logger.error(str(ex))

            # 执行结束
            StartupTeardown.teardown()

            # 生成xml文件
            # 输入用例ID
            case = xml.createElement("case")
            case.setAttribute("id", testid)
            # 输入用例名称
            name = xml.createElement("name")
            name.appendChild(xml.createTextNode(testname))
            # 输入接口类型
            method = xml.createElement("method")
            method.appendChild(xml.createTextNode(testmethod))
            # 输入用例测试结果
            result = xml.createElement("result")
            result.appendChild(xml.createTextNode(report))
            # 输入用例执行时间
            time = xml.createElement("time")
            time.appendChild(xml.createTextNode(CreateTest.test_time()))

            case.appendChild(name)
            case.appendChild(method)
            case.appendChild(result)
            case.appendChild(time)
            caselist.appendChild(case)
            # xml文件生成结束

            #统计失败的用例ID和name
            if report == self.failmsg :
                self.failcaseID.append(testid)
                self.errorcouting = self.failcaseID

        # 生成测试报告文件,放到日志文件的同一路径下
        filename = io.open(self.reportpath, 'w+', encoding='utf-8')
        xml.writexml(writer=filename, indent='\t', newl='\n', addindent='\t', encoding='utf-8')
        filename.close()

        return (self.errorcouting, self.nrows)















