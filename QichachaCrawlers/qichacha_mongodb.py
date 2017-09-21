import pymongo, re, csv
import pandas as pd

collection = pymongo.MongoClient(host='localhost', port=27017)['employee']['qichacha_guangzhoushareholders1']
# for i, j in enumerate(collection.find({}), 1):
#     print(i, j)

# collection.remove({'company': '上海寿全斋电子商务有限公司'})
# collection.drop()

with open('/media/salesmind/Other/MongoDB_files/e签宝股东.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        # print(row)
        # print(row[0], str(row[1]).split(','))
        with open('/media/salesmind/Other/MongoDB_files/e签宝股东_new.csv', 'a+') as f2:
            writer = csv.writer(f2)
            writer.writerow((str(row[1]).split(',')))