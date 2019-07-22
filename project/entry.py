#!/usr/bin/env python
# coding=utf-8

from mergefood.entry import Entry as MergeFoodEntry
from mergegarden.entry import Entry as MergeGardenEntry
from idlesheep.entry import Entry as IdleSheepEntry
from mergegardenjrtt.entry import Entry as MergeGardenJrttEntry
from idlesheepjrtt.entry import Entry as IdleSheepJrttEntry
from idlesheepcn.entry import Entry as IdleSheepCnEntry
from idledisaster.entry import Entry as IdleDisasterEntry
from idledisastercn.entry import Entry as IdleDisasterCnEntry

def generate_report_us(option, *parameter):
    # MergeFoodEntry(option, *parameter).generate_report()
    # MergeGardenEntry(option, *parameter).generate_report()
    # MergeGardenJrttEntry(option, *parameter).generate_report()
    # IdleDisasterEntry(option, *parameter).generate_report()
    IdleSheepEntry(option, *parameter).generate_report()
    # IdleSheepCnEntry(option, *parameter).generate_report()
    # IdleSheepJrttEntry(option, *parameter).generate_report()
    # IdleDisasterCnEntry(option, *parameter).generate_report()

def generate_report_cn(option, *parameter):
    # MergeFoodEntry(option, *parameter).generate_report()
    # MergeGardenEntry(option, *parameter).generate_report()
    # MergeGardenJrttEntry(option, *parameter).generate_report()
    # IdleSheepEntry(option, *parameter).generate_report()
    IdleDisasterCnEntry(option, *parameter).generate_report()
    # IdleSheepCnEntry(option, *parameter).generate_report()
    # IdleSheepJrttEntry(option, *parameter).generate_report()
    # IdleDisasterEntry(option, *parameter).generate_report()
