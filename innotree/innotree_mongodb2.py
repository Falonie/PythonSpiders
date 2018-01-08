import pymongo

db = pymongo.MongoClient(host='localhost', port=27017)['Falonie']
# collection = db['innotree_beijing_zhongzi_filter_duplicates_crawled_result']
collection = db['innotree_种子期']
collection_filter_duplicates = db['innotree_种子期_filter_duplicates']
for i, j in enumerate(collection.find({}), 1):
    # print(i,j)
    pass
# print(list(collection.find({})).__len__())

url_filter_duplicates = set()
for i, _ in enumerate(collection.find({}), 1):
    # print(i, _['url'])
    url_filter_duplicates.add(_['url'])
print(url_filter_duplicates.__len__())
url_filter_duplicates_set={url['url'] for url in collection.find({})}
url_filter_duplicates_list=[{'url':url} for url in url_filter_duplicates_set]
# collection_filter_duplicates.insert_many(url_filter_duplicates_list)
for i, j in enumerate(collection_filter_duplicates.find({}), 1):
    print(i,j)