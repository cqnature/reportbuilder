#!/usr/bin/env python
# coding=utf-8

import os
import json
from ..base.date import *
from ..base.helper import *
from ..base.query import *
from ..base.report import *

lost_day = 0
area_id = 1

def generate_retention_stage_report(query_config, date):
    return Report(query_config, date).generate()

class Report(BaseReport):
    def __init__(self, query_config, date):
        super(Report, self).__init__(query_config, date)
        self.etc_filename = 'stage_progress_of_retention_users.csv'
        country_string = "CN" if self.query_config.geo_country == 'China' else "US"
        platform_string = "AND" if self.query_config.platform == 'ANDROID' else "iOS"
        self.output_filename = "{0}-{1}-Day{2}-RetentionUser-Area{3}-Level-{4}.csv".format(country_string, platform_string, lost_day + 1, area_id, self.end_date)

    def do_generate(self):
        print 'do generate report'
        with open(self.output_filepath, mode='w+') as out:
            report_lines = []
            with open(self.etc_filepath) as file:
                lines = file.readlines()
                head_lines1 = [x.strip() for x in lines[0:1]]
                report_lines.extend(head_lines1)
                file.close()
            for single_date in self.extra_date:
                self.generate_retention_stage_report_at_date(report_lines, single_date)
            for single_date in Date(self.start_date).rangeto(self.end_date, True):
                self.generate_retention_stage_report_at_date(report_lines, single_date)
            reportstring = '\n'.join(report_lines)
            out.write(reportstring)
            out.close()
        return [self.output_filepath]

    def generate_retention_stage_report_at_date(self, report_lines, date):
        print("generate_retention_stage_report_at_date ", date)
        with open(self.etc_filepath) as file:
            firstopen_usercount = self.get_firstopen_count(date)
            if firstopen_usercount == 0:
                return;

            lines = file.readlines()
            head_line = [x.strip() for x in lines[1:2]][0]
            line_string = ""
            line_string += "{0},".format(Date(date).formatmd())
            line_string += "{0},".format(firstopen_usercount)
            # 留存率查询
            single_date = Date(date).adddays(lost_day)
            if Date(single_date).between(self.end_date) > 0:
                current_retention_usercount = self.get_retention_count(date, single_date)
                # 流失分布查询
                retention_day_results = self.get_result("stage_progress_of_retention_users.sql", date, single_date)

                retention_base_datas = []
                for row in retention_day_results:
                    retention_base_data = [row.rebirth, row.level, row.user_count, 100*float(row.user_count)/float(firstopen_usercount)]
                    retention_base_datas.append(retention_base_data)
                first_retention_usercount = current_retention_usercount - sum(t[2] for t in retention_base_datas)
                retention_base_datas.insert(0, [0, 1, first_retention_usercount, 100*float(first_retention_usercount)/float(firstopen_usercount)])

                head_lines = head_line.split(',')[2:]
                for head in head_lines:
                    headsegments = head.split('|')
                    min_level = int(headsegments[0])
                    max_level = sys.maxint if len(headsegments) == 1 else int(headsegments[1])
                    level_user_percent = 0
                    for k in range(len(retention_base_datas)):
                        data = retention_base_datas[k]
                        if data[0] == area_id - 1 and data[1] >= min_level and data[1] <= max_level:
                            level_user_percent += data[3]
                    line_string += "{0:.2f}%,".format(level_user_percent)
            # 数据拼接
            append_line(report_lines, len(report_lines), line_string)
            file.close()
        return report_lines
