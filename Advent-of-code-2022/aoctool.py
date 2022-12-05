# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 11:41:47 2022

@author: connorgrannis
"""

import os, sys
from datetime import datetime as dt

def date_snippet():
    return dt.now().strftime("%a %b %d, %Y %I:%M:%S")

def input_scraper(filename, how='l'):
    """
    Reads in input for AOC puzzles
    #TODO change to web scrape
    
    Parameters
    ----------
    filename : str
        filename to be read
    
    how : str, optional
        describes how input will be returned, 'l' returns an item per line
        'w' returns a nested list, with lines split by spaces. 
        The default is 'l'.
    
    Returns
    -------
    format_input : list
        returns a list (or nested list) from the input file itemized by line

    """
    
    with open(filename, 'r') as f:
        format_input = f.readlines()
        
    if how == 'l':
        pass
    elif how == 'w':
        format_input = [i.split() for i in format_input]
    else:
        raise ValueError(f"{how} arg not recognized")
    
    return format_input


def dirstruct(path, day):
    """
    Generates file structure for AOC
    
    Parameters
    ----------
    path : str
        path where day dirs will be generated. for WINOS must be passed as 
raw str

    Returns
    -------
    None.

    """
    
    header = f"""# -*- coding: utf-8 -*-
\"""
Created on {date_snippet()}

@author: connorgrannis
\"""
    
import sys
sys.path.append("{path}")

from aoctool import input_scraper

"""
    
    os.chdir(path)
    # make directory
    if not os.path.isdir(f"Day_{day}"):
        os.mkdir(f"Day_{day}")
    # make files
    open(f"./Day_{day}/day_{day}_input.txt", "w").close()
    with open(f"./Day_{day}/day_{day}_code.py", "w") as f:
        f.write(header)

if __name__ == '__main__':
    day = sys.argv[1]
    dirstruct("/Users/connorgrannis/Documents/Programming/AoC_2022", day)
    
    
