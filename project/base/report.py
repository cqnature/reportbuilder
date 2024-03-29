#!/usr/bin/env python
# coding=utf-8

import os
from project.base.date import *
from project.base.query import *
from project.base.helper import *
from enum import Enum


class ReportMode(Enum):
    file = 1
    mail = 2


class BaseReport(object):
    def __init__(self, query_config, date):
        self.mode = ReportMode.file
        self.output_folder = 'output'
        self.etc_filename = ''
        self.output_filename = ''
        self.output_filepath = ''
        self.subject = ''
        self.query_config = query_config
        self.project_config = self.query_config.project_config
        self.querysql = QuerySql(self.query_config)
        self.queryreport = QueryReport(self.query_config)
        self.start_date = date.date_string
        self.end_date = date.enddate(self.query_config.geo_country)
        self.extra_date = []
        if self.query_config.extra_date != "":
            self.extra_date = self.query_config.extra_date.split("|")

    def get_retention_date(self, date_string):
        return min(self.end_date, Date(date_string).adddays(7))

    def generate(self):
        if self.mode == ReportMode.file:
            path = self.create_output_folder()
            self.output_filepath = os.path.join(path, self.output_filename)
        else:
            self.subject = "{0}项目{1}平台{2}数据总报表".format(
                self.project_config.project_name, self.query_config.platform, self.end_date)
        self.etc_filepath = os.path.join(
            self.project_config.etc_path, self.etc_filename)
        return self.do_generate()

    def create_output_folder(self):
        project_name = self.query_config.project_config.project_name
        platform = self.query_config.platform
        geo_country = self.query_config.geo_country
        folders = (self.output_folder, project_name, platform,
                   geo_country, self.start_date, self.end_date)
        path = '.'
        for x in folders:
            path = os.path.join(path, x)
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError:
                print("Creation of the directory %s failed" % path)
            else:
                print("Successfully created the directory %s" % path)
        return path

    def do_generate(self):
        print('do generate report')
        return []

    def get_daily_report(self, *parameter):
        return self.queryreport.get_daily_result(*parameter)

    def get_partners_daily_report(self, *parameter):
        return self.queryreport.get_partners_daily_result(*parameter)

    def get_result(self, filename, *parameter):
        return self.querysql.get_result(filename, *parameter)

    def append_output_filename(self, filename):
        splits = os.path.splitext(self.output_filepath)
        return splits[0] + filename + splits[1]

    def get_firstopen_count(self, date):
        return get_firstopen_usercount(self.querysql, date)

    def get_firstopen_version(self, date):
        firstopen_results = self.querysql.get_result(
            "firstopen_app_version.sql", date)
        app_versions = [x[0] for x in firstopen_results]
        return '|'.join(app_versions)

    def get_lost_count(self, start_date, end_date):
        return get_lost_usercount(self.querysql, start_date, end_date)

    def get_retention_count(self, start_date, end_date):
        return get_retention_usercount(self.querysql, start_date, end_date)

    def get_daily_count(self, date):
        return get_daily_usercount(self.querysql, date)

    def get_iap_revenue(self, date, end_date):
        return get_iap_revenue_bysql(self.querysql, date, end_date)

    def get_iap_summary(self, date, end_date):
        return get_iap_summary_bysql(self.querysql, date, end_date)
