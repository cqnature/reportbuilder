#!/usr/bin/env python
# coding=utf-8

from mergefood.entry import Entry as MergeFoodEntry
from mergegarden.entry import Entry as MergeGardenEntry
from idlesheep.entry import Entry as IdleSheepEntry

def generate_report(option, *parameter):
    MergeFoodEntry(option, *parameter).generate_report()
    # MergeGardenEntry(option, *parameter).generate_report()
    # IdleSheepEntry(option, *parameter).generate_report()
