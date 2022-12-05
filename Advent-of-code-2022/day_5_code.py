# -*- coding: utf-8 -*-
"""
Created on Mon Dec 05, 2022 09:02:37

@author: connorgrannis
"""

"""
stacks: Last-in, first-out LIFO
queue:  First-in, last-out FIFO
"""


import sys, re
sys.path.append("/Users/connorgrannis/Documents/Programming/AoC_2022")
from aoctool import input_scraper
from collections import deque
import numpy as np
from itertools import compress
# import pandas as pd

# load and format the hints
hints = input_scraper("day_5_input.txt")
orig_stacks = hints[:8]
hints = hints[10:]

# %% clean and format stacks
# right strip the new line character
# DON'T right strip. Want the extra white space at the end
orig_stacks = np.array([i for i in orig_stacks])
# 9 columns
# 8 spaces
# 35 characters
# chunk into 4 character bites: 3 characters + 1 white space
def chunker(row, n=4):
    chunks = [row[i:i+n] for i in range(0, len(row), n)]
    return list(map(str.strip, chunks))


class Xlator(dict):
    """ Pronounced translator. All-in-one multiple-string-substitution class """
    def _make_regex(self):
        """ Build re object based on the keys of the current dictionary """
        return re.compile("|".join(map(re.escape, self.keys(  ))))

    def __call__(self, match):
        """ Handler invoked for each regex match """
        return self[match.group(0)]

    def xlat(self, text):
        """ Translate text, returns the modified text. """
        return self._make_regex(  ).sub(self, text)


def stack_format(row):
    adict = {"[": "", "]": ""}
    xlat = Xlator(adict)
    return list(map(lambda x: xlat.xlat(x), chunker(row)))

frmt_stacks = np.array(list(map(stack_format, orig_stacks))).T
# filter out Nones
stack_filter = list(map(lambda x: x != "", frmt_stacks))
frmt_stacks = [list(compress(frmt_stacks[idx], stack_filter[idx])) for idx in range(len(frmt_stacks))]
# create empty stacks
stacks = {idx: deque() for idx in range(1,len(frmt_stacks)+1)}

def populate_stacks(idx):
    stacks[idx+1].extend(frmt_stacks[idx])

_ = list(map(populate_stacks, list(range(len(frmt_stacks)))))

# reverse the stacks
def reverse_stack(stack_idx):
    stacks[stack_idx] = deque(reversed(stacks[stack_idx]))

list(map(reverse_stack, range(1, len(stacks)+1)))
# print(stacks)

# %% clean hints
hints = list(map(lambda x: x.strip(), hints))

# %% Task 1: After the rearrangement procedure completes, what crate ends up on top of each stack?
def extract_instructions(hint):
    return list(map(int, hint.split()[1::2]))

def make_a_move(hint):
    amount, start, stop = extract_instructions(hint)
    for i in range(amount):
        crate = stacks[start].pop()
        stacks[stop].append(crate)
    return

_ = list(map(make_a_move, hints))

answer_1 = ''.join([stacks[i][-1] for i in stacks.keys()])
print(answer_1)

# %% Task 2: ah! Multiple crates get moved at the same time
# After the rearrangement procedure completes, what crate ends up on top of each stack?

def move_multiple_crates_at_once(hint):
    amount, start, stop = extract_instructions(hint)
    temp_stack = []
    for i in range(amount):
        crate = stacks[start].pop()
        temp_stack.append(crate)
    stacks[stop].extend(list(reversed(temp_stack)))
    return

_ = list(map(move_multiple_crates_at_once, hints))

answer_2 = ''.join([stacks[i][-1] for i in stacks.keys()])
print(answer_2)
