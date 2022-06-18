#!/usr/bin/env python
# coding=utf-8

from project.entry import generate_report_us
from project.base.configs import ReportFlag
import os
import json

if __name__ == '__main__':
    flags = [
        ReportFlag.mail,
        ReportFlag.lost_push,
        ReportFlag.retention_push,
        ReportFlag.lost_stage,
        ReportFlag.retention_stage,
        ReportFlag.new_ads,
        ReportFlag.dau_ads,
        ReportFlag.total_ads,
        ReportFlag.iap_behaviour,
        ReportFlag.lost_behaviour,
        ReportFlag.retention_behaviour,
        ReportFlag.will_ads,
        ReportFlag.day_stage,
        ReportFlag.button_behaviour,
        ReportFlag.retention_event,
        ReportFlag.lost_ads,
        ReportFlag.retention_ads_count,
        ReportFlag.lost_reset,
        ReportFlag.retention_reset,
    ]
    option = ReportFlag(flags).option

    with open('./config/params.json') as file:
        content = json.load(file)
        for x in content:
            generate_report_us(option, x['start_date'], x['project_name'], x['table_prefix'], x['appsflyer_api_token'], x['app_id'], x['fb_app_id'],
                               x['fb_access_token'], x['admob_app_id'], x['platform'], x['geo_country'], x['contain_roi'], x['send_partner_email'], x['extra_date'])
        file.close()
