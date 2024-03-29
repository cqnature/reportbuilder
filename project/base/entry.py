#!/usr/bin/env python
# coding=utf-8

from project.base.date import *
from project.base.mail import *
from project.base.configs import *


class BaseEntry(object):
    def __init__(self, option, *parameter):
        self.option = option
        self.start_date = Date(parameter[0])
        self.project_config = ProjectConfig(
            parameter[1], parameter[2], parameter[3], parameter[4], parameter[5], parameter[6], parameter[7])
        self.query_config = QueryConfig(
            self.project_config, parameter[8], parameter[9], parameter[10], parameter[11], parameter[12])
        self.end_date = Date(self.start_date).enddate(
            self.query_config.geo_country)
        self.detail_email = []

    def generate_report(self):
        self.project_config.enable_proxy()
        self.project_config.enable_credential()
        self.query_config.validate(self.start_date)
        reports = self.do_generate_report()
        if len(reports) > 0:
            subject = "{0}项目{1}平台{2}数据明细报表".format(
                self.project_config.project_name, self.query_config.platform, self.end_date)
            send_mail(subject, '<p>详情见附件</p>', reports, self.detail_email)

    def do_generate_report(self):
        print('do_generate_report')
        return []
