#!/usr/bin/env python
# coding=utf-8

import os
import json
from project.base.date import *
from project.base.helper import *
from project.base.query import *
from project.base.report import *


def generate_retention_ads_count_report(query_config, date):
    return Report(query_config, date).generate()


class Report(BaseReport):
    def __init__(self, query_config, date):
        super(Report, self).__init__(query_config, date)
        self.etc_filename = 'ads_count_of_retention_users.csv'
        country_string = self.query_config.geo_country
        platform_string = self.query_config.platform
        self.output_filename = "{0}-{1}-Day1-Ad-Range-{2}.csv".format(
            country_string, platform_string, self.end_date)

    def do_generate(self):
        print('do generate report')
        with open(self.output_filepath, mode='w+') as out:
            report_lines = []
            with open(self.etc_filepath) as file:
                lines = file.readlines()
                head_lines1 = [x.strip() for x in lines[0:1]]
                for k in range(len(head_lines1)):
                    append_line(report_lines, k, head_lines1[k])
                file.close()
            for single_date in self.extra_date:
                self.generate_retention_ads_count_report_at_date(
                    report_lines, single_date)
            lately_date = max(
                Date(self.end_date).adddays(-14), self.start_date)
            for single_date in Date(lately_date).rangeto(self.end_date, True):
                self.generate_retention_ads_count_report_at_date(
                    report_lines, single_date)
            reportstring = '\n'.join(report_lines)
            out.write(reportstring)
            out.close()
        return [self.output_filepath]

    def generate_retention_ads_count_report_at_date(self, report_lines, date):
        print("generate_retention_ads_count_report_at_date ", date)
        with open(self.etc_filepath) as file:
            firstopen_usercount = self.get_firstopen_count(date)
            if firstopen_usercount == 0:
                return
            ads_count_results = self.get_result(
                "ads_count_of_retention_users.sql", date, date)
            if len(ads_count_results) == 0:
                return
            line_string = ""
            line_string += "{0},".format(Date(date).formatmd())
            line_string += "{0},".format(firstopen_usercount)
            ads_usercount_results = self.get_result(
                "ads_usercount_of_retention_users.sql", date, date)
            ads_usercount = sum(1 for _ in ads_usercount_results)
            line_string += "{0},".format(ads_usercount)

            lines = file.readlines()
            head_line = [x.strip() for x in lines[1:2]][0]
            head_lines = head_line.split(',')[3:]
            for head in head_lines:
                headsegments = head.split('|')
                min_count = int(headsegments[0])
                max_count = sys.maxint if len(
                    headsegments) == 1 else int(headsegments[1])
                level_user_count = 0
                for k in range(len(ads_count_results)):
                    data = ads_count_results[k]
                    if data[0] >= min_count and data[0] <= max_count:
                        level_user_count += data[1]
                line_string += "{0},".format(level_user_count)
            append_line(report_lines, len(report_lines), line_string)
            file.close()
