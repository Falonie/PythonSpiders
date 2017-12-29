import requests, re, time, pymongo, logging, random, xlrd
from lxml import html
from multiprocessing import Pool
from pprint import pprint

url2 = 'https://ehire.51job.com/Candidate/ResumeView.aspx?hidUserID=353662301&hidEvents=23&pageCode=3&hidKey=fd9f0df0b7049e8f5c86a775a8eb158f'
headers = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
]
cookies = {
    'Cookie': 'guid=15118321204924090012; EhireGuid=0ccd7bcab23140c48a37e666de1e57f3; 51job=cenglish%3D0%26%7C%26; ASP.NET_SessionId=412olx3hpdgwxxqdklzkh4gr; HRUSERINFO=CtmID=2585839&DBID=3&MType=02&HRUID=2965014&UserAUTHORITY=1100111011&IsCtmLevle=1&UserName=%e8%b6%85%e4%b9%90%e5%81%a5%e5%ba%b7&IsStandard=0&LoginTime=11%2f28%2f2017+16%3a22%3a40&ExpireTime=11%2f28%2f2017+16%3a32%3a40&CtmAuthen=0000011000000001000110010000000011100001&BIsAgreed=true&IsResetPwd=0&CtmLiscense=2&AccessKey=afffec3efd1ab2ee; AccessKey=7aa8d4200e8f47a; RememberLoginInfo=member_name=E2BF04DB6CCD2D50FAD638DD50DCF144&user_name=E2BF04DB6CCD2D50FAD638DD50DCF144; LangType=Lang=&Flag=1'}
file = '/media/salesmind/Other/cloud_bird/智联-测试数据（11.27）_.xlsx'
collection = pymongo.MongoClient(host='localhost', port=27017)['Falonie']['51Job_Resume_matching_keyword_company']
data = {
    '__EVENTTARGET': 'ctrlSerach$search_submit',
    '__VIEWSTATE': '/wEPDwUJODA0MTA0NTMxDxYOHgRJc0VOaB4QdnNTZWxlY3RlZEZpZWxkcwUzQUdFLFdPUktZRUFSLFNFWCxBUkVBLFdPUktGVU5DLFRPUERFR1JFRSxMQVNUVVBEQVRFHghQYWdlU2l6ZQIyHgxzdHJTZWxlY3RDb2wFM0FHRSxXT1JLWUVBUixTRVgsQVJFQSxXT1JLRlVOQyxUT1BERUdSRUUsTEFTVFVQREFURR4JUGFnZUluZGV4AhAeCFBhZ2VEYXRhBbQQODAxfDEwMDB8MjAwfDE2NjZ8NzIxNTg0MTMsNTQ4NDgyLDI2MDA1MzI2LDM2NDA0OTQxOSwzNDYwNjMzMjUsMzk1MzI1MiwzNDQ5ODIxODYsOTIwNTE1OTEsMzU5ODMzMDMyLDQxNDQ3MzIsMjYwMjUzNzMsMTQ5MjgwODcsMTM3NzM2MTEsNjIwNTYxNzQsMzIwNjU3MDEzLDI4NDE1MTc5LDM1MDk2MTcyMCw3ODg0OTEsMzU3MjM4NTM2LDMyMDcyMzcwNiw1MTYwOTQzNSwzNjQxMTQ4MzksNTI4ODY0NjcsMzYwNzI2NzE0LDM2MzMyOTAwOCwyNDI4MDg5NiwzNTU2Mjk4ODIsNDA4ODU1NiwzMjgyNjg1MDQsMzQ1OTM1ODc1LDMyNTQ3Mjk1NSw2NzY3NTk0MSwzNTc3Njc5ODYsODUzMTkwOCw5MDY5NDA4MSwzNjM4NDY1MzIsNjQ2NzUzMiwxMzE5ODk1NSwyNzUxNzg3NSwxOTAzNTc3NiwzNjQxMTg1ODIsNjY4MjY2OSwzNTM2OTU0NDUsODA0Nzk1LDU0Mzg2NzU2LDMyNDE1ODEwLDMzODkyMjQ3NSw4MjIyODg2MiwxNzQwODM1MCwzNTc0NzIxOTAsMzU2NjA1MDAxLDExOTM5MzQzLDMxMzExOTM2MSw4NTAzNzA2MiwyOTY4Njc4LDM2MjcyODA0NiwxNTA1MjU1Niw1ODUzMDQxOSw2MzQ1Mzg5LDExMTk3MjAxLDMxOTc0MzEwMywzNjM5ODUzMzgsNjI3MTk4NzUsMzA4NzY5MDA0LDM0OTYzNTA1MCwzMTk1MjIwMTEsMjUzMzI5MTAsMzUyNDI0MTc2LDY0NTMyNDk2LDcyODU3MzI1LDM1NDM3OTQxOCwyOTE3MzQ1NiwzNjM3OTAxMTYsNTUxMDIwLDM1NDk4NDU0MywzMTE3MzU2OTMsMzYyMDE2MTYyLDMyMjUzMTcxNSwzMzk1NjI0MzksMjcyNzE5MjIsNzYyODI1MjMsMzIxNzgwMjU5LDk1MDQ5NDAsMzUwOTE0MzkyLDM2MzcxODA4Niw3NTYyNzIyMSw1ODgyMjIxLDMxOTQ1Nzc5LDIzNzQ4ODIsMzYzMzEyODgwLDc3NzAwNTcyLDMxNzY2ODQsMzA5MjEyMDA2LDM1NjQyMzQ3NCwzNjI2OTU2NzQsMzQ4NjgzMzIxLDM2MDcwNjYwMyw1NTM4NDcwLDE0OTc5NjgzLDI3MTc3MTIxLDY2NjI3NjI1LDQ0OTM4ODEsNTgzMTM4NTcsMzU0NzgwNjk2LDE0MTk2OTM4LDM2MTUxMjMzNiw1MzkyMTIwNCwzNjMyNTc4MjgsMTI0MDI0Niw1MzgzNDYwNSwzMTMzMDY5Myw3ODM2MTA2OSw5MDk5MDQ4LDM2MjkwMjkxOCwzNjMyOTgxNTYsMzYyNDE2ODI4LDcyMDQ2MzgxLDgxNzc3NzIxLDkzNjQ3MDUsODAxNDkyNjgsMTIzODg0Miw1NTE5NzM3LDE4MjI3NzY4LDM2MTU4NTAzNiwxNDQzNTQ0NCwzMjQzNTc5NzQsODE3MjU0NDQsNTEwMDE1MDYsMzQ5Mzc2NTA3LDc1MzI5NjM5LDMxNzEwNjgzOCw1MTM4MjYsMzIxMDc4MzQzLDk2MDA5MDQsMzA0Njc5NDY4LDMxNTAyODM2NCwzMTQyOTQyNzgsOTYxMjU5NTEsMjUzMjU4MDYsMzYwNDE0ODE2LDg0MTIzMjM1LDU4MjgwOTE0LDMxNjE4MzMzLDM1OTIwMDE2Nyw0OTU3MDA1NCwzMDcxMzA2NDcsOTAxMTQ5MjMsNTA1MTIyNzcsMzU4NjIzMDYzLDYzOTg0NDAyLDM1OTUzMzA4NSwzNTEyNjk3NTYsMTA3MzY0NjMsMzU5NDIzOTMzLDM0NDIwNTM3NCw2ODAzODIwLDM2MjU3MDUzNSw0OTQwMTE3OSwzMTI4NTE5NDcsMzYwNDM2NDQwLDM1NDM3MzAyMCwzNTg0MTEzMjYsMzYxNzkxMDQ0LDM1NjkxMTM0NiwzMjA0NDIwMTksODk4OTU3OTEsMzYyMjk2MjA3LDY0Mjg2NDExLDcwNTM3MTQ2LDM0NjA1NDEwNywxNjQyODAxMywxMDkyNzU5MCwzNjAwNzY3NjYsMTM0MjQxMSw3NjE0MDE2Myw2MTgyMzM1MCwyNjkxNzAwNywzMDgzMjYyOTMsNTE3NTE4NDYsNzAwOTAxOTcsMTU5MTUwMDYsNjgxMjM4MTMsMzYyNDM0NTU0LDQ4NjM2MCwzMzMzNjQ1MTMsMzI1MjM3MzAwLDY5NjA3MDcsNjc4OTA5NjIsMzM0Mjg2NzkwLDg5MjI0MTIyLDM5ODI4ODYsMzYwMjUyMTMxLDM2MjI3NTA5NiwzNjE1MTgwNzUsMzU3NDYzNjA1LDM1NTIxNzg5MiwzNDM2NTA3OTUsNzE4Nzg2NCwzNjIyMDk5MTgsNjQ5NjQ2MTB8TUNNd0l6QWpPWHd3TVRBd01EQXdNakF3TURBd05UQXdNREI4TURneU56QTRNamd3T0RJMWZEQXdmREF3ZkRBd01EQjhNakF4TmpFd016RjhNakF4TnpFd016RjhNREF3TURBd01EQjhNREF3TURBd01EQjhNSHc1ZkRCOE1Id3dmREI4TURBd01Id3dNREF3ZkRCOE1IeDhmREI4TUh3NWZEbDhPWHc1ZkRsOE9Yd3dNREF3TURCOE1EQXdNSHd3TURBd2ZEQXdNREF3TUh3eGZEbDhPREF4SXpFd01EQWpFQkFRHgxUb3RhbFJlY29yZHMCgg0WAgIBD2QWGAICDw8WBB4RSXNDb3JyZWxhdGlvblNvcnQFATAeCElzVXNlcklEBQEwZGQCBQ9kFgJmDxAPFgIeB0NoZWNrZWRoZGRkZAIGDw8WBB4IQ3NzQ2xhc3MFF1NlYXJjaF9yZXN1bWVfYnV0dG9uX29uHgRfIVNCAgJkZAIHDw8WBB8KBSZDb21tb25faWNvbiBTZWFyY2hfYnRuX2xhYmVsX2Fycm93X0Nvch8LAgJkZAIIDw8WBB8KBRlTZWFyY2hfcmVzdW1lX2J1dHRvbl9vdXQyHwsCAmRkAgkPDxYEHwoFFFNlYXJjaF9idG5fbGFibGVfbm9uHwsCAmRkAgoPDxYCHgRUZXh0BQrlhbExNjY25p2hZGQCCw8PFgQfCgUqQ29tbW9uX2ljb24gU2VhcmNoX3Jlc3VtZV9idXR0b25fZGlzaW1nX29uHwsCAmRkAgwPDxYEHwoFLENvbW1vbl9pY29uIFNlYXJjaF9yZXN1bWVfYnV0dG9uX2Rpc2ltZ19kb3V0HwsCAmRkAg0PDxYIHwBoHgpQUGFnZUluZGV4AhAfAgIyHwYCgg1kFgICAg8QZGQWAQICZAIODw8WCB8AaB8NAhAfAgIyHwYCgg1kFhACAQ8PFgofDAUCMTUeD0NvbW1hbmRBcmd1bWVudAUCMTUeB1Rvb2xUaXAFAjE1HwplHwsCAmRkAgIPDxYKHwwFAjE2Hw4FAjE2Hw8FAjE2HwplHwsCAmRkAgMPDxYKHwwFAjE3Hw4FAjE3Hw8FAjE3HwoFBmFjdGl2ZR8LAgJkZAIEDw8WCh8MBQIxOB8OBQIxOB8PBQIxOB8KZR8LAgJkZAIFDw8WCh8MBQIxOR8OBQIxOR8PBQIxOR8KZR8LAgJkZAIGDw8WAh8MBQMuLi5kZAIHDw8WAh8MBQMuLi5kZAIIDw8WBh8PBQIzNB8MBQIzNB8OBQIzNGRkAg8PEGQQFQ0G5bm06b6EDOW3peS9nOW5tOmZkAbmgKfliKsJ5bGF5L2P5ZywBuiBjOiDvQblrabljoYS566A5Y6G5pu05paw5pe26Ze0BuaIt+WPowzmnJ/mnJvmnIjolqoM55uu5YmN5pyI6JaqBuihjOS4mgbkuJPkuJoJ5a2m5qCh5ZCNFQ0DQUdFCFdPUktZRUFSA1NFWARBUkVBCFdPUktGVU5DCVRPUERFR1JFRQpMQVNUVVBEQVRFBUhVS09VDEVYUEVDVFNBTEFSWQ1DVVJSRU5UU0FMQVJZDFdPUktJTkRVU1RSWQhUT1BNQUpPUglUT1BTQ0hPT0wUKwMNZ2dnZ2dnZ2dnZ2dnZ2RkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYQBQ1jaGtIYXNQaWNfYmFrBQljaGtIYXNQaWMFDGNieENvbHVtbnMkMAUMY2J4Q29sdW1ucyQxBQxjYnhDb2x1bW5zJDIFDGNieENvbHVtbnMkMwUMY2J4Q29sdW1ucyQ0BQxjYnhDb2x1bW5zJDUFDGNieENvbHVtbnMkNgUMY2J4Q29sdW1ucyQ3BQxjYnhDb2x1bW5zJDgFDGNieENvbHVtbnMkOQUNY2J4Q29sdW1ucyQxMAUNY2J4Q29sdW1ucyQxMQUNY2J4Q29sdW1ucyQxMgUNY2J4Q29sdW1ucyQxMg==',
}


class CrawlingResumes(object):
    def __init__(self):
        self.url = 'https://ehire.51job.com/Candidate/SearchResumeNew.aspx'
        self.search_value = 'ERP or SAP or CRM or OA or 招聘系统 or 钉钉 or 金蝶 or HR信息系统 or oracle or 用友 or K3 or U8 or PLM or SRM or EHR or PDM or MES or APS or WMS##0#########{}###########近1年|6##1#1###0#0#0'

    def generate_response_txt_read(self):
        with open('/media/salesmind/Other/cloud_bird/智联-测试数据（11.27）_.txt', 'r') as f:
            for i, line in enumerate(f.readlines(), 1):
                # print(i,line.strip())
                # yield self.search_value.format(line.strip())
                self.searching_company = line.strip()
                data.update({'ctrlSerach$hidSearchValue': self.search_value.format(line.strip())})
                response = requests.post(url=self.url, data=data, headers={'User-Agent': random.choice(headers)},
                                         cookies=cookies).text
                yield response

    def generate_response_excel_read(self, file):
        with xlrd.open_workbook(file) as data_:
            table = data_.sheets()[0]
            # print(table.ncols)
            for rownum in range(1, table.nrows):
                row = table.row_values(rownum)
                self.searching_company = row[0]
                data.update({'ctrlSerach$hidSearchValue': self.search_value.format(row[0])})
                # yield data
                response = requests.post(url=self.url, data=data, headers={'User-Agent': random.choice(headers)},
                                         cookies=cookies).text
                yield response

    def urls(self, r):
        try:
            selector = html.fromstring(r)
            url_list = []
            for i in selector.xpath('//div[@class="Common_list-table"]/table/tbody/tr[@class="inbox_tr1"]|'
                                    '//div[@class="Common_list-table"]/table/tbody/tr[@class="inbox_tr2"]'):
                href = i.xpath('td[@class="Common_list_table-id-text"]/span/a/@href')[0]
                ID = i.xpath('td[@class="Common_list_table-id-text"]/span/a/text()')[0]
                # print(ID, 'http://ehire.51job.com/{}'.format(href))
                url_list.append('http://ehire.51job.com/{}'.format(href))
            return url_list
        except Exception:
            pass

    def parse_url(self, url):
        response = requests.get(url=url, headers={'User-Agent': random.choice(headers)}, cookies=cookies).text
        sel = html.fromstring(response)
        working_experience_list = []
        try:
            a = sel.xpath('//*[@id="divInfo"]/td/table[4]/tr[2]/td/table/tr[1]/td/table/tbody/tr[1]/td[2]/span[1]/text()')[0]
            for i in sel.xpath('//*[@id="divInfo"]/td/table[4]/tr[2]/td/table/tr'):
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
                description = ''.join(str(i).strip() for i in i.xpath('td/table/tbody/tr[4]/descendant::text()'))
                description = re.sub(r'[#→star←end ]', '', description)
                ID = re.findall('<title>\s*(.*?)\s*</title>', response)[0]
                working_experience = {'ID': ID, 'update_time': update_time, 'time': time, 'company': company,
                                      'period': period, 'industry': industry, 'scale': scale, 'nature': nature,
                                      'position': position, 'description': description,
                                      'searching_company': self.searching_company}
                working_experience_list.append(working_experience)
            return working_experience_list
        except Exception:
            for i in sel.xpath('//*[@id="divInfo"]/td/table[3]/tr[2]/td/table/tr'):
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
                description = re.sub(r'[#→star←end ]', '', description)
                ID = re.findall('<title>\s*(.*?)\s*</title>', response)[0]
                working_experience = {'ID': ID, 'update_time': update_time, 'time': time, 'company': company,
                                      'period': period, 'industry': industry, 'scale': scale, 'nature': nature,
                                      'position': position, 'description': description,
                                      'searching_company': self.searching_company}
                working_experience_list.append(working_experience)
            return working_experience_list


def main():
    resume = CrawlingResumes()
    for i, j in enumerate(resume.generate_response_excel_read(file=file), 1):
        t0 = time.time()
        if resume.urls(j):
            # print(i, type(urls(j)), urls(j))
            with Pool() as pool:
                p = pool.map(resume.parse_url, resume.urls(j))
                # print(p, len(p), type(p))
                for i, j in enumerate(p, 1):
                    print(i, j, type(j))
                    try:
                        collection.insert_many(j)
                    except Exception as e:
                        print(e)
        print(time.time() - t0)
        time.sleep(10)


if __name__ == '__main__':
    main()