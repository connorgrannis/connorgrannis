#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 08:28:04 2022

@author: connorgrannis
"""


with open("day_1_input.txt", "r") as f:
    hints = f.readlines()
    hints = list(map(lambda x: x.strip(), hints))

hints[:10]

# %% Task 1: Find the Elf carrying the most Calories. How many total Calories is that Elf carrying?
def get_all_indicies(haystack, needle):
    return [i for i, x in enumerate(haystack) if x == needle]

def chunk_list(_list, start_point, stop_point):
    return _list[start_point: stop_point]

# %%
indices = get_all_indicies(hints, '')
start_point = 0

elf_load = []
for stop_point in indices:
    elf_load.append(chunk_list(hints, start_point, stop_point))
    start_point = stop_point + 1


# %% get the sum of each elf
elf_sums = []
for elf in elf_load:
    elf_sums.append(sum(list(map(int, elf))))

answer_1 = max(elf_sums)

# %% Task 2: find the total calories carried by top 3 elves
answer_2 = sum(sorted(elf_sums)[-3:])
