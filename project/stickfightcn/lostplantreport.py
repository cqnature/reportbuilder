#!/usr/bin/env python
# coding=utf-8

import os
import json
from project.base.date import *
from project.base.helper import *
from project.base.query import *
from project.base.report import *

extra_retation_date = [18, 21, 24, 27, 30]
max_lately_date = 15
max_chapter_id = 15
lost_day = 1


def generate_lostplant_report(query_config, date):
    return Report(query_config, date).generate()


class Report(BaseReport):
    def __init__(self, query_config, date):
        super(Report, self).__init__(query_config, date)
        self.etc_filename = 'plant_progress_of_lost_users.csv'
        country_string = self.query_config.geo_country
        platform_string = self.query_config.platform
        self.output_filename = "{0}-{1}-LostUser-Chapter-{2}.csv".format(
            country_string, platform_string, self.end_date)

    def do_generate(self):
        print('do generate report')
        with open(self.output_filepath, mode='w+') as out:
            report_lines = []
            with open(self.etc_filepath) as file:
                lines = file.readlines()
                head_lines1 = [x.strip() for x in lines[0:2]]
                for k in range(len(head_lines1)):
                    append_line(report_lines, k, head_lines1[k])
                head_lines2 = [x.strip() for x in lines[2:4]]
                for k in range(len(head_lines2)):
                    append_line(report_lines, k, head_lines2[k])
                head_lines3 = [x.strip() for x in lines[4:6]]
                for k in range(len(head_lines3)):
                    append_line(report_lines, k, head_lines3[k])
                # head_lines4 = [x.strip() for x in lines[6:8]]
                # for d in range(13):
                #     for k in range(len(head_lines4)):
                #         append_line(report_lines, k, head_lines4[k].format(d + 3))
                # for d in extra_retation_date:
                #     for k in range(len(head_lines4)):
                #         append_line(report_lines, k, head_lines4[k].format(d))
                file.close()
            for single_date in self.extra_date:
                self.generate_lostplant_report_at_date(
                    report_lines, single_date)
            lately_date = max(Date(self.end_date).adddays(
                1 - max_lately_date), self.start_date)
            for single_date in Date(lately_date).rangeto(self.end_date, True):
                self.generate_lostplant_report_at_date(
                    report_lines, single_date)
            reportstring = '\n'.join(report_lines)
            out.write(reportstring)
            out.close()
        return [self.output_filepath]

    def get_plane_chapter_id(self):
        return max_chapter_id

    def generate_lostplant_report_at_date(self, report_lines, date):
        print("generate_lostplant_report_at_date ", date)
        chapter_id = self.get_plane_chapter_id()
        with open(self.etc_filepath) as file:
            firstopen_usercount = self.get_firstopen_count(date)
            if firstopen_usercount == 0:
                return

            line_string = ""
            line_string += "{0},".format(Date(date).formatmd())
            signup_day_progress_results = self.get_result(
                "plant_progress_of_signup_users.sql", date)
            total_level_user_count = 0
            signup_base_datas = []
            progress_data_map = {}
            for k in range(0, chapter_id):
                signup_base_data = [k + 1, 0, 0]
                signup_base_datas.append(signup_base_data)
                progress_data_map[k + 1] = signup_base_data
            for row in signup_day_progress_results:
                progress_data = progress_data_map[row.chapter_id]
                progress_data[1] = row.user_count
                progress_data[2] = 100 * \
                    float(row.user_count)/float(firstopen_usercount)
                total_level_user_count += row.user_count
            first_progress_data = progress_data_map[1]
            first_progress_data[1] = first_progress_data[1] + \
                firstopen_usercount - total_level_user_count
            first_progress_data[2] = 100 * \
                float(first_progress_data[1])/float(firstopen_usercount)
            line_string += "{0},".format(firstopen_usercount)
            for k in range(len(signup_base_datas)):
                data = signup_base_datas[k]
                line_string += "{0:.2f}%,".format(data[2])

            currentDayIndex = 1
            lost_base_datas = []
            lost_base_usercount = 0
            for single_date in Date(date).rangeto(Date(date).adddays(lost_day)):
                date_string = ""
                if Date(single_date).between(self.end_date) <= 0:
                    date_string += ",,,,,"
                else:
                    # 留存率查询
                    current_lost_usercount = self.get_lost_count(
                        date, single_date)
                    # 流失分布查询
                    lost_day_results = self.get_result(
                        "plant_progress_of_lost_users.sql", date, single_date)
                    if currentDayIndex == 1:
                        progress_data_map = {}
                        for k in range(0, chapter_id):
                            lost_base_data = [k + 1, 0, 0]
                            lost_base_datas.append(lost_base_data)
                            progress_data_map[k + 1] = lost_base_data
                        for row in lost_day_results:
                            progress_data = progress_data_map[row.chapter_id]
                            progress_data[1] = row.user_count
                            progress_data[2] = 100 * \
                                float(row.user_count) / \
                                float(firstopen_usercount)
                        first_progress_data = progress_data_map[1]
                        first_progress_data[1] = first_progress_data[1] + \
                            current_lost_usercount - \
                            sum(t[1] for t in lost_base_datas)
                        first_progress_data[2] = 100 * \
                            float(first_progress_data[1]) / \
                            float(firstopen_usercount)
                        lost_base_usercount = current_lost_usercount
                        date_string += "{0:.2f}%,".format(100*float(
                            firstopen_usercount - current_lost_usercount)/float(firstopen_usercount))
                        for k in range(len(lost_base_datas)):
                            data = lost_base_datas[k]
                            date_string += "{0:.2f}%,".format(data[2])
                    else:
                        current_lost_datas = []
                        progress_data_map = {}
                        for k in range(0, chapter_id):
                            current_lost_data = [k + 1, 0, 0]
                            current_lost_datas.append(current_lost_data)
                            progress_data_map[k + 1] = current_lost_data
                        for row in lost_day_results:
                            progress_data = progress_data_map[row.chapter_id]
                            progress_data[1] = row.user_count
                            progress_data[2] = 100 * \
                                float(row.user_count) / \
                                float(firstopen_usercount)
                        first_progress_data = progress_data_map[1]
                        first_progress_data[1] = first_progress_data[1] + \
                            current_lost_usercount - \
                            sum(t[1] for t in current_lost_datas)
                        first_progress_data[2] = 100 * \
                            float(first_progress_data[1]) / \
                            float(firstopen_usercount)
                        lost_base_usercount = current_lost_usercount
                        date_string += "{0:.2f}%,".format(100*float(
                            firstopen_usercount - current_lost_usercount)/float(firstopen_usercount))
                        for k in range(len(current_lost_datas)):
                            data = current_lost_datas[k]
                            base_data = lost_base_datas[k]
                            date_string += "{0:.2f}%,".format(
                                data[2] - base_data[2])
                        lost_base_datas = current_lost_datas

                diffDay = Date(date).between(single_date)
                if diffDay <= 15 or diffDay in extra_retation_date:
                    line_string += date_string
                # 增加天数索引
                currentDayIndex += 1
            # 数据拼接
            append_line(report_lines, len(report_lines), line_string)
            file.close()
