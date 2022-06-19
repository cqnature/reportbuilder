#!/usr/bin/env python
# coding=utf-8

import os
import json
import sys
from project.base.date import *
from project.base.helper import *
from project.base.query import *
from project.base.report import *

retention_day = [1, 2, 3, 4, 5, 6]
extra_retention_day = [7]


def generate_retention_push_report(query_config, date):
    return Report(query_config, date).generate()


class Report(BaseReport):
    def __init__(self, query_config, date):
        super(Report, self).__init__(query_config, date)
        self.etc_filename = '留存玩家推进占比.csv'
        country_string = self.query_config.geo_country
        platform_string = self.query_config.platform
        self.output_filename = "{0}-{1}-RetentionUser-Stage-{2}.csv".format(
            country_string, platform_string, self.end_date)

    def do_generate(self):
        print('do generate report')
        with open(self.output_filepath, mode='w+') as out:
            report_lines = []
            with open(self.etc_filepath) as file:
                lines = file.readlines()
                head_lines1 = [x.strip() for x in lines[0:2]]
                # 日期和新增
                for k in range(len(head_lines1)):
                    append_line(report_lines, k, head_lines1[k])
                # 1-6天
                for d in retention_day:
                    startline = 2 + 3 * (d - 1)
                    endline = 4 + 3 * (d - 1)
                    head_lines2 = [x.strip() for x in lines[startline:endline]]
                    for k in range(len(head_lines2)):
                        append_line(report_lines, k, head_lines2[k])
                # 7天
                head_lines3 = [x.strip() for x in lines[20:22]]
                for d in extra_retention_day:
                    append_line(report_lines, 0, head_lines3[0].format(d))
                    append_line(report_lines, 1, head_lines3[1].format(d))
                file.close()
            for single_date in self.extra_date:
                self.generate_retention_push_report_at_date(
                    report_lines, single_date)
            for single_date in Date(self.start_date).rangeto(self.end_date, True):
                self.generate_retention_push_report_at_date(
                    report_lines, single_date)
            reportstring = '\n'.join(report_lines)
            out.write(reportstring)
            out.close()
        return [self.output_filepath]

    def generate_retention_push_report_at_date(self, report_lines, date):
        print("generate_retention_push_report_at_date ", date)
        with open(self.etc_filepath) as file:
            firstopen_usercount = self.get_firstopen_count(date)
            if firstopen_usercount == 0:
                return

            lines = file.readlines()
            line_string = ""
            line_string += "{0},".format(Date(date).formatmd())
            line_string += "{0},".format(firstopen_usercount)
            all_retention_day = []
            all_retention_day.extend(retention_day)
            all_retention_day.extend(extra_retention_day)

            for k in all_retention_day:
                # 留存率查询
                day = k - 1
                single_date = Date(date).adddays(day)
                if Date(single_date).between(self.end_date) > 0:
                    current_retention_usercount = self.get_retention_count(
                        date, single_date)
                    # 留存分布查询
                    retention_day_results = self.get_result(
                        "留存用户关卡推进.sql", date, single_date)

                    # 留存率
                    if day > 0:
                        line_string += "{0:.2f}%,".format(
                            100*float(current_retention_usercount)/float(firstopen_usercount))

                    retention_base_datas = []
                    for row in retention_day_results:
                        retention_base_data = [row.max_stage, row.user_count, 100*float(
                            row.user_count)/float(firstopen_usercount)]
                        retention_base_datas.append(retention_base_data)
                    first_retention_usercount = current_retention_usercount - \
                        sum(t[1] for t in retention_base_datas)
                    first_stage_found = False
                    for item in retention_base_datas:
                        if item[0] == 0:
                            first_stage_found = True
                            item[1] = item[1] + first_retention_usercount
                            item[2] = 100*float(item[2]) / \
                                float(firstopen_usercount)
                            break
                    if not first_stage_found:
                        retention_base_datas.insert(0, [0, first_retention_usercount, 100*float(
                            first_retention_usercount)/float(firstopen_usercount)])

                    line_index = min(day, 6)
                    startline = 4 + 3 * line_index
                    endline = 5 + 3 * line_index
                    head_line = [x.strip()
                                 for x in lines[startline:endline]][0]

                    head_lines = head_line.split(',')
                    for head in head_lines:
                        headsegments = head.split('|')
                        min_level = int(headsegments[0])
                        max_level = sys.maxsize if len(
                            headsegments) == 1 else int(headsegments[1])
                        level_user_percent = 0
                        for k in range(len(retention_base_datas)):
                            data = retention_base_datas[k]
                            if data[0] >= min_level and data[0] <= max_level:
                                level_user_percent += data[2]
                        line_string += "{0:.2f}%,".format(level_user_percent)
            # 数据拼接
            append_line(report_lines, len(report_lines), line_string)
            file.close()
        return report_lines
