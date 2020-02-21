from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time


drive = webdriver.Chrome()

def get_data():
    """
    根据股票代码获取数据
    :param num: 股票代码
    :return:
    """
    url = "https://search.jd.com/Search?keyword=%E8%BD%A6%E5%8E%98%E5%AD%90&enc=utf-8&wq=%E8%BD%A6%E5%8E%98%E5%AD%90&pvid=a4aa735b48324cb1b77ed694579e3ebd"
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
        "content-type": "application/x-www-form-urlencoded", "accept-language": "zh-CN,zh;q=0.9"
        }
    # res = requests.get(url,headers = header)
    # res.encoding="gb2312"
    # html = res.text
    # # print(html)
    # soup = BeautifulSoup(html, "html.parser")
    # div = soup.find_all(class_="hq_details has_limit")
    # print(div)
    drive.get(url)

    time.sleep(3)
    drive.maximize_window()
    a = drive.find_elements_by_css_selector("#.gl-warp clearfix")
    print(a)
    drive.close()



if __name__ == '__main__':
    get_data()
