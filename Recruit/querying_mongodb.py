import pymongo,os

collection = pymongo.MongoClient(host='127.0.0.1', port=27017)['Falonie']['recruit_urls_shenzhen_sales_representative']
collection_filter_duplicates = pymongo.MongoClient(host='127.0.0.1', port=27017)['Falonie']['recruit_urls_shanghai_sales_representative_filter_duplicates']
for i,j in enumerate(collection.find({}),1):
    print(i,j)
    pass

# print(33063/50)
filter_urls={_['url'] for _ in collection.find({})}
filter_urls_list=[{'url':_} for _ in filter_urls]
print(filter_urls_list.__len__())
# print(list(collection.find({'url':'http://jobs.51job.com/shenzhen-ftq/89192371.html?s=01&t=0'})))
# collection_filter_duplicates.insert_many(filter_urls_list)
# print(len(list(collection_filter_duplicates.find({}))))
# collection.drop()
print(os.path.abspath('.'))