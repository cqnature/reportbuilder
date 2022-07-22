#!/usr/bin/env python
# coding=utf-8

import os
import json
import sys
from project.base.date import *
from project.base.helper import *
from project.base.query import *
from project.base.report import *

price_map = {'聖火令': 9.99, '150寶石': 1.99, '330寶石': 3.99,
             '900寶石': 9.99, '1950寶石': 19.99, '5250寶石': 49.99, '11250寶石': 99.99}


def generate_iap_behaviour_report(query_config, date):
    return Report(query_config, date).generate()


class Report(BaseReport):
    def __init__(self, query_config, date):
        super(Report, self).__init__(query_config, date)
        self.etc_filename = '付费用户行为.csv'
        country_string = self.query_config.geo_country
        platform_string = self.query_config.platform
        self.output_filename = "{0}-{1}-IAPUser-Behaviour-{2}.csv".format(
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
                # 7天
                head_lines2 = [x.strip() for x in lines[2:4]]
                for d in range(6):
                    append_line(report_lines, 0, head_lines2[0].format(d + 1))
                    append_line(report_lines, 1, head_lines2[1])
                file.close()
            for single_date in self.extra_date:
                self.generate_iap_behaviour_report_at_date(
                    report_lines, single_date)
            for single_date in Date(self.start_date).rangeto(self.end_date, True):
                self.generate_iap_behaviour_report_at_date(
                    report_lines, single_date)
            reportstring = '\n'.join(report_lines)
            out.write(reportstring)
            out.close()
        return [self.output_filepath]

    def generate_iap_behaviour_report_at_date(self, report_lines, date):
        print("generate_iap_behaviour_report_at_date ", date)
        with open(self.etc_filepath) as file:
            firstopen_usercount = self.get_firstopen_count(date)
            if firstopen_usercount == 0:
                return

            # 付费用户查询
            iap_users = self.get_result(
                "内购玩家列表.sql", date, self.end_date)
            for row in iap_users:
                user_pseudo_id = row.user_pseudo_id

                user_register_info = self.get_result(
                    "内购玩家注册信息.sql", date, user_pseudo_id)
                register_ver = user_register_info[0].app_version
                register_date = user_register_info[0].event_date
                line_string = ""
                line_string += "{0},".format(register_ver)
                line_string += "{0},".format(Date(date).formatmd())
                line_string += "{0},".format(firstopen_usercount)

                print("内购玩家id: ", user_pseudo_id)
                # 玩家行为数据
                iap_user_behaviors = self.get_result(
                    "内购玩家行为.sql", date, self.end_date, user_pseudo_id)
                iap_line_string = ""
                user_id = ""
                for behavior_row in iap_user_behaviors:
                    if behavior_row.user_id and len(behavior_row.user_id) > 0:
                        user_id = behavior_row.user_id

                    iap_max_stage = self.get_result(
                        "内购玩家付费时关卡.sql", date, self.end_date, user_pseudo_id, behavior_row.event_timestamp)
                    max_stage = iap_max_stage[0].max_stage
                    price = price_map.get(behavior_row.product_name, 0)
                    iap_line_string += "{0},{1},{2},{3},{4},".format(
                        behavior_row.app_version, behavior_row.product_name, price, max_stage, behavior_row.event_date)

                line_string += "{0},{1},".format(
                    user_pseudo_id, user_id)
                line_string += iap_line_string
                # 数据拼接
                append_line(report_lines, len(report_lines), line_string)
            file.close()
        return report_lines
