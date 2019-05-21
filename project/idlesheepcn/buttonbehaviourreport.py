#!/usr/bin/env python
# coding=utf-8

import os
import json
from ..base.date import *
from ..base.helper import *
from ..base.query import *
from ..base.report import *

def generate_button_behaviour_report(query_config, date):
    return Report(query_config, date).generate()

class Report(BaseReport):
    def __init__(self, query_config, date):
        super(Report, self).__init__(query_config, date)
        self.etc_filename = 'button_behaviour_of_users.csv'
        self.output_filename = 'button_behaviour_report.csv'

    def do_generate(self):
        print 'do generate report'
        with open(self.output_filepath, mode='w+') as out:
            report_lines = []
            for single_date in Date(self.start_date).rangeto(self.end_date, True):
                self.generate_button_behaviour_report_at_date(report_lines, single_date)
            reportstring = '\n'.join(report_lines)
            out.write(reportstring)
            out.close()
        return [self.output_filepath]

    def generate_button_behaviour_report_at_date(self, report_lines, date):
        print("generate_button_behaviour_report_at_date ", date)
        with open(self.etc_filepath) as file:
            lines = file.readlines()
            for single_date in Date(date).rangeto(self.end_date, True):
                first_user_count = self.get_firstopen_count(single_date)
                if first_user_count == 0:
                    continue
                show_button_of_signup_results = self.get_result("show_button_of_signup_users.sql", single_date)
                show_count = sum(1 for _ in show_button_of_signup_results)
                click_button_of_signup_results = self.get_result("click_button_of_signup_users.sql", single_date)
                click_count = sum(1 for _ in click_button_of_signup_results)
                average_rate = 0 if show_count == 0 else float(click_count)/float(show_count) * 100
                append_line(report_lines, len(report_lines), "{0},{1},{2},{3:.2f%},".format(first_user_count, show_count, click_count, average_rate))
            file.close()
