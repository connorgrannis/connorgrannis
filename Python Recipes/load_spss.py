import pyreadstat

def open_spss(filename):
    df, _ = pyreadstat.read_sav(filename)
    return df

