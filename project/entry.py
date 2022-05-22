#!/usr/bin/env python
# coding=utf-8

from project.idlegongfu.entry import Entry as IdleGongfuEntry
import sys
print(sys.modules)

# from project.stickfightcn.entry import Entry as StickFightCnEntry


def generate_report_us(option, *parameter):
    print("do nothing")


def generate_report_cn(option, *parameter):
    IdleGongfuEntry(option, *parameter).generate_report()
