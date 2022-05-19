#!/usr/bin/env python
# coding=utf-8

import os
import json
from project.base.date import *
from project.base.helper import *
from project.base.query import *
from project.base.report import *


def generate_retention_event_report(query_config, date):
    return Report(query_config, date).generate()


class Report(BaseReport):
    def __init__(self, query_config, date):
        super(Report, self).__init__(query_config, date)
        self.etc_filename = 'event_of_retention_users.csv'
        self.output_filename = 'retention_event_report.csv'

    def do_generate(self):
        print('do generate report')
        with open(self.output_filepath, mode='w+') as out:
            tmp_lines = []
            for single_date in Date('20190629').rangeto(self.end_date, True):
                report_single_lines = self.generate_retention_event_report_at_date(
                    single_date)
                if report_single_lines != None:
                    tmp_lines.append(report_single_lines)
            report_lines = append_line_list(tmp_lines, ',,,')
            reportstring = '\n'.join(report_lines)
            out.write(reportstring)
            out.close()
        return [self.output_filepath]

    def generate_retention_event_report_at_date(self, date):
        print("generate_retention_event_report_at_date ", date)
        report_lines = []
        with open(self.etc_filepath) as file:
            firstopen_usercount = self.get_firstopen_count(date)
            if firstopen_usercount == 0:
                return

            lineIndex = 0
            lines = file.readlines()
            signup_day_progress_lines = [x.strip() for x in lines[0:4]]
            signup_day_progress_results = self.get_result(
                "event_progress_of_signup_users.sql", date)
            signup_day_progress_lines[1] = signup_day_progress_lines[1].format(
                Date(date).formatmd())
            signup_day_progress_lines[3] = signup_day_progress_lines[3].format(
                firstopen_usercount, 100)
            signup_base_datas = []
            for row in signup_day_progress_results:
                signup_base_data = [row.instancegame_id, row.event_count,
                                    row.user_count, 100*float(row.user_count)/float(firstopen_usercount)]
                signup_base_datas.append(signup_base_data)
            for k in range(len(signup_base_datas)):
                data = signup_base_datas[k]
                signup_day_progress_lines.append(
                    "{0}-{1},{2},{3:.2f}%,".format(data[0], data[1], data[2], data[3]))
            for k in range(len(signup_day_progress_lines)):
                append_line(report_lines, lineIndex + k,
                            signup_day_progress_lines[k])
            lineIndex += len(signup_day_progress_lines)

            currentDayIndex = 1
            retention_day_progress_lines = []
            # 留存率查询
            for single_date in Date(date).rangeto(self.get_retention_date(date)):
                current_retention_usercount = self.get_retention_count(
                    date, single_date)
                # 流失分布查询
                retention_day_results = self.get_result(
                    "event_progress_of_retention_users.sql", date, single_date)
                if currentDayIndex == 1:
                    retention_day_progress_lines.extend(
                        [x.strip() for x in lines[4:9]])
                else:
                    retention_day_progress_lines.extend(
                        [x.strip() for x in lines[9:]])
                    retention_day_progress_lines[0] = retention_day_progress_lines[0].format(
                        Date(date).between(single_date))
                retention_base_datas = []
                for row in retention_day_results:
                    retention_base_data = [row.instancegame_id, row.event_count,
                                           row.user_count, 100*float(row.user_count)/float(firstopen_usercount)]
                    retention_base_datas.append(retention_base_data)

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
                for k in range(len(retention_base_datas)):
                    data = retention_base_datas[k]
                    retention_day_progress_lines.append(
                        "{0}-{1},{2},{3:.2f}%,".format(data[0], data[1], data[2], data[3]))

                # 数据拼接
                for k in range(len(retention_day_progress_lines)):
                    append_line(report_lines, lineIndex + k,
                                retention_day_progress_lines[k])
                lineIndex += len(retention_day_progress_lines)
                # 增加天数索引
                currentDayIndex += 1
                # 清空缓存
                del retention_day_progress_lines[:]
            file.close()
        return report_lines
