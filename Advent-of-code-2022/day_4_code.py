#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 09:18:37 2022

@author: connorgrannis
"""
import sys
sys.path.append("/Users/connorgrannis/Documents/Programming/AoC_2022")
from aoctool import input_scraper

hints = list(map(lambda x: x.strip(), input_scraper("day_4_input.txt")))
# print(hints[:10])

# %% Task1: In how many assignment pairs does one range fully contain the other?
def convert_to_range(assignment, inclusive=False):
    start, stop = list(map(int, assignment.split('-')))
    if inclusive:
        return range(start, stop+1)
    else:
        return range(start, stop)


def find_full_overlap(assignment):
    # a.issubset(b)             # a is fully contained in b
    # a.issuperset(b)           # b is fully contained in a
    assignment_a, assignment_b = assignment.split(',')
    assignment_a = convert_to_range(assignment_a, inclusive=True)
    assignment_b = convert_to_range(assignment_b, inclusive=True)
    if set(assignment_a).issubset(assignment_b) | set(assignment_a).issuperset(assignment_b):
        return True
    else:
        return False


answer_1 = sum(list(map(find_full_overlap, hints)))
print(answer_1)

# %% Task 2: find the number of overlapping pairs (not full)
def find_overlap(assignment):
    assignment_a, assignment_b = assignment.split(',')
    assignment_a = convert_to_range(assignment_a, inclusive=True)
    assignment_b = convert_to_range(assignment_b, inclusive=True)
    return set(assignment_a).intersection(assignment_b)

answer_2 = sum(list(map(lambda a: True if len(find_overlap(a)) > 0 else False, hints)))
print(answer_2)
