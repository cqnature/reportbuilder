#!/usr/bin/env python
# coding=utf-8

import os
import json
from ..base.date import *
from ..base.helper import *
from ..base.query import *
from ..base.report import *

lost_day = 0

def generate_new_ads_report(query_config, date):
    return Report(query_config, date).generate()

class Report(BaseReport):
    def __init__(self, query_config, date):
        super(Report, self).__init__(query_config, date)
        self.etc_filename = 'ads_view_of_new_users.csv'
        country_string = "CN" if self.query_config.geo_country == 'China' else "US"
        platform_string = "AND" if self.query_config.platform == 'ANDROID' else "iOS"
        self.output_filename = "{0}-{1}-Day{2}-Ad-Scene-{3}.csv".format(country_string, platform_string, lost_day + 1, self.end_date)

    def do_generate(self):
        print 'do generate report'
        with open(self.output_filepath, mode='w+') as out:
            report_lines = []
            with open(self.etc_filepath) as file:
                lines = file.readlines()
                head_lines1 = [x.strip() for x in lines[0:2]]
                for k in range(len(head_lines1)):
                    append_line(report_lines, k, head_lines1[k])
                file.close()
            for single_date in self.extra_date:
                self.generate_new_ads_report_at_date(report_lines, single_date)
            lately_date = max(Date(self.end_date).adddays(-14), self.start_date)
            for single_date in Date(lately_date).rangeto(self.end_date, True):
                self.generate_new_ads_report_at_date(report_lines, single_date)
            reportstring = '\n'.join(report_lines)
            out.write(reportstring)
            out.close()
        return [self.output_filepath]

    def generate_new_ads_report_at_date(self, report_lines, date):
        print("generate_new_ads_report_at_date ", date)
        with open(self.etc_filepath) as file:
            firstopen_usercount = self.get_firstopen_count(date)
            if firstopen_usercount == 0:
                return
            single_date = Date(date).adddays(lost_day)
            ads_view_count_results = self.get_result("new_ads_view_count.sql", date, single_date)
            if len(ads_view_count_results) == 0:
                return
            ads_view_user_results = self.get_result("new_ads_view_users.sql", date, single_date)

            line_string = ""
            line_string += "{0},".format(Date(date).formatmd())
            line_string += "{0},".format(firstopen_usercount)

            lines = [x.strip() for x in file.readlines()]
            headlines = lines[2].split('|')
            for i in headlines:
                ads_scene = i
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
                line_string += "{0:.2f}%,{1:.2f},".format(daily_ad_view_user_percent * 100, daily_average_ad_view_count)
            append_line(report_lines, len(report_lines), line_string)
            file.close()
