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



############ Below is a class version of these functions
class OptimizedDataFrame(pd.DataFrame):
    def optimize_floats(self) -> pd.DataFrame:
        floats = self.select_dtypes(include=['float64']).columns.tolist()
        self[floats] = self[floats].apply(pd.to_numeric, downcast='float')
        return self
    def optimize_ints(self) -> pd.DataFrame:
        ints = self.select_dtypes(include=['int64']).columns.tolist()
        self[ints] = self[ints].apply(pd.to_numeric, downcast='integer')
        return self
    def optimize_objects(self, datetime_features: List[str]) -> pd.DataFrame:
        for col in self.select_dtypes(include=['object']):
            if col not in datetime_features:
                if not (type(self[col][0])==list):
                    num_unique_values = len(self[col].unique())
                    num_total_values = len(self[col])
                    if float(num_unique_values) / num_total_values < 0.5:
                        # get rid of hyphens
                        try:
                            self[col] = list(map(lambda x: Xlator({"-": " "}).xlat(x), self[col]))
                        except TypeError:
                            pass
                        self[col] = self[col].astype('category')
            else:
                self[col] = pd.to_datetime(self[col])
        return self
    def optimize(self, datetime_features: List[str] = []) -> pd.DataFrame:
        return self.optimize_floats().optimize_ints().optimize_objects(datetime_features)

df = pd.DataFrame({'A': [1, 2, 3], 'B': [4.0, 5.0, 6.0], 'C': ['foo', 'bar', 'baz']})

orig_mem = df.memory_usage().sum()
df = OptimizedDataFrame(df)
_ = df.optimize()     # suppress output
opt_mem = df.memory_usage().sum()
print(f"Memory usage reduced by {round(((orig_mem-opt_mem)/orig_mem)*100, 2)}%")

