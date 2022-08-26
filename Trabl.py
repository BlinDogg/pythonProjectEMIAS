import pandas as pd
#import os
from io import BytesIO
import numpy
#from datetime import datetime,date
from pandas.io.excel import ExcelWriter


def opener():
    df = pd.read_excel('test.xlsx', sheet_name='Лист 1')
    return df

z = opener()['ФИО']
z = z.drop_duplicates()
z = z.reset_index(drop=True)
print(z)