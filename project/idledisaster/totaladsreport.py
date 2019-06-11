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
        self.output_filename = 'total_ads_report.csv'

    def do_generate(self):
        print 'do generate report'
        with open(self.output_filepath, mode='w+') as out:
            report_lines = []
            for single_date in Date(self.start_date).rangeto(self.end_date, True):
                self.generate_total_ads_report_at_date(report_lines, single_date)
            reportstring = '\n'.join(report_lines)
            out.write(reportstring)
            out.close()
        return [self.output_filepath]

    def generate_total_ads_report_at_date(self, report_lines, date):
        print("generate_total_ads_report_at_date ", date)
        if date == self.start_date:
            with open(self.etc_filepath) as file:
                lines = file.readlines()
                for k in range(2):
                    append_line(report_lines, k, lines[k].strip())
                for single_date in Date(date).rangeto(self.end_date, True):
                    append_line(report_lines, 0, lines[2].strip().format(Date(date).between(single_date) - 1))
                    append_line(report_lines, 1, lines[3].strip())
                file.close()

        index = len(report_lines)
        append_line(report_lines, index, "{0},".format(Date(date).formatmd()))
        for single_date in Date(date).rangeto(self.end_date, True):
            ads_view_count_results = self.get_result("ads_view_of_retention_users.sql", date, single_date)
            user_count = 0
            if date == single_date:
                user_count = self.get_firstopen_count(single_date)
            else:
                user_count = self.get_retention_count(date, single_date)
            view_count = sum(1 for _ in ads_view_count_results)
            average_view_count = 0 if user_count == 0 else float(view_count)/float(user_count)
            append_line(report_lines, index, "{0},{1},{2:.2f},".format(user_count, view_count, average_view_count))
