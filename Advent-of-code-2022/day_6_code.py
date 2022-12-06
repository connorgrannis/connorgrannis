# -*- coding: utf-8 -*-
"""
Created on Tue Dec 06, 2022 07:42:48

@author: connorgrannis
"""
    
import sys
sys.path.append("/Users/connorgrannis/Documents/Programming/AoC_2022")

from aoctool import input_scraper

hints = list(map(lambda x: x.strip(), input_scraper("day_6_input.txt")))[0]

# %% Task 1: How many characters need to be processed before the first start-of-packet marker is detected?
# first chunk of 4 non-duplicate characters
def chunker(row, n=4):
    chunks = [row[i:i+n] for i in range(0, len(row))]
    return list(map(str.strip, chunks))


def find_first_non_repeating_chunk(chunks, n):
    for idx, chunk in enumerate(chunks):
        if len(set(chunk)) != n:
            continue
        else:
            break
    return idx + n

answer_1 = find_first_non_repeating_chunk(chunker(hints), n=4)
print(answer_1)

# %% Find first chunk of 14 non-duplicate characters instead of 4
answer_2 = find_first_non_repeating_chunk(chunker(hints, 14), n=14)
print(answer_2)
