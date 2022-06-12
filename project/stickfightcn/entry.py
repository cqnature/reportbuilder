#!/usr/bin/env python
# coding=utf-8

import os
import json
from project.base.configs import *
from project.base.date import *
from project.base.entry import *
from project.stickfightcn.mailreport import generate_mail_report
from project.stickfightcn.lostplantreport import generate_lostplant_report
from project.stickfightcn.retentionplantreport import generate_retentionplant_report
from project.stickfightcn.retentionadsreport import generate_retention_ads_report
from project.stickfightcn.newadsreport import generate_new_ads_report
from project.stickfightcn.totaladsreport import generate_total_ads_report
from project.stickfightcn.stagereport import generate_stage_report
from project.stickfightcn.retentionstagereport import generate_retention_stage_report
from project.stickfightcn.daystagereport import generate_day_stage_report
from project.stickfightcn.buttonbehaviourreport import generate_button_behaviour_report
from project.stickfightcn.lostbehaviourreport import generate_lostbehaviour_report
from project.stickfightcn.lostadsreport import generate_lost_ads_report
from project.stickfightcn.retentionadscountreport import generate_retention_ads_count_report


class Entry(BaseEntry):
    def __init__(self, option, *parameter):
        super(Entry, self).__init__(option, *parameter)
        self.detail_email.extend(['nero@peakxgames.com', 'bear@peakxgames.com', 'eli@peakxgames.com',
                                  'near@peakxgames.com', 'young@peakxgames.com', 'xiaobai@peakxgames.com'])

    def generate_report(self):
        package_name = __name__.split('.')[-2]
        print('current package name: ', package_name)
        if package_name != self.project_config.project_name:
            print('package name not equal project name, return')
            return
        return super(Entry, self).generate_report()

    def do_generate_report(self):
        print('stickfightcn do_generate_report')
        report_filepaths = []
        # 开启代理
        if self.option & ReportFlag.mail:
            report_filepaths.extend(generate_mail_report(
                self.query_config, self.start_date))
        # if self.option & ReportFlag.lost_level:
        #     report_filepaths.extend(generate_lostplant_report(
        #         self.query_config, self.start_date))
        # if self.option & ReportFlag.retention_level:
        #     report_filepaths.extend(generate_retentionplant_report(self.query_config, self.start_date))
        # if self.option & ReportFlag.lost_stage:
        #     report_filepaths.extend(generate_stage_report(
        #         self.query_config, self.start_date))
        # if self.option & ReportFlag.retention_stage:
        #     report_filepaths.extend(generate_retention_stage_report(self.query_config, self.start_date))
        # if self.option & ReportFlag.new_ads:
        #     report_filepaths.extend(generate_new_ads_report(self.query_config, self.start_date))
        # if self.option & ReportFlag.retention_ads:
        #     report_filepaths.extend(generate_retention_ads_report(self.query_config, self.start_date))
        # if self.option & ReportFlag.total_ads:
        #     report_filepaths.extend(generate_total_ads_report(self.query_config, self.start_date))
        # if self.option & ReportFlag.iap_behaviour:
        #     report_filepaths.extend(generate_iap_behaviour_report(self.query_config, self.start_date))
        # if self.option & ReportFlag.lost_behaviour:
        #     report_filepaths.extend(generate_lostbehaviour_report(self.query_config, self.start_date))
        # if self.option & ReportFlag.retention_behaviour:
        #     report_filepaths.extend(generate_retentionbehaviour_report(self.query_config, self.start_date))
        # if self.option & ReportFlag.day_stage:
        #     report_filepaths.extend(generate_day_stage_report(self.query_config, self.start_date))
        # if self.option & ReportFlag.button_behaviour:
        #     report_filepaths.extend(generate_button_behaviour_report(self.query_config, self.start_date))
        # if self.option & ReportFlag.lost_ads:
        #     report_filepaths.extend(generate_lost_ads_report(self.query_config, self.start_date))
        # if self.option & ReportFlag.retention_ads_count:
        #     report_filepaths.extend(generate_retention_ads_count_report(self.query_config, self.start_date))
        return report_filepaths
