import pandas as pd
import re,csv

data=pd.read_csv('lagou_update.csv')
#This file is intended to split the column 'Salary' into 'Salary1' and 'Salary2'.
#拆分Salary列为工资相对较低的列'Salary1'和相对较高的列'Salary2'

with open('Salary1.txt', 'w+',encoding='utf-8') as f,open('Salary2.txt', 'w+',encoding='utf-8') as f2:
    for line in data['Salary']:
        Salary1 = re.split(r'[-,以上]', line)[0]
        Salary2 = re.split(r'[-,以上]', line)[1]
        f.write(Salary1 + '\n')
        f2.write(Salary2 + '\n')
        print(Salary1, Salary2)