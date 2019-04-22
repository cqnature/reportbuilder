from adnw_requests import *
from adnw_utils import *
from adnw_response import *
from time import sleep
from datetime import date, datetime
import json

""" Run async request to get request id (no limitations on params),
    then run sync request with request id.
    No max metric and breakdowns per request.
"""
def run_async_request(app_id, access_token, country_code, platform, from_date, to_date):
    builder = ADNWRequestBuilder(app_id, access_token)
    builder.add_metric(Metric.ADNW_REVENUE)
    builder.add_metric(Metric.ADNW_CPM)
    builder.add_metric(Metric.ADNW_IMPRESSION)
    builder.add_metric(Metric.ADNW_REQUEST)
    builder.add_filter(Filter(Breakdown.COUNTRY, FilterOperator.IN, [country_code]))
    builder.add_filter(Filter(Breakdown.PLATFORM, FilterOperator.IN, [platform]))
    builder.add_breakdown(Breakdown.COUNTRY)
    builder.add_breakdown(Breakdown.PLACEMENT)
    builder.set_date_range(datetime.strptime(from_date, "%Y%m%d").date(), datetime.strptime(to_date, "%Y%m%d").date())
    builder.set_limit(MAX_ROW_LIMIT_ASYNC)
    async_request = builder.build_async_request()
    adnw_response = ADNWResponse.get_instance()
    adnw_response.validate_response(async_request)
    query_id = adnw_response.get_query_id(async_request.json())
    print("Successfully get valid query id: " + query_id)
    return query_id

def run_async_request_for_result(app_id, access_token, country_code, platform, from_date, to_date):
    query_id = run_async_request(app_id, access_token, country_code, platform, from_date, to_date)
    """The waiting period here is to make sure the results have been generated on our backend."""
    sleep(10)
    return run_async_request_with_query_ids(app_id, access_token, [query_id])

def run_async_request_with_query_ids(app_id, access_token, query_ids):
    builder = ADNWRequestBuilder(app_id, access_token)
    builder.set_query_ids(query_ids)
    sync_request = builder.build_sync_request_with_query_ids()
    ADNWResponse.get_instance().validate_response(sync_request)
    return json.dumps(sync_request.json())
