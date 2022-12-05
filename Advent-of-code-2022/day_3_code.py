#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 10:26:02 2022

@author: connorgrannis
"""


import sys, string
from functools import reduce
sys.path.append("/Users/connorgrannis/Documents/Programming/AoC_2022")
from aoctool import input_scraper

hints = list(map(lambda x: x.strip(), input_scraper("day_3_input.txt")))

# %% Task 1: find the sum of the priorities

def split_in_half(rucksack):
    half = int(len(rucksack)/2)
    return tuple([rucksack[:half], rucksack[half:]])

def find_duplicate(rucksack):
    comp_a, comp_b = split_in_half(rucksack)
    return list(set(comp_a).intersection(comp_b))[0]

def find_priority(duplicate):
    points = {}
    points.update(dict(zip(string.ascii_lowercase, range(1 ,len(string.ascii_lowercase)+1 ))))
    points.update(dict(zip(string.ascii_uppercase, range(27,len(string.ascii_uppercase)+27))))
    return points[duplicate]

answer_1 = sum(list(map(lambda hint: find_priority(find_duplicate(hint)), hints)))
print(answer_1)

# %% Task 2: find the item type that is common between all 3 elves in a group
# find the sum of each group's priority

def form_groups():
    return [hints[i:i+3] for i in range(0, len(hints), 3)]

def find_common(group):
    # set(groups[0][0]).intersection(groups[0][1]).intersection(groups[0][2])
    return list(reduce(lambda x, y: set(x).intersection(y), group))[0]

# %%
groups = form_groups()
answer_2 = sum(list(map(lambda group: find_priority(find_common(group)), groups)))
print(answer_2)
