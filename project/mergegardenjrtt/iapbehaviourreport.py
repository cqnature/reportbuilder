#!/usr/bin/env python
# coding=utf-8

import os
import json
from ..base.date import *
from ..base.helper import *
from ..base.query import *
from ..base.report import *


def event_timestamp(e):
    return e.event_timestamp


def generate_iap_behaviour_report(query_config, date):
    return Report(query_config, date).generate()


class Report(BaseReport):
    def __init__(self, query_config, date):
        super(Report, self).__init__(query_config, date)
        self.etc_filename = 'behaviour_of_spend_gems.csv'
        self.output_filename = 'iap_behaviour_report.csv'

    def do_generate(self):
        print('do generate report')
        with open(self.output_filepath, mode='w+') as out:
            report_lines = []
            for single_date in Date(self.start_date).rangeto(self.end_date, True):
                self.generate_iap_behaviour_report_at_date(
                    report_lines, single_date)
            reportstring = '\n'.join(report_lines)
            out.write(reportstring)
            out.close()
        return [self.output_filepath]

    def generate_iap_behaviour_report_at_date(self, report_lines, date):
        print("generate_iap_behaviour_report_at_date ", date)
        with open(self.etc_filepath) as file:
            lines = file.readlines()
            iap_purchase_results = self.get_result(
                "in_app_purchase_users.sql", date, self.end_date)
            if len(iap_purchase_results) == 0:
                return
            spend_gems_results = self.get_result(
                "spend_virtual_currency_detail.sql", date, self.end_date)
            iap_purchase_lines = [x.strip() for x in lines[0:1]]
            iap_purchase_lines[0] = iap_purchase_lines[0].format(
                Date(date).formatmd())
            spend_gems_map = {}
            for i in range(3, len(lines)):
                line = lines[i].strip()
                linesegments = line.split('|', 1)
                spend_scene = linesegments[0]
                formatstring = linesegments[1]
                spend_gems_map[spend_scene] = formatstring
            iap_purchase_users = {}
            for k in range(len(iap_purchase_results)):
                iap_purchase_result = iap_purchase_results[k]
                if not iap_purchase_users.has_key(iap_purchase_result.user_pseudo_id):
                    iap_purchase_users[iap_purchase_result.user_pseudo_id] = 1
            iap_purchase_datas = {}
            max_result_count = 0
            for key, value in iap_purchase_users.iteritems():
                spend_gems_datas = [
                    x for x in iap_purchase_results if x.user_pseudo_id == key]
                spend_gems_datas.extend(
                    [x for x in spend_gems_results if x.user_pseudo_id == key])
                spend_gems_datas.sort(key=event_timestamp)
                iap_purchase_datas[key] = spend_gems_datas
                max_result_count = max(max_result_count, len(spend_gems_datas))
            for key, spend_gems_datas in iap_purchase_datas.iteritems():
                append_line(iap_purchase_lines, 1,
                            lines[1].strip().format(key))
                append_line(iap_purchase_lines, 2, lines[2].strip())
                for k in range(0, max_result_count):
                    if k >= len(spend_gems_datas):
                        append_line(lines, 3 + k, ",,,")
                    else:
                        spend_gems_data = spend_gems_datas[k]
                        try:
                            append_line(iap_purchase_lines, 3 + k, spend_gems_map[spend_gems_data.item_name].format(
                                spend_gems_data.event_timestamp, -spend_gems_data.value))
                        except AttributeError:
                            append_line(iap_purchase_lines, 3 + k, spend_gems_map[spend_gems_data.item_name].format(
                                spend_gems_data.event_timestamp))
            report_lines.extend(iap_purchase_lines)
            file.close()
