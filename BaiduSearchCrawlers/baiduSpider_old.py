import requests, re, pprint, pandas, xlrd, time, csv, xlsxwriter
from lxml import html

url = 'http://www.baidu.com/s?q1={}'.format('蚂蚁金服@V')
url1 = 'https://www.baidu.com/s?ie=utf-8&f=3&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%E4%B8%8A%E6%B5%B7%E9%97%A8%E8%BF%AA%E6%99%BA%E8%83%BD%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%20%40v&oq=%25E4%25B8%258A%25E6%25B5%25B7%25E9%2597%25A8%25E8%25BF%25AA%25E6%2599%25BA%25E8%2583%25BD%25E7%25A7%2591%25E6%258A%2580%25E6%259C%2589%25E9%2599%2590%25E5%2585%25AC%25E5%258F%25B8&rsv_pq=de667e6f00038b9a&rsv_t=6a35ya7FU4CHw242DZ1IeSlpYxzNJBFhdmVRemfkto2JJTwigd98BRYU3nE&rqlang=cn&rsv_enter=1&inputT=2835&rsv_sug3=16&rsv_sug1=13&rsv_sug7=100&rsv_sug2=0&rsv_sug4=2968'
url2 = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd=%E4%B8%8A%E6%B5%B7%E8%BF%AA%E9%97%A8%E6%99%BA%E8%83%BD%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%20%40v&rsv_pq=9b84b6110003280f&rsv_t=4722eaCQd5aL6pZaoZCbu4YL0B1N%2BTyfC4m8t80eIBJ7Ce0geSdt9SnezJk&rqlang=cn&rsv_enter=1&rsv_sug3=16&rsv_sug1=17&rsv_sug7=100&sug=%25E4%25B8%258A%25E6%25B5%25B7%25E9%2597%25A8%25E8%25BF%25AA%25E6%2599%25BA%25E8%2583%25BD%25E7%25A7%2591%25E6%258A%2580%25E6%259C%2589%25E9%2599%2590%25E5%2585%25AC%25E5%258F%25B8%2520%2540v&rsv_n=2&rsv_sug2=0&inputT=16483&rsv_sug4=16483&rsv_sug=1'
url3 = 'https://www.baidu.com/s?ie=utf-8&f=3&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%E6%B5%99%E6%B1%9F%E9%98%BF%E9%87%8C%E5%B7%B4%E5%B7%B4%E5%B0%8F%E9%A2%9D%E8%B4%B7%E6%AC%BE%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%20%40v&oq=%25E6%25B5%2599%25E6%25B1%259F%25E9%2598%25BF%25E9%2587%258C%25E5%25B7%25B4%25E5%25B7%25B4%25E5%25B0%258F%25E9%25A2%259D%25E8%25B4%25B7%25E6%25AC%25BE%25E8%2582%25A1%25E4%25BB%25BD%25E6%259C%2589%25E9%2599%2590%25E5%2585%25AC%25E5%258F%25B8&rsv_pq=db65bc1f00005f7c&rsv_t=c8eemM2qwHnzBOlPNKDLIl2p9NyDVIliw6wMwk5G90hnheWKnj07J14hSCY&rqlang=cn&rsv_enter=1&inputT=2671&rsv_sug3=19&rsv_sug1=18&rsv_sug7=100&rsv_sug2=0&rsv_sug4=2825'
url4 = 'https://www.baidu.com/s?ie=utf-8&f=3&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%E6%B5%99%E6%B1%9F%E5%A4%A9%E7%8C%AB%E6%8A%80%E6%9C%AF%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%20%40v&oq=%25E6%25B5%2599%25E6%25B1%259F%25E5%25A4%25A9%25E7%258C%25AB%25E6%258A%2580%25E6%259C%25AF%25E6%259C%2589%25E9%2599%2590%25E5%2585%25AC%25E5%258F%25B8&rsv_pq=d0f64b0600005732&rsv_t=5ef8NOXZH9gzD%2F0kZc%2B8mlJieA%2FOR5%2FgN6ncFKxrPlEY9%2BiRZ%2BrV0S8L%2BWE&rqlang=cn&rsv_enter=1&inputT=1899&rsv_sug3=20&rsv_sug1=20&rsv_sug7=100&rsv_sug2=0&rsv_sug4=1994'
url5 = 'https://www.baidu.com/s?ie=utf-8&f=3&rsv_bp=1&rsv_idx=1&tn=baidu&wd={}%20%40v&oq=%25E4%25B8%258A%25E6%25B5%25B7%25E9%2597%25A8%25E8%25BF%25AA%25E6%2599%25BA%25E8%2583%25BD%25E7%25A7%2591%25E6%258A%2580%25E6%259C%2589%25E9%2599%2590%25E5%2585%25AC%25E5%258F%25B8&rsv_pq=de667e6f00038b9a&rsv_t=6a35ya7FU4CHw242DZ1IeSlpYxzNJBFhdmVRemfkto2JJTwigd98BRYU3nE&rqlang=cn&rsv_enter=1&inputT=2835&rsv_sug3=16&rsv_sug1=13&rsv_sug7=100&rsv_sug2=0&rsv_sug4=2968'
file = '/media/salesmind/Other/cloud_bird/Recruit_51Job_Resume_directors_BSG.xlsx'
file2 = '/media/salesmind/Other/cloud_bird/测试-官网采集.xlsx'
file3='/media/salesmind/Other/baidu_homepage_search/2017.11.8+官网采集名单_test.xlsx'
file4='/media/salesmind/Other/baidu_homepage_search/2017.11.8+官网采集名单_test2.xlsx'

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


def excel_write(file):
    with xlsxwriter.Workbook('/media/salesmind/Other/PycharmProjects/project_1/Exercise2.xlsx') as workbook:
        worksheet = workbook.add_worksheet('exercise_sheet')
        row = 0;col = 0


if __name__ == '__main__':
    # print(baiduSearch('蚂蚁金服@V'))
    # pprint(baiduSearch('上海门迪智能科技有限公司'))
    # print(list(excel_read(file4)))
    for i,j in enumerate(excel_read(file3),1):
        # print(i,j[0])
        pass
    s = Search
    # print(s.baiduSearch('京东方科技集团股份有限公司'))
    for i, j in enumerate(excel_read(file=file3), 1):
        # print(i, j)
        # data=[i.insert(0,j[0]) for i in baiduSearch(j[0])]
        print(i, s.baiduSearch(j[0]))
        # for i in baiduSearch(j[0]):
        #     with open('/media/salesmind/Other/cloud_bird/测试-官网采集_result_sample.csv', 'a+') as f:
        #         writer = csv.writer(f)
        #         list_ = i
        #         list_.insert(0, j[0])
        #         # list_.extend(j)
        #         writer.writerow(list_)
        #         print(list_)
        # with open('/media/salesmind/Other/cloud_bird/测试-官网采集_result_sample3.csv', 'a+') as f:
        #     writer = csv.writer(f)
        #     writer.writerows(s.baiduSearch(keyword=j[0]))
        # time.sleep(2)
        pass