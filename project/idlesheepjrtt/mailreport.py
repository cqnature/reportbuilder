#!/usr/bin/env python
# coding=utf-8

import os
import json
import csv
from ..lib.HTML import *
from ..base.date import *
from ..base.mail import send_mail
from ..base.helper import *
from ..base.query import *
from ..base.report import *
from yattag import Doc

def sortbydate(e):
    return e['start']

def generate_mail_report(query_config, date):
    return Report(query_config, date).generate()

class Report(BaseReport):
    def __init__(self, query_config, date):
        super(Report, self).__init__(query_config, date)
        self.mode = ReportMode.mail

    def do_generate(self):
        print 'do generate report'
        mail_content = self.generate_mail_report()
        send_mail(self.subject, mail_content)
        return []

    def generate_mail_report(self):
        doc, tag, text, line = Doc().ttl()
        doc.asis('<!DOCTYPE html>')
        with tag('html'):
            with tag('body'):
                latelyhtmlcode = self.generate_mail_lately_report()
                adshtmlcode = self.generate_mail_ads_report()
                retentionhtmlcode = self.generate_mail_retention_report()
                line('h1', '一、三日基础数据更新')
                doc.asis(str(latelyhtmlcode))
                line('h1', '二、数据对比，分析问题')
                line('h2', '广告人均观看次数对比')
                doc.asis(str(adshtmlcode))
                line('h2', '留存率对比')
                doc.asis(str(retentionhtmlcode))
                if self.query_config.contain_roi:
                    line('h2', '回收数据')
                    roihtmlcode = self.generate_mail_roi_report()
                    doc.asis(str(roihtmlcode))
        return doc.getvalue()

    def generate_mail_roi_report(self):
        print 'generate_mail_roi_report from: ', self.start_date, " to: ", self.end_date
        htmlcode = Table()
        header_row = ['日期', '花费($)', 'cpi($)', '安装', '自然量', 'DAU', '总收入($)', '总APRDAU($', 'ROI', '广告收入($)', '广告ARPDAU($)', 'eCPM($)', '展示次数', '人均广告次数', 'IAP的ARPDAU($)', 'IAP收入($)']
        cells = []
        for k in range(len(header_row)):
            cells.append(TableCell(header_row[k], header=True, bgcolor='grey'))
        htmlcode.rows.append(cells)
        for date in Date(self.start_date).rangeto(self.end_date, True):
            iap_revenue_result = self.get_result('in_app_purchase_revenue.sql', date, date)
            iap_revenue_data = iap_revenue_result[0].total_revenue
            iap_revenue = float((0 if iap_revenue_data == None else iap_revenue_data))
            daily_user_count = self.get_daily_count(date)
            appsflyer_data = self.get_appsflyer_detail(date)
            an_data = self.get_audiencenetwork_detail(date)
            admob_data = self.get_admob_detail(date)
            ad_imp = int(an_data[0]) + int(admob_data[0])
            ad_revenue = float(an_data[1]) + float(admob_data[1])
            total_revenue = iap_revenue + ad_revenue
            total_cost = appsflyer_data[0]

            cells = []
            cells.append(Date(date).formatmd())
            cells.append(str(total_cost))
            cells.append("{0:.2f}".format((0 if appsflyer_data[1] == 0 else appsflyer_data[0]/float(appsflyer_data[1]))))
            cells.append(str(appsflyer_data[1]))
            cells.append(str(appsflyer_data[2]))
            cells.append(str(daily_user_count))
            cells.append(str(total_revenue))
            cells.append(TableCell("{0:.3f}".format((0 if daily_user_count == 0 else total_revenue/float(daily_user_count))), bgcolor='lightpink'))
            cells.append(TableCell(("N/A" if total_cost == 0 else "{0:.1f}%".format(100*total_revenue/total_cost)), bgcolor='lightpink'))
            cells.append("{0:.2f}".format(ad_revenue))
            cells.append("{0:.3f}".format((0 if daily_user_count == 0 else ad_revenue/float(daily_user_count))))
            if ad_imp > 0:
                cells.append("{0:.2f}".format(ad_revenue/(float(ad_imp)/1000.0)))
            else:
                cells.append("0.00");
            cells.append(str(ad_imp))
            cells.append(TableCell("{0:.2f}".format((0 if daily_user_count == 0 else float(ad_imp)/float(daily_user_count))), bgcolor='lightpink'))
            cells.append("{0:.3f}".format((0 if daily_user_count == 0 else iap_revenue/float(daily_user_count))))
            cells.append("{0:.2f}".format(iap_revenue))
            htmlcode.rows.append(cells)
        return htmlcode

    def get_appsflyer_detail(self, date):
        dailyreport = self.get_daily_report(date, date)
        if dailyreport == None:
            return (0, 0, 0)
        datas = [x.strip() for x in dailyreport.split('\n')[1:]]
        cost = 0
        organic_install_count = 0
        non_organic_install_count = 0
        for x in datas:
            if len(x) == 0:
                continue
            fields = x.split(',')
            if fields[2] == 'Organic':
                organic_install_count += (0 if fields[7] == 'N/A' else int(fields[7]))
            else:
                cost += (0 if fields[12] == 'N/A' else float(fields[12]))
                non_organic_install_count += (0 if fields[7] == 'N/A' else int(fields[7]))
        return (cost, non_organic_install_count, organic_install_count)

    def get_audiencenetwork_detail(self, date):
        datas = self.queryads.get_result(date, date)
        fb_ad_network_imp = next((int(x['value']) for x in datas if x['metric'] == 'fb_ad_network_imp'), 0)
        fb_ad_network_revenue = next((float(x['value']) for x in datas if x['metric'] == 'fb_ad_network_revenue'), 0.0)
        return (fb_ad_network_imp, fb_ad_network_revenue)

    def get_admob_detail(self, date):
        datas = self.queryadscene.get_result(date, date)
        return (datas[3], datas[4])

    def generate_mail_lately_report(self):
        print 'generate_mail_lately_report from: ', self.start_date, " to: ", self.end_date
        htmlcode = Table()
        header_row = ['日期', '新注册用户', '首日广告观看次数', '次日广告观看次数', '三日广告观看次数', '次留', '三留']
        cells = []
        for k in range(len(header_row)):
            cells.append(TableCell(header_row[k], header=True, bgcolor='grey'))
        htmlcode.rows.append(cells)
        lately_date = max(Date(self.end_date).adddays(-2), self.start_date)
        for date in Date(lately_date).rangeto(self.end_date, True):
            first_user_count = self.get_firstopen_count(date)
            if first_user_count == 0:
                continue
            cells = []
            cells.append(Date(date).formatmd())
            cells.append(str(first_user_count))
            for k in range(3):
                single_date = Date(date).adddays(k)
                ads_view_count_results = self.get_result("ads_view_of_retention_users.sql", date, single_date)
                user_count = self.get_retention_count(date, single_date)
                view_count = sum(1 for _ in ads_view_count_results)
                average_view_count = 0 if user_count == 0 else float(view_count)/float(user_count)
                cells.append("{0:.2f}".format(average_view_count))
            for k in range(2):
                single_date = Date(date).adddays(k + 1)
                user_count = self.get_retention_count(date, single_date)
                cells.append("{0:.2f}%".format(100*float(user_count)/float(first_user_count)))
            htmlcode.rows.append(cells)
        return htmlcode

    def generate_mail_ads_report(self):
        print 'generate_mail_ads_report from: ', self.start_date, " to: ", self.end_date
        htmlcode = Table()
        cells = []
        cells.append(TableCell("日期", header=True, bgcolor='grey', attribs={"rowspan":2}))
        for k in range(8):
            cells.append(TableCell("D{0}".format(k), header=True, bgcolor='grey', attribs={"colspan":3}))
        htmlcode.rows.append(cells)
        cells = []
        cells.append(TableCell("注册人数".format(k), bgcolor='grey'))
        cells.append(TableCell("观看次数".format(k), bgcolor='grey'))
        cells.append(TableCell("人均次数".format(k), bgcolor='grey'))
        for k in range(7):
            cells.append(TableCell("留存人数".format(k), bgcolor='grey'))
            cells.append(TableCell("观看次数".format(k), bgcolor='grey'))
            cells.append(TableCell("人均次数".format(k), bgcolor='grey'))
        htmlcode.rows.append(cells)
        for date in Date(self.start_date).rangeto(self.end_date, True):
            cells = []
            cells.append(Date(date).formatmd())
            for k in range(8):
                single_date = Date(date).adddays(k)
                if Date(single_date).between(self.end_date) <= 0:
                    cells.append("0")
                    cells.append("0")
                    cells.append("0.00")
                else:
                    ads_view_count_results = self.get_result("ads_view_of_retention_users.sql", date, single_date)
                    user_count = 0
                    if date == single_date:
                        user_count = self.get_firstopen_count(single_date)
                    else:
                        user_count = self.get_retention_count(date, single_date)
                    view_count = sum(1 for _ in ads_view_count_results)
                    average_view_count = 0 if user_count == 0 else float(view_count)/float(user_count)
                    cells.append(str(user_count))
                    cells.append(str(view_count))
                    cells.append("{0:.2f}".format(average_view_count))
            htmlcode.rows.append(cells)
        return htmlcode

    def generate_mail_retention_report(self):
        print 'generate_mail_retention_report from: ', self.start_date, " to: ", self.end_date
        htmlcode = Table()
        cells = []
        cells.append(TableCell("日期", header=True, bgcolor='grey'))
        cells.append(TableCell("用户数", header=True, bgcolor='grey'))
        for k in range(8):
            cells.append(TableCell("D{0}留存".format(k), header=True, bgcolor='grey'))
        htmlcode.rows.append(cells)
        for date in Date(self.start_date).rangeto(self.end_date, True):
            first_user_count = self.get_firstopen_count(date)
            if first_user_count == 0:
                continue
            cells = []
            cells.append(Date(date).formatmd())
            cells.append(str(first_user_count))
            for k in range(8):
                single_date = Date(date).adddays(k)
                if Date(single_date).between(self.end_date) <= 0:
                    cells.append("0%")
                else:
                    user_count = self.get_retention_count(date, single_date)
                    cells.append("{0:.2f}%".format(100*float(user_count)/float(first_user_count)))
            htmlcode.rows.append(cells)
        return htmlcode
