import urllib.request
import urllib.error
import json
import time
import re
import os
import csv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
driver = webdriver.Chrome('C:\Users\yanli\Desktop\python\spider\chromedriver')
url = "https://search.jd.com/search?keyword=%E4%B8%89%E6%98%9F&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&bs=1&wq=%E4%B8%89%E6%98%9F&ev=exbrand_%E4%B8%89%E6%98%9F%EF%BC%88SAMSUNG%EF%BC%89%5E&cid3=655#J_searchWrap"
driver.get(url)

actions=ActionChains(driver)
main_links = []
page_number = 1
itemCnt = 1
while (page_number!=17):
    for _ in range(3):
        actions.send_keys(Keys.PAGE_DOWN).perform()
        sleep(2)
    # Find all hotels in the container
    for element in driver.find_elements_by_class_name("gl-item"):            
        links = element.find_element_by_tag_name("a")
        href = links.get_attribute('href')
        main_links.append(href) 
        itemCnt += 1
    try:
        link = driver.find_element_by_xpath('//*[@id="J_bottomPage"]/span[1]/a[9]')
    except NoSuchElementException:
        break     

    link.click()
    driver.get(driver.current_url)

    # While True, scrap next page
    page_number += 1
    sleep(2)


from collections import OrderedDict
main_links = list(dict.fromkeys(main_links))


def url_open(url):
    try: 
        urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        print("HTTP ERROR")
        print("error code:",e.code)
    except urllib.error.URLError as e:
        print("CAN'T REACH A SERVER")
        print("error:",e.reason)
    else:
        req=urllib.request.Request(url)
        req.add_header('User-Agent',"Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1")
        response=urllib.request.urlopen(req)
        html=response.read()
        return html

def get_item(url):
    pattern=r'target="_blank" href="(//item.jd.com/[^"]+\.html)'
    items_url=re.findall(pattern,url)
    return items_url

def get_long_name(item_html):
    #item_html=url_open("https:"+item_url).decode("gbk")
    item_name=re.findall(r'当季新品|京东物流|京东精选',item_html)
    if len(item_name)!= 0:
        pattern=r'<div class="sku-name">\n[^<]+<img src="//[^>]+>\n([^"]+)</div>\n                        <div cl'
    else:
        pattern=r'<div class="sku-name">\n([^"]+)</div>'
    item_name=re.findall(pattern,item_html)
    return item_name
def get_name(item_html):
    pattern=r'商品名称：([^<]+)<'
    item_name=re.findall(pattern,item_html)
    return item_name

def get_price(item_url):
    item_id=re.findall(r'//item.jd.com/([^.]+)\.html',item_url)
    url="http://p.3.cn/prices/mgets?skuIds=J_"+str(item_id[0])
    price_html=url_open(url).decode("gbk")
    item_price=re.findall(r'"p":"([^"]+)"',price_html)
    return item_price

def get_storage(item_html):
    #item_html=url_open("https:"+item_url).decode("gbk")
    pattern=r'([^>]+)<[^<]+<dt>存储卡</dt>'
    item_storage=re.findall(pattern,item_html)
    return item_storage

def get_battery_capacity(item_html):
    #item_html=url_open("https:"+item_url).decode("gbk")
    pattern=r'<dt>电池容量（mAh）</dt><dd>([^<]+)<'
    battery_capacity=re.findall(pattern,item_html)
    return battery_capacity

def get_color(item_html):
    #item_html=url_open("https:"+item_url).decode("gbk")
    pattern=r'机身颜色</dt><dd>([^<]+)<'
    item_color=re.findall(pattern,item_html)
    return item_color

def get_camera_piexl(item_html):
    #item_html=url_open("https:"+item_url).decode("gbk")
    pattern_front=r'<dt>前置摄像头</dt><dd>([^<]+)<'
    pattern_rear=r'<dt>后置摄像头</dt><dd>([^<]+)<'
    front_pixel=re.findall(pattern_front,item_html)
    rear_pixel=re.findall(pattern_rear,item_html)
    return front_pixel,rear_pixel

def get_next_page_url(current_url):
    page=re.findall(r'page=(\d)',current_url)[0]
    page=str(int(page)+2)
    next_url="https://search.jd.com/search?keyword=samsung&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&bs=1&wq=samsung&cid2=653&cid3=655&ev=exbrand_%E4%B8%89%E6%98%9F%EF%BC%88SAMSUNG%EF%BC%89%5E&page="+page+"&s=58&click=0"
    return next_url

def read_current_url(current_url):
    html=url_open(current_url).decode("utf-8")
    item_url=get_item(html)
    return item_url


name=[]
price=[]
RAM=[]
battery=[]
color=[]
front_pixel=[]
rear_pixel=[]
if __name__=='__main__':
    for each in main_links:
        print(count)
        if(len(each)<100):
            item_html=url_open(each).decode("gb18030")
            name.append(get_name(item_html))
            price.append(get_price(each))
            RAM.append(get_storage(item_html))
            battery.append(get_battery_capacity(item_html))
            color.append(get_color(item_html))
            front,rear=get_camera_piexl(item_html)
            front_pixel.append(front)
            rear_pixel.append(rear)
        time.sleep(2)
        count+=1

if os.path.exists("data.csv"):
    os.remove("data.csv")
csvFile = open("data.csv", "w")
writer = csv.writer(csvFile)
writer.writerow(name)
writer.writerow(price)
writer.writerow(RAM)
writer.writerow(battery)
writer.writerow(color)
writer.writerow(front_pixel)
writer.writerow(rear_pixel)
csvFile.close()