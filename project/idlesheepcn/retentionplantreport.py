#!/usr/bin/env python
# coding=utf-8

import os
import json
from ..base.date import *
from ..base.helper import *
from ..base.query import *
from ..base.report import *


def generate_retentionplant_report(query_config, date):
    return Report(query_config, date).generate()


class Report(BaseReport):
    def __init__(self, query_config, date):
        super(Report, self).__init__(query_config, date)
        self.etc_filename = 'plant_progress_of_retention_users.csv'
        self.output_filename = 'retentionuser_plant_report.csv'

    def do_generate(self):
        print('do generate report')
        with open(self.output_filepath, mode='w+') as out:
            report_lines = []
            for single_date in Date('20190701').rangeto(self.end_date, True):
                self.generate_retentionplant_report_at_date(
                    report_lines, single_date)
            reportstring = '\n'.join(report_lines)
            out.write(reportstring)
            out.close()
        return [self.output_filepath]

    def get_plane_max_level(self):
        return 8

    def generate_retentionplant_report_at_date(self, report_lines, date):
        print("generate_retentionplant_report_at_date ", date)
        max_level = self.get_plane_max_level()
        with open(self.etc_filepath) as file:
            firstopen_usercount = self.get_firstopen_count(date)
            if firstopen_usercount == 0:
                return

            lineIndex = 0
            lines = file.readlines()
            signup_day_progress_lines = [x.strip() for x in lines[0:4]]
            signup_day_progress_results = self.get_result(
                "plant_progress_of_signup_users.sql", date)
            total_level_user_count = 0
            signup_day_progress_lines[1] = signup_day_progress_lines[1].format(
                Date(date).formatmd())
            signup_day_progress_lines[3] = signup_day_progress_lines[3].format(
                firstopen_usercount, 100)
            signup_base_datas = []
            progress_data_map = {}
            for k in range(0, max_level + 1):
                data = [k, 0, 0]
                signup_base_datas.append(data)
                progress_data_map[k] = data
            for row in signup_day_progress_results:
                progress_data = progress_data_map[row.max_level]
                progress_data[1] = row.user_count
                progress_data[2] = 100 * \
                    float(row.user_count)/float(firstopen_usercount)
                total_level_user_count += row.user_count
            first_progress_data = progress_data_map[0]
            first_progress_data[1] = first_progress_data[1] + \
                firstopen_usercount - total_level_user_count
            first_progress_data[2] = 100 * \
                float(first_progress_data[1])/float(firstopen_usercount)
            for k in range(len(signup_base_datas)):
                data = signup_base_datas[k]
                signup_day_progress_lines.append(
                    "{0},{1},{2:.2f}%,".format(data[0], data[1], data[2]))
            for k in range(len(signup_day_progress_lines)):
                append_line(report_lines, lineIndex + k,
                            signup_day_progress_lines[k], k != 0)
            lineIndex += len(signup_day_progress_lines)

            currentDayIndex = 1
            retention_day_progress_lines = []
            for single_date in Date(date).rangeto(self.get_retention_date(date)):
                # 留存率查询
                current_retention_usercount = self.get_retention_count(
                    date, single_date)
                # 留存分布查询
                retention_day_results = self.get_result(
                    "plant_progress_of_retention_users.sql", date, single_date)
                if currentDayIndex == 1:
                    retention_day_progress_lines.extend(
                        [x.strip() for x in lines[4:9]])
                else:
                    retention_day_progress_lines.extend(
                        [x.strip() for x in lines[9:]])
                    retention_day_progress_lines[0] = retention_day_progress_lines[0].format(
                        Date(date).between(single_date))
                current_retention_datas = []
                progress_data_map = {}
                for k in range(0, max_level + 1):
                    data = [k, 0, 0]
                    current_retention_datas.append(data)
                    progress_data_map[k] = data
                for row in retention_day_results:
                    progress_data = progress_data_map[row.max_level]
                    progress_data[1] = row.user_count
                    progress_data[2] = 100 * \
                        float(row.user_count)/float(firstopen_usercount)
                retention_day_progress_lines[1] = retention_day_progress_lines[1].format(
                    Date(date).formatmd())
                retention_day_progress_lines[3] = retention_day_progress_lines[3].format(
                    firstopen_usercount, 100)
                if currentDayIndex == 1:
                    retention_day_progress_lines[4] = retention_day_progress_lines[4].format(
                        current_retention_usercount, 100*float(current_retention_usercount)/float(firstopen_usercount))
                else:
                    retention_day_progress_lines[4] = retention_day_progress_lines[4].format(Date(date).between(
                        single_date), current_retention_usercount, 100*float(current_retention_usercount)/float(firstopen_usercount))
                current_retention_datas[0][1] = current_retention_datas[0][1] + \
                    current_retention_usercount - \
                    sum(t[1] for t in current_retention_datas)
                current_retention_datas[0][2] = 100*float(
                    current_retention_datas[0][1])/float(firstopen_usercount)
                for k in range(len(current_retention_datas)):
                    data = current_retention_datas[k]
                    retention_day_progress_lines.append(
                        "{0},{1},{2:.2f}%,".format(data[0], data[1], data[2]))

                # 数据拼接
                for k in range(len(retention_day_progress_lines)):
                    append_line(report_lines, lineIndex + k,
                                retention_day_progress_lines[k], k != 0)
                lineIndex += len(retention_day_progress_lines)
                # 增加天数索引
                currentDayIndex += 1
                # 清空缓存
                del retention_day_progress_lines[:]
            file.close()
