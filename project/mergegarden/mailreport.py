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

# # 7) sample table with column attributes and styles:
# table_data = [
#         ['Smith',       'John',         30,    4.5],
#         ['Carpenter',   'Jack',         47,    7],
#         ['Johnson',     'Paul',         62,    10.55],
#     ]
# htmlcode = HTML.table(table_data,
#     header_row = ['Last name',   'First name',   'Age', 'Score'],
#     col_width=['', '20%', '10%', '10%'],
#     col_align=['left', 'center', 'right', 'char'],
#     col_styles=['font-size: large', '', 'font-size: small', 'background-color:yellow'])
# f.write(htmlcode + '<p>\n')
# print htmlcode
# print '-'*79

def sortbydate(e):
  return e['start']

def generate_mail_lately_report(platform, start_date, end_date):
    print 'generate_mail_lately_report from: ', start_date, " to: ", end_date
    htmlcode = HTML.Table()
    header_row = ['日期', '新注册用户', '首日广告观看次数', '次日广告观看次数', '三日广告观看次数', '次留', '三留']
    cells = []
    for k in range(len(header_row)):
        cells.append(HTML.TableCell(header_row[k], header=True, bgcolor='grey'))
    htmlcode.rows.append(cells)
    lately_date = max(date_add(end_date, -2), start_date)
    for date in daterange(lately_date, end_date, True):
        first_user_count = get_firstopen_usercount(platform, date)
        if first_user_count == 0:
            break
        cells = []
        cells.append(formatdate(date))
        cells.append(str(first_user_count))
        for k in range(3):
            single_date = date_add(date, k)
            ads_view_count_results = querysql("./sql/ads_view_of_retention_users.sql", platform, date, single_date)
            user_count = get_retention_usercount(platform, date, single_date)
            view_count = sum(1 for _ in ads_view_count_results)
            average_view_count = 0 if user_count == 0 else float(view_count)/float(user_count)
            cells.append("{0:.2f}".format(average_view_count))
        for k in range(2):
            single_date = date_add(date, k + 1)
            user_count = get_retention_usercount(platform, date, single_date)
            cells.append("{0:.2f}%".format(100*float(user_count)/float(first_user_count)))
        htmlcode.rows.append(cells)
    return htmlcode

def generate_mail_ads_report(platform, start_date, end_date):
    print 'generate_mail_ads_report from: ', start_date, " to: ", end_date
    htmlcode = HTML.Table()
    cells = []
    cells.append(HTML.TableCell("日期", header=True, bgcolor='grey', attribs={"rowspan":2}))
    for k in range(8):
        cells.append(HTML.TableCell("D{0}".format(k), header=True, bgcolor='grey', attribs={"colspan":3}))
    htmlcode.rows.append(cells)
    cells = []
    for k in range(8):
        cells.append(HTML.TableCell("观看人数".format(k), bgcolor='grey'))
        cells.append(HTML.TableCell("观看次数".format(k), bgcolor='grey'))
        cells.append(HTML.TableCell("人均次数".format(k), bgcolor='grey'))
    htmlcode.rows.append(cells)
    for date in daterange(start_date, end_date, True):
        cells = []
        cells.append(formatdate(date))
        for k in range(8):
            single_date = date_add(date, k)
            ads_view_count_results = querysql("./sql/ads_view_of_retention_users.sql", platform, date, single_date)
            user_count = 0
            if date == single_date:
                user_count = get_firstopen_usercount(platform, single_date)
            else:
                user_count = get_retention_usercount(platform, date, single_date)
            view_count = sum(1 for _ in ads_view_count_results)
            average_view_count = 0 if user_count == 0 else float(view_count)/float(user_count)
            cells.append(str(user_count))
            cells.append(str(view_count))
            cells.append("{0:.2f}".format(average_view_count))
        htmlcode.rows.append(cells)
    return htmlcode

def generate_mail_retention_report(platform, start_date, end_date):
    print 'generate_mail_retention_report from: ', start_date, " to: ", end_date
    htmlcode = HTML.Table()
    cells = []
    cells.append(HTML.TableCell("日期", header=True, bgcolor='grey'))
    cells.append(HTML.TableCell("用户数", header=True, bgcolor='grey'))
    for k in range(8):
        cells.append(HTML.TableCell("D{0}留存".format(k), header=True, bgcolor='grey'))
    htmlcode.rows.append(cells)
    for date in daterange(start_date, end_date, True):
        first_user_count = get_firstopen_usercount(platform, date)
        if first_user_count == 0:
            break
        cells = []
        cells.append(formatdate(date))
        cells.append(str(first_user_count))
        for k in range(8):
            single_date = date_add(date, k)
            user_count = get_retention_usercount(platform, date, single_date)
            cells.append("{0:.2f}%".format(100*float(user_count)/float(first_user_count)))
        htmlcode.rows.append(cells)
    return htmlcode

def generate_mail_report_at_date(querysql, start_date, end_date):
    # version_datas = None
    # with open("./etc/version.json") as file:
    #     file_config = json.load(file)
    #     version_datas = file_config[platform]
    #     file.close()
    # if version_datas == None:
    #     return;
    #
    # htmlcode = HTML.Table(header_row=['日期', '新增用户', '首日人均广告观看次数', '次日人均广告观看次数', '三日人均广告观看次数', '次留', '3留'])
    # version_datas.sort(key=sortbydate)
    # current_version = ''
    # version_start_date = start_date
    # for version_data in version_datas:
    #     if version_data.has_key('end') and version_data['end'] < start_date:
    #         continue
    #     version_end_date = end_date
    #     if version_data.has_key('end'):
    #         version_end_date = max(version_end_date, version_data['end'])
    #     for single_date in daterange(version_start_date, version_end_date, True):
    #         cells = []
    #         version_changed = False
    #         if version_data['name'] != current_version:
    #             current_version = version_data['name']
    #             version_changed = True
    #         # append version info
    #         if version_changed:
    #             span = betweenday(version_start_date, version_end_date)
    #             cells.append(HTML.TableCell(version_data['name'], attribs={"rowspan":span}))
    #             cells.append(HTML.TableCell(version_data['content'], attribs={"rowspan":span}))
    #
    #         # append the row with cells:
    #         htmlcode.rows.append(cells)
    #     version_start_date = date_add(version_end_date)
    # htmlcode = str(t)
    # return str(htmlcode)
    doc, tag, text, line = Doc().ttl()
    doc.asis('<!DOCTYPE html>')
    with tag('html'):
        with tag('body'):
            latelyhtmlcode = generate_mail_lately_report(platform, start_date, end_date)
            adshtmlcode = generate_mail_ads_report(platform, start_date, end_date)
            retentionhtmlcode = generate_mail_retention_report(platform, start_date, end_date)
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
    send_mail("{0}平台{1}数据报表".format(platform, end_date), reportstring)
