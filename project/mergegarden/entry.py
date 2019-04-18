#!/usr/bin/env python
# coding=utf-8

import os
import json
from ..base.config import *
from ..base.date import *
from ..base.entry import *
from mailreport import generate_mail_report
from lostplantreport import generate_lostplant_report
from retentionplantreport import generate_retentionplant_report
from stagereport import generate_stage_report
from retentionadsreport import generate_retention_ads_report
from newadsreport import generate_new_ads_report
from totaladsreport import generate_total_ads_report
from iapbehaviourreport import generate_iap_behaviour_report
from lostbehaviourreport import generate_lostbehaviour_report
from retentionbehaviourreport import generate_retentionbehaviour_report

class Entry(BaseEntry):

    def do_generate_report(self):
        print 'mergegarden do_generate_report'
        # 开启代理
        if self.option & ReportFlag.mail:
            generate_mail_report(self.query_config, this.start_date)
        if self.option & ReportFlag.lost_level:
            generate_lostplant_report(self.query_config, this.start_date)
        if self.option & ReportFlag.lost_level:
            generate_retentionplant_report(self.query_config, this.start_date)
        if self.option & ReportFlag.lost_level:
            generate_stage_report(self.query_config, this.start_date)
        if self.option & ReportFlag.lost_level:
            generate_new_ads_report(self.query_config, this.start_date)
        if self.option & ReportFlag.lost_level:
            generate_retention_ads_report(self.query_config, this.start_date)
        if self.option & ReportFlag.lost_level:
            generate_total_ads_report(self.query_config, this.start_date)
        if self.option & ReportFlag.lost_level:
            generate_iap_behaviour_report(self.query_config, this.start_date)
        if self.option & ReportFlag.lost_level:
            generate_lostbehaviour_report(self.query_config, this.start_date)
        if self.option & ReportFlag.lost_level:
            generate_retentionbehaviour_report(self.query_config, this.start_date)
