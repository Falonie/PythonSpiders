import requests, hashlib, re, time, os, logging, pymongo
from multiprocessing import Pool
from concurrent import futures

# path = '/media/salesmind/0002C1F9000B55A8/download_pictures'
path = 'D:\download_pictures'
collection = pymongo.MongoClient(host='127.0.0.1', port=27017)['Falonie']['instagram_urls_test3']


def log(level, msg, file_name='Instagram.log'):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    # ch = logging.StreamHandler()
    ch = logging.FileHandler(file_name)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(filename)s %(funcName)s %(asctime)s %(name)s %(levelname)s %(levelno)s %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.log(level=level, msg=msg)


class InstagramCrawler(object):
    def create_folder(self):
        os.mkdir(path) if not os.path.exists(path) else print('Aleady exists folder {}'.format(path))

    def read_mongodb(self):
        urls = [_['image_url'] for _ in collection.find({})]
        return urls

    def crawl_images(self, url):
        session = requests.session()
        image = session.get(url=url).content
        s = re.split(r'[/.]', url)[-2].encode('utf-8')
        image_name = '{}.jpg'.format(hashlib.sha224(s).hexdigest())
        file_name = os.path.join(path, image_name)
        with open(file_name, 'wb') as f:
            f.write(image)
            # self.logger.log(level=logging.DEBUG, msg='image {} has been downloaded.'.format(image_name))
            log(level=logging.DEBUG, msg='image {} has been downloaded.'.format(image_name))
            print('image {} has been downloaded.'.format(image_name))


def main():
    instagram = InstagramCrawler()
    instagram.create_folder()
    with Pool() as pool:
        p = pool.map(instagram.crawl_images, instagram.read_mongodb())
    return len(p)


def main_process():
    t0 = time.time()
    instagram = InstagramCrawler()
    instagram.create_folder()
    with futures.ProcessPoolExecutor() as executor:
        res = executor.map(instagram.crawl_images, instagram.read_mongodb())
    log(logging.INFO, msg='time elapse {}s'.format(time.time() - t0))
    return len(list(res))


def main_thread():
    t0 = time.time()
    instagram = InstagramCrawler()
    instagram.create_folder()
    with futures.ThreadPoolExecutor(max_workers=3) as executor:
        res = executor.map(instagram.crawl_images, instagram.read_mongodb())
    log(logging.INFO, msg='time elapse {}s'.format(time.time() - t0))
    return len(list(res))


if __name__ == '__main__':
    print(main_thread())