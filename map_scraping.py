from selenium import webdriver
import os
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("start-maximized")
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
browser.get("https://www.google.com")

def find_nearest(lat, lon, search) :
    
    url, details_lst = None, []

    if search.lower() == "hospital" : url = "https://www.google.com/maps/search/hospital/@"+str(lat)+str(lon)
    elif search.lower() == "pharmacy" : url = "https://www.google.com/maps/search/pharmacy/@"+str(lat)+str(lon)
    
    browser.get(url)
    
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
