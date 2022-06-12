#!/usr/bin/env python
# coding=utf-8

import os
import json
from project.base.date import *
from project.base.helper import *
from project.base.query import *
from project.base.report import *

lost_day = 0


def generate_new_ads_report(query_config, date):
    return Report(query_config, date).generate()


class Report(BaseReport):
    def __init__(self, query_config, date):
        super(Report, self).__init__(query_config, date)
        self.etc_filename = '新增用户广告次数.csv'
        country_string = self.query_config.geo_country
        platform_string = self.query_config.platform
        self.output_filename = "{0}-{1}-Day{2}-Ad-Scene-{3}.csv".format(
            country_string, platform_string, lost_day + 1, self.end_date)

    def do_generate(self):
        print('do generate report')
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
            lately_date = max(
                Date(self.end_date).adddays(-21), self.start_date)
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
            ads_view_count_results = self.get_result(
                "新增用户观看广告次数.sql", date, single_date)
            if len(ads_view_count_results) == 0:
                return
            ads_view_user_results = self.get_result(
                "新增用户观看广告用户.sql", date, single_date)

            line_string = ""
            line_string += "{0},".format(Date(date).formatmd())
            line_string += "{0},".format(firstopen_usercount)

            total_avg_ads_count = 0
            for k in range(len(ads_view_count_results)):
                ads_view_count_result = ads_view_count_results[k]
                total_avg_ads_count += ads_view_count_result.daily_average_ad_view_count

            line_string += "{0:.2f},".format(total_avg_ads_count)

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
                    if ads_view_count_result.ad_position == ads_scene:
                        ad_view_count = ads_view_count_result.ad_view_count
                        daily_average_ad_view_count = ads_view_count_result.daily_average_ad_view_count
                        break
                for k in range(len(ads_view_user_results)):
                    ads_view_user_result = ads_view_user_results[k]
                    if ads_view_user_result.ad_position == ads_scene:
                        ad_view_user_count = ads_view_user_result.ad_view_user_count
                        daily_ad_view_user_percent = ads_view_user_result.daily_ad_view_user_percent
                        break
                line_string += "{0:.2f}%,{1:.2f},".format(
                    daily_ad_view_user_percent * 100, daily_average_ad_view_count)
            append_line(report_lines, len(report_lines), line_string)
            file.close()
