#!/usr/bin/env python
# coding=utf-8

import os
import json

if __name__ == '__main__':
    # set proxy config
    commonconfig_path = 'config/config.json'
    if not os.path.exists(commonconfig_path):
        try:
            os.makedirs('config')
        except OSError:
            print "Creation of the directory %s failed" % commonconfig_path
        else:
            print "Successfully created the directory %s" % commonconfig_path
        with open(commonconfig_path, mode='w+') as out:
            proxy_config = {'https_proxy': 'http://127.0.0.1:6152', 'http_proxy': 'http://127.0.0.1:6152', 'all_proxy': 'socks5://127.0.0.1:6153'}
            out.write(json.dumps(proxy_config))
            out.close()
            print "Generate default proxy config, should check it"

    credentials_path = 'credentials'
    if not os.path.exists(credentials_path):
        try:
            os.makedirs(credentials_path)
        except OSError:
            print "Creation of the directory %s failed" % credentials_path
        else:
            print "Successfully created the directory %s" % credentials_path

        print 'Should set credentials from google console: https://console.cloud.google.com/apis/credentials/serviceaccountkey?authuser=0&hl=zh-cn&_ga=2.185422062.-675937386.1541684771'
