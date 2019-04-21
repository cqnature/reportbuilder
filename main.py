#!/usr/bin/env python
# coding=utf-8

from project.entry import generate_report
from project.base.config import ReportFlag

if __name__ == '__main__':
    flags = [
        ReportFlag.mail,
        ReportFlag.lost_level,
        ReportFlag.retention_level,
        ReportFlag.stage,
        ReportFlag.new_ads,
        ReportFlag.retention_ads,
        ReportFlag.total_ads,
        ReportFlag.iap_behaviour,
        ReportFlag.lost_behaviour,
        ReportFlag.retention_behaviour
    ]
    option = ReportFlag(flags).option

    # generate_report(option, 'mergefood', 'analytics_188328474', 'ANDROID', 'United States', '20190401')
    generate_report(option, 'mergefood', 'analytics_188328474', 'IOS', 'China', '20190401')

    generate_report(option, 'mergegarden', 'analytics_195246954', 'ANDROID', 'United States', '20190329')
    generate_report(option, 'mergegarden', 'analytics_195246954', 'IOS', 'United States', '20190326')
