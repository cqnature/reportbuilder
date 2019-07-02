#!/usr/bin/env python
# coding=utf-8

import os
import json
from ..base.date import *
from ..base.helper import *
from ..base.query import *
from ..base.report import *

def generate_day_stage_report(query_config, date):
    return Report(query_config, date).generate()

class Report(BaseReport):
    def __init__(self, query_config, date):
        super(Report, self).__init__(query_config, date)
        self.etc_filename = 'day_stage_progress_of_users.csv'
        self.output_filename = 'day_lost_level_report.csv'

    def do_generate(self):
        print 'do generate report'
        with open(self.output_filepath, mode='w+') as out:
            report_lines = []
            for single_date in Date(self.start_date).rangeto(self.end_date, True):
                self.generate_day_stage_report_at_date(report_lines, single_date)
            reportstring = '\n'.join(report_lines)
            out.write(reportstring)
            out.close()
        return [self.output_filepath]

    def generate_day_stage_report_at_date(self, report_lines, date):
        print("generate_stage_report_at_date ", date)
        max_rebirth = 2
        max_level = 200
        with open(self.etc_filepath) as file:
            firstopen_usercount = self.get_firstopen_count(date)
            if firstopen_usercount == 0:
                return;

            lineIndex = 0
            lines = file.readlines()
            signup_day_progress_lines = [x.strip() for x in lines[0:4]]
            signup_day_progress_results = self.get_result("stage_progress_of_signup_users.sql", date)
            signup_day_progress_lines[1] = signup_day_progress_lines[1].format(Date(date).formatmd())
            signup_day_progress_lines[3] = signup_day_progress_lines[3].format(firstopen_usercount, 100)
            signup_base_datas = []
            stage_config_maps = {}
            for k in range(0, max_rebirth + 1):
                for n in range(1, max_level + 1):
                    signup_base_data = [k, n, 0, 0]
                    signup_base_datas.append(signup_base_data)
                    if not stage_config_maps.has_key(k):
                        stage_config_maps[k] = {}
                    stage_config_maps[k][n] = signup_base_data
            for row in signup_day_progress_results:
                if row.rebirth > max_rebirth or row.level > max_level:
                    break
                signup_base_data = stage_config_maps[row.rebirth][row.level]
                signup_base_data[2] = row.user_count
                signup_base_data[3] = 100*float(row.user_count)/float(firstopen_usercount)
            tmp_base_datas = []
            for row in signup_day_progress_results:
                tmp_base_data = [row.rebirth, row.level, row.user_count, 100*float(row.user_count)/float(firstopen_usercount)]
                tmp_base_datas.append(tmp_base_data)
            first_level_usercount = firstopen_usercount - sum(t[2] for t in tmp_base_datas)
            stage_config_maps[0][1][2] = first_level_usercount
            stage_config_maps[0][1][3] = 100*float(first_level_usercount)/float(firstopen_usercount)
            for k in range(len(signup_base_datas)):
                data = signup_base_datas[k]
                signup_day_progress_lines.append("{0}-{1},{2},{3:.2f}%,".format(data[0], data[1], data[2], data[3]))
            for k in range(len(signup_day_progress_lines)):
                append_line(report_lines, lineIndex + k, signup_day_progress_lines[k], k != 0)
            lineIndex += len(signup_day_progress_lines)

            currentDayIndex = 1
            lost_base_datas = []
            lost_base_usercount = 0
            lost_day_progress_lines = []
            for single_date in Date(date).rangeto(self.get_retention_date(date)):
                # 留存率查询
                current_lost_usercount = self.get_lost_count(date, single_date)
                # 流失分布查询
                lost_day_results = self.get_result("stage_progress_of_lost_users.sql", date, single_date)
                if currentDayIndex == 1:
                    lost_day_progress_lines.extend([x.strip() for x in lines[4:10]])
                    stage_config_maps = {}
                    for k in range(0, max_rebirth + 1):
                        for n in range(1, max_level + 1):
                            lost_base_data = [k, n, 0, 0]
                            lost_base_datas.append(lost_base_data)
                            if not stage_config_maps.has_key(k):
                                stage_config_maps[k] = {}
                            stage_config_maps[k][n] = lost_base_data
                    for row in lost_day_results:
                        if row.rebirth > max_rebirth or row.level > max_level:
                            break
                        lost_base_data = stage_config_maps[row.rebirth][row.level]
                        lost_base_data[2] = row.user_count
                        lost_base_data[3] = 100*float(row.user_count)/float(firstopen_usercount)
                    tmp_base_datas = []
                    for row in lost_day_results:
                        tmp_base_data = [row.rebirth, row.level, row.user_count, 100*float(row.user_count)/float(firstopen_usercount)]
                        tmp_base_datas.append(tmp_base_data)
                    first_lost_usercount = current_lost_usercount - sum(t[2] for t in tmp_base_datas)
                    stage_config_maps[0][1][2] = first_lost_usercount
                    stage_config_maps[0][1][3] = 100*float(first_lost_usercount)/float(firstopen_usercount)

                    lost_base_usercount = current_lost_usercount
                    lost_day_progress_lines[1] = lost_day_progress_lines[1].format(Date(date).formatmd())
                    lost_day_progress_lines[3] = lost_day_progress_lines[3].format(firstopen_usercount, 100)
                    lost_day_progress_lines[4] = lost_day_progress_lines[4].format(firstopen_usercount - current_lost_usercount, 100*float(firstopen_usercount - current_lost_usercount)/float(firstopen_usercount))
                    lost_day_progress_lines[5] = lost_day_progress_lines[5].format(lost_base_usercount, 100* float(lost_base_usercount)/float(firstopen_usercount))
                    for k in range(len(lost_base_datas)):
                        data = lost_base_datas[k]
                        lost_day_progress_lines.append("{0}-{1},{2},{3:.2f}%,".format(data[0], data[1], data[2], data[3]))
                else:
                    current_lost_datas = []
                    lost_day_progress_lines.extend([x.strip() for x in lines[10:]])
                    stage_config_maps = {}
                    for k in range(0, max_rebirth + 1):
                        for n in range(1, max_level + 1):
                            current_lost_data = [k, n, 0, 0]
                            current_lost_datas.append(current_lost_data)
                            if not stage_config_maps.has_key(k):
                                stage_config_maps[k] = {}
                            stage_config_maps[k][n] = current_lost_data
                    for row in lost_day_results:
                        if row.rebirth > max_rebirth or row.level > max_level:
                            break
                        current_lost_data = stage_config_maps[row.rebirth][row.level]
                        current_lost_data[2] = row.user_count
                        current_lost_data[3] = 100*float(row.user_count)/float(firstopen_usercount)
                    tmp_base_datas = []
                    for row in lost_day_results:
                        tmp_base_data = [row.rebirth, row.level, row.user_count, 100*float(row.user_count)/float(firstopen_usercount)]
                        tmp_base_datas.append(tmp_base_data)
                    first_lost_usercount = current_lost_usercount - sum(t[2] for t in tmp_base_datas)
                    stage_config_maps[0][1][2] = first_lost_usercount
                    stage_config_maps[0][1][3] = 100*float(first_lost_usercount)/float(firstopen_usercount)

                    origin_lost_base_usercount = lost_base_usercount
                    lost_base_usercount = current_lost_usercount
                    relative_lost_usercount = current_lost_usercount - origin_lost_base_usercount
                    lost_day_progress_lines[0] = lost_day_progress_lines[0].format(Date(date).between(single_date))
                    lost_day_progress_lines[1] = lost_day_progress_lines[1].format(Date(date).formatmd())
                    lost_day_progress_lines[3] = lost_day_progress_lines[3].format(firstopen_usercount, 100)
                    lost_day_progress_lines[4] = lost_day_progress_lines[4].format(Date(date).between(single_date), firstopen_usercount - current_lost_usercount, 100*float(firstopen_usercount - current_lost_usercount)/float(firstopen_usercount))
                    lost_day_progress_lines[5] = lost_day_progress_lines[5].format(relative_lost_usercount, 100*float(relative_lost_usercount)/float(firstopen_usercount))
                    for k in range(len(current_lost_datas)):
                        data = current_lost_datas[k]
                        base_data = lost_base_datas[k]
                        lost_day_progress_lines.append("{0}-{1},{2},{3:.2f}%,".format(data[0], data[1], data[2] - base_data[2], data[3] - base_data[3]))
                    lost_base_datas = current_lost_datas
                # 数据拼接
                for k in range(len(lost_day_progress_lines)):
                    append_line(report_lines, lineIndex + k, lost_day_progress_lines[k], k != 0)
                lineIndex += len(lost_day_progress_lines)
                # 增加天数索引
                currentDayIndex += 1
                # 清空缓存
                del lost_day_progress_lines[:]
            file.close()
