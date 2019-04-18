#!/usr/bin/env python
# coding=utf-8

import os
import json
from util import validate, daterange, formatdate, betweenday, append_line
from common import get_firstopen_usercount, get_lost_usercount
from query import querysql

def generate_retention_ads_report_at_date(report_lines, platform, date):
    print("generate_retention_ads_report_at_date ", date)
    with open("./etc/ads_view_of_retention_users.csv") as file:
        lines = file.readlines()
        ads_view_count_results = querysql("./sql/retention_ads_view_count.sql", platform, date)
        if len(ads_view_count_results) == 0:
            return
        ads_view_user_results = querysql("./sql/retention_ads_view_users.sql", platform, date)
        lines[0] = lines[0].format(formatdate(date))
        lines[1] = lines[1].format(ads_view_count_results[0].daily_user_count)
        for i in range(3, len(lines) - 1):
            line = lines[i]
            linesegments = line.split('|', 1)
            ads_scene = linesegments[0]
            formatstring = linesegments[1]
            ad_view_count = 0
            daily_average_ad_view_count = 0
            ad_view_user_count = 0
            daily_ad_view_user_percent = 0
            for k in range(len(ads_view_count_results)):
                ads_view_count_result = ads_view_count_results[k]
                if ads_view_count_result.af_ad_scene == ads_scene:
                    ad_view_count = ads_view_count_result.ad_view_count
                    daily_average_ad_view_count = ads_view_count_result.daily_average_ad_view_count
                    break
            for k in range(len(ads_view_user_results)):
                ads_view_user_result = ads_view_user_results[k]
                if ads_view_user_result.af_ad_scene == ads_scene:
                    ad_view_user_count = ads_view_user_result.ad_view_user_count
                    daily_ad_view_user_percent = ads_view_user_result.daily_ad_view_user_percent
                    break
            lines[i] = formatstring.format(ad_view_user_count, daily_ad_view_user_percent * 100, ad_view_count, daily_average_ad_view_count)
        lines[len(lines) - 1] = lines[len(lines) - 1].format(sum(t.daily_average_ad_view_count for t in ads_view_count_results))
        report_lines.extend(lines)
        file.close()

def generate_retention_ads_report(platform, start_date, end_date):
    if platform != "IOS" and platform != "ANDROID":
        print("You must pass platform in IOS or ANDROID")
        exit(1)
    try:
        validate(start_date)
        validate(end_date)
    except ValueError, Argument:
        print(Argument)
        exit(1)

    output = "output/retention_ads_report_{0}_from_{1}_to_{2}.csv".format(platform, start_date, end_date)
    with open(output, mode='w+') as out:
        report_lines = []
        for single_date in daterange(start_date, end_date, True):
            generate_retention_ads_report_at_date(report_lines, platform, single_date)
        reportstring = ''.join(report_lines)
        out.write(reportstring)
        out.close()
