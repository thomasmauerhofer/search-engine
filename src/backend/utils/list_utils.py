#!/usr/bin/env python3
# encoding: utf-8


def insert_dict_into_list(mlist, mdict, key):
    lo = 0
    hi = len(mlist)

    while lo < hi:
        mid = (lo + hi) // 2
        if mlist[mid][key] > mdict[key]:
            lo = mid + 1
        else:
            hi = mid
    mlist.insert(lo, mdict)
