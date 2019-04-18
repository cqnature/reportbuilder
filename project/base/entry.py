#!/usr/bin/env python
# coding=utf-8

from config import *
from date import *

class BaseEntry:
    def __init__(self, option, *parameter):
        self.option = option
        self.project_config = ProjectConfig(parameter[0], parameter[1])
        self.query_config = QueryConfig(this.project_config, parameter[2], parameter[3])
        this.start_date = Date(parameter[4])

    def generate_report(self):
        package_name = __name__.split('.')[-1]
        print 'current package name: ', package_name
        if package_name != this.project_config.project_name:
            print 'package name not equal project name, return'
            return
        self.project_config.enable_proxy()
        self.project_config.enable_credential()
        self.query_config.validate(self.start_date)
        self.do_generate_report()

    def do_generate_report(self):
        print 'do_generate_report'
