import pymongo, xlrd, os, csv

db = pymongo.MongoClient(host='localhost', port=27017)['Falonie']
collection = db['zdao_总裁_filter_duplicates_crawled_result']
collection_filter_duplicates = db['zdao_总裁_filter_duplicates']
for i, j in enumerate(collection.find({}), 1):
    # print(i,j)
    pass

# collection.drop()
url_list = []
url_set = set()


def read_excel():
    with xlrd.open_workbook('zdao_总裁_filter_duplicates.xlsx') as data_:
        table = data_.sheets()[0]
        # url_list = [table.row_values(rownum)[0] for rownum in range(0, table.nrows)]
        # return url_list
        crawled_urls = [_['url'] for _ in list(collection.find({}))]
        # for i,rownum in enumerate(range(table.nrows),1):
        #     row = table.row_values(rownum)
        # print(i,row[0])
        for rownum in range(0, table.nrows):
            row = table.row_values(rownum)
            if row[0] not in crawled_urls:
                url_set.add(row[0])
                # print(row)
        return url_set


def write_csv():
    with open('uncrawled_urls.csv', 'a+', newline='') as f:
        writer = csv.writer(f)
        # writer.writerows([read_excel()])
        for row in read_excel():
            writer.writerow((row,))


# for i, _ in enumerate(collection.find({}), 1):
#     print(i, _['url'])
if __name__ == '__main__':
    print(read_excel().__len__())
    # write_csv()
    # print(list(collection.find({})))
    print([_['url'] for _ in list(collection.find({}))].__len__())