#!/usr/bin/env python
# coding=utf-8

from query import *

def append_line(report_lines, index, content, appendLine = True):
    if len(report_lines) > index:
        report_lines[index] = report_lines[index] + content if appendLine else content
    else:
        for k in range(len(report_lines), index + 1):
            report_lines.append('')
        report_lines[index] = report_lines[index] + content if appendLine else content

def get_firstopen_usercount(querysql, date):
    firstopen_results = querysql.get_result("firstopen_user_id.sql", date)
    firstopen_usercount = sum(1 for _ in firstopen_results)
    return firstopen_usercount

def get_lost_usercount(querysql, start_date, end_date):
    lost_user_ids = querysql.get_result("lost_user_id.sql", start_date, end_date)
    current_lost_usercount = sum(1 for _ in lost_user_ids)
    return current_lost_usercount

def get_retention_usercount(querysql, start_date, end_date):
    retention_user_ids = querysql.get_result("retention_user_id.sql", start_date, end_date)
    current_retention_usercount = sum(1 for _ in retention_user_ids)
    return current_retention_usercount
