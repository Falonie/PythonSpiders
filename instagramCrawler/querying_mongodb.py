import pymongo,os

collection = pymongo.MongoClient(host='127.0.0.1', port=27017)['Falonie']['instagram_urls']
collection2 = pymongo.MongoClient(host='127.0.0.1', port=27017)['Falonie']['instagram_urls_test3']
for i, j in enumerate(collection2.find({}), 1):
    print(i, j)

# collection.drop()
print(os.path.abspath('.'))