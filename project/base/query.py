#!/usr/bin/env python
# coding=utf-8

import os
import json
import requests
import time
from config import *
from date import *
from google.cloud import bigquery
from io import open as ioopen
from ..fbadnw.adnw_examples import *
from ..adscene.generate_report import *

class BaseQuery(object):
    def __init__(self, config):
        self.config = config

    def create_folder(self, *parameter):
        folders = (self.config.cache_folder,) + parameter
        path = '.'
        for x in folders: path = os.path.join(path, str(x))
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError:
                print "Creation of the directory %s failed" % path
            else:
                print "Successfully created the directory %s" % path
        return path

class QuerySql(BaseQuery):
    def __init__(self, config):
        super(QuerySql, self).__init__(config)
        self.commonParms = (self.config.project_config.table_prefix, self.config.platform, self.config.geo_country)

    def create_cache_folder(self, filename, *parameter):
        sql_file = os.path.splitext(os.path.basename(filename))[0]
        parameter = (sql_file,) + parameter
        return self.create_folder(*parameter)

    def get_cache(self, filename, *parameter):
        path = self.create_cache_folder(filename, *parameter)
        print 'try to get cache in file path: ', path
        file_path = os.path.join(path, self.config.file_name)
        if not os.path.exists(file_path):
            return None
        else:
            result = None
            with open(file_path) as file:
                try:
                    file_content = json.load(file)
                    if (len(file_content) > 0):
                        result = []
                        for x in file_content:
                            result.append(bigquery.Row(x['values'], x['field_to_index']))
                except ValueError:
                    result = None
                file.close()
                print 'load cache in file path: ', path
        return result

    def set_cache(self, rows, filename, *parameter):
        path = self.create_cache_folder(filename, *parameter)
        print 'save cache in file path: ', path
        file_path = os.path.join(path, self.config.file_name)
        with open(file_path, mode='w+') as out:
            result = []
            for row in rows:
                result.append({'values': row._xxx_values, 'field_to_index': row._xxx_field_to_index})
            out.write(json.dumps(result))
            out.close()

    def get_result(self, filename, *parameter):
        parameter = self.commonParms + parameter
        result = self.get_cache(filename, *parameter)
        if result != None:
            return result
        filepath = os.path.join(self.config.project_config.sql_path, filename)
        if os.path.exists(filepath) and os.path.isfile(filepath):
            print 'query result for: ', filename
            for k in range(self.config.retry_count):
                try:
                    result = self.do_query(filepath, *parameter)
                except Exception, e:
                    print 'catch exception', e
                if result != None:
                    break
            if result == None:
                print 'query result failed!'
                exit(1)
            self.set_cache(result, filename, *parameter)
            return result
        else:
            print "Make sure you have sql file in path: ", filepath

    def do_query(self, filepath, *parameter):
        client = bigquery.Client()
        with open(filepath) as file:
            content = file.read()
            sql = content.format(*parameter)
            query_job = client.query(sql)
            results = query_job.result()  # Waits for job to complete.
            file.close()
        rows = list(results)
        return rows

class QueryReport(BaseQuery):

    def get_cache(self, report_type, *parameter):
        parameter = (report_type,) + parameter
        path = self.create_folder(*parameter)
        print 'try to get cache in file path: ', path
        file_path = os.path.join(path, self.config.file_name)
        if not os.path.exists(file_path):
            return None
        else:
            result = None
            with ioopen(file_path, encoding="utf-8") as file:
                result = file.read()
                file.close()
                print 'load cache in file path: ', path
        return result

    def set_cache(self, text, report_type, *parameter):
        parameter = (report_type,) + parameter
        path = self.create_folder(*parameter)
        print 'save cache in file path: ', path
        file_path = os.path.join(path, self.config.file_name)
        with ioopen(file_path, mode='w+', encoding="utf-8") as out:
            out.write(text)
            out.close()

    def get_daily_result(self, *parameter):
        return self.get_result('daily_report', *parameter)

    def get_partners_daily_result(self, *parameter):
        return self.get_result("partners_by_date_report", *parameter)

    def get_result(self, report_type, *parameter):
        parameter = (self.config.project_config.appsflyer_api_token,) + parameter
        folders = (self.config.project_config.project_name, self.config.platform) + parameter
        result = self.get_cache(report_type, *folders)
        if result != None:
            return result
        print 'query result for: ', report_type
        for k in range(self.config.retry_count):
            try:
                result = self.do_query(report_type, *parameter)
            except Exception, e:
                print 'catch exception', e
            if result != None:
                break
        if result == None:
            print 'query result failed!'
            return result
        self.set_cache(result, report_type, *folders)
        return result

    def do_query(self, report_type, *parameter):
        params = {
            'api_token': parameter[0],
            'from': Date(parameter[1]).formatymd(),
            'to': Date(parameter[2]).formatymd(),
            'timezone': 'America/Los_Angeles'
        }
        request_url = 'https://hq.appsflyer.com/export/{}/{}/v5'.format(self.config.project_config.app_id, report_type)
        res = requests.request('GET', request_url, params=params)
        time.sleep(60)
        if res.status_code != 200:
            if res.status_code == 404:
                raise RuntimeError('There is a problem with the request URL. Make sure that it is correct')
            else:
                raise RuntimeError('There was a problem retrieving data: ', res.text)
        else:
            return res.text

class QueryAds(BaseQuery):

    def get_cache(self, *parameter):
        path = self.create_folder(*parameter)
        print 'try to get cache in file path: ', path
        file_path = os.path.join(path, self.config.file_name)
        if not os.path.exists(file_path):
            return None
        else:
            result = None
            with open(file_path) as file:
                result = file.read()
                file.close()
                print 'load cache in file path: ', path
        return result

    def set_cache(self, text, *parameter):
        path = self.create_folder(*parameter)
        print 'save cache in file path: ', path
        file_path = os.path.join(path, self.config.file_name)
        with open(file_path, mode='w+') as out:
            out.write(text)
            out.close()

    def get_result(self, *parameter):
        folder = (self.config.project_config.fb_app_id, self.config.platform) + parameter
        result = self.get_cache(*folder)
        if result != None:
            content = json.loads(result)
            return content['data'][0]['results']
        for k in range(self.config.retry_count):
            try:
                result = self.do_query(*parameter)
                if result != None:
                    break
            except Exception, e:
                print(e.message)
                """Waiting 60 seconds if first async request fails, because clustering too many requests
                in our backend will slow your process of fetching results."""
                sleep(60)
                continue
        if result == None:
            print 'query result failed!'
            exit(1)
        self.set_cache(result, *folder)
        content = json.loads(result)
        return content['data'][0]['results']

    def do_query(self, *parameter):
        return run_async_request_for_result(self.config.project_config.fb_app_id, self.config.project_config.fb_access_token, self.config.platform.lower(), parameter[0], parameter[1])

class QueryAdScene(BaseQuery):

    def get_cache(self, *parameter):
        path = self.create_folder(*parameter)
        print 'try to get cache in file path: ', path
        file_path = os.path.join(path, self.config.file_name)
        if not os.path.exists(file_path):
            return None
        else:
            result = None
            with open(file_path) as file:
                result = file.read()
                file.close()
                print 'load cache in file path: ', path
        return result

    def set_cache(self, text, *parameter):
        path = self.create_folder(*parameter)
        print 'save cache in file path: ', path
        file_path = os.path.join(path, self.config.file_name)
        with open(file_path, mode='w+') as out:
            out.write(text)
            out.close()

    def get_result(self, *parameter):
        folder = ('admob', self.config.project_config.project_name, self.config.platform) + parameter
        result = self.get_cache(*folder)
        if result != None:
            content = json.loads(result)
            return content['rows'][0]
        for k in range(self.config.retry_count):
            try:
                result = self.do_query(*parameter)
                if result != None:
                    break
            except Exception, e:
                print(e.message)
                """Waiting 60 seconds if first async request fails, because clustering too many requests
                in our backend will slow your process of fetching results."""
                sleep(60)
                continue
        if result == None:
            print 'query result failed!'
            exit(1)
        self.set_cache(result, *folder)
        content = json.loads(result)
        return content['rows'][0]

    def do_query(self, *parameter):
        return generate_report(self.config.project_config.admob_app_id, self.config.platform, parameter[0], parameter[1])
