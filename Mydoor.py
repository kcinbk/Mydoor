import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from datetime import datetime as dt
import numpy as np

# Activate the environment
envrionment_path = #Put in the the path to fhe chromdriver
os.environ['PATH'] += f"{envrionment_path}"

# Activate Chromedriver
options = Options()
options.page_load_strategy = 'normal'
driver = webdriver.Chrome()
driver.get('https://nextdoor.com/login/')

# In order for this to work, a Nextdoor account is requred 

# Fill out username
email = driver.find_element(By.CLASS_NAME, "css-wg4cxf")
WebDriverWait(email, 5)
email.send_keys(#Nextdoor account username)

# Fill out password
psd = driver.find_element(By.CLASS_NAME, "css-eojkw")
WebDriverWait(psd, 5)
psd.send_keys(#Nextdoor account username)

# Sign in
WebDriverWait(driver, 5)
login = driver.find_element(By.ID,'signin_button')
login.click()

# Now that it's loged in,

options = Options()
options.page_load_strategy = 'normal'

# Nextdoor's neigborhood feed endpoint:
# https://nextdoor.com/neighborhood/f{neighborhood}--f{city}--f{state}/?source=neighborhood_name

# Say that we want to focus on Charlestown, RI
driver.get('https://nextdoor.com/neighborhood/charlestownri--charlestown--ri/')


nextdoor_list = []
seen_ids = set()

def scroll_and_scrape():
    count = 0
    
    # set number of pages that will be crawled. 
    page = 30
    while count < page:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
    
        boxes = driver.find_elements(By.XPATH, "//div[@class='css-n4lbsh' and @id]")
        for box in boxes:
            post_id = box.get_attribute('id')
            if post_id in seen_ids:
                pass
            else:
                seen_ids.add(post_id)
                author = box.find_element(By.CLASS_NAME, "E7NPJ3WK").text
                location = box.find_element(By.CLASS_NAME,"post-byline-redesign").text
                date = box.find_element(By.XPATH, ".//a[@class='post-byline-redesign'][2]").text
                try:
                    body = box.find_element(By.XPATH, ".//span[@class='Linkify']").text
                except:
                    body = np.nan
                post_link = box.find_element(By.XPATH, ".//a[@class='post-byline-redesign'][2]").get_attribute('href')
                try:
                    comment = box.find_element(By.CLASS_NAME, "post-action-container").find_element(By.CLASS_NAME, "css-10hdpyl").text
                except:
                    comment = np.nan
                try:
                    reaction = box.find_element(By.CLASS_NAME, "post-action-container").find_element(By.CLASS_NAME,"_2b1vgpTX").text
                except:
                    reaction = np.nan
                nextdoor_list.append([post_id, author, location, date, body, post_link, comment, reaction])
                
        count += 1
        print("Page " + str(count) + " is finished.")
        
    print("It's done!")

# call the scroll and scrape function
scroll_and_scrape()

# close out driver
driver.quit()

# Load the data into a df
df = pd.DataFrame(nextdoor_list, columns=['post_id', 'author', 'location', 'date', 'body', 'post_link', 'comment', 'reaction'])
