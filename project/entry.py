#!/usr/bin/env python
# coding=utf-8

from mergefood.entry import Entry as MergeFoodEntry
from mergegarden.entry import Entry as MergeGardenEntry
from idlesheep.entry import Entry as IdleSheepEntry
from mergegardenjrtt.entry import Entry as MergeGardenJrttEntry
from idlesheepjrtt.entry import Entry as IdleSheepJrttEntry
from idlesheepcn.entry import Entry as IdleSheepCnEntry

def generate_report(option, *parameter):
    # MergeFoodEntry(option, *parameter).generate_report()
    # MergeGardenEntry(option, *parameter).generate_report()
    # MergeGardenJrttEntry(option, *parameter).generate_report()
    # IdleSheepEntry(option, *parameter).generate_report()
    IdleSheepCnEntry(option, *parameter).generate_report()
    # IdleSheepJrttEntry(option, *parameter).generate_report()
