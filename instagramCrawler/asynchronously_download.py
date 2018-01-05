import asyncio, aiohttp, pymongo
from lxml import html
import hashlib, re, time, os, requests
from multiprocessing import Pool

path = '/media/salesmind/0002C1F9000B55A8/download_pictures'
collection = pymongo.MongoClient(host='127.0.0.1', port=27017)['Falonie']['instagram_image_urls']


def mkdir():
    os.mkdir(path) if not os.path.exists(path) else print('Aleady exists folder {}'.format(path))


def read_mongodb():
    urls = [_['image_url'] for _ in collection.find({})]
    return urls


def crawl_images(url):
    session = requests.session()
    image = session.get(url=url).content
    s = re.split(r'[/.]', url)[-2].encode('utf-8')
    file_name = path + '/' + '{}.jpg'.format(hashlib.sha224(s).hexdigest())
    with open(file_name, 'wb') as f:
        f.write(image)
    # print(image_url, image_id, type(image_url))


async def image_content(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.read()
            return content


async def download_image(url):
    image = await image_content(url)
    s = re.split(r'[/.]', url)[-2].encode('utf-8')
    file_name = path + '/' + '{}.jpg'.format(hashlib.sha224(s).hexdigest())
    with open(file_name, 'wb') as f:
        f.write(image)


def main():
    with Pool() as pool:
        p = pool.map(crawl_images, read_mongodb())


# print(read_mongodb())
# print(hashlib.sha224('https://scontent-nrt1-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/c171.0.682.682/16789204_1787867008204935_9219447566322630656_n.jpg').hesdigest())
# a='https://scontent-nrt1-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/c171.0.682.682/16789204_1787867008204935_9219447566322630656_n.jpg'
# print(re.search('/',a).group())
# print(re.split(r'[/.]',a)[-2])
# print(hashlib.sha224(re.split(r'[/.]',a)[-2].encode('utf-8')).hexdigest())
if __name__ == '__main__':
    mkdir()
    t0 = time.time()
    # urls = read_mongodb()
    # tasks = [download_image(url) for url in urls]
    # loop = asyncio.get_event_loop()
    # results = loop.run_until_complete(asyncio.gather(*tasks))
    # loop.close()
    main()
    print(time.time() - t0)