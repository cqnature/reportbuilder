#!/usr/bin/env python
# coding=utf-8

from project.base.query import *


def append_line(report_lines, index, content, appendLine=True):
    if len(report_lines) > index:
        report_lines[index] = report_lines[index] + \
            content if appendLine else content
    else:
        for k in range(len(report_lines), index + 1):
            report_lines.append('')
        report_lines[index] = report_lines[index] + \
            content if appendLine else content


def append_line_list(report_line_list, append_text):
    max_line_count = max(len(t) for t in report_line_list)
    for report_lines in report_line_list:
        for i in range(len(report_lines), max_line_count):
            report_lines.append(append_text)
    result = []
    for i in range(0, max_line_count):
        for report_lines in report_line_list:
            append_line(result, i, report_lines[i])
    return result


def get_firstopen_usercount(querysql: QuerySql, date):
    firstopen_results = querysql.get_result("firstopen_user_id.sql", date)
    firstopen_usercount = sum(1 for _ in firstopen_results)
    return firstopen_usercount


def get_lost_usercount(querysql: QuerySql, start_date, end_date):
    lost_user_ids = querysql.get_result(
        "lost_user_id.sql", start_date, end_date)
    current_lost_usercount = sum(1 for _ in lost_user_ids)
    return current_lost_usercount


def get_retention_usercount(querysql: QuerySql, start_date, end_date):
    retention_user_ids = querysql.get_result(
        "retention_user_id.sql", start_date, end_date)
    current_retention_usercount = sum(1 for _ in retention_user_ids)
    return current_retention_usercount


def get_daily_usercount(querysql: QuerySql, date):
    daily_results = querysql.get_result("daily_user_id.sql", date)
    daily_usercount = sum(1 for _ in daily_results)
    return daily_usercount


def get_iap_revenue_bysql(querysql: QuerySql, date, end_date):
    iap_revenue = querysql.get_result(
        "内购总收入.sql", date, end_date)
    total_revenue = iap_revenue[0].total_revenue
    return total_revenue


def get_iap_summary_bysql(querysql: QuerySql, date, end_date):
    iap_summary_result = querysql.get_result(
        "内购用户和次数.sql", date, end_date)
    iap_summary = iap_summary_result[0]
    return iap_summary
