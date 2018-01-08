import requests, time, pymongo, xlrd
from lxml import html
from selenium import webdriver
from multiprocessing import Pool
from pprint import pprint
from innotree_search_text import text

url = 'https://www.innotree.cn/inno/search/ajax/getInstitutionSearchResultV2?query=&areaName=%E5%8C%97%E4%BA%AC%E5%B8%82&rounds=1-2&st=1&ps=10&sInum=1&sEnum=-1&sEdate=-1'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'}
cookies = {
    'Cookie': '_user_identify_=06c73d83-e39f-35cc-99d4-01475a7fcd59; JSESSIONID=aaaqUZqo52kQef6UEa0aw; uID=461384; sID=45990bad645f6f76bf6e38016969fb85; Hm_lvt_37854ae85b75cf05012d4d71db2a355a=1512701031; Hm_lpvt_37854ae85b75cf05012d4d71db2a355a=1512721796; Hm_lvt_ddf0d99bc06024e29662071b7fc5044f=1512701030; Hm_lpvt_ddf0d99bc06024e29662071b7fc5044f=1512721796'}
collection = pymongo.MongoClient(host='localhost', port=27017)['Falonie']['innotree_成熟期']
file = 'innotree_成熟期_filter_duplicates.xlsx'
test_list = [{'logo_url': 'https://innotreelogo.qiniu.innotree.cn/Fk-5x2MdQm61XBMneKzGUVzrMmks', 'product_name': '企加云',
              'product_url': 'https://www.innotree.cn/inno/company/4957871552628651946.html'},
             {'logo_url': 'https://innotreelogo.qiniu.innotree.cn/FqXPsWFyl-m9mUjZiv2zj6VRXFPo',
              'product_name': '富勒FLUX', 'product_url': 'https://www.innotree.cn/inno/company/6354892653699219687.html'},
             {'logo_url': 'https://innotreelogo.qiniu.innotree.cn/Fs8sk6PYMJ5U0jJwrgockE-mDJS1', 'product_name': '唐人医药',
              'product_url': 'https://www.innotree.cn/inno/company/10548078748520937734.html'},
             {'logo_url': 'https://innotreelogo.qiniu.innotree.cn/FnkkWORkkEG0fIF47mMxKNreX_fE', 'product_name': '帛珑',
              'product_url': 'https://www.innotree.cn/inno/company/1183084103595171085.html'},
             {'logo_url': 'https://innotreelogo.qiniu.innotree.cn/FpkSIaay3OBeM91QkCO5riDn2GdE', 'product_name': '盟科医药',
              'product_url': 'https://www.innotree.cn/inno/company/999980423478866118.html'},
             {'logo_url': 'https://innotreelogo.qiniu.innotree.cn/FsR-qnw7jsNvW2pIIiTft-XUAm-3', 'product_name': '云途腾',
              'product_url': 'https://www.innotree.cn/inno/company/10005682308130865808.html'},
             {'logo_url': 'https://innotreelogo.qiniu.innotree.cn/FhrYl_FpoPSW0C0F9cI9CD3z4Njn', 'product_name': '国大药房',
              'product_url': 'https://www.innotree.cn/inno/company/7609729055695446200.html'},
             {'logo_url': 'https://innotreelogo.qiniu.innotree.cn/FuhBlsv64JhgDjYu-FsF3KCOFJjB', 'product_name': '盛开体育',
              'product_url': 'https://www.innotree.cn/inno/company/12044156300577152751.html'},
             {'logo_url': 'https://innotreelogo.qiniu.innotree.cn/FmHq3QMKqq8A7Hek-W-TeZavXdbd',
              'product_name': 'TransferEasy',
              'product_url': 'https://www.innotree.cn/inno/company/4020570908260780691.html'},
             {'logo_url': 'https://innotreelogo.qiniu.innotree.cn/FlpnPzR4dkjqn_JlohHf9g99P-V5',
              'product_name': '青芒果旅行网',
              'product_url': 'https://www.innotree.cn/inno/company/10151547046756713819.html'}]


class Innotree(object):
    def get_pagesource(self):
        driver = webdriver.Chrome(executable_path='D:\Softwares\chromedriver.exe')
        driver.get('https://www.innotree.cn/inno/database/totalDatabase')
        driver.maximize_window()
        driver.find_element_by_id("login_c").click()
        time.sleep(5)
        driver.find_element_by_id("login_username").send_keys('18516630543')
        driver.find_element_by_id("login_pwd").send_keys('413154831')
        time.sleep(20)
        # driver.find_element_by_class_name("inno-form-smt l_reg_submit").click()
        # driver.find_element_by_xpath('//*[@class="inno-form-smt l_reg_submit"]').click()
        driver.get('https://www.innotree.cn/inno/database/totalDatabase')
        # driver.find_element_by_xpath('//div[@class="list01_d01_cen_d list01_d01_cen_d_ov"]/a[@data_name="北京市"]').click()
        driver.find_element_by_xpath('//div/a[@data_name="成熟期"]').click()
        while True:
            yield driver.page_source
            time.sleep(5)
            js = "var q=document.documentElement.scrollTop=100000"
            driver.execute_script(js)
            driver.find_element_by_xpath('//div[@id="compPageDiv"]/a[last()-1]').click()
            time.sleep(5)

    def read_excel(self, file):
        with xlrd.open_workbook(file) as data_:
            table = data_.sheets()[0]
            for rownum in range(0, table.nrows):
                self.row = table.row_values(rownum)
                yield self.row[0]

    def parse_page(self, pagesource):
        positions = ' or '.join(i for i in ['position()={}'.format(i) for i in range(2, 21, 2)])
        selector = html.fromstring(pagesource)
        items = []
        for _ in selector.xpath('//*[@id="compTable"]/tr[{}]'.format(positions)):
            product_name = _.xpath('td[1]/div/a/text()')[0]
            logo_url = _.xpath('td[1]/a/div/img/@src')[0]
            product_url = 'https://www.innotree.cn{}'.format(_.xpath('td[1]/div/a/@xhref')[0])
            item = {'product_name': product_name, 'logo_url': logo_url, 'product_url': product_url}
            items.append(item)
        return items

    def parse_company(self, url):
        collection = pymongo.MongoClient(host='localhost', port=27017)['Falonie']['innotree_成熟期_filter_duplicates_crawled_result']
        selector = html.fromstring(requests.get(url=url, headers=headers, cookies=cookies).text)
        item_dict = {}
        for _ in selector.xpath('//div[@class="de_170822_d01_d"]/table'):
            title = _.xpath('tr/td[position()=1 or position()=3]/span/text()')
            text = _.xpath('tr/td[position()=2 or position()=4]/span/text()')
            item_dict.update({k: v for k, v in zip(title, text)})
        for _ in selector.xpath('//div[@class="mech_170525_nav"]/table/tr/td[2]/div'):
            province = _.xpath('a[1]/text()')
            province = ''.join(str(i).strip() for i in province)
            homepage = _.xpath('a[2]/text()')
            homepage = ''.join(str(i).strip() for i in homepage)
            item_dict.update({'province': province, 'homepage': homepage})
        logo_url = selector.xpath('//div[@class="mech_170525_nav"]/table/tr/td[1]/img/@src')
        logo_url = ''.join(str(i).strip() for i in logo_url)
        product = selector.xpath('//h3[@class="mech_170525_nav_h3"]/descendant::text()')
        product = ''.join(str(i).strip() for i in product)
        tags = selector.xpath('//div[@class="mech_170525_nav_d01"]/span/a/text()')
        brief_intro = selector.xpath('//div[@class="de_170822_d01_d02"]/descendant::text()')
        brief_intro = ''.join(str(i).strip() for i in brief_intro)
        investment = selector.xpath('//div[@class="de_170822_d01_d03"]/table/tr/td/descendant::text()')
        investment = ''.join(str(i).strip() for i in investment)
        leadership = selector.xpath(
            '//div[@class="de_170822_d01_d05 de_170822_d01_d05_ov"]/table/tr/td[position()>1]/span/text()')
        leadership = ''.join(str(i).strip() for i in leadership)
        item_dict.update({'brief_intro': brief_intro, 'investment': investment, 'leadership': leadership, 'tags': tags,
                          'product': product, 'logo_url': logo_url, 'url': url})
        collection.insert(item_dict)
        return item_dict


def main():
    innotree = Innotree()
    for i, _ in enumerate(innotree.get_pagesource(), 1):
        print('page {}'.format(i))
        time.sleep(2)
        urls = [url.setdefault('product_url', '') for url in innotree.parse_page(pagesource=_)]
        urls_list = [{'url': url} for url in urls]
        try:
            collection.insert_many(urls_list)
        except Exception as e:
            print(e)
        print(urls_list)
        # with Pool() as pool:
        #     p = pool.map(innotree.parse_company, urls)
        #     for i, j in enumerate(p, 1):
        #         print(i, j)
        time.sleep(5)


def main_excel():
    innotree = Innotree()
    for i, j in enumerate(innotree.read_excel(file), 1):
        print(i, innotree.parse_company(j))
        time.sleep(10)


if __name__ == '__main__':
    # innotree = Innotree()
    main_excel()
    # print(get_pagesource())
    # urls=[url.setdefault('product_url', '') for url in innotree.parse_page(text)]
    # print(urls)
    # print([{'url':u for u in urls}])
    # print([{'url':url} for url in urls])
    # print(parse_page(get_pagesource()))
    # for i, j in enumerate(get_pagesource(), 1):
    #     print(i, parse_page(j))
    # print(parse_company('https://www.innotree.cn/inno/company/4957871552628651946.html'))
    # for i, j in enumerate(innotree.read_excel(file), 1):
    #     print(i, j)
    pass