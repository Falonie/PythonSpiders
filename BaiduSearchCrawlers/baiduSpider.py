import requests, re, pandas, xlrd, time, csv, xlsxwriter
from lxml import html
from multiprocessing import Pool
from contextlib import contextmanager

file = '/media/salesmind/Other/cloud_bird/Recruit_51Job_Resume_directors_BSG.xlsx'
file2 = 'F:\GitHub\PythonSpiders\BaiduSpider\测试-官网采集.xlsx'
file3 = '/media/salesmind/Other/baidu_homepage_search/测试-官网采集 _2.xlsx'
file4 = '/media/salesmind/Other/baidu_homepage_search/2017.11.8+官网采集名单_test.xlsx'
file5 = '/media/salesmind/Other/baidu_homepage_search/2017.11.8+官网采集名单_test2.xlsx'
file6='/media/salesmind/Other/baidu_homepage_search/官网_test.xlsx'


class Search(object):
    def baiduSearch(keyword):
        search_result = []
        time.sleep(5)
        url = 'http://www.baidu.com/s?q1={}@V'.format(keyword)
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'}
        response = requests.get(url=url, headers=headers).text
        selector = html.fromstring(response)
        # print(selector.xpath('//div[@class="c-row section main-section last"]/div[1]/table/tr[2]/td/a[1]/text()'))
        try:
            company = selector.xpath('//div[@class="ecl-vmp-card2"]/div[@class="ecl-vmp-contianer c-border"]/'
                                     'div[@class="c-row section header-section"]/h2/text()')
            company2 = re.findall(r'<h2 class="c-gap-bottom">(.*?)</h2>', response)
            link = selector.xpath('//div[@class="c-row section main-section last"]/'
                                  'div[1]/table/tr[2]/td/a[1]/text()')[0]
            link = re.sub('\xa0', '', link)
            # print(company[0],link)
            # print(company2[0],link)
            search_result.append([keyword, company[0], link])
        except:
            for i in selector.xpath('//div[@id="content_left"]/div[position()<7]'):
                company = ''.join(str(i).strip() for i in i.xpath('h3/a/descendant::text()'))
                link = i.xpath('div/div[@class="c-span18 c-span-last"]/div[@class="f13"]/a/text()|'
                               'div[@class="f13"]/a/text()|div/div[2]/p[2]/span[1]/text()')
                if not link:
                    link = ['']
                link = re.sub('\xa0', '', link[0])
                a = [keyword, company, link]
                search_result.append(a)
        finally:
            return search_result


def excel_read(file):
    with xlrd.open_workbook(file) as data:
        table = data.sheets()[0]
        # print(table.ncols)
        for rownum in range(1, table.nrows):
            row = table.row_values(rownum)
            yield row


def company_list(file):
    company = []
    with xlrd.open_workbook(file) as data:
        table = data.sheets()[0]
        # print(table.ncols)
        for rownum in range(1, table.nrows):
            row = table.row_values(rownum)
            # yield row
            company.append(row[0])
            # print(row[0])
        return company


def main_run():
    s = Search
    for i, j in enumerate(excel_read(file=file2), 1):
        time.sleep(3)
        search_result = s.baiduSearch(j[0])
        print(i, search_result, search_result.__len__())
        for i in search_result:
            with open('F:\GitHub\PythonSpiders\BaiduSpider\测试-官网采集_result_sample3.csv', 'a+') as f:
                writer = csv.writer(f)
                writer.writerow(i)
        time.sleep(2)

@contextmanager
def timethis(label):
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        print('{}:{}'.format(label, end - start))

def main():
    with timethis('counting'):
        t0 = time.time()
        s = Search
        with Pool() as pool:
            p = pool.map(s.baiduSearch, company_list(file=file6))
            for i, j in enumerate(p, 1):
                print(i, j)
                with open('/media/salesmind/Other/baidu_homepage_search/官网_search_result.csv', 'a+') as f:
                    writer = csv.writer(f)
                    writer.writerows(j)
        # for i,j in enumerate(company_list(file5),1):
        #     print(i,j[0])
        # print(time.time() - t0)



if __name__ == '__main__':
    main()
    # print(company_list(file=file6))
    # s=Search
    # for i,j in enumerate(company_list(file5),1):
    #     print(i,j[0])
    #     print(s.baiduSearch(j[0]))
    # for i, j in enumerate(excel_read(file5), 1):
    #     print(i, j[0])
    #     s = Search
    #     print(s.baiduSearch(j[0))
    # print(list(excel_read(file4)).__len__())
    # print(company_list(file=file2))
    # time.sleep(3)
    pass