#libs
import pandas as pd
from random import randint
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver import Chrome
#key vars
cars = [
    'YT16JUK',
    'LT65DHJ',
    'KW17SRV',
    'YB65OXC',
    'LA70VOD',
    'DP64FLG'
]
base_url = 'https://www.gov.uk/check-mot-history'
search_url = 'https://www.check-mot.service.gov.uk/'

#driver options
options = webdriver.ChromeOptions()
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = Chrome(service=Service(ChromeDriverManager().install()), options=options)
# driver.get(search_url)

for c in cars:
    driver.get(search_url)
    forms = driver.find_elements(By.CSS_SELECTOR, 'input[type *= "text"]')
    # find the needed element from the hidden ones by clicking them
    for f in forms:
        if f.get_attribute('class') != 'form-control': continue
        try:
            f.click()
            search_form = f
            break
        except:
            continue
    search_form.send_keys(c)
    driver.find_element(By.NAME, 'submit').click()
    sleep(randint(0, 5))  # remove or change pauses here if neded
    # Parse date here

    driver.delete_all_cookies() # clean cookies every loop just in case