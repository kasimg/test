# -*- coding: utf-8 -*-

from selenium import webdriver as wd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

driver=wd.Chrome('./chromedriver.exe')
driver.get("http://v.youku.com/v_show/id_XMTY2NTk5ODAwMA==.html?from=y1.3-idx-beta-1519-23042.223465.3-3")

print 'start'
# time.sleep(15)
WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID , "videocomment")))

element = driver.find_elements_by_id("videocomment") #如果有多个符合条件的，返回第一个

for each in element :
    print each.text