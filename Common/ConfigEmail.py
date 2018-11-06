# -*- coding: utf-8 -*-

import os
import io
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from Common.ReadConfig import ReadConfig
from Common.Log import Log

localReadCongig = ReadConfig()

class Email:
    def __init__(self):
        global host, port, user, password, sender, receiver, title
        host = localReadCongig.get_email("mail_host")
        port = localReadCongig.get_email("mail_port")
        user = localReadCongig.get_email('mail_user')
        password = localReadCongig.get_email('mail_pass')
        sender = localReadCongig.get_email('sender')
        title = localReadCongig.get_email('subject')
        self.value = localReadCongig.get_email('receiver')
        self.receiver = []
        #获取收件人列表
        for n in str(self.value).split("/"):
            self.receiver.append(n)
        #定义邮件的subject
        date = datetime.now().strftime('%Y-%m-%d')
        self.subject = title + "" + date
        self.msg = MIMEMultipart('mixed')

        self.log = Log()
        self.logger = self.log.get_logger()

    def config_header(self):
        self.msg['Subject'] = self.subject
        self.msg['From'] = sender
        self.msg['To'] = ":".join(self.receiver) #python群发邮件的配置

    def config_content(self, totalcase, errorcasecouting, errorcaseid):
        body = '本次接口测试完成。\n' \
               '接口数：7，用例总数：%s，失败用例数：%s，失败用例id：%s。\n' \
               '执行详情见附件。' % (totalcase, errorcasecouting, errorcaseid)
        content_plain = MIMEText(body, 'plain', 'utf-8')
        self.msg.attach(content_plain)

    def config_file(self):
        if self.check_file():
            # 获取日志附件的路径
            logpath = self.log.get_log_path()
            att_logfile = io.open(logpath, 'rb')
            file = MIMEBase('application', 'octet-stream')
            file.set_payload((att_logfile).read())
            encoders.encode_base64(file)
            file.add_header('Content-Disposition', 'attachment', filename='log.log',encoders = 'utf-8')
            self.msg.attach(file)

    def check_file(self):
        logpath = self.log.get_log_path()
        if os.path.isfile(logpath) and not os.stat(logpath) == 0:
            return True
        else:
            return False

    def send_email(self, totalcase, errorcasecouting, errorcaseid):
        total = totalcase
        number = errorcasecouting
        list = errorcaseid
        self.config_header()
        self.config_content(total, number, list)
        self.config_file()

        try:
            smtp = smtplib.SMTP(host)
            smtp.login(user, password)
            smtp.sendmail(sender, self.receiver, self.msg.as_string())
            smtp.quit()
            self.logger.info("邮件已发送成功。")
        except Exception as ex:
            self.logger.error(str(ex))
