### import packages
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import json
from pymongo import MongoClient
### launch browser using webdriver
r_options = Options()
r_options.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=r_options)
driver.get("https://www.thantai1.net/so-ket-qua")

### crawl data from website using while loop, implementation date = at the end of the day 15/8/2024, period = 20 consecutive years, assumed that there are 365 days in a year.
lottery_data = {}
current_day = datetime.now().date()
index_number = 1
while True:
    day = driver.find_element(By.ID, "end")
    day.clear()
    day.send_keys("{}-{}-{}".format(current_day.day, current_day.month, current_day.year))
    button = driver.find_element(By.XPATH, "/html/body/div[3]/main/div/form/div[2]/div/button[9]")
    button.click()
    list_result = driver.find_elements(By.CLASS_NAME, "font-weight-bold.text-danger.col-12.d-block.p-1.m-0") 
    list_date = driver.find_elements(By.CLASS_NAME,"d-inline-block")
    for i in range(len(list_result)):
        lottery_data[list_date[i+2].text] = list_result[i].text
        index_number += 1
        if index_number > 20*365:
            break
    if index_number > 20*365:
        break
    
    last_day_string = list_date[len(list_date)-1].text
    last_day = datetime.strptime(last_day_string, "%d-%m-%Y").date()
    current_day = last_day - timedelta(days = 1)
### save data into json file:
list_lottery_data = [{"date": key, "XSMB": value} for key, value in lottery_data.items()]
with open("XSKT.json", "w") as f:
    json.dump(list_lottery_data, f, indent=4)
# client = MongoClient('mongodb://localhost:27017/')
# db = client['Lottery']
# collection = db['Crawl_XSMB']
# collection.insert_many(list_lottery_data)


