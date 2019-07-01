#!/usr/bin/env python
# coding=utf-8

import os
import json
from ..base.date import *
from ..base.helper import *
from ..base.query import *
from ..base.report import *

def generate_new_ads_report(query_config, date):
    return Report(query_config, date).generate()

class Report(BaseReport):
    def __init__(self, query_config, date):
        super(Report, self).__init__(query_config, date)
        self.etc_filename = 'ads_view_of_new_users.csv'
        self.output_filename = 'new_ads_report.csv'

    def do_generate(self):
        print 'do generate report'
        with open(self.output_filepath, mode='w+') as out:
            report_lines = []
            for single_date in Date(self.start_date).rangeto(self.end_date, True):
                self.generate_new_ads_report_at_date(report_lines, single_date)
            reportstring = '\n'.join(report_lines)
            out.write(reportstring)
            out.close()
        return [self.output_filepath]

    def generate_new_ads_report_at_date(self, report_lines, date):
        print("generate_new_ads_report_at_date ", date)
        with open(self.etc_filepath) as file:
            lines = [x.strip() for x in file.readlines()]
            result_lines = []
            for add_day in range(7):
                retention_date = Date(date).adddays(add_day)
                if Date(retention_date).between(self.end_date) <= 0:
                    break
                retention_user_count = self.get_retention_count(date, retention_date)
                ads_view_count_results = self.get_result("new_ads_view_count.sql", date, retention_date)
                if len(ads_view_count_results) == 0:
                    break
                ads_view_user_results = self.get_result("new_ads_view_users.sql", date, retention_date)
                if add_day == 0:
                    append_line(result_lines, 0, lines[0].format(Date(date).formatmd()))
                    append_line(result_lines, 1, lines[1].format(ads_view_count_results[0].new_user_count))
                append_line(result_lines, 2, lines[2].format(Date(date).between(retention_date) - 1))
                append_line(result_lines, 3, lines[3])
                for i in range(4, len(lines) - 1):
                    line = lines[i]
                    linesegments = line.split('|', 1)
                    ads_scene = linesegments[0]
                    formatstring = linesegments[1]
                    ad_view_count = 0
                    daily_average_ad_view_count = 0
                    ad_view_trigger_user_count = 0
                    ad_view_user_count = 0
                    daily_ad_view_user_percent = 0
                    if ads_scene == 'levelup':
                        max_level = 10 if Date(retention_date).between('20190621', 0) <= 0 else 2
                        trigger_user_results = self.get_result("trigger_levelup_ads_user_id.sql", date, retention_date, max_level)
                        ad_view_trigger_user_count = sum(1 for _ in trigger_user_results)
                    elif ads_scene == 'freeupgrade':
                        if Date(retention_date).between('20190621', 0) <= 0:
                            trigger_user_results = self.get_result("trigger_freeupgrade_ads_user_id_2.sql", date, retention_date)
                            ad_view_trigger_user_count = sum(1 for _ in trigger_user_results)
                        else:
                            trigger_user_results = self.get_result("trigger_freeupgrade_ads_user_id.sql", date, retention_date)
                            ad_view_trigger_user_count = sum(1 for _ in trigger_user_results)
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
                    append_line(result_lines, i, formatstring.format(ad_view_trigger_user_count, float(ad_view_trigger_user_count) / float(retention_user_count) * 100, ad_view_user_count, daily_ad_view_user_percent * 100, ad_view_count, daily_average_ad_view_count))
                append_line(result_lines, len(lines) - 1, lines[len(lines) - 1].format(sum(t.daily_average_ad_view_count for t in ads_view_count_results)))
            report_lines.extend(result_lines)
            file.close()
