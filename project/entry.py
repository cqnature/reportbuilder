#!/usr/bin/env python
# coding=utf-8

from mergegarden.entry import Entry as MergeGardenEntry

def generate_report(option, *parameter):
    MergeGardenEntry(option, *parameter).generate_report()
