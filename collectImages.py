import os
import time
import requests
import base64
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

exercises = ['pushup', 'pullup', 'chest dips', 'bent over row', 
             'shoulder press', 'squat', 'lunges', 'plank', 'glute bridge']
queries = ["full body person doing "] * len(exercises)

#build list of queries
for x in range(len(queries)):
    queries[x] = queries[x] + exercises[x]

print(queries)

#build webdriver
op = webdriver.ChromeOptions()
#op.add_argument('headless')
op.add_argument('--ignore-certificate-errors')
op.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(options=op)

for query in queries:
    try:
        #This is to get the url for google images w/ selenium
        time.sleep(5)
        driver.get("https://www.images.google.com")
        #wait for the element
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'gLFyf')))
        #get element send query and submit
        sBox = driver.find_element(By.CLASS_NAME, 'gLFyf')
        sBox.send_keys(query)
        sBox.send_keys(Keys.ENTER)
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'islrc')))

        SCROLL_PAUSE_TIME = 0.5

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        #make directory for images
        path = query.replace("full body person doing ", '')
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)
        #pass page source to beautiful soup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        images = soup.findAll(class_= 'rg_i Q4LuWd')

        for x in range(len(images)):
            #get base64 source of image
            src = images[x]['src']

            #decode base64 image
            head, data = src.split(',', 1)
            file_ext = '.' + head.split(';')[0].split('/')[1]
            src_decoded = base64.b64decode(data)

            #write file
            filepath = os.path.join(path, (query + str(x) + file_ext))
            with open(filepath, 'wb') as f:
                f.write(src_decoded)

    except Exception as e: 
        print(e)

driver.close()
