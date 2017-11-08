# -*- coding: utf-8 -*-
from selenium import webdriver as wd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import lxml.html
import csv
import codecs


class taobaoSpider:
    def __init__(self):
        self.goods_info=[]
        self.url=''
        self.tips_and_input()

    def tips_and_input(self):
        print unicode('请输入关键字：\n','utf-8')
        self.keywords=raw_input()

    def process(self):
        self.create_url()
        self.get_pageContent()
        self.analyse()
        self.to_csv()
        self.driver.close()

    def create_url(self):
        pattern='https://s.taobao.com/search?q={}'
        self.url=pattern.format(self.keywords)

    def get_pageContent(self):
        driver=wd.Chrome('./chromedriver.exe')
        driver.get(self.url)
        #让页面充分加载
        # time.sleep(5)
        #等待30秒，如果没加载出感兴趣内容就不玩儿了
        try:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "mainsrp-itemlist")))
            self.html=str(driver.page_source)
            self.driver=driver

        except Exception as e:
            print unicode('加载了30秒仍然没有有用的东西','utf-8')

    def analyse(self):
        #使用webelement对象提取信息除链接之外的信息，用xpath语句提取链接信息
        all_items=self.driver.find_elements_by_xpath('//div[@data-category="auctions"]')
        selector = lxml.html.fromstring(self.html)
        link_list=selector.xpath('//div[@class="row row-2 title"]/a/@href')

        for i in range(min(len(link_list),len(all_items))):
            info_dict={}
            info_list=all_items[i].text.split('\n')
            info_dict['goods_name']=info_list[2]
            info_dict['location']=info_list[4]
            info_dict['shop_name']=info_list[3]
            info_dict['price']=info_list[0]

            info_dict['link']=link_list[i]
            self.goods_info.append(info_dict)

    def to_csv(self):
        with open(self.keywords+u'商品信息.csv','w') as f:
            f.write(codecs.BOM_UTF8)
            writer = csv.DictWriter(f, fieldnames=['goods_name', 'location', 'shop_name','price','link'])
            writer.writeheader()
            writer.writerows(self.goods_info)

    def get_info(self):
        return self.goods_info

if __name__=='__main__':
    spider=taobaoSpider()
    spider.process()

