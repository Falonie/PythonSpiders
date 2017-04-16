import requests,re,time
from bs4 import BeautifulSoup

base_url = 'https://www.lagou.com/zhaopin/shujufenxishi/{}/?filterOption=3'
cookie = {
    'Cookie': 'user_trace_token=20170326001734-ec41389ced6b4a4882609bf9e467bdb2; LGUID=20170326001734-8e3315f4-1176-11e7-9569-5254005c3644; TG-TRACK-CODE=deliver_guess; JSESSIONID=197AA9B8333FB8CB7DF60C237916266D; _putrc=43700CED3E324D1B; login=true; unick=%E7%8E%8B%E6%99%B4%E6%99%A8; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=5; _gat=1; LGSID=20170329210923-ee02d0e2-1480-11e7-a717-525400f775ce; LGRID=20170329214841-6b11e72a-1486-11e7-9574-5254005c3644; SEARCH_ID=81650aaa6c154f45a2b11a1d4107a646; index_location_city=%E4%B8%8A%E6%B5%B7; _ga=GA1.2.1946463376.1490458642; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1490458642; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1490795326'}
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
session = requests.session()

def lagou_shanghai():
    for i in range(1,31):
        url = base_url.format(i)
        #    r = requests.get(url, cookies=cookie, headers=header).text
        r = session.get(url, cookies=cookie, headers=header).content
        bsobj = BeautifulSoup(r, 'html.parser')
        pattern = re.compile(r'<span class="money">(.*?)</span>')
        pattern2 = re.compile(r'class="con_list_item default_list" data-company=(.*?) data-companyid=')
        pattern3 = re.compile(r'<span class="add">\[<em>(.*?)</em>\]')
        company = pattern.findall(str(bsobj))
        salary = pattern2.findall(str(bsobj))
        block = pattern3.findall(str(bsobj))
        print('Page %s' % i)
        for c, s, b in zip(company, salary, block):
            print(c, s, b)
        time.sleep(.5)

if __name__=='__main__':
    lagou_shanghai()