import pandas as pd
from typing import List

# Code is mostly taken from https://medium.com/bigdatarepublic/advanced-pandas-optimize-speed-and-memory-a654b53be6c2
# However, it also uses the Xlator class that can be found in the multiple_replacements file.

# NB: Xlator is only looking for hyphens by default. Alter line 36 to look for other characters to replace.

def optimize_floats(df: pd.DataFrame) -> pd.DataFrame:
    """ reduces floats to the lowest number of bits it can """
    floats = df.select_dtypes(include=['float64']).columns.tolist()
    df[floats] = df[floats].apply(pd.to_numeric, downcast='float')
    return df


def optimize_ints(df: pd.DataFrame) -> pd.DataFrame:
    """ reduces integers to the lowest number of bits it can """
    ints = df.select_dtypes(include=['int64']).columns.tolist()
    df[ints] = df[ints].apply(pd.to_numeric, downcast='integer')
    return df


def optimize_objects(df: pd.DataFrame, datetime_features: List[str]) -> pd.DataFrame:
    """ 
    convert dates to datetime and 
    nominal to category if only a few unique categories 
    """
    for col in df.select_dtypes(include=['object']):
        if col not in datetime_features:
            if not (type(df[col][0])==list):
                num_unique_values = len(df[col].unique())
                num_total_values = len(df[col])
                if float(num_unique_values) / num_total_values < 0.5:
                    # get rid of hyphens
                    try:
                        df[col] = list(map(lambda x: Xlator({"-": " "}).xlat(x), df[col]))
                    except TypeError:
                        pass
                    df[col] = df[col].astype('category')
        else:
            df[col] = pd.to_datetime(df[col])
    return df



def optimize(df: pd.DataFrame, datetime_features: List[str] = []):
    return optimize_floats(optimize_ints(optimize_objects(df, datetime_features)))

# this modifies in place, so perform optimization on a copy if you want to retain original
# but this defeats the purpose of memory optimization
_ = optimize(df, ["col_that_is_a_date"])
