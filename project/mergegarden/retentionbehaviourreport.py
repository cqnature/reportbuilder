#!/usr/bin/env python
# coding=utf-8

import os
import json
from util import validate, date_add, daterange, formatdate, betweenday, append_line
from common import get_firstopen_usercount, get_retention_usercount
from query import querysql

# 次留=1 三留=2 四留=3
add_day = 1

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
            append_line(lines, start_index + k, "{0},{1},{2:.2f}%,".format(key, value, 100*float(value)/float(first_open_usercount)))

def generate_retentionbehaviour_report_at_date(report_lines, platform, date, level):
    print("generate_retentionbehaviour_report_at_date ", date)
    with open("./etc/behaviour_of_retention_users.csv") as file:
        # 新增用户数
        firstopen_usercount = get_firstopen_usercount(platform, date)
        if firstopen_usercount == 0:
            return;
        lines = file.readlines()
        lines[0] = lines[0].strip().format(formatdate(date))
        lines[1] = lines[1].strip().format(firstopen_usercount)
        # 次日留存用户数
        retention_usercount = get_retention_usercount(platform, date, date_add(date, add_day))
        lines[2] = lines[2].strip().format(retention_usercount, 100*float(retention_usercount)/float(firstopen_usercount))
        behaviour_results = querysql("./sql/behaviour_of_retention_users.sql", platform, date, date_add(date, add_day), level)
        level_retention_usercount = sum(1 for _ in behaviour_results)
        lines[3] = lines[3].strip().format(level, level_retention_usercount, 100*float(level_retention_usercount)/float(firstopen_usercount))
        lines[4] = lines[4].strip().format(level)
        dataset_map = []
        key_count = 16
        key_offset = 2
        for k in range(key_count):
            dataset_map.append({})
        for k in range(len(behaviour_results)):
            behaviour_result = behaviour_results[k]
            for t in range(key_count):
                add_map_key_count(dataset_map[t], behaviour_result[t + key_offset])
        max_count = max(len(map) for map in dataset_map)
        start_index = len(lines)
        for k in range(key_count):
            print_map(lines, dataset_map[k], start_index, max_count, firstopen_usercount)
        report_lines.extend(lines)
        file.close()

def generate_retentionbehaviour_report(platform, start_date, end_date):
    if platform != "IOS" and platform != "ANDROID":
        print("You must pass platform in IOS or ANDROID")
        exit(1)
    try:
        validate(start_date)
        validate(end_date)
    except ValueError, Argument:
        print(Argument)
        exit(1)

    for level in range(7, 9):
        output = "output/retentionuser_behaviour_report_{0}_from_{1}_to_{2}_level_{3}.csv".format(platform, start_date, end_date, level)
        with open(output, mode='w+') as out:
            report_lines = []
            for single_date in daterange(start_date, end_date, True):
                if single_date == end_date:
                    continue
                generate_retentionbehaviour_report_at_date(report_lines, platform, single_date, level)
            reportstring = '\n'.join(report_lines)
            out.write(reportstring)
            out.close()
