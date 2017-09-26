import pandas as pd
import path

data = pd.read_csv('./helpers/datatable.csv')

def lookup(val):
    val = float(val)
    group = data.loc[(val > data['low']) & (val < data['high'])]['desc'].tolist()
    return group[0]