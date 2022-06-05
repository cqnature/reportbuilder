#!/usr/bin/env python
# coding=utf-8

import os
import json
import csv
from ..lib.HTML import *
from project.base.date import *
from project.base.mail import send_mail
from project.base.helper import *
from project.base.query import *
from project.base.report import *
from yattag import Doc


def sortbydate(e):
    return e['start']


def generate_mail_report(query_config, date):
    return Report(query_config, date).generate()


class Report(BaseReport):
    def __init__(self, query_config, date):
        super(Report, self).__init__(query_config, date)
        self.mode = ReportMode.mail
        self.partner_email = []

    def do_generate(self):
        print('do generate report')
        mail_content = self.generate_mail_report()
        send_mail(self.subject, mail_content)
        if self.query_config.send_partner_email:
            send_mail(self.subject, mail_content, [], self.partner_email)
        return []

    def generate_mail_report(self):
        doc, tag, text, line = Doc().ttl()
        doc.asis('<!DOCTYPE html>')
        with tag('html'):
            with tag('body'):
                latelyhtmlcode = self.generate_mail_lately_report()
                doc.asis(str(latelyhtmlcode))
        return doc.getvalue()

    def generate_mail_lately_report(self):
        print('generate_mail_lately_report from: ',
              self.start_date, " to: ", self.end_date)
        htmlcode = Table()
        cells = []
        cells.append(TableCell("日期", header=True,
                     bgcolor='grey', attribs={"rowspan": 2}))
        cells.append(TableCell("DAU", header=True,
                     bgcolor='grey', attribs={"rowspan": 2}))
        cells.append(TableCell("新增", header=True,
                     bgcolor='grey', attribs={"rowspan": 2}))
        cells.append(TableCell("留存", header=True,
                     bgcolor='grey', attribs={"colspan": 6}))
        cells.append(TableCell("广告次数", header=True,
                     bgcolor='grey', attribs={"colspan": 7}))
        cells.append(TableCell("7日总广告次数", header=True,
                     bgcolor='grey', attribs={"rowspan": 2}))
        htmlcode.rows.append(cells)
        cells = []
        cells.append(TableCell("次留", bgcolor='grey'))
        for k in range(5):
            cells.append(TableCell("{0}留".format(
                k + 3), header=True, bgcolor='grey'))
        for k in range(7):
            cells.append(TableCell("D{0}".format(
                k + 1), header=True, bgcolor='grey'))
        htmlcode.rows.append(cells)
        for date in self.extra_date:
            self.generate_mail_lately_htmlcode(date, htmlcode)
        lately_date = max(Date(self.end_date).adddays(-14), self.start_date)
        for date in Date(lately_date).rangeto(self.end_date, True):
            self.generate_mail_lately_htmlcode(date, htmlcode)
        return htmlcode

    def generate_mail_lately_htmlcode(self, date, htmlcode):
        daily_user_count = self.get_daily_count(date)
        if daily_user_count == 0:
            return
        first_user_count = self.get_firstopen_count(date)
        if first_user_count == 0:
            return
        cells = []
        cells.append(Date(date).formatmd())
        cells.append(str(daily_user_count))
        cells.append(str(first_user_count))
        for k in range(6):
            single_date = Date(date).adddays(k + 1)
            if Date(single_date).between(self.end_date) <= 0:
                cells.append("N/A")
            else:
                user_count = self.get_retention_count(date, single_date)
                cells.append("{0:.2f}%".format(
                    100*float(user_count)/float(first_user_count)))
        total_ad_count = 0
        for k in range(7):
            single_date = Date(date).adddays(k)
            if Date(single_date).between(self.end_date) <= 0:
                cells.append("N/A")
            else:
                ads_view_count_results = self.get_result(
                    "留存用户广告次数.sql", date, single_date)
                user_count = self.get_retention_count(date, single_date)
                view_count = sum(1 for _ in ads_view_count_results)
                average_view_count = 0 if user_count == 0 else float(
                    view_count)/float(user_count)
                cells.append("{0:.2f}".format(average_view_count))
                total_ad_count += average_view_count
        cells.append("{0:.2f}".format(total_ad_count))
        htmlcode.rows.append(cells)
