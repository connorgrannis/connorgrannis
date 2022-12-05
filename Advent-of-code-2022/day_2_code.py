#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 09:40:29 2022

@author: connorgrannis
"""

import sys
sys.path.append("/Users/connorgrannis/Documents/Programming/AoC_2022")
from aoctool import input_scraper

hints = list(map(lambda x: x.strip(), input_scraper("day_2_input.txt")))

# %% Rules:
"""
Rock     : 1
Paper    : 2
Scissors : 3
         
Loss     : 0
Draw     : 3
Win      : 6

rock beats scissors
scissors beats paper
paper beats rock
"""
# %% Task 1:  what is your total score if everything goes accoring to plan?
decryption_key = {
    "A": ["Rock", 1],
    "B": ["Paper", 2],
    "C": ["Scissors", 3],
    "X": ["Rock", 1],
    "Y": ["Paper", 2],
    "Z": ["Scissors", 3]
    }

def calculate_outcome(moves):
    opponent, me = moves.split()
    # they play rock
    if opponent == "A" and me == "X":
        return 3
    elif opponent == "A" and me == "Y":
        return 6
    elif opponent == "A" and me == "Z":
        return 0
    # they play paper
    if opponent == "B" and me == "X":
        return 0
    elif opponent == "B" and me == "Y":
        return 3
    elif opponent == "B" and me == "Z":
        return 6
    # they play scissors
    if opponent == "C" and me == "X":
        return 6
    elif opponent == "C" and me == "Y":
        return 0
    elif opponent == "C" and me == "Z":
        return 3
    else:
        raise ValueError("Somehow you messed up the input.")

def round_score(moves):
    """ moves are a string like 'A Y' """
    opponent, me = moves.split()
    # points for playing
    play_points = decryption_key[me][1]
    # points for outcome
    outcome_points = calculate_outcome(moves)
    # total points for me for the round
    return play_points + outcome_points

my_points = sum(list(map(round_score, hints)))

# %% Task 2: figure out what you need to play and calculate your total points.
"""
X = lose
Y = draw
Z = win
"""

def strategy(moves):
    opponent, desired_outcome = moves.split()
    if desired_outcome == "X":
        # I need to lose
        if opponent == "A":
            return "C"
        elif opponent == "B":
            return "A"
        elif opponent == "C":
            return "B"
    elif desired_outcome == "Y":
        # We need to tie
        return opponent
    elif desired_outcome == "Z":
        # I need to win
        if opponent == "A":
            return "B"
        elif opponent == "B":
            return "C"
        elif opponent == "C":
            return "A"

def calculate_outcome_2(moves):
    opponent, desired_outcome = moves.split()
    me = strategy(moves)
    # they play rock
    if opponent == "A" and me == "A":
        return 3
    elif opponent == "A" and me == "B":
        return 6
    elif opponent == "A" and me == "C":
        return 0
    # they play paper
    if opponent == "B" and me == "A":
        return 0
    elif opponent == "B" and me == "B":
        return 3
    elif opponent == "B" and me == "C":
        return 6
    # they play scissors
    if opponent == "C" and me == "A":
        return 6
    elif opponent == "C" and me == "B":
        return 0
    elif opponent == "C" and me == "C":
        return 3
    else:
        raise ValueError("Somehow you messed up the input.")

def round_score(moves):
    """ moves are a string like 'A Y' """
    me = strategy(moves)
    # points for playing
    play_points = decryption_key[me][1]
    # points for outcome
    outcome_points = calculate_outcome_2(moves)
    # total points for me for the round
    return play_points + outcome_points

my_points = sum(list(map(round_score, hints)))
