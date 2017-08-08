import numpy as np
import pandas as pd

data = pd.read_csv('lagou_update.csv')
# print(data.describe(),'\n')
# print(data['Salary1'].value_counts(),'\n')

data2 = pd.read_csv('lagou_hangzhou.csv')
print(data2['Experience'].value_counts(), '\n')
print(data2['Category'].value_counts())