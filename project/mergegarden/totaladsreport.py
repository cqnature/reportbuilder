#!/usr/bin/env python
# coding=utf-8

import os
import json
from util import validate, daterange, formatdate, betweenday, append_line
from common import get_firstopen_usercount, get_retention_usercount
from query import querysql

def generate_total_ads_report_at_date(report_lines, platform, date, start_date, end_date):
    print("generate_total_ads_report_at_date ", date)
    if date == start_date:
        with open("./etc/total_ads_view_of_users.csv") as file:
            lines = file.readlines()
            for k in range(2):
                append_line(report_lines, k, lines[k].strip())
            for single_date in daterange(date, end_date, True):
                append_line(report_lines, 0, lines[2].strip().format(betweenday(date, single_date) - 1))
                append_line(report_lines, 1, lines[3].strip())
            file.close()

    index = len(report_lines)
    append_line(report_lines, index, "{0},".format(formatdate(date)))
    for single_date in daterange(date, end_date, True):
        ads_view_count_results = querysql("./sql/ads_view_of_retention_users.sql", platform, date, single_date)
        user_count = 0
        if date == single_date:
            user_count = get_firstopen_usercount(platform, single_date)
        else:
            user_count = get_retention_usercount(platform, date, single_date)
        view_count = sum(1 for _ in ads_view_count_results)
        average_view_count = 0 if user_count == 0 else float(view_count)/float(user_count)
        append_line(report_lines, index, "{0},{1},{2:.2f},".format(user_count, view_count, average_view_count))

def generate_total_ads_report(platform, start_date, end_date):
    if platform != "IOS" and platform != "ANDROID":
        print("You must pass platform in IOS or ANDROID")
        exit(1)
    try:
        validate(start_date)
        validate(end_date)
    except ValueError, Argument:
        print(Argument)
        exit(1)

    output = "output/total_ads_report_{0}_from_{1}_to_{2}.csv".format(platform, start_date, end_date)
    with open(output, mode='w+') as out:
        report_lines = []
        for single_date in daterange(start_date, end_date, True):
            generate_total_ads_report_at_date(report_lines, platform, single_date, start_date, end_date)
        reportstring = '\n'.join(report_lines)
        out.write(reportstring)
        out.close()
