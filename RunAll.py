# -*- coding: utf-8 -*-
import time
from Common.CreateTest import CreateTest
from Common.Log import Log
from Common.ConfigEmail import Email

class RunAll:
    log = Log()
    logger = log.get_logger()
    email = Email()

    def test_run(self):
        try:
            self.logger.info("********接口测试开始********")
            start = time.clock()

            data = CreateTest.test_main()
            errorlist = data[0]
            totalcase = data[1]-1
            errorcouting = len(errorlist)

            self.email.send_email(totalcase, errorcouting, errorlist)
            end = time.clock()

            self.logger.info("********接口测试结束********")
            self.logger.info("接口自动化脚本运行时间：%.03f seconds"% (end - start))

        except Exception as ex:
            self.logger.error(str(ex))


if __name__ == "__main__":
    obj = RunAll()
    obj.test_run()
    
    






