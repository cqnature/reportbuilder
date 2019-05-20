#!/usr/bin/env python
# coding=utf-8

import os
import json
from date import *

class ReportFlag:
    mail = 1
    lost_level = 1 << 1
    retention_level = 1 << 2
    lost_stage = 1 << 3
    retention_stage = 1 << 4
    new_ads = 1 << 5
    retention_ads = 1 << 6
    total_ads = 1 << 7
    iap_behaviour = 1 << 8
    lost_behaviour = 1 << 9
    retention_behaviour = 1 << 10
    will_ad = 1 << 11

    def __init__(self, flags):
        self.option = 0
        for x in flags:
            self.option = self.option | x

class ProjectConfig:
    def __init__(self, project_name, table_prefix, appsflyer_api_token, app_id, fb_app_id, fb_access_token, admob_app_id):
        self.project_name = project_name
        self.table_prefix = table_prefix
        self.project_path = os.path.join('./project', self.project_name)
        self.sql_path = os.path.join('./sql', self.project_name)
        self.etc_path = os.path.join('./etc', self.project_name)
        self.credentials_path = os.path.join('./credentials', self.project_name)
        self.appsflyer_api_token = appsflyer_api_token
        self.app_id = app_id
        self.fb_app_id = fb_app_id
        self.fb_access_token = fb_access_token
        self.admob_app_id = admob_app_id

    def set_env_from_config(self, config, key):
        if config.has_key(key):
            os.environ[key] = config[key]

    def enable_proxy(self):
        with open("./config/config.json") as file:
            file_config = json.load(file)
            self.set_env_from_config(file_config, "https_proxy")
            self.set_env_from_config(file_config, "http_proxy")
            self.set_env_from_config(file_config, "all_proxy")
            file.close()

    def enable_credential(self):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(self.credentials_path, 'credentials.json')

class QueryConfig:
    def __init__(self, project_config, platform, geo_country, contain_roi, send_partner_email):
        self.project_config = project_config
        self.platform = platform
        self.geo_country = geo_country
        self.contain_roi = contain_roi
        self.send_partner_email = send_partner_email
        self.cache_folder = 'library'
        self.file_name = 'cache.json'
        self.retry_count = 3

    def set_platform(self, platform):
        self.platform = platform

    def set_country(self, geo_country):
        self.geo_country = geo_country

    def validate(self, date):
        if self.platform != "IOS" and self.platform != "ANDROID":
            print("You must pass platform in IOS or ANDROID")
            exit(1)
        try:
            date.validate()
        except ValueError, Argument:
            print(Argument)
            exit(1)
