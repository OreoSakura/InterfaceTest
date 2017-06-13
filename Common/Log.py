import os
import logging
from datetime import datetime
from Common.ReadConfig import ReadConfig

localReadConfig = ReadConfig()

class Log:
    def __init__(self):
        global logPath, resultPath, proDir
        proDir = os.getcwd()
        resultPath = os.path.join(proDir, "Result")
        if not os.path.exists(resultPath):
            os.mkdir(resultPath)
        logPath = os.path.join(resultPath, str(datetime.now().strftime("%Y-%m-%d")))
        if not os.path.exists(logPath):
            os.mkdir(logPath)
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        # 增加判断，不会出现重复记录日志的问题
        if not self.logger.handlers:
            # 定义handler
            handler = logging.FileHandler(os.path.join(logPath, "log.log"))
            # 设置日志的输出格式
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def get_logger(self):
        return self.logger

    def get_report_path(self):
        report_path = os.path.join(logPath, "report.html")
        return report_path

    def get_log_path(self):
        log_path = os.path.join(logPath, "log.log")
        return log_path





