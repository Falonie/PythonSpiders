from pprint import pprint
import numpy as np
import pandas as pd
import csv, xlrd

a = {"奴隶社会": [{"非洲": []}, {"亚洲": [{"古印度": []}]}, {"欧洲": []}]}
# pprint(a)
file_path = '/media/salesmind/0002C1F9000B55A8/interview/history.csv'
file2 = 'history2.csv'
file3 = 'history2.xlsx'
file_test = '/media/salesmind/0002C1F9000B55A8/interview/newseed_天使_scrapy2.xlsx'
with open(file2, 'r', newline='') as f:
    reader = csv.reader(f)
    # reader=csv.DictReader(f)
    for row_ in reader:
        # print(row)
        pass

# df=pd.read_csv(file2)
# print(df)

print('\n')
with xlrd.open_workbook(file3) as data:
    table = data.sheets()[0]
    for rownum in range(0, table.nrows):
        row_ = table.row_values(rownum)
        # print(row)

print('\n')


def read_excel():
    with xlrd.open_workbook(file_test) as data:
        table = data.sheets()[0]
        ncols = table.ncols
        colnames = table.row_values(0)
        print(colnames)
        list = []
        for rownum in range(1, table.nrows):
            row = table.row_values(rownum)
            # print(row)
            app = {}
            for i in range(len(colnames)):
                app[colnames[i]] = row[0]
            # print(app)
            list.append(app)
        return list


# print(read_excel())
with xlrd.open_workbook(file3) as data:
    table = data.sheets()[0]
    ncols = table.ncols
    colnames = table.row_values(0)
    for colnum in range(0, ncols):
        col = table.col_values(colnum)
        for col2 in col:
            print(col)