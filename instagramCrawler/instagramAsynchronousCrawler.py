import requests, os, asyncio, aiohttp
from lxml import html
from pprint import pprint

variable1 = {"id": "22543622", "first": 12,
             "after": "AQArqOBtes-iKFkToFh2LK3pBuvq0_l9FcI_o-Lln6TxR1l2wOxdO43ayLdMEdxZ0A9lt6s6EyEy7JyV9MCkia3DR81iVkdflacH7WhFyebZtA"}
variable2 = {"id": "22543622", "first": 12,
             "after": "AQDPF9i5L0ISISzRhjp8xkoTD0rQWtTyZk3waC8HAN_YNEI3ugz3VFMXxiebUvFbCMT9L_Dx9ulH3EHQAK94fECT9n2UVGd1KryLvyfso-U_zg"}
url = 'https://www.instagram.com/graphql/query/?query_id=17888483320059182&variables=%7B%22id%22%3A%2222543622%22%2C%22first%22%3A12%2C%22after%22%3A%22AQCMyvT5ap6JKsqJoNynwx7tFaAi11Dhy-sXKJKRN2O2nIZ8HvRXMiGfUmMwxzzMuOcNTDxB04G1M8Vok2IvhQQhjtGriqmn7hBsyzIVEo2bqQ%22%7D'
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
cookies = {
    'cookie': 'csrftoken=pcJFqR9OzjuIyvXD5JK9ycRBIv7AKyRA; mid=Wk7gcAAEAAGgKVpMEwCZJGYvQ7o-; ig_vw=1366; ig_pr=1; ig_or=landscape-primary; ig_vh=407; rur=FRC; urlgen="{\"time\": 1515118704\054 \"104.238.151.149\": 20473\054 \"45.77.31.59\": 20473}:1eXHdo:qKzXIoJAjHFgzem61gsNtOgRZ3Y"'}
# pprint(data)
path = '/media/salesmind/0002C1F9000B55A8/download_pictures'

if not os.path.exists(path):
    os.mkdir(path)
else:
    pass
session = requests.session()


async def asynchronously_crawl_images(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            # print(response.text(), type(response.text()))
            content=await response.read()
            return content

if __name__ == '__main__':
    # crawl_images()
    tasks = [asynchronously_crawl_images(url=url)]
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()
    pass
