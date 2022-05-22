#!/usr/bin/env python
# coding=utf-8

import os
import json
from project.base.date import *
from project.base.helper import *
from project.base.query import *
from project.base.report import *

# 次留=1 三留=2 四留=3
lost_day = 1
area_id = 1
max_level = 30


def add_map_key_count(map, key):
    if key == None:
        key = 0
    map[key] = map.get(key, 0) + 1


def print_map(map):
    total_count_of_two = 0
    for key, value in map.iteritems():
        if key > 2:
            total_count_of_two += value
    return "{0},{1},{2},{3},".format(map.get(0, 0), map.get(1, 0), map.get(2, 0), total_count_of_two)


def print_detail_map(map):
    output_string = ''
    for k in range(1, 9):
        output_string += "{0},".format(map.get(k, 0))
    return output_string


def generate_lostbehaviour_report(query_config, date):
    return Report(query_config, date).generate()


class Report(BaseReport):
    def __init__(self, query_config, date):
        super(Report, self).__init__(query_config, date)
        self.etc_filename = 'behaviour_of_lost_users.csv'
        country_string = self.query_config.geo_country
        platform_string = self.query_config.platform
        self.output_filename = "{0}-{1}-Day{2}-LostUser-Area{3}-Behaviour-{4}.csv".format(
            country_string, platform_string, lost_day, area_id, self.end_date)

    def do_generate(self):
        print('do generate report')
        report_filepaths = []
        for single_date in self.extra_date:
            self.generate_lostbehaviour_report_at(
                single_date, report_filepaths)
        for single_date in Date(self.start_date).rangeto(self.end_date, True):
            self.generate_lostbehaviour_report_at(
                single_date, report_filepaths)
        return report_filepaths

    def generate_lostbehaviour_report_at(self, single_date, report_filepaths):
        if Date(single_date).between(self.end_date) <= lost_day:
            return
        filepath = self.append_output_filename('_date_' + single_date)
        report_filepaths.append(filepath)
        with open(filepath, mode='w+') as out:
            report_lines = []
            with open(self.etc_filepath) as file:
                lines = file.readlines()
                head_lines1 = [x.strip() for x in lines[0:2]]
                report_lines.extend(head_lines1)
                file.close()
            for rebirth in range(0, area_id):
                for level in range(1, max_level + 1):
                    if rebirth == 1 and level == 1:
                        continue
                    self.generate_lostbehaviour_report_at_date(
                        report_lines, single_date, rebirth, level)
            reportstring = '\n'.join(report_lines)
            out.write(reportstring)
            out.close()

    def generate_lostbehaviour_report_at_date(self, report_lines, date, rebirth, level):
        print("generate_lostbehaviour_report_at_date ", date)
        with open(self.etc_filepath) as file:
            # 新增用户数
            firstopen_usercount = get_firstopen_usercount(self.querysql, date)
            if firstopen_usercount == 0:
                return

            cur_date = Date(date)
            behaviour_results = None
            if rebirth == 0 and level == 1:
                behaviour_results = self.querysql.get_result(
                    "behaviour_of_lost_users_0.sql", date, cur_date.adddays(lost_day), cur_date.adddays(lost_day - 1))
            else:
                behaviour_results = self.querysql.get_result("behaviour_of_lost_users.sql", date, cur_date.adddays(
                    lost_day), cur_date.adddays(lost_day - 1), rebirth, level)
            dataset_map = []
            key_count = 7
            key_offset = 3
            detail_count_index = 3
            for k in range(key_count):
                dataset_map.append({})
            for k in range(len(behaviour_results)):
                behaviour_result = behaviour_results[k]
                for t in range(key_count):
                    add_map_key_count(
                        dataset_map[t], behaviour_result[t + key_offset])

            line_string = "{0},".format(level)
            for k in range(detail_count_index):
                line_string += print_map(dataset_map[k])

            line_string += print_detail_map(dataset_map[detail_count_index])
            for k in range(detail_count_index + 1, key_count):
                line_string += print_map(dataset_map[k])

            # 数据拼接
            append_line(report_lines, len(report_lines), line_string)
            file.close()
