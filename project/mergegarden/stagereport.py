#!/usr/bin/env python
# coding=utf-8

import os
import json
from util import validate, daterange, formatdate, betweenday, append_line
from common import get_firstopen_usercount, get_lost_usercount
from query import querysql

def get_stage_configs():
    stage_configs = None
    with open("./etc/stage.json") as file:
        file_config = json.load(file)
        stage_configs = file_config['property']
        file.close()
    return stage_configs

def generate_stage_report_at_date(report_lines, platform, date, end_date):
    print("generate_stage_report_at_date ", date)
    max_stage = 40
    with open("./etc/stage_progress_of_users.csv") as file:
        firstopen_usercount = get_firstopen_usercount(platform, date)
        if firstopen_usercount == 0:
            return;

        lineIndex = 0
        lines = file.readlines()
        signup_day_progress_lines = [x.strip() for x in lines[0:4]]
        signup_day_progress_results = querysql("./sql/stage_progress_of_signup_users.sql", platform, date)
        signup_day_progress_lines[1] = signup_day_progress_lines[1].format(formatdate(date))
        signup_day_progress_lines[3] = signup_day_progress_lines[3].format(firstopen_usercount, 100)
        signup_base_datas = []
        stage_config_maps = {}
        for k in range(1, max_stage + 1):
            signup_base_data = [k, 0, 0]
            signup_base_datas.append(signup_base_data)
            stage_config_maps[k] = signup_base_data
        for row in signup_day_progress_results:
            if row.max_stage > 40:
                break
            signup_base_data = stage_config_maps[row.max_stage]
            signup_base_data[1] = row.user_count
            signup_base_data[2] = 100*float(row.user_count)/float(firstopen_usercount)
        for k in range(len(signup_base_datas)):
            data = signup_base_datas[k]
            signup_day_progress_lines.append("{0},{1},{2:.2f}%,".format(data[0], data[1], data[2]))
        for k in range(len(signup_day_progress_lines)):
            append_line(report_lines, lineIndex + k, signup_day_progress_lines[k], k != 0)
        lineIndex += len(signup_day_progress_lines)

        currentDayIndex = 1
        lost_base_datas = []
        lost_base_usercount = 0
        lost_day_progress_lines = []
        for single_date in daterange(date, end_date):
            # 留存率查询
            current_lost_usercount = get_lost_usercount(platform, date, single_date)
            # 流失分布查询
            lost_day_results = querysql("./sql/stage_progress_of_lost_users.sql", platform, date, single_date)
            if currentDayIndex == 1:
                lost_day_progress_lines.extend([x.strip() for x in lines[4:10]])
                stage_config_maps = {}
                for k in range(1, max_stage + 1):
                    lost_base_data = [k, 0, 0]
                    lost_base_datas.append(lost_base_data)
                    stage_config_maps[k] = lost_base_data
                for row in lost_day_results:
                    if row.max_stage > 40:
                        break
                    lost_base_data = stage_config_maps[row.max_stage]
                    lost_base_data[1] = row.user_count
                    lost_base_data[2] = 100*float(row.user_count)/float(firstopen_usercount)
                lost_base_usercount = current_lost_usercount
                lost_day_progress_lines[1] = lost_day_progress_lines[1].format(formatdate(date))
                lost_day_progress_lines[3] = lost_day_progress_lines[3].format(firstopen_usercount, 100)
                lost_day_progress_lines[4] = lost_day_progress_lines[4].format(firstopen_usercount - current_lost_usercount, 100*float(firstopen_usercount - current_lost_usercount)/float(firstopen_usercount))
                lost_day_progress_lines[5] = lost_day_progress_lines[5].format(lost_base_usercount, 100* float(lost_base_usercount)/float(firstopen_usercount))
                for k in range(len(lost_base_datas)):
                    data = lost_base_datas[k]
                    lost_day_progress_lines.append("{0},{1},{2:.2f}%,".format(data[0], data[1], data[2]))
            else:
                current_lost_datas = []
                lost_day_progress_lines.extend([x.strip() for x in lines[10:]])
                stage_config_maps = {}
                for k in range(1, max_stage + 1):
                    current_lost_data = [k, 0, 0]
                    current_lost_datas.append(current_lost_data)
                    stage_config_maps[k] = current_lost_data
                for row in lost_day_results:
                    if row.max_stage > 40:
                        break
                    current_lost_data = stage_config_maps[row.max_stage]
                    current_lost_data[1] = row.user_count
                    current_lost_data[2] = 100*float(row.user_count)/float(firstopen_usercount)
                origin_lost_base_usercount = lost_base_usercount
                lost_base_usercount = current_lost_usercount
                relative_lost_usercount = current_lost_usercount - origin_lost_base_usercount
                lost_day_progress_lines[0] = lost_day_progress_lines[0].format(betweenday(date, single_date))
                lost_day_progress_lines[1] = lost_day_progress_lines[1].format(formatdate(date))
                lost_day_progress_lines[3] = lost_day_progress_lines[3].format(firstopen_usercount, 100)
                lost_day_progress_lines[4] = lost_day_progress_lines[4].format(betweenday(date, single_date), firstopen_usercount - current_lost_usercount, 100*float(firstopen_usercount - current_lost_usercount)/float(firstopen_usercount))
                lost_day_progress_lines[5] = lost_day_progress_lines[5].format(relative_lost_usercount, 100*float(relative_lost_usercount)/float(firstopen_usercount))
                for k in range(len(current_lost_datas)):
                    data = current_lost_datas[k]
                    base_data = lost_base_datas[k]
                    lost_day_progress_lines.append("{0},{1},{2:.2f}%,".format(data[0], data[1] - base_data[1], data[2] - base_data[2]))
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

def generate_stage_report(platform, start_date, end_date):
    if platform != "IOS" and platform != "ANDROID":
        print("You must pass platform in IOS or ANDROID")
        exit(1)
    try:
        validate(start_date)
        validate(end_date)
    except ValueError, Argument:
        print(Argument)
        exit(1)

    output = "output/stage_report_{0}_from_{1}_to_{2}.csv".format(platform, start_date, end_date)
    with open(output, mode='w+') as out:
        report_lines = []
        for single_date in daterange(start_date, end_date, True):
            generate_stage_report_at_date(report_lines, platform, single_date, end_date)
        reportstring = '\n'.join(report_lines)
        out.write(reportstring)
        out.close()
