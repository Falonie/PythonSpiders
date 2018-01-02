import requests, re, pymongo, random, time, logging, xlrd
from lxml import html

collection = pymongo.MongoClient(host='127.0.0.1', port=27017)['Falonie']['company_old_name']
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
cookies = {
    'Cookie': 'acw_tc=AQAAAMObsw/BVAQAo/ycy8Hpwv1w6mmt; PHPSESSID=1nb24s48qbj0sgjtq3956cqob1; UM_distinctid=160972eb254c2-06207728587b3a-3a75045d-100200-160972eb25587a; zg_did=%7B%22did%22%3A%20%22160972eb31a9c8-0a7d813b74ab4a-3a75045d-100200-160972eb31bac8%22%7D; _uab_collina=151436490946871446679795; _umdata=70CF403AFFD707DF5EDBFBB819EB875F91344DDB3127AD82CA1600FEF09F6637DB2299DD733EDDFACD43AD3E795C914C317021820AA4FC33F8C09611486860D7; CNZZDATA1254842228=1727299625-1514363699-%7C1514424974; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201514429208645%2C%22updated%22%3A%201514429638804%2C%22info%22%3A%201514364908322%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%22dad2b2131a760fad57cbbb67ceea827c%22%7D'}
file_path = '/media/salesmind/0002C1F9000B55A8/Ctrip/曾用名核查_1225.xlsx'


def company_list_excel(file_path):
    with xlrd.open_workbook(file_path) as data:
        table = data.sheets()[0]
        for rownum in range(0, table.nrows):
            row = table.row_values(rownum)
            yield row[0]


def check_old_name(name):
    page_num = 1
    items = []
    while page_num < 3:
        # items = []
        url = 'http://www.qichacha.com/search_index?key={name}&ajaxflag=1&p={page}&'.format(name=name, page=page_num)
        session = requests.session()
        r = session.get(url=url, headers=headers, cookies=cookies).text
        selector = html.fromstring(r)
        for _ in selector.xpath('//*[@id="searchlist"]/table/tbody/tr'):
            company_name = _.xpath('td[2]/a/descendant::text()')
            company = ''.join(str(i).strip() for i in company_name)
            company_old_name = _.xpath('td[2]/p[4]/descendant::text()')
            company_old_name = ''.join(str(i).strip() for i in company_old_name)
            item = {'company_input': name, 'company_name': company, 'company_old_name': company_old_name}
            items.append(item)
        page_num += 1
    collection.insert_many(items)
    # print(items)
    return items


def main():
    for _ in company_list_excel(file_path):
        print(check_old_name(_))
        # check_old_name(_)
        time.sleep(7)


if __name__ == '__main__':
    main()