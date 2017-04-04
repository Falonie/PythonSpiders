import numpy as np
import pandas as pd
from pandas import Series,DataFrame

data=pd.read_csv('lagou_update.csv')
print(data.describe(),'\n')
