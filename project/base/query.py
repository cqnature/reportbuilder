#!/usr/bin/env python
import os
import json
from config import *
from google.cloud import bigquery

class QuerySql:
    def __init__(self, config):
        self.config = config
        self.commonParms = (self.config.project_config.table_prefix, self.config.platform, self.config.geo_country)

    def create_cache_folder(self, filename, *parameter):
        project_name = self.config.project_config.project_name
        table_prefix = self.config.project_config.table_prefix
        geo_country = self.config.geo_country
        platform = self.config.platform
        sql_file = os.path.splitext(os.path.basename(filename))[0]
        folders = (self.config.cache_folder, sql_file) + parameter
        path = '.'
        for x in folders: path = os.path.join(path, x)
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError:
                print "Creation of the directory %s failed" % path
            else:
                print "Successfully created the directory %s" % path
        return path

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
                    result = self.do_query(filepath)
                except Exception:
                    print 'catch exception'
                if result != None:
                    break
            if result == None:
                print 'query result failed!'
                exit(1)
            self.set_cache(rows, filename, *parameter)
            return rows
        else:
            print "Make sure you have sql file in path: ", filepath

    def do_query(self, filepath):
        client = bigquery.Client()
        with open(filepath) as file:
            content = file.read()
            sql = content.format(*parameter)
            query_job = client.query(sql)
            results = query_job.result()  # Waits for job to complete.
            file.close()
        rows = list(results)
        return rows
