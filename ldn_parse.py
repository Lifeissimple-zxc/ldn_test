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
from datetime import datetime
from dependencies import search_url, pdf_folder, read_data, read_mot_valid, rename_file

#driver options
options = webdriver.ChromeOptions()
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('prefs', {
"download.default_directory": pdf_folder, #Change default directory for downloads
"download.prompt_for_download": False, #To auto download the file
"download.directory_upgrade": True,
"plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
})

driver = Chrome(service = Service(ChromeDriverManager().install()), options = options)

#create dataframe to store logs
logs = pd.DataFrame(columns = [
    'timestamp', 'car', 'v5c_nr', 'mot_check', 'pdf_status', 'filename'
])

df = read_data() #paste path to csv with inputs here
cars, nums = list(df[df.columns[0]]), list(df[df.columns[1]])
print('\t'.join(list(logs.columns)))

# Data collection starts here
for c, n in zip(cars, nums):
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
    f.send_keys(c)
    driver.find_element(By.NAME, 'submit').click()
    sleep(randint(0, 5))  # remove or change pauses here if needed
    log_stamp = datetime.now()

    mot_date = read_mot_valid(driver)  # extract mot_date
    if mot_date <= datetime.now():
        mot_check = 'None valid MOT found'
        # record result here instead of print
        print(c, mot_date, mot_check, datetime.now())
        logs = logs.append({
            'timestamp': log_stamp,
            'car': c,
            'v5c_nr': n,
            'mot_check': mot_check,
            'pdf_status': '',
            'filename': ''
        }, ignore_index=True)
        print('\t'.join([str(log_stamp), c, n, mot_check, '', '']))

    mot_check = 'Valid MOT found'
    log_stamp = datetime.now()

    # block to enter v5c
    driver.find_element(By.ID, 'mot-history-description').click()
    sleep(1)
    driver.find_element(By.XPATH, "//span[contains(text(), 'View test certificate')]").find_element(By.XPATH,
                                                                                                    "..").click()
    v5c_input = driver.find_elements(By.CSS_SELECTOR, "input[id = 'v5c-print-cert-input']")[0].send_keys(n)
    driver.find_elements(By.CSS_SELECTOR, "input[id = 'show-test-certificate']")[0].click()
    sleep(1)
    # check for unexpected error try / except
    try:
        # check for pdf availability try / except
        try:
            driver.implicitly_wait(5)
            err_msg = driver.find_element(By.CSS_SELECTOR, "div[class = 'validation-message']").get_attribute('innerHTML')
            pdf_status = err_msg
            pdf_file = ''
        except:
            driver.find_element(By.ID,"cert-download-link").click()  # this click downloads file to the folder specifies in options
            pdf_file = f'{n}.pdf'
            rename_file(pdf_folder=pdf_folder, new_name=pdf_file)
            pdf_status = 'downloaded'
    except:
        pdf_status = 'unexpected error'
        # log
        logs = logs.append({
            'timestamp': log_stamp,
            'car': c,
            'v5c_nr': n,
            'mot_check': mot_check,
            'pdf_status': pdf_status,
            'filename': ''
        }, ignore_index=True)
        print('\t'.join([str(log_stamp), c, n, mot_check, pdf_status, '']))
    # add print statements
    driver.delete_all_cookies()
    log_stamp = datetime.now()
    # log
    logs = logs.append({
        'timestamp': log_stamp,
        'car': c,
        'v5c_nr': n,
        'mot_check': mot_check,
       'pdf_status': pdf_status,
        'filename': pdf_file
    }, ignore_index=True)
    print('\t'.join([str(log_stamp), c, n, mot_check, pdf_status, pdf_file]))
out_csv = 'logs.csv'
print(f'Data collection - done! Saving logs to {out_csv}.')
logs.to_csv(out_csv, index=False)
print('All Steps are finished.')

