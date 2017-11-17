import pymysql, pymongo, re, xlrd
from pprint import pprint

base_url = 'http://www.baidu.com/s?q1={}@V'
file6 = '/media/salesmind/Other/baidu_homepage_search/官网_test.xlsx'
list1 = [['北京蓝色光标电子商务股份有限公司', '北京蓝色光标品牌管理顾问股份有限公司', 'www.bluefocusgroup.com/'], ['北京蓝色光标电子商务股份有限公司', '蓝色光标电子商务股份有限公司官网', 'www.bfecom.com/'], ['北京蓝色光标电子商务股份有限公司', '蓝色光标电子商务股份有限公司官网', 'www.beilianec.com/'], ['北京蓝色光标电子商务股份有限公司', '北京蓝色光标电子商务股份有限公司_837467.蓝标电商', 'cwzx.shdjt.com/gpdmf.....'], ['北京蓝色光标电子商务股份有限公司', '北京蓝色光标电子商务股份有限公司联系方式_信用报告_工商信息-...', 'www.qixin.com/company/...'], ['北京蓝色光标电子商务股份有限公司', '【北京蓝色光标电子商务股份有限公司2017最新招聘信息】-猎聘网', 'https://www.liepin.com/company...']]
list2 = [['北京信宇佳信息科技有限公司', '北京信宇佳信息科技有限公司招聘信息_电话_地址-智联招聘', 'company.zhaopin.com/CC...'], ['北京信宇佳信息科技有限公司', '北京信宇佳信息科技有限公司_百度百科', ''], ['北京信宇佳信息科技有限公司', '首页_北京信宇佳信息科技有限公司', '27762842.b2b.11467.com/'], ['北京信宇佳信息科技有限公司', '北京信宇佳信息科技有限公司最新招聘【找工易】', 'www.hunt007.com/employ...'], ['北京信宇佳信息科技有限公司', '北京信宇佳信息科技有限公司工资怎么样?(福利待遇、薪酬..._职友集', 'www.jobui.com/company/...'], ['北京信宇佳信息科技有限公司', '北京信宇佳信息科技有限公司【企业信用, 电话, 地址, ..._阿里巴巴', 'https://www.1688.com/xinyong/4...']]
list3 = [['中物永泰纸业有限公司', '中物永泰纸业有限公司_百度百科', ''], ['中物永泰纸业有限公司', '中物永泰纸业有限公司', 'zwytzwyt.chinapaper.net/'], ['中物永泰纸业有限公司', '中物永泰纸业有限公司招聘信息_电话_地址-智联招聘', 'company.zhaopin.com/CC...'], ['中物永泰纸业有限公司', '中物永泰纸业有限公司_印刷|包装|造纸', 'zwytzy.cn.biz72.com/'], ['中物永泰纸业有限公司', '北京中物永泰纸业有限公司_工商信息_电话_地址_信用信息_财..._悉知', 'www.xizhi.com/COMDgALU...'], ['中物永泰纸业有限公司', '中物永泰纸业有限公司工资怎么样?(福利待遇、薪酬概况) -..._职友集', 'www.jobui.com/company/...']]
collection = pymongo.MongoClient(host='127.0.0.1', port=27017)['Falonie']['Baidu_Search']

def company_list(file):
    with xlrd.open_workbook(file) as data:
        table = data.sheets()[0]
        # print(table.ncols)
        # company = []
        # for rownum in range(1, table.nrows):
        #     row = table.row_values(rownum)
        #     company.append(row[0])
        company_list_ = [table.row_values(rownum)[0] for rownum in range(1, table.nrows)]
        return company_list_


if __name__ == '__main__':
    # print(company_list(file6))
    company_urls = [base_url.format(i) for i in company_list(file=file6)]
    # print(company_urls)
    for i, j in enumerate(company_urls, 1):
        # print(i,j)
        # company_name = re.findall('q1=(.*?)@V', j)
        # company_name2 = re.search('q1=(.*?)@V', j).group()
        # print(i, company_name[0])
        pass
    for i,j in enumerate(list1,1):
        # print({'company_name':c for c in j})
        pass
    # pprint(list(collection.find({})))
    # collection.drop()