from selenium import webdriver  # open webdriver for specific browser
from selenium.webdriver.common.keys import Keys  # for necessary browser action
from selenium.webdriver.common.by import By  # For selecting html code
import time

driver = webdriver.Chrome(executable_path='/media/salesmind/0002C1F9000B55A8/Linux Softwares/chromedriver')
driver.get("http://www.jabong.com/men/clothing/polos-tshirts/")


def url_scrp():
    for i in range(0, 5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
    url = driver.find_elements(By.XPATH, '//ul[@id="productsCatalog"]/li')
    return url


if __name__ == '__main__':
    print(url_scrp())