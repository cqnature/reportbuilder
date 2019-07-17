#!/usr/bin/env python
# coding=utf-8

import os
import json
from ..base.date import *
from ..base.helper import *
from ..base.query import *
from ..base.report import *

def generate_retention_ads_count_report(query_config, date):
    return Report(query_config, date).generate()

class Report(BaseReport):
    def __init__(self, query_config, date):
        super(Report, self).__init__(query_config, date)
        self.etc_filename = 'ads_count_of_retention_users.csv'
        self.output_filename = 'retention_ads_count_report.csv'

    def do_generate(self):
        print 'do generate report'
        with open(self.output_filepath, mode='w+') as out:
            report_lines = []
            for single_date in Date(self.start_date).rangeto(self.end_date, True):
                self.generate_retention_ads_count_report_at_date(report_lines, single_date)
            reportstring = ''.join(report_lines)
            out.write(reportstring)
            out.close()
        return [self.output_filepath]

    def generate_retention_ads_count_report_at_date(self, report_lines, date):
        print("generate_retention_ads_count_report_at_date ", date)
        with open(self.etc_filepath) as file:
            lines = file.readlines()
            retention_user_count = self.get_retention_count(date, date)
            ads_count_results = self.get_result("ads_count_of_retention_users.sql", date, date)
            if len(ads_count_results) == 0:
                return
            lines[0] = lines[0].format(Date(date).formatmd())
            lines[1] = lines[1].format(retention_user_count)
            linesegments = lines[3].split('|', 2)
            zero_user_count = retention_user_count - sum(t[1] for t in ads_count_results)
            lines[3] = linesegments[2].format(zero_user_count, float(zero_user_count)/float(retention_user_count) * 100)
            for i in range(4, len(lines)):
                line = lines[i]
                linesegments = line.split('|', 2)
                start_count = linesegments[0]
                end_count = linesegments[1]
                formatstring = linesegments[2]
                total_user_count = 0
                for k in range(len(ads_count_results)):
                    ads_count_result = ads_count_results[k]
                    if ads_count_result.view_count >= start_count and (end_count == '' or ads_count_result.view_count <= end_count):
                        total_user_count += ads_count_result.user_count
                lines[i] = formatstring.format(total_user_count, float(total_user_count)/float(retention_user_count))
            report_lines.extend(lines)
            file.close()
