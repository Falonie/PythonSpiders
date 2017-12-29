import pymongo,os

collection = pymongo.MongoClient(host='127.0.0.1', port=27017)['Falonie']['recruit_shenzhen_sales_representative']
collection_filter_duplicates = pymongo.MongoClient(host='127.0.0.1', port=27017)['Falonie']['recruit_urls2']
for i,j in enumerate(collection.find({}),1):
    print(i,j)
    pass
# print('0x80'.encode('utf-8').decode('utf-8'))
# collection.drop()
# print((219.0161566734314/(28464-22288))*5400)
# print(list(collection.find({'url':'http://jobs.51job.com/shenzhen/95730969.html?s=01&t=0'})))
# filter_urls={_['url'] for _ in collection.find({})}
# filter_urls_list=[{'url':_} for _ in filter_urls]
# print(filter_urls_list,filter_urls_list.__len__())
# # collection_filter_duplicates.insert_many(filter_urls_list)
# print(len(list(collection_filter_duplicates.find({}))))
# # collection.drop()http://jobs.51job.com/shanghai/95945356.html?s=01&t=0
# print(os.path.abspath('.'))