import csv,xlrd
import numpy as np

a=['奴隶社会', '', '', '']
b=['非洲', '亚洲', '', '欧洲']
c=['', '', '古印度', '']

# for i in a:
#     for j in b:
#         for k in c:
#             print(i,j,k)
file1 = '/media/salesmind/0002C1F9000B55A8/interview/history.csv'
file2 = 'history2.csv'
file3 = 'history.xlsx'
def read_csv():
    with open(file1, 'r', newline='') as f:
        reader = csv.reader(f)
        list=[]
        # reader=csv.DictReader(f)
        for row in reader:
            # print(row)
            list.append(row)
        # print(list)
        return list
        # pass
# print(read_csv())
d=np.array(read_csv())
print(d)
print()
# print(d[2][0])
print(d.transpose())
print()
# print(d)

with xlrd.open_workbook(file3) as data:
    table = data.sheets()[0]
    ncols = table.ncols
    colnames = table.row_values(0)
    list = []
    for colnum in range(0, ncols):
        col = table.col_values(colnum)
        # for col2 in col:
        # print(col)
        # list.append(col)
    # print(list)