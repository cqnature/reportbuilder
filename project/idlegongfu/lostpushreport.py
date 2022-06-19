#!/usr/bin/env python
# coding=utf-8

import os
import json
import sys
from project.base.date import *
from project.base.helper import *
from project.base.query import *
from project.base.report import *

lost_day = [2, 3, 4, 5, 6]
extra_lost_day = [7]


def generate_lost_push_report(query_config, date):
    return Report(query_config, date).generate()


class Report(BaseReport):
    def __init__(self, query_config, date):
        super(Report, self).__init__(query_config, date)
        self.etc_filename = '流失玩家推进占比.csv'
        country_string = self.query_config.geo_country
        platform_string = self.query_config.platform
        self.output_filename = "{0}-{1}-LostUser-Stage-{2}.csv".format(
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
                # 2-6天
                for d in lost_day:
                    startline = 2 + 3 * (d - 2)
                    endline = 4 + 3 * (d - 2)
                    head_lines2 = [x.strip() for x in lines[startline:endline]]
                    for k in range(len(head_lines2)):
                        append_line(report_lines, k, head_lines2[k])
                # 7天
                head_lines3 = [x.strip() for x in lines[17:19]]
                for d in extra_lost_day:
                    append_line(report_lines, 0, head_lines3[0].format(d))
                    append_line(report_lines, 1, head_lines3[1].format(d))
                file.close()
            for single_date in self.extra_date:
                self.generate_lost_push_report_at_date(
                    report_lines, single_date)
            for single_date in Date(self.start_date).rangeto(self.end_date, True):
                self.generate_lost_push_report_at_date(
                    report_lines, single_date)
            reportstring = '\n'.join(report_lines)
            out.write(reportstring)
            out.close()
        return [self.output_filepath]

    def generate_lost_push_report_at_date(self, report_lines, date):
        print("generate_lost_push_report_at_date ", date)
        with open(self.etc_filepath) as file:
            firstopen_usercount = self.get_firstopen_count(date)
            if firstopen_usercount == 0:
                return

            lines = file.readlines()
            line_string = ""
            line_string += "{0},".format(Date(date).formatmd())
            line_string += "{0},".format(firstopen_usercount)
            all_lost_day = []
            all_lost_day.extend(lost_day)
            all_lost_day.extend(extra_lost_day)

            for k in all_lost_day:
                # 留存率查询
                day = k - 1
                single_date = Date(date).adddays(day)
                if Date(single_date).between(self.end_date) > 0:
                    current_lost_usercount = self.get_lost_count(
                        date, single_date)

                    # 留存率
                    line_string += "{0:.2f}%,".format(100*float(
                        firstopen_usercount - current_lost_usercount)/float(firstopen_usercount))

                    # 流失分布查询
                    lost_day_results = self.get_result(
                        "流失用户关卡推进.sql", date, single_date)

                    lost_base_datas = []
                    for row in lost_day_results:
                        lost_base_data = [row.max_stage, row.user_count,
                                          100*float(row.user_count)/float(firstopen_usercount)]
                        lost_base_datas.append(lost_base_data)
                    first_lost_usercount = current_lost_usercount - \
                        sum(t[1] for t in lost_base_datas)
                    first_stage_found = False
                    for item in lost_base_datas:
                        if item[0] == 0:
                            first_stage_found = True
                            item[1] = item[1] + first_lost_usercount
                            item[2] = 100*float(item[2]) / \
                                float(firstopen_usercount)
                            break
                    if not first_stage_found:
                        lost_base_datas.insert(
                            0, [0, first_lost_usercount, 100*float(first_lost_usercount)/float(firstopen_usercount)])

                    line_index = min(day, 6)
                    startline = 1 + 3 * line_index
                    endline = 2 + 3 * line_index
                    head_line = [x.strip()
                                 for x in lines[startline:endline]][0]
                    head_lines = head_line.split(',')
                    for head in head_lines:
                        headsegments = head.split('|')
                        min_level = int(headsegments[0])
                        max_level = sys.maxsize if len(
                            headsegments) == 1 else int(headsegments[1])
                        level_user_percent = 0
                        for k in range(len(lost_base_datas)):
                            data = lost_base_datas[k]
                            if data[0] >= min_level and data[0] <= max_level:
                                level_user_percent += data[2]
                        line_string += "{0:.2f}%,".format(level_user_percent)

            # 数据拼接
            append_line(report_lines, len(report_lines), line_string)
            file.close()
