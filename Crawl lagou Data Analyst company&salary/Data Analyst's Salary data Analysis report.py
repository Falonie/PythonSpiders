import numpy as np
import pandas as pd

data=pd.read_csv('lagou_update.csv')
print(data.describe(),'\n')

#print(data['Salary1'].value_counts(),'\n')