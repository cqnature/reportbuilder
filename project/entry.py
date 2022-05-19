#!/usr/bin/env python
# coding=utf-8

from project.idlegongfu.entry import Entry as IdleGongfuEntry
import sys
print(sys.modules)

# from project.mergefood.entry import Entry as MergeFoodEntry
# from project.mergegarden.entry import Entry as MergeGardenEntry
# from project.idlesheep.entry import Entry as IdleSheepEntry
# from project.mergegardenjrtt.entry import Entry as MergeGardenJrttEntry
# from project.idlesheepjrtt.entry import Entry as IdleSheepJrttEntry
# from project.idlesheepcn.entry import Entry as IdleSheepCnEntry
# from project.idledisaster.entry import Entry as IdleDisasterEntry
# from project.idledisastercn.entry import Entry as IdleDisasterCnEntry
# from project.stickfightcn.entry import Entry as StickFightCnEntry


def generate_report_us(option, *parameter):
    # MergeFoodEntry(option, *parameter).generate_report()
    # MergeGardenEntry(option, *parameter).generate_report()
    # MergeGardenJrttEntry(option, *parameter).generate_report()
    # IdleDisasterEntry(option, *parameter).generate_report()
    # IdleSheepEntry(option, *parameter).generate_report()
    # IdleSheepCnEntry(option, *parameter).generate_report()
    # IdleSheepJrttEntry(option, *parameter).generate_report()
    # IdleDisasterCnEntry(option, *parameter).generate_report()
    print("do nothing")


def generate_report_cn(option, *parameter):
    # MergeFoodEntry(option, *parameter).generate_report()
    # MergeGardenEntry(option, *parameter).generate_report()
    # MergeGardenJrttEntry(option, *parameter).generate_report()
    # IdleSheepEntry(option, *parameter).generate_report()
    # IdleDisasterCnEntry(option, *parameter).generate_report()
    # IdleSheepCnEntry(option, *parameter).generate_report()
    # IdleSheepJrttEntry(option, *parameter).generate_report()
    # IdleDisasterEntry(option, *parameter).generate_report()
    IdleGongfuEntry(option, *parameter).generate_report()
