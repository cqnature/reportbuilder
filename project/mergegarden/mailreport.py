#!/usr/bin/env python
# coding=utf-8

import os
import json
from ..lib.HTML import *
from ..base.date import *
from ..base.mail import send_mail
from ..base.helper import *
from ..base.query import *
from yattag import Doc

def sortbydate(e):
  return e['start']

def generate_mail_lately_report(querysql, start_date, end_date):
    print 'generate_mail_lately_report from: ', start_date, " to: ", end_date
    htmlcode = Table()
    header_row = ['日期', '新注册用户', '首日广告观看次数', '次日广告观看次数', '三日广告观看次数', '次留', '三留']
    cells = []
    for k in range(len(header_row)):
        cells.append(TableCell(header_row[k], header=True, bgcolor='grey'))
    htmlcode.rows.append(cells)
    lately_date = max(Date(end_date).adddays(-2), start_date)
    for date in Date(lately_date).rangeto(end_date, True):
        first_user_count = get_firstopen_usercount(querysql, date)
        if first_user_count == 0:
            break
        cells = []
        cells.append(formatdate(date))
        cells.append(str(first_user_count))
        for k in range(3):
            single_date = Date(date).adddays(k)
            ads_view_count_results = querysql.get_result("ads_view_of_retention_users.sql", date, single_date)
            user_count = get_retention_usercount(querysql, date, single_date)
            view_count = sum(1 for _ in ads_view_count_results)
            average_view_count = 0 if user_count == 0 else float(view_count)/float(user_count)
            cells.append("{0:.2f}".format(average_view_count))
        for k in range(2):
            single_date = Date(date).adddays(k + 1)
            user_count = get_retention_usercount(querysql, date, single_date)
            cells.append("{0:.2f}%".format(100*float(user_count)/float(first_user_count)))
        htmlcode.rows.append(cells)
    return htmlcode

def generate_mail_ads_report(querysql, start_date, end_date):
    print 'generate_mail_ads_report from: ', start_date, " to: ", end_date
    htmlcode = Table()
    cells = []
    cells.append(TableCell("日期", header=True, bgcolor='grey', attribs={"rowspan":2}))
    for k in range(8):
        cells.append(TableCell("D{0}".format(k), header=True, bgcolor='grey', attribs={"colspan":3}))
    htmlcode.rows.append(cells)
    cells = []
    for k in range(8):
        cells.append(TableCell("观看人数".format(k), bgcolor='grey'))
        cells.append(TableCell("观看次数".format(k), bgcolor='grey'))
        cells.append(TableCell("人均次数".format(k), bgcolor='grey'))
    htmlcode.rows.append(cells)
    for date in Date(start_date).rangeto(end_date, True):
        cells = []
        cells.append(formatdate(date))
        for k in range(8):
            single_date = Date(date).adddays(k)
            ads_view_count_results = querysql.get_result("ads_view_of_retention_users.sql", date, single_date)
            user_count = 0
            if date == single_date:
                user_count = get_firstopen_usercount(querysql, single_date)
            else:
                user_count = get_retention_usercount(querysql, date, single_date)
            view_count = sum(1 for _ in ads_view_count_results)
            average_view_count = 0 if user_count == 0 else float(view_count)/float(user_count)
            cells.append(str(user_count))
            cells.append(str(view_count))
            cells.append("{0:.2f}".format(average_view_count))
        htmlcode.rows.append(cells)
    return htmlcode

def generate_mail_retention_report(querysql, start_date, end_date):
    print 'generate_mail_retention_report from: ', start_date, " to: ", end_date
    htmlcode = Table()
    cells = []
    cells.append(TableCell("日期", header=True, bgcolor='grey'))
    cells.append(TableCell("用户数", header=True, bgcolor='grey'))
    for k in range(8):
        cells.append(TableCell("D{0}留存".format(k), header=True, bgcolor='grey'))
    htmlcode.rows.append(cells)
    for date in Date(start_date).rangeto(end_date, True):
        first_user_count = get_firstopen_usercount(querysql, date)
        if first_user_count == 0:
            break
        cells = []
        cells.append(formatdate(date))
        cells.append(str(first_user_count))
        for k in range(8):
            single_date = Date(date).adddays(k)
            user_count = get_retention_usercount(querysql, date, single_date)
            cells.append("{0:.2f}%".format(100*float(user_count)/float(first_user_count)))
        htmlcode.rows.append(cells)
    return htmlcode

def generate_mail_report_at_date(querysql, start_date, end_date):
    doc, tag, text, line = Doc().ttl()
    doc.asis('<!DOCTYPE html>')
    with tag('html'):
        with tag('body'):
            latelyhtmlcode = generate_mail_lately_report(querysql, start_date, end_date)
            adshtmlcode = generate_mail_ads_report(querysql, start_date, end_date)
            retentionhtmlcode = generate_mail_retention_report(querysql, start_date, end_date)
            line('h1', '一、三日基础数据更新')
            doc.asis(str(latelyhtmlcode))
            line('h1', '二、数据对比，分析问题')
            line('h2', '广告人均观看次数对比')
            doc.asis(str(adshtmlcode))
            line('h2', '留存率对比')
            doc.asis(str(retentionhtmlcode))
    return doc.getvalue()

def generate_mail_report(query_config, date):
    querysql = QuerySql(query_config)
    start_date = date.date_string
    end_date = date.enddate()
    reportstring = generate_mail_report_at_date(querysql, start_date, end_date)
    send_mail("{0}平台{1}数据报表".format(query_config.platform, end_date), reportstring)
