#!/usr/bin/env python
# coding=utf-8

import os
import json
from ..base.date import *
from ..base.helper import *
from ..base.query import *
from ..base.report import *

area_id = 0

def generate_retention_ads_report(query_config, date):
    return Report(query_config, date).generate()

class Report(BaseReport):
    def __init__(self, query_config, date):
        super(Report, self).__init__(query_config, date)
        self.etc_filename = 'ads_view_of_retention_users.csv'
        country_string = "CN" if self.query_config.geo_country == 'China' else "US"
        platform_string = "AND" if self.query_config.platform == 'ANDROID' else "iOS"
        self.output_filename = "{0}-{1}-Day1-Ad-Area{2}-Level-{3}.csv".format(country_string, platform_string, area_id + 1, self.end_date)

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
                self.generate_retention_ads_report_at_date(report_lines, single_date)
            lately_date = max(Date(self.end_date).adddays(-14), self.start_date)
            for single_date in Date(lately_date).rangeto(self.end_date, True):
                self.generate_retention_ads_report_at_date(report_lines, single_date)
            reportstring = '\n'.join(report_lines)
            out.write(reportstring)
            out.close()
        return [self.output_filepath]

    def generate_retention_ads_report_at_date(self, report_lines, date):
        print("generate_retention_ads_report_at_date ", date)
        with open(self.etc_filepath) as file:
            firstopen_usercount = self.get_firstopen_count(date)
            if firstopen_usercount == 0:
                return
            level_view_count_results = self.get_result("level_ads_view_of_retention_users.sql", date, date, area_id)
            if len(level_view_count_results) == 0:
                return
            area_view_count_results = self.get_result("area_ads_view_of_retention_users.sql", date, date)

            lines = file.readlines()
            line_string = ""
            line_string += "{0},".format(Date(date).formatmd())
            line_string += "{0},".format(firstopen_usercount)

            user_count = firstopen_usercount
            for row in area_view_count_results:
                if row.max_area == area_id:
                    line_string += "{0:.2f}%,{1:.2f},".format(100*float(row.ads_user_count)/float(user_count), float(row.ads_view_count)/float(user_count))

            head_line = [x.strip() for x in lines[2:3]][0]
            head_lines = head_line.split(',')
            for head in head_lines:
                headsegments = head.split('|')
                min_level = int(headsegments[0])
                max_level = sys.maxint if len(headsegments) == 1 else int(headsegments[1])
                ads_user_count = 0
                ads_view_count = 0
                for k in range(len(level_view_count_results)):
                    level_view_count_result = level_view_count_results[k]
                    if level_view_count_result.level >= min_level and level_view_count_result.level <= max_level:
                        ads_user_count += level_view_count_result.ads_user_count
                        ads_view_count += level_view_count_result.ads_view_count
                line_string += "{0:.2f}%,{1:.2f},".format(100*float(ads_user_count)/float(user_count), float(ads_view_count)/float(user_count))
            append_line(report_lines, len(report_lines), line_string)
            file.close()
