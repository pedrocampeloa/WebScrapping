import pandas as pd

from pprint import pprint

df = pd.read_pickle('dataframe_acoes')

pprint(list(df))