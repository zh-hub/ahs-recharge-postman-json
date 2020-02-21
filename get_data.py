import pymongo
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from pyquery import PyQuery as pq

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

KEYWORD = 'iMac'


def index_page(page):
    print('正在爬取第', page, '页')
    try:
        url = 'https://s.taobao.com/search?q=' + quote(KEYWORD)
        driver.get(url)
        if page > 1:
            input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                '#mainsrp-pager  div.form > input')))
            submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            '#mainsrp-pager div.form > span.btn.J_Submit')))
            input.clear()
            input.send_keys(page)
            submit.click()
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page))
        )
        wait.until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, '.m-itemlist .items .item')))
        get_products()
    except TimeoutException:
        index_page(page)


def get_products():
    html = driver.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('data-src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text(),
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        print(product)
        save_to_mongo(product)
        print('\n')


# def save_to_mongo(result):
#     client = pymongo.MongoClient('mongodb://admin:admin123@localhost:27017/')
#     db = client['taobao']
#     collection = db['products']
#     try:
#         if collection.insert(result):
#             print("成功保存到MongoDB")
#     except Exception:
#         print('someing wrong with MongDB')


MAX_PAGE = 100


def main():
    for i in range(1, MAX_PAGE + 1):
        index_page(i)
    driver.close()


if __name__ == '__main__':
    main()