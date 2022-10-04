from selenium import webdriver
import os, time
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

CHROMEDRIVER_PATH = "/app/.chromedriver/bin/chromedriver"
    
chrome_options = webdriver.ChromeOptions()
    
chrome_options.binary_location = '.apt/usr/bin/google-chrome-stable'
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('headless')
    
browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)

def find_nearest(lat, lon, search) :
    
    url, details_lst = None, []

    if search.lower() == "hospital" : url = "https://www.google.com/maps/search/hospital/@"+str(lat)+str(lon)
    elif search.lower() == "pharmacy" : url = "https://www.google.com/maps/search/pharmacy/@"+str(lat)+str(lon)
    
    browser.get(url)
    time.sleep(3)
    
    cnt = 0
    while True :
        if len(details_lst) >= 5 : break
        try :
            t = browser.find_element_by_xpath('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div['+str(cnt)+']/div/div[2]/div[2]/div[1]/div')
            details_lst.append(t.text)
        except : 
            None
        cnt += 1
        
    lst = [n.split("\n") for n in details_lst]
    lst = [n for n in lst if n.pop(1)]
    
    #print(lst)
    
    return lst
