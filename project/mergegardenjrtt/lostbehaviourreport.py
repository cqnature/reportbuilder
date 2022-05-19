#!/usr/bin/env python
# coding=utf-8

import os
import json
from project.base.date import *
from project.base.helper import *
from project.base.query import *
from project.base.report import *

# 次留=1 三留=2 四留=3
add_day = 2


def add_map_key_count(map, key):
    if key == None:
        key = 0
    map[key] = map.get(key, 0) + 1


def print_map(lines, map, start_index, max_count, first_open_usercount):
    mapKeys = map.keys()
    mapKeys.sort()
    for k in range(max_count):
        if k >= len(mapKeys):
            append_line(lines, start_index + k, ",,,")
        else:
            key = mapKeys[k]
            value = map.get(key)
            append_line(lines, start_index + k, "{0},{1},{2:.2f}%,".format(
                key, value, 100*float(value)/float(first_open_usercount)))


def generate_lostbehaviour_report(query_config, date):
    return Report(query_config, date).generate()


class Report(BaseReport):
    def __init__(self, query_config, date):
        super(Report, self).__init__(query_config, date)
        self.etc_filename = 'behaviour_of_lost_users.csv'
        self.output_filename = 'lostuser_behaviour_report.csv'

    def do_generate(self):
        print('do generate report')
        report_filepaths = []
        for level in range(7, 9):
            filepath = self.append_output_filename('_level_' + str(level))
            report_filepaths.append(filepath)
            with open(filepath, mode='w+') as out:
                report_lines = []
                for single_date in Date(self.start_date).rangeto(self.end_date, True):
                    if Date(single_date).between(self.end_date) <= add_day:
                        continue
                    self.generate_lostbehaviour_report_at_date(
                        report_lines, single_date, level)
                reportstring = '\n'.join(report_lines)
                out.write(reportstring)
                out.close()
        return report_filepaths

    def generate_lostbehaviour_report_at_date(self, report_lines, date, level):
        print("generate_lostbehaviour_report_at_date ", date)
        with open(self.etc_filepath) as file:
            # 新增用户数
            firstopen_usercount = get_firstopen_usercount(self.querysql, date)
            if firstopen_usercount == 0:
                return
            lines = file.readlines()
            lines[0] = lines[0].strip().format(Date(date).formatmd())
            lines[1] = lines[1].strip().format(firstopen_usercount)
            # 次日留存用户数
            cur_date = Date(date)
            retention_usercount = get_retention_usercount(
                self.querysql, date, cur_date.adddays(add_day))
            lines[2] = lines[2].strip().format(retention_usercount, 100 *
                                               float(retention_usercount)/float(firstopen_usercount))
            behaviour_results = self.querysql.get_result(
                "behaviour_of_lost_users.sql", date, cur_date.adddays(add_day), cur_date.adddays(add_day - 1), level)
            lost_usercount = sum(1 for _ in behaviour_results)
            lines[3] = lines[3].strip().format(level, lost_usercount,
                                               100*float(lost_usercount)/float(firstopen_usercount))
            lines[4] = lines[4].strip().format(level)
            dataset_map = []
            key_count = 16
            key_offset = 2
            for k in range(key_count):
                dataset_map.append({})
            for k in range(len(behaviour_results)):
                behaviour_result = behaviour_results[k]
                for t in range(key_count):
                    add_map_key_count(
                        dataset_map[t], behaviour_result[t + key_offset])
            max_count = max(len(map) for map in dataset_map)
            start_index = len(lines)
            for k in range(key_count):
                print_map(
                    lines, dataset_map[k], start_index, max_count, firstopen_usercount)
            report_lines.extend(lines)
            file.close()
