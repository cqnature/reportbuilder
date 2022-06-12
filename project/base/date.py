#!/usr/bin/env python
# coding=utf-8

import pytz
from datetime import timedelta, datetime


class Date:
    def __init__(self, date_string):
        self.date_string = date_string

    def enddate(self, country='United States'):
        timezone = 'America/Los_Angeles'
        if country == 'China' or country == "Taiwan":
            timezone = 'Asia/Shanghai'
        tz = pytz.timezone(timezone)
        end_date = datetime.now(tz) + timedelta(days=-1)
        return end_date.strftime('%Y%m%d')

    def validate(self):
        try:
            datetime.strptime(self.date_string, '%Y%m%d')
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYYMMDD")

    def rangeto(self, end_date_string, containStart=False):
        start_date = datetime.strptime(self.date_string, "%Y%m%d").date()
        if not containStart:
            start_date = start_date + timedelta(days=1)
        end_date = datetime.strptime(
            end_date_string, "%Y%m%d").date() + timedelta(days=1)
        for n in range(int((end_date - start_date).days)):
            yield (start_date + timedelta(n)).strftime("%Y%m%d")

    def adddays(self, days=1):
        new_date = datetime.strptime(
            self.date_string, "%Y%m%d").date() + timedelta(days=days)
        return new_date.strftime("%Y%m%d")

    def formatmd(self):
        date = datetime.strptime(self.date_string, "%Y%m%d").date()
        return date.strftime("%m-%d")

    def formatymd(self):
        date = datetime.strptime(self.date_string, "%Y%m%d").date()
        return date.strftime("%Y-%m-%d")

    def between(self, end_date_string, adddays=1):
        start_date = datetime.strptime(self.date_string, "%Y%m%d").date()
        end_date = datetime.strptime(
            end_date_string, "%Y%m%d").date() + timedelta(days=adddays)
        return int((end_date - start_date).days)
