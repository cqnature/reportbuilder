#!/usr/bin/env python
# coding=utf-8

import os
import json
from util import validate, daterange, formatdate, betweenday, append_line
from common import get_firstopen_usercount, get_retention_usercount
from query import querysql

def get_plane_max_level():
    max_level = 0
    with open("./etc/food.json") as file:
        file_config = json.load(file)
        max_level = file_config['config']['maxId']
        file.close()
    return max_level;

def generate_retentionplant_report_at_date(report_lines, platform, date, end_date):
    print("generate_retentionplant_report_at_date ", date)
    max_level = get_plane_max_level()
    with open("./etc/plant_progress_of_retention_users.csv") as file:
        firstopen_usercount = get_firstopen_usercount(platform, date)
        if firstopen_usercount == 0:
            return;

        lineIndex = 0
        lines = file.readlines()
        signup_day_progress_lines = [x.strip() for x in lines[0:4]]
        signup_day_progress_results = querysql("./sql/plant_progress_of_signup_users.sql", platform, date)
        total_level_user_count = 0
        signup_day_progress_lines[1] = signup_day_progress_lines[1].format(formatdate(date))
        signup_day_progress_lines[3] = signup_day_progress_lines[3].format(firstopen_usercount, 100)
        signup_base_datas = []
        progress_data_map = {}
        for k in range(1, max_level + 1):
            data = [k, 0, 0]
            signup_base_datas.append(data)
            progress_data_map[k] = data
        for row in signup_day_progress_results:
            progress_data = progress_data_map[row.max_level]
            progress_data[1] = row.user_count
            progress_data[2] = 100*float(row.user_count)/float(firstopen_usercount)
            total_level_user_count += row.user_count
        first_level_user_count = firstopen_usercount - total_level_user_count
        signup_base_datas[0][1] = first_level_user_count
        signup_base_datas[0][2] = 100*float(first_level_user_count)/float(firstopen_usercount)
        for k in range(len(signup_base_datas)):
            data = signup_base_datas[k]
            signup_day_progress_lines.append("{0},{1},{2:.2f}%,".format(data[0], data[1], data[2]))
        for k in range(len(signup_day_progress_lines)):
            append_line(report_lines, lineIndex + k, signup_day_progress_lines[k], k != 0)
        lineIndex += len(signup_day_progress_lines)

        currentDayIndex = 1
        retention_day_progress_lines = []
        for single_date in daterange(date, end_date):
            # 留存率查询
            current_retention_usercount = get_retention_usercount(platform, date, single_date)
            # 留存分布查询
            retention_day_results = querysql("./sql/plant_progress_of_retention_users.sql", platform, date, single_date)
            if currentDayIndex == 1:
                retention_day_progress_lines.extend([x.strip() for x in lines[4:9]])
            else:
                retention_day_progress_lines.extend([x.strip() for x in lines[9:]])
                retention_day_progress_lines[0] = retention_day_progress_lines[0].format(betweenday(date, single_date))
            current_retention_datas = []
            progress_data_map = {}
            for k in range(1, max_level + 1):
                data = [k, 0, 0]
                current_retention_datas.append(data)
                progress_data_map[k] = data
            for row in retention_day_results:
                progress_data = progress_data_map[row.max_level]
                progress_data[1] = row.user_count
                progress_data[2] = 100*float(row.user_count)/float(firstopen_usercount)
            retention_day_progress_lines[1] = retention_day_progress_lines[1].format(formatdate(date))
            retention_day_progress_lines[3] = retention_day_progress_lines[3].format(firstopen_usercount, 100)
            if currentDayIndex == 1:
                retention_day_progress_lines[4] = retention_day_progress_lines[4].format(current_retention_usercount, 100*float(current_retention_usercount)/float(firstopen_usercount))
            else:
                retention_day_progress_lines[4] = retention_day_progress_lines[4].format(betweenday(date, single_date), current_retention_usercount, 100*float(current_retention_usercount)/float(firstopen_usercount))
            current_retention_datas[0][1] = current_retention_usercount - sum(t[1] for t in current_retention_datas)
            current_retention_datas[0][2] = 100*float(current_retention_datas[0][1])/float(firstopen_usercount)
            for k in range(len(current_retention_datas)):
                data = current_retention_datas[k]
                retention_day_progress_lines.append("{0},{1},{2:.2f}%,".format(data[0], data[1], data[2]))

            # 数据拼接
            for k in range(len(retention_day_progress_lines)):
                append_line(report_lines, lineIndex + k, retention_day_progress_lines[k], k != 0)
            lineIndex += len(retention_day_progress_lines)
            # 增加天数索引
            currentDayIndex += 1
            # 清空缓存
            del retention_day_progress_lines[:]
        file.close()

def generate_retentionplant_report(platform, start_date, end_date):
    if platform != "IOS" and platform != "ANDROID":
        print("You must pass platform in IOS or ANDROID")
        exit(1)
    try:
        validate(start_date)
        validate(end_date)
    except ValueError, Argument:
        print(Argument)
        exit(1)

    output = "output/retentionuser_plant_report_{0}_from_{1}_to_{2}.csv".format(platform, start_date, end_date)
    with open(output, mode='w+') as out:
        report_lines = []
        for single_date in daterange(start_date, end_date, True):
            generate_retentionplant_report_at_date(report_lines, platform, single_date, end_date)
        reportstring = '\n'.join(report_lines)
        out.write(reportstring)
        out.close()
