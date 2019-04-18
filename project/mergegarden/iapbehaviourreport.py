#!/usr/bin/env python
# coding=utf-8

import os
import json
from util import validate, daterange, formatdate, betweenday, append_line
from common import get_firstopen_usercount, get_lost_usercount
from query import querysql

def event_timestamp(e):
  return e.event_timestamp

def generate_iap_behaviour_report_at_date(report_lines, platform, date, end_date):
    print("generate_iap_behaviour_report_at_date ", date)
    with open("./etc/behaviour_of_spend_gems.csv") as file:
        lines = file.readlines()
        iap_purchase_results = querysql("./sql/in_app_purchase_users.sql", platform, date, end_date)
        if len(iap_purchase_results) == 0:
            return
        spend_gems_results = querysql("./sql/spend_virtual_currency_detail.sql", platform, date, end_date)
        iap_purchase_lines = [x.strip() for x in lines[0:1]]
        iap_purchase_lines[0] = iap_purchase_lines[0].format(formatdate(date))
        spend_gems_map = {}
        for i in range(3, len(lines) - 1):
            line = lines[i].strip()
            linesegments = line.split('|', 1)
            spend_scene = linesegments[0]
            formatstring = linesegments[1]
            spend_gems_map[spend_scene] = formatstring
        iap_purchase_users = {}
        for k in range(len(iap_purchase_results)):
            iap_purchase_result = iap_purchase_results[k]
            if not iap_purchase_users.has_key(iap_purchase_result.user_pseudo_id):
                iap_purchase_users[iap_purchase_result.user_pseudo_id] = 1
        iap_purchase_datas = {}
        max_result_count = 0
        for key,value in iap_purchase_users.iteritems():
            spend_gems_datas = [x for x in iap_purchase_results if x.user_pseudo_id == key]
            spend_gems_datas.extend([x for x in spend_gems_results if x.user_pseudo_id == key])
            spend_gems_datas.sort(key=event_timestamp)
            iap_purchase_datas[key] = spend_gems_datas
            max_result_count = max(max_result_count, len(spend_gems_datas))
        for key,spend_gems_datas in iap_purchase_datas.iteritems():
            append_line(iap_purchase_lines, 1, lines[1].strip().format(key))
            append_line(iap_purchase_lines, 2, lines[2].strip())
            for k in range(0, max_result_count):
                if k >= len(spend_gems_datas):
                    append_line(lines, 3 + k, ",,,")
                else:
                    spend_gems_data = spend_gems_datas[k]
                    try:
                        append_line(iap_purchase_lines, 3 + k, spend_gems_map[spend_gems_data.item_name].format(spend_gems_data.event_timestamp, -spend_gems_data.value))
                    except AttributeError:
                        append_line(iap_purchase_lines, 3 + k, spend_gems_map[spend_gems_data.item_name].format(spend_gems_data.event_timestamp))
        report_lines.extend(iap_purchase_lines)
        file.close()

def generate_iap_behaviour_report(platform, start_date, end_date):
    if platform != "IOS" and platform != "ANDROID":
        print("You must pass platform in IOS or ANDROID")
        exit(1)
    try:
        validate(start_date)
        validate(end_date)
    except ValueError, Argument:
        print(Argument)
        exit(1)

    output = "output/iap_behaviour_report_{0}_from_{1}_to_{2}.csv".format(platform, start_date, end_date)
    with open(output, mode='w+') as out:
        report_lines = []
        for single_date in daterange(start_date, end_date, True):
            generate_iap_behaviour_report_at_date(report_lines, platform, single_date, end_date)
        reportstring = '\n'.join(report_lines)
        out.write(reportstring)
        out.close()
