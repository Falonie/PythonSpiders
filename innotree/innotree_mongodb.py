import pymongo
from pprint import pprint

db = pymongo.MongoClient(host='localhost', port=27017)['Falonie']
collection = db['innotree_早期_filter_duplicates']
collection_filter_duplicates = db['innotree_beijing_成熟期_filter_duplicates']
for i, j in enumerate(collection.find({}), 1):
    print(i,j)
    pass
# collection.drop()
# collection.rename('innotree_beijing_zaoqi')
url_filter_duplicates = set()
for i, _ in enumerate(list(collection.find({})), 1):
    # print(i, _['url'])
    url_filter_duplicates.add(_['url'])
    pass
# print(url_filter_duplicates.__len__())
# url_filter_duplicates_dict = [{'url': url} for url in url_filter_duplicates]
# print(url_filter_duplicates_dict)
# collection_filter_duplicates.insert_many(url_filter_duplicates_dict)

for i, j in enumerate(collection_filter_duplicates.find({}), 1):
    # print(i, j)
    pass

# collection.create_index([('url',pymongo.ASCENDING)])
# collection_filter_duplicates.create_index([('_id',pymongo.ASCENDING)])
# print(collection.)
pprint(list(collection.list_indexes()))
# pprint(list(collection_filter_duplicates.list_indexes()))