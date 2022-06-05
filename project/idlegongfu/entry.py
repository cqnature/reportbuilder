#!/usr/bin/env python
# coding=utf-8

import os
import json
from project.base.configs import *
from project.base.date import *
from project.base.entry import *
from project.idlegongfu.mailreport import generate_mail_report
from project.idlegongfu.lostresetreport import generate_lost_reset_report
from project.idlegongfu.loststagereport import generate_lost_stage_report
from project.idlegongfu.retentionresetreport import generate_retention_reset_report
from project.idlegongfu.retentionstagereport import generate_retention_stage_report
from project.idlegongfu.newadsreport import generate_new_ads_report
from project.idlegongfu.dauadsreport import generate_dau_ads_report


class Entry(BaseEntry):
    def __init__(self, option, *parameter):
        super(Entry, self).__init__(option, *parameter)
        self.detail_email.extend(['bear@peakxgames.com'])

    def generate_report(self):
        package_name = __name__.split('.')[-2]
        print('current package name: ', package_name)
        if package_name != self.project_config.project_name:
            print('package name not equal project name, return')
            return
        return super(Entry, self).generate_report()

    def do_generate_report(self):
        print('idlegongfu do_generate_report')
        report_filepaths = []
        # 开启代理
        # if self.option & ReportFlag.mail:
        #     report_filepaths.extend(generate_mail_report(
        #         self.query_config, self.start_date))
        # if self.option & ReportFlag.lost_stage:
        #     report_filepaths.extend(generate_lost_stage_report(
        #         self.query_config, self.start_date))
        # if self.option & ReportFlag.retention_stage:
        #     report_filepaths.extend(generate_retention_stage_report(
        #         self.query_config, self.start_date))
        # if self.option & ReportFlag.lost_reset:
        #     report_filepaths.extend(generate_lost_reset_report(
        #         self.query_config, self.start_date))
        # if self.option & ReportFlag.retention_reset:
        #     report_filepaths.extend(generate_retention_reset_report(
        #         self.query_config, self.start_date))
        # if self.option & ReportFlag.new_ads:
        #     report_filepaths.extend(generate_new_ads_report(
        #         self.query_config, self.start_date))
        # if self.option & ReportFlag.dau_ads:
        #     report_filepaths.extend(generate_dau_ads_report(
        #         self.query_config, self.start_date))
        return report_filepaths
