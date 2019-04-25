#!/usr/bin/python
#
# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Retrieves a saved report or generates a new one.

To get ad clients, run get_all_ad_clients.py.

Tags: reports.generate
"""

__author__ = 'jalc@google.com (Jose Alcerreca)'

import argparse
import sys
import json

from adsense_util import get_account_id
from adsense_util_data_collator import DataCollator
from apiclient import sample_tools
from oauth2client import client
from datetime import date, datetime

# Declare command-line flags.
argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument(
    '--report_id',
    help='The ID of the saved report to generate')


def generate_report(app_id, platform, from_date, to_date):
    # Authenticate and construct service.
    service, flags = sample_tools.init(
        [], 'adsense', 'v1.4', __doc__, __file__, parents=[argparser],
        scope='https://www.googleapis.com/auth/adsense.readonly')
    ad_platform = 'Android' if platform == 'ANDROID' else 'iOS'
    report_from_date = datetime.strptime(from_date, "%Y%m%d").date().strftime("%Y-%m-%d")
    report_to_date = datetime.strptime(to_date, "%Y%m%d").date().strftime("%Y-%m-%d")
    try:
        # Let the user pick account if more than one.
        account_id = get_account_id(service)

        # Retrieve report.
        result = service.accounts().reports().generate(
            accountId=account_id, startDate=report_from_date, endDate=report_to_date,
            filter=['APP_ID=={}'.format(app_id), 'APP_PLATFORM=={}'.format(ad_platform)],
            metric=['AD_REQUESTS', 'VIEWED_IMPRESSIONS', 'EARNINGS'],
            dimension=['APP_ID', 'APP_PLATFORM'],
            sort=['+DAY']).execute()
        result = DataCollator([result]).collate_data()
        return json.dumps(result)
    except client.AccessTokenRefreshError:
        print ('The credentials have been revoked or expired, please re-run the '
            'application to re-authorize')
