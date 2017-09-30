from selenium import webdriver

def phantomJS():
    driver = webdriver.PhantomJS(executable_path=r'E:\files\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    driver.get('https://www.amazon.cn/ref=z_cn?tag=zcn0e-23')
    print(driver.page_source)

if __name__=='__main__':
    phantomJS()