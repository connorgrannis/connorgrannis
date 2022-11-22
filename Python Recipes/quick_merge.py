import pandas as pd
from functools import reduce

def quick_merge(dfs):
    return reduce(lambda left, right: pd.merge(left, right, left_index=True, right_index=True), dfs)
