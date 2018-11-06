# -*- coding: utf-8 -*-

import os
import codecs
import configparser

#获取配置文件的路径
proDir = os.getcwd()
configPath = os.path.join(proDir, 'Config.ini')

class ReadConfig:
    def __init__(self):
        self.cf = configparser.ConfigParser()
        self.cf.read(configPath, encoding="utf-8")

    # 读取EMAIL的配置
    def get_email(self, name):
        value = self.cf.get('EMAIL', name)
        return value
