import os
from selenium import webdriver


opts = webdriver.ChromeOptions()
opts.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

opts.add_argument("--headless")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")

browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=opts)

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
