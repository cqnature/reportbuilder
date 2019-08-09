#!/usr/bin/env python
# coding=utf-8

import os
import json
from ..base.date import *
from ..base.helper import *
from ..base.query import *
from ..base.report import *

def generate_total_ads_report(query_config, date):
    return Report(query_config, date).generate()

class Report(BaseReport):
    def __init__(self, query_config, date):
        super(Report, self).__init__(query_config, date)
        self.etc_filename = 'total_ads_view_of_users.csv'
        country_string = "CN" if self.query_config.geo_country == 'China' else "US"
        platform_string = "AND" if self.query_config.platform == 'ANDROID' else "iOS"
        self.output_filename = "{0}-{1}-Ad-Area-{2}.csv".format(country_string, platform_string, self.end_date)


    def do_generate(self):
        print 'do generate report'
        with open(self.output_filepath, mode='w+') as out:
            report_lines = []
            with open(self.etc_filepath) as file:
                lines = file.readlines()
                head_lines1 = [x.strip() for x in lines[0:3]]
                for k in range(len(head_lines1)):
                    append_line(report_lines, k, head_lines1[k])
                head_lines2 = [x.strip() for x in lines[3:6]]
                for d in range(7):
                    for k in range(len(head_lines2)):
                        append_line(report_lines, k, head_lines2[k].format(d + 1))
                file.close()
            for single_date in self.extra_date:
                self.generate_total_ads_report_at_date(report_lines, single_date)
            lately_date = max(Date(self.end_date).adddays(-14), self.start_date)
            for single_date in Date(lately_date).rangeto(self.end_date, True):
                self.generate_total_ads_report_at_date(report_lines, single_date)
            reportstring = '\n'.join(report_lines)
            out.write(reportstring)
            out.close()
        return [self.output_filepath]

    def get_plane_max_level(self):
        return 5

    def generate_total_ads_report_at_date(self, report_lines, date):
        print("generate_total_ads_report_at_date ", date)
        max_level = self.get_plane_max_level()
        firstopen_usercount = self.get_firstopen_count(date)
        if firstopen_usercount == 0:
            return

        line_string = ""
        line_string += "{0},".format(Date(date).formatmd())
        line_string += "{0},".format(firstopen_usercount)
        for single_date in Date(date).rangeto(Date(date).adddays(6), True):
            if Date(single_date).between(self.end_date) <= 0:
                line_string += ",,,,,"
            else:
                ads_view_count_results = self.get_result("area_ads_view_of_retention_users.sql", date, single_date)
                user_count = 0
                if date == single_date:
                    user_count = self.get_firstopen_count(single_date)
                else:
                    user_count = self.get_retention_count(date, single_date)
                ads_base_datas = []
                progress_data_map = {}
                for k in range(0, max_level):
                    data = [k, 0, 0]
                    ads_base_datas.append(data)
                    progress_data_map[k] = data
                for row in ads_view_count_results:
                    progress_data = progress_data_map[row.max_area]
                    progress_data[1] = 100*float(row.ads_user_count)/float(user_count)
                    progress_data[2] = float(row.ads_view_count)/float(user_count)
                for k in ads_base_datas:
                    line_string += "{0:.2f}%,{1:.2f},".format(k[1], k[2])
        append_line(report_lines, len(report_lines), line_string)
