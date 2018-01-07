import requests, os, asyncio, aiohttp, pymongo, re, hashlib, time
from lxml import html
from pprint import pprint

url = 'https://www.instagram.com/graphql/query/?query_id=17888483320059182&variables=%7B%22id%22%3A%2222543622%22%2C%22first%22%3A12%2C%22after%22%3A%22AQCMyvT5ap6JKsqJoNynwx7tFaAi11Dhy-sXKJKRN2O2nIZ8HvRXMiGfUmMwxzzMuOcNTDxB04G1M8Vok2IvhQQhjtGriqmn7hBsyzIVEo2bqQ%22%7D'
# path = '/media/salesmind/0002C1F9000B55A8/download_pictures'
path = 'D:\download_pictures'
collection = pymongo.MongoClient(host='127.0.0.1', port=27017)['Falonie']['instagram_urls_test3']
session = requests.session()
sema = asyncio.Semaphore(3)


def create_folder():
    os.mkdir(path) if not os.path.exists(path) else print('Aleady exists folder {}'.format(path))


def read_mongodb():
    urls = [_['image_url'] for _ in collection.find({})]
    return urls


async def image_content(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.content.read()

            return content


async def download_image(url):
    image = await image_content(url)
    s = re.split(r'[/.]', url)[-2].encode('utf-8')
    file_name = os.path.join(path, '{}.jpg'.format(hashlib.sha224(s).hexdigest()))
    with open(file_name, 'wb') as f:
        f.write(image)


async def download_image_(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.read()
            await asyncio.sleep(1)
            print(content)
            # print(await response.text())
            # image = await content
            # s = re.split(r'[/.]', url)[-2].encode('utf-8')
            # file_name = os.path.join(path, '{}.jpg'.format(hashlib.sha224(s).hexdigest()))
            # with open(file_name, 'wb') as f:
            #     f.write(image)


def main():
    t0 = time.time()
    create_folder()
    urls = read_mongodb()
    # tasks = [download_image(url) for url in urls]
    tasks = [download_image_(url) for url in urls]
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()
    print(time.time() - t0)


if __name__ == '__main__':
    t0 = time.time()
    # create_folder()
    # urls = read_mongodb()
    # url1 = 'https://scontent-nrt1-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/c0.124.1080.1080/26066692_349677568834014_7416964411983659008_n.jpg'
    # url2 = 'https://scontent-nrt1-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/25009074_153564655285942_2398760361760129024_n.jpg'
    url1 = 'https://api.github.com/events'
    url2 = 'http://www.jianshu.com/p/cd14482184a6'
    # urls = [url1, url2]
    tasks=[download_image_(url1),download_image_(url2)]
    # tasks = [download_image(url) for url in urls]
    # tasks = [download_image_(url) for url in urls]
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()
    print(time.time()-t0)
    pass