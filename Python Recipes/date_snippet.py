import os, sys
from datetime import datetime as dt

def date_snippet():
    return dt.now().strftime("%a %b %d, %Y %I:%M:%S")

header = f"""# -*- coding: utf-8 -*-
\"""
Created on {date_snippet()}

@author: connorgrannis
\"""
"""

print(header)
