import pymongo,xlrd


file2 = 'zdao_IT_filter_duplicates.xlsx'
db=pymongo.MongoClient(host='localhost', port=27017)['Falonie']
collection = db['zdao_董事_filter_duplicates_crawled_result']
for i, j in enumerate(collection.find({}), 1):
    # print(i,j)
    pass
def read_excel(file):
    with xlrd.open_workbook(file) as data_:
        table = data_.sheets()[0]
        for rownum in range(0, table.nrows):
            row = table.row_values(rownum)
            yield row[0]

print(list(read_excel(file2)).__len__())