#!/usr/bin/env python
# coding=utf-8

import os
import json
from project.base.date import *
from project.base.helper import *
from project.base.query import *
from project.base.report import *


def generate_will_ads_report(query_config, date):
    return Report(query_config, date).generate()


class Report(BaseReport):
    def __init__(self, query_config, date):
        super(Report, self).__init__(query_config, date)
        self.etc_filename = 'ads_will_of_new_users.csv'
        self.output_filename = 'will_ads_report.csv'

    def do_generate(self):
        print('do generate report')
        report_filepaths = []
        for level in range(6, 11):
            filepath = self.append_output_filename('_level_' + str(level))
            report_filepaths.append(filepath)
            with open(filepath, mode='w+') as out:
                report_lines = []
                for single_date in Date(self.start_date).rangeto(self.end_date, True):
                    self.generate_will_ads_report_at_date(
                        report_lines, single_date, level)
                reportstring = '\n'.join(report_lines)
                out.write(reportstring)
                out.close()
        return report_filepaths

    def generate_will_ads_report_at_date(self, report_lines, date, level):
        print("generate_will_ads_report_at_date ", date)
        with open(self.etc_filepath) as file:
            lines = [x.strip() for x in file.readlines()]
            result_lines = []
            for add_day in range(1):
                retention_date = Date(date).adddays(add_day)
                if Date(retention_date).between(self.end_date) <= 0:
                    break
                ads_show_count_results = self.get_result(
                    "will_ads_show_count.sql", date, retention_date, level)
                if len(ads_show_count_results) == 0:
                    break
                ads_view_count_results = self.get_result(
                    "will_ads_view_count.sql", date, retention_date, level)
                if add_day == 0:
                    firstopen_usercount = self.get_firstopen_count(date)
                    append_line(result_lines, 0, lines[0].format(
                        Date(date).formatmd()))
                    append_line(result_lines, 1, lines[1].format(
                        firstopen_usercount))
                append_line(result_lines, 2, lines[2].format(
                    Date(date).between(retention_date) - 1))
                append_line(result_lines, 3, lines[3])
                for i in range(4, len(lines) - 1):
                    line = lines[i]
                    linesegments = line.split('|', 1)
                    ads_scene = linesegments[0]
                    formatstring = linesegments[1]
                    ad_view_show_count = 0
                    ad_view_play_count = 0
                    for k in range(len(ads_show_count_results)):
                        ads_show_count_result = ads_show_count_results[k]
                        if ads_show_count_result.af_ad_scene == ads_scene:
                            ad_view_show_count = ads_show_count_result.ad_show_count
                            break
                    for k in range(len(ads_view_count_results)):
                        ads_view_count_result = ads_view_count_results[k]
                        if ads_view_count_result.af_ad_scene == ads_scene:
                            ad_view_play_count = ads_view_count_result.ad_play_count
                            break
                    ad_view_play_rate = float(
                        ad_view_play_count)/float(ad_view_show_count) * 100 if ad_view_show_count > 0 else 0
                    append_line(result_lines, i, formatstring.format(
                        ad_view_show_count, ad_view_play_count, ad_view_play_rate))
            report_lines.extend(result_lines)
            file.close()
