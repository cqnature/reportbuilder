#!/usr/bin/env python
# coding=utf-8

import os
import json
from ..base.date import *
from ..base.helper import *
from ..base.query import *
from ..base.report import *

def generate_retention_ads_report(query_config, date):
    Report(query_config, date).generate()

class Report(BaseReport):
    def __init__(self, query_config, date):
        super(Report, self).__init__(query_config, date)
        self.etc_filename = 'ads_view_of_retention_users.csv'
        self.output_filename = 'retention_ads_report.csv'

    def do_generate(self):
        print 'do generate report'
        with open(self.output_filepath, mode='w+') as out:
            report_lines = []
            for single_date in Date(self.start_date).rangeto(self.end_date, True):
                self.generate_retention_ads_report_at_date(report_lines, single_date)
            reportstring = ''.join(report_lines)
            out.write(reportstring)
            out.close()

    def generate_retention_ads_report_at_date(self, report_lines, date):
        print("generate_retention_ads_report_at_date ", date)
        with open(self.etc_filepath) as file:
            lines = file.readlines()
            ads_view_count_results = self.get_result("retention_ads_view_count.sql", date)
            if len(ads_view_count_results) == 0:
                return
            ads_view_user_results = self.get_result("retention_ads_view_users.sql", date)
            lines[0] = lines[0].format(Date(date).formatmd())
            lines[1] = lines[1].format(ads_view_count_results[0].daily_user_count)
            for i in range(3, len(lines) - 1):
                line = lines[i]
                linesegments = line.split('|', 1)
                ads_scene = linesegments[0]
                formatstring = linesegments[1]
                ad_view_count = 0
                daily_average_ad_view_count = 0
                ad_view_user_count = 0
                daily_ad_view_user_percent = 0
                for k in range(len(ads_view_count_results)):
                    ads_view_count_result = ads_view_count_results[k]
                    if ads_view_count_result.af_ad_scene == ads_scene:
                        ad_view_count = ads_view_count_result.ad_view_count
                        daily_average_ad_view_count = ads_view_count_result.daily_average_ad_view_count
                        break
                for k in range(len(ads_view_user_results)):
                    ads_view_user_result = ads_view_user_results[k]
                    if ads_view_user_result.af_ad_scene == ads_scene:
                        ad_view_user_count = ads_view_user_result.ad_view_user_count
                        daily_ad_view_user_percent = ads_view_user_result.daily_ad_view_user_percent
                        break
                lines[i] = formatstring.format(ad_view_user_count, daily_ad_view_user_percent * 100, ad_view_count, daily_average_ad_view_count)
            lines[len(lines) - 1] = lines[len(lines) - 1].format(sum(t.daily_average_ad_view_count for t in ads_view_count_results))
            report_lines.extend(lines)
            file.close()
