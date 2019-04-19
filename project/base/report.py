#!/usr/bin/env python
# coding=utf-8

import os
from date import *
from query import *
from helper import *
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
        self.start_date = date.date_string
        self.end_date = date.enddate()

    def generate(self):
        if self.mode == ReportMode.file:
            path = self.create_output_folder()
            self.output_filepath = os.path.join(path, self.output_filename)
        else:
            self.subject = "{0}平台{1}数据报表".format(self.query_config.platform, self.end_date)
        self.etc_filepath = os.path.join(self.project_config.etc_path, self.etc_filename)
        self.do_generate()

    def create_output_folder(self):
        project_name = self.query_config.project_config.project_name
        platform = self.query_config.platform
        geo_country = self.query_config.geo_country
        folders = (self.output_folder, project_name, platform, geo_country, self.start_date, self.end_date)
        path = '.'
        for x in folders: path = os.path.join(path, x)
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError:
                print "Creation of the directory %s failed" % path
            else:
                print "Successfully created the directory %s" % path
        return path

    def do_generate(self):
        print 'do generate report'

    def get_result(self, filename, *parameter):
        return self.querysql.get_result(filename, *parameter)

    def get_firstopen_count(self, date):
        return get_firstopen_usercount(self.querysql, date)

    def get_lost_count(self, start_date, end_date):
        return get_lost_usercount(self.querysql, start_date, end_date)

    def get_retention_count(self, start_date, end_date):
        return get_retention_usercount(self.querysql, start_date, end_date)
