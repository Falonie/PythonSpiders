import pymongo,random,time

db = pymongo.MongoClient(host='localhost', port=27017)['Falonie']
# collection = db['innotree_种子期_filter_duplicates_crawled_result']
collection = db['innotree_战略投资_filter_duplicates_crawled_result']
collection_filter_duplicates = db['innotree_成熟期_filter_duplicates']
for i, j in enumerate(collection.find({}), 1):
    print(i,j)
    pass
time_sleep = random.choice(list(range(10, 15)))
print(time_sleep)
# time.sleep(time_sleep)
# collection.drop()
# print(random.choice(list(range(10,15))))