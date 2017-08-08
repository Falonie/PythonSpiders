import requests, json, re, time, os, csv

base_url = 'http://weibo.com/aj/v6/comment/big?ajwvr=6&id=4090258591184334&root_comment_max_id=13883125907851111&root_comment_max_id_type=0&root_comment_ext_param=&page={page}&filter=hot'

cookie = {
    'Cookie': 'TC-Ugrow-G0=0149286e34b004ccf8a0b99657f15013; login_sid_t=bfc63a0a4ed30c3c3f14fe6608f2693f; TC-V5-G0=c427b4f7dad4c026ba2b0431d93d839e; _s_tentry=-; Apache=614236817117.7325.1490449015297; SINAGLOBAL=614236817117.7325.1490449015297; ULV=1490449015314:1:1:1:614236817117.7325.1490449015297:; SSOLoginState=1490449107; TC-Page-G0=b1761408ab251c6e55d3a11f8415fc72; wb_publish_fist100_2682846513=1; UOR=,,www.google.com.hk; SCF=AmovXSi_nKdmLFHZHOKMOmVZmKgHLCAdrPaLd4KDRHJfYMgxi0skavY2XGc-l3mgV9dF_6W0OxdwyUI2PgNqPyg.; SUB=_2A2513yYBDeRxGeRI41AZ9CjJyj-IHXVWrRDJrDV8PUNbmtAKLWjYkW8AF7_G0CqDwO0KxufgM5G2Kby5Uw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh-HT3hyw4nEHp3KKm4KI.m5JpX5KzhUgL.Fozc1hzRShqfeKe2dJLoI79hqPSLdr.t; SUHB=0ftYKbX9Ce1ICB; ALF=1522305488; wvr=6'}
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
pattern = re.compile(r'</a>(.*?)</div>')
chinese_pattern = re.compile(r'[\u4e00-\u9fa5]+')

for i in range(1, 6, 1):
    url = base_url.format(page=i)
    r = requests.get(url, cookies=cookie, headers=header).json()
    data = r['data']['html']
    comment = pattern.findall(data)
    for i in comment:
        chinese_comment = chinese_pattern.findall(i)
        chinese_comment = ''.join(chinese_comment) + '\n'
        with open('ipanda_live.csv', 'a+', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(chinese_comment)
        print(chinese_comment)
    time.sleep(.5)