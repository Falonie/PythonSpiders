import requests, re, time, random, pymongo
from selenium import webdriver
from lxml import html
from multiprocessing import Pool

collection = pymongo.MongoClient(host='localhost', port=27017)['Falonie']['Recruit_51Job_Resume_shenzhen_update2']
header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
cookies = [{'secure': False, 'name': 'LangType', 'httpOnly': True, 'value': 'Lang=&Flag=1', 'expiry': 1513993375.509251, 'domain': 'ehire.51job.com', 'path': '/'}, {'secure': False, 'name': 'RememberLoginInfo', 'httpOnly': True, 'value': 'member_name=E2BF04DB6CCD2D50FAD638DD50DCF144&user_name=E2BF04DB6CCD2D50FAD638DD50DCF144', 'expiry': 1542937363.737393, 'domain': 'ehire.51job.com', 'path': '/'}, {'secure': False, 'name': 'EhireGuid', 'httpOnly': True, 'value': 'e58887defa2a414291dd938c05207bbb', 'expiry': 1826934153.696084, 'domain': 'ehire.51job.com', 'path': '/'}, {'secure': False, 'name': 'HRUSERINFO', 'value': 'CtmID=2585839&DBID=3&MType=02&HRUID=2965014&UserAUTHORITY=1100111011&IsCtmLevle=1&UserName=%e8%b6%85%e4%b9%90%e5%81%a5%e5%ba%b7&IsStandard=0&LoginTime=11%2f23%2f2017+09%3a42%3a39&ExpireTime=11%2f23%2f2017+09%3a52%3a39&CtmAuthen=0000011000000001000110010000000011100001&BIsAgreed=true&IsResetPwd=0&CtmLiscense=2&AccessKey=49937c0e04700236', 'httpOnly': True, 'domain': 'ehire.51job.com', 'path': '/'}, {'secure': False, 'name': 'ASP.NET_SessionId', 'value': 'gelgilqizcqv4qodzqckzo5c', 'httpOnly': True, 'domain': 'ehire.51job.com', 'path': '/'}, {'secure': False, 'name': 'AccessKey', 'httpOnly': True, 'value': 'dff30248dfa24a0', 'expiry': 1511487763.737355, 'domain': 'ehire.51job.com', 'path': '/'}]

def obtain_pagesource():
    driver = webdriver.Chrome(executable_path='/media/salesmind/Other/Softwares/chromedriver')
    driver.get('https://ehire.51job.com/')
    for cookie in cookies:
        driver.add_cookie(cookie)
    time.sleep(1)
    driver.get('https://ehire.51job.com/Navigate.aspx?ShowTips=11&PwdComplexity=')
    driver.find_element_by_link_text('搜索简历').click()
    time.sleep(1)
    # driver.find_element_by_id('search_keywod_txt').send_keys('VP  CIO CEO CSO 副总裁 副总经理 市场总监 客户总监 运营招商总监 全国区域总监 营销总监 拓展总监')
    driver.find_element_by_id('search_keywod_txt').send_keys('SAP')
    time.sleep(1)
    # driver.find_element_by_id("search_area_txt").send_keys('深圳')
    # driver.find_element_by_xpath('//*[@id="search_area_txt"]').send_keys('深圳')
    time.sleep(1)
    driver.find_element_by_id('search_keyword_anykey').click()
    time.sleep(4)
    driver.find_element_by_id('search_submit').click()
    time.sleep(1)
    # page_num,page_total=driver.find_element_by_xpath('//li[@class="Search_num-set"]/span').text.split('/')
    page_num, page_total = 1, 100
    # driver.find_element_by_xpath('//*[@id="pagerBottomNew_nextButton"]').click()
    time.sleep(2)
    print(page_num, page_total)
    # print(driver.page_source)
    while page_num < page_total:
        print(page_num, page_total)
        yield driver.page_source
        time.sleep(10)
        driver.find_element_by_xpath('//*[@id="pagerBottomNew_nextButton"]').click()
        # page_num += 1
        # if page_num >= 26:
        #     yield driver.page_source


def urls(page_source):
    # r = requests.post(url=url, data=data, headers=header, cookies=cookie).text
    selector = html.fromstring(page_source)
    path = selector.xpath(
        '//div[@class="Common_list-table"]/table/tbody/tr[@class="inbox_tr1"]/td[@class="Common_list_table-id-text"]/span/a/@href|'
        '//div[@class="Common_list-table"]/table/tbody/tr[@class="inbox_tr2"]/td[@class="Common_list_table-id-text"]/span/a/@href')
    url_list = ['http://ehire.51job.com/{}'.format(href) for href in path]
    return url_list


def parse_url(url):
    session = requests.session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])
    # response = requests.get(url=url, headers=header).text
    response = session.get(url=url, headers=header).text
    sel = html.fromstring(response)
    try:
        a = sel.xpath('//*[@id="divInfo"]/td/table[4]/tr[2]/td/table/tr[1]/td/table/tbody/tr[1]/td[2]/span[1]/text()')[0]
        for i in sel.xpath('//*[@id="divInfo"]/td/table[4]/tr[2]/td/table/tr[1]'):
            update_time = sel.xpath('//*[@id="lblResumeUpdateTime"]/descendant::text()')
            update_time = ''.join(str(i).strip() for i in update_time)
            time = i.xpath('td/table/tbody/tr[1]/td[1]/text()')[0]
            company = i.xpath('td/table/tbody/tr[1]/td[2]/span[1]/text()')[0]
            company = re.sub(r'[#→star←end]', '', str(company))
            period = ''.join(str(i).strip() for i in i.xpath('td/table/tbody/tr[1]/td[2]/span[2]/text()'))
            period = re.sub(r'[\n ]', '', period)
            try:
                industry = i.xpath('td/table/tbody/tr[2]/td[2]/descendant::text()')[0]
                industry = re.sub(r'[#→star←end]', '', str(industry))
            except Exception:
                industry = 'N/A'
            # industry = re.sub(r'[#→star←end]', '', industry)
            text = i.xpath('td/table/tbody/tr[2]/td[2]/descendant::text()')
            try:
                scale = text[2]
            except Exception:
                scale = ''
            try:
                nature = text[4]
            except Exception:
                nature = ''
            position = i.xpath('td/table/tbody/tr[3]/descendant::text()')
            position = re.sub(r'[#→star←end]', '', ''.join(str(i).strip() for i in position))
            description = ''.join(
                str(i).strip() for i in i.xpath('td/table/tbody/tr[4]/descendant::text()'))
            # print(a, company, period, industry, description)
            ID = re.findall('<title>\s*(.*?)\s*</title>', response)[0]
            if 'SAP' in description:
                return {'ID': ID, 'update_time': update_time, 'time': time, 'company': company, 'period': period,
                        'industry': industry, 'scale': scale, 'nature': nature, 'position': position,
                        'description': description}
            # else:
            #     return
    except Exception:
        for i in sel.xpath('//*[@id="divInfo"]/td/table[3]/tr[2]/td/table/tr[1]'):
            update_time = sel.xpath('//*[@id="lblResumeUpdateTime"]/descendant::text()')
            update_time = ''.join(str(i).strip() for i in update_time)
            try:
                time = i.xpath('td/table/tbody/tr[1]/td[1]/text()')[0]
            except Exception:
                time = 'N/A'
            try:
                company = i.xpath('td/table/tbody/tr[1]/td[2]/span[1]/text()')[0]
                company = re.sub(r'[#→star←end]', '', str(company))
            except Exception:
                company = 'N/A'
            period = ''.join(str(i).strip() for i in i.xpath('td/table/tbody/tr[1]/td[2]/span[2]/text()'))
            period = re.sub(r'[\n ]', '', period)
            try:
                industry = i.xpath('td/table/tbody/tr[2]/td[2]/descendant::text()')[0]
                industry = re.sub(r'[#→star←end]', '', str(industry))
            except Exception:
                industry = 'N/A'
            # industry = re.sub(r'[#→star←end]', '', industry)
            # recruit['test']=i.xpath('td/table/tbody/tr[2]/td[2]/descendant::text()').extract()
            text = i.xpath('td/table/tbody/tr[2]/td[2]/descendant::text()')
            try:
                scale = text[2]
            except Exception:
                scale = ''
            try:
                nature = text[4]
            except Exception:
                nature = ''
            position = i.xpath('td/table/tbody/tr[3]/descendant::text()')
            position = re.sub(r'[#→star←end]', '', ''.join(str(i).strip() for i in position))
            description = ''.join(
                str(i).strip() for i in i.xpath('td/table/tbody/tr[4]/descendant::text()'))
            ID = re.findall('<title>\s*(.*?)\s*</title>', response)[0]
            # print(a, company, period, industry, description)
            if 'SAP' in description:
                return {'ID': ID, 'update_time': update_time, 'time': time, 'company': company, 'period': period,
                        'industry': industry, 'scale': scale, 'nature': nature, 'position': position,
                        'description': description}
            # else:
            #     return


def main():
    t0 = time.time()
    with Pool() as pool:
        p = pool.map(parse_url, urls(page_source=obtain_pagesource()))
        for i, j in enumerate(p, 1):
            # j.update(pd.Series(1, index=list(range(i, i + 1))))
            print(i, j, type(j))
            try:
                collection.insert_one(j)
            except Exception as e:
                print(e)
            # collection.insert_many(p)
    print(time.time() - t0)


def manage():
    for i, _ in enumerate(obtain_pagesource(), 1):
        print('page {}'.format(i))
        t0 = time.time()
        with Pool() as pool:
            p = pool.map(parse_url, urls(page_source=_))
            # print(p, len(p), type(p))
            for i, j in enumerate(p, 1):
                print(i, j, type(j))
                try:
                    collection.insert_one(j)
                except Exception as e:
                    print(e)
            # collection.insert_many(p)
        print(time.time() - t0)
    time.sleep(10)


if __name__ == '__main__':
    # print(urls(page_source=driver.page_source))
    manage()