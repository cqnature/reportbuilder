#!/usr/bin/env python
# coding=utf-8

from config import *
from date import *

class BaseEntry(object):
    def __init__(self, option, *parameter):
        self.option = option
        self.project_config = ProjectConfig(parameter[0], parameter[1])
        self.query_config = QueryConfig(self.project_config, parameter[2], parameter[3])
        self.start_date = Date(parameter[4])

    def generate_report(self):
        self.project_config.enable_proxy()
        self.project_config.enable_credential()
        self.query_config.validate(self.start_date)
        self.do_generate_report()

    def do_generate_report(self):
        print 'do_generate_report'
