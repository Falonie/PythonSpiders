import pymongo,xlrd,os

db = pymongo.MongoClient(host='localhost', port=27017)['Falonie']
collection = db['zdao_监事']
collection_filter_duplicates = db['zdao_监事_filter_duplicates']
for i, j in enumerate(collection.find({}), 1):
    # print(i,j)
    pass

# collection.drop()
url_list = []
url_set = set()
for _ in collection.find({}):
    if _['url'] not in url_list:
        url_list.append(_['url'])
    url_set.add(_['url'])
print(url_set.__len__())
print(list(url_set).__len__())
print(url_list.__len__())
# print({i for i in range(1,10)})
# print({i for i in collection.find({})['url']})
print([i['url'] for i in collection.find({})].__len__())
filter_duplicates_set = {i['url'] for i in collection.find({})}  # .__len__()
filter_duplicates_list = [{'url': _} for _ in filter_duplicates_set]
print(filter_duplicates_list.__len__())
# collection_filter_duplicates.insert_many(filter_duplicates_list)
# for i,j in enumerate(collection_filter_duplicates.find({}),1):
#     print(i,j)

# collection_=db['zdao_法人_filter_duplicates_crawled_result']
# for i,_ in enumerate(collection_.find({}),1):
#     print(i,_)

print(os.path.abspath(__file__))