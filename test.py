#!/usr/bin/env python
# coding=utf-8
import os
# import datetime
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

# def count_date(start_date_string, end_date_string):
#     start_date = datetime.datetime.strptime(start_date_string, "%Y%m%d").date()
#     end_date = datetime.datetime.strptime(end_date_string, "%Y%m%d").date()
#     current_date = start_date
#     while current_date <= end_date:
#         print("current_date", current_date)
#         current_date += datetime.timedelta(days=1)

if __name__ == '__main__':
    # results = querysql("./sql/signup_user_id.sql", "ANDROID", "20190305")
    # print(sum(1 for _ in results))
    # signup_layers_progress_results = querysql("./sql/signup_layers_progress.sql", "ANDROID", "20190305")
    # for row in signup_layers_progress_results:
    #     print("{} : {} views".format(row.max_layer, row.user_count))
    # generate_report("ANDROID", "20190409", "20190411")
    # generate_report("IOS", "20190305", "20190312")

    my_app_id = '579011819262592'
    my_app_secret = '510f69548ee4b16210dc43dc2f2da641'
    my_access_token = 'EAAIOm7HO0oABAIn0k5cnocVcEhEdfZA8uIGKYPnMcIKZB2je48UZB3V4Mb9PIJfD55DbrjB4jM8aZBZAfJxQHbdOIobDemmZA4qyozypIxn7REPBuyXVmC1O9PTZCn5lBsMeg8YIJvoYBwYkyMlpL9DWGr3eaW5BVzYSv6kRU5UMFdyCO3aygJu'
    FacebookAdsApi.init(access_token=my_access_token)
    my_account = AdAccount('act_516803115131473')
    fields = [
        'name',
        'objective',
    ]
    params = {
        'effective_status': ['ACTIVE','PAUSED'],
    }
    campaigns = my_account.get_campaigns(
        fields=fields,
        params=params,
    )
    print(campaigns)
