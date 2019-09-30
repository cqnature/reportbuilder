#!/usr/bin/env python
# coding=utf-8

import os
import json
from ..base.date import *
from ..base.helper import *
from ..base.query import *
from ..base.report import *

add_scene_count = 8

def generate_lost_ads_report(query_config, date):
    return Report(query_config, date).generate()

class Report(BaseReport):
    def __init__(self, query_config, date):
        super(Report, self).__init__(query_config, date)
        self.etc_filename = 'ads_view_of_lost_users.csv'
        self.output_filename = 'lost_ads_report.csv'

    def do_generate(self):
        print 'do generate report'
        with open(self.output_filepath, mode='w+') as out:
            report_lines = []
            for single_date in Date(self.start_date).rangeto(self.end_date, True):
                self.generate_lost_ads_report_at_date(report_lines, single_date)
            reportstring = '\n'.join(report_lines)
            out.write(reportstring)
            out.close()
        return [self.output_filepath]

    def generate_lost_ads_report_at_date(self, report_lines, date):
        print("generate_lost_ads_report_at_date ", date)
        with open(self.etc_filepath) as file:
            lines = [x.strip() for x in file.readlines()]
            result_lines = []
            for add_day in range(1, 2):
                retention_date = Date(date).adddays(add_day)
                if Date(retention_date).between(self.end_date) <= 0:
                    break
                ads_view_count_results = self.get_result("lost_ads_view_count.sql", date, retention_date, Date(retention_date).adddays(-1))
                if len(ads_view_count_results) == 0:
                    break
                ads_view_user_results = self.get_result("lost_ads_view_users.sql", date, retention_date, Date(retention_date).adddays(-1))
                if add_day == 1:
                    append_line(result_lines, 0, lines[0].format(Date(date).formatmd()))
                    append_line(result_lines, 1, lines[1].format(ads_view_count_results[0].lost_user_count))
                append_line(result_lines, 2, lines[2].format(Date(date).between(retention_date) - 1))
                append_line(result_lines, 3, lines[3])
                ads_click_count_results = self.get_result("lost_ads_click_count.sql", date, retention_date, Date(retention_date).adddays(-1))
                currentIndex = 4 + add_scene_count
                for i in range(4, currentIndex):
                    line = lines[i]
                    linesegments = line.split('|', 2)
                    ads_scene = linesegments[0]
                    ads_click_button = linesegments[1]
                    formatstring = linesegments[2]
                    ad_view_count = 0
                    ad_click_count = 0
                    lost_average_ad_view_count = 0
                    ad_view_user_count = 0
                    lost_ad_view_user_percent = 0
                    for k in range(len(ads_view_count_results)):
                        ads_view_count_result = ads_view_count_results[k]
                        if ads_view_count_result.af_ad_scene == ads_scene:
                            ad_view_count = ads_view_count_result.ad_view_count
                            lost_average_ad_view_count = ads_view_count_result.lost_average_ad_view_count
                            break
                    for k in range(len(ads_view_user_results)):
                        ads_view_user_result = ads_view_user_results[k]
                        if ads_view_user_result.af_ad_scene == ads_scene:
                            ad_view_user_count = ads_view_user_result.ad_view_user_count
                            lost_ad_view_user_percent = ads_view_user_result.lost_ad_view_user_percent
                            break
                    for k in range(len(ads_click_count_results)):
                        ads_click_count_result = ads_click_count_results[k]
                        if ads_click_count_result.af_button_name == ads_click_button:
                            ad_click_count = ads_click_count_result.ad_click_count
                            break
                    append_line(result_lines, i, formatstring.format(ad_view_user_count, lost_ad_view_user_percent * 100, ad_click_count, ad_view_count, lost_average_ad_view_count))
                append_line(result_lines, currentIndex, lines[currentIndex].format(sum(t.lost_average_ad_view_count for t in ads_view_count_results)))

                ads_view_count_results = self.get_result("new_retention_ads_view_count.sql", date, retention_date, Date(retention_date).adddays(-1))
                if len(ads_view_count_results) == 0:
                    break
                ads_view_user_results = self.get_result("new_retention_ads_view_users.sql", date, retention_date, Date(retention_date).adddays(-1))
                if add_day == 1:
                    append_line(result_lines, currentIndex + 1, lines[currentIndex + 1].format(Date(date).formatmd()))
                    append_line(result_lines, currentIndex + 2, lines[currentIndex + 2].format(ads_view_count_results[0].retention_user_count))
                append_line(result_lines, currentIndex + 3, lines[currentIndex + 3].format(Date(date).between(retention_date) - 1))
                append_line(result_lines, currentIndex + 4, lines[currentIndex + 4])
                ads_click_count_results = self.get_result("new_retention_ads_click_count.sql", date, retention_date, Date(retention_date).adddays(-1))
                for i in range(currentIndex + 5, currentIndex + 5 + add_scene_count):
                    line = lines[i]
                    linesegments = line.split('|', 2)
                    ads_scene = linesegments[0]
                    ads_click_button = linesegments[1]
                    formatstring = linesegments[2]
                    ad_view_count = 0
                    ad_click_count = 0
                    retetion_average_ad_view_count = 0
                    ad_view_user_count = 0
                    retetion_ad_view_user_percent = 0
                    for k in range(len(ads_view_count_results)):
                        ads_view_count_result = ads_view_count_results[k]
                        if ads_view_count_result.af_ad_scene == ads_scene:
                            ad_view_count = ads_view_count_result.ad_view_count
                            retetion_average_ad_view_count = ads_view_count_result.retetion_average_ad_view_count
                            break
                    for k in range(len(ads_view_user_results)):
                        ads_view_user_result = ads_view_user_results[k]
                        if ads_view_user_result.af_ad_scene == ads_scene:
                            ad_view_user_count = ads_view_user_result.ad_view_user_count
                            retetion_ad_view_user_percent = ads_view_user_result.retetion_ad_view_user_percent
                            break
                    for k in range(len(ads_click_count_results)):
                        ads_click_count_result = ads_click_count_results[k]
                        if ads_click_count_result.af_button_name == ads_click_button:
                            ad_click_count = ads_click_count_result.ad_click_count
                            break
                    append_line(result_lines, i, formatstring.format(ad_view_user_count, retetion_ad_view_user_percent * 100, ad_click_count, ad_view_count, retetion_average_ad_view_count))
                append_line(result_lines, len(lines) - 1, lines[len(lines) - 1].format(sum(t.retetion_average_ad_view_count for t in ads_view_count_results)))
            report_lines.extend(result_lines)
            file.close()
