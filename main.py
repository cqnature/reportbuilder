#!/usr/bin/env python
# coding=utf-8

from project.entry import generate_report
from project.base.config import ReportFlag
import os
import json

if __name__ == '__main__':
    flags = [
        ReportFlag.mail,
        ReportFlag.lost_level,
        ReportFlag.retention_level,
        ReportFlag.lost_stage,
        ReportFlag.retention_stage,
        ReportFlag.new_ads,
        ReportFlag.retention_ads,
        ReportFlag.total_ads,
        ReportFlag.iap_behaviour,
        ReportFlag.lost_behaviour,
        ReportFlag.retention_behaviour,
        ReportFlag.will_ads,
        ReportFlag.day_stage,
        ReportFlag.button_behaviour
    ]
    option = ReportFlag(flags).option

    with open('./config/params.json') as file:
        content = json.load(file)
        for x in content:
            generate_report(option, x['start_date'], x['project_name'], x['table_prefix'], x['appsflyer_api_token'], x['app_id'], x['fb_app_id'], x['fb_access_token'], x['admob_app_id'], x['platform'], x['geo_country'], x['contain_roi'], x['send_partner_email'])
        file.close()
