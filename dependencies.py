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
import glob
import os
#key vars
base_url = 'https://www.gov.uk/check-mot-history'
search_url = 'https://www.check-mot.service.gov.uk/'
pdf_folder = r"C:\Users\Makario\Documents\ldf_test_pdfs" # enter folder to save pdfs here
#function for test data
def read_data(csv_path = ''):
    '''A function to read data into pandas dataframe.
    Takes CSV path as an input. In case no path provided uses test data.'''
    test_data = {
    'car_reg_nr':[
        'YT16JUK',
        'LT65DHJ',
        'YB65OXC',
        'KW17SRV',
        'DP64FLG',
        'RE66XAR',
        'KX15XTK',
        'VE17YNZ',
        'YR61WPU'
    ],
    'v5c_nr': [
        '9169 846 1671',
        '9060 603 1123',
        '1043 125 0082',
        '9069 672 0251',
        '8297 504 2939',
        '9033 672 0654',
        '9316 510 5366',
        '1179 678 5625',
        '7293 847 1230'
    ]
       }
    df = pd.DataFrame.from_dict(test_data)
    if csv_path != '' or csv_path is None: df = pd.read_csv(csv_path)
    return df
def read_mot_valid(driver):
    mot_hdr = driver.find_element(By.XPATH, "//span[contains(text(), 'MOT valid until')]").find_element(By.XPATH, '..')
    strs = mot_hdr.get_attribute('innerHTML').split('\n')
    mot_date = datetime.strptime(strs[len(strs) - 1].strip(), '%d %B %Y')
    return mot_date
def rename_file(pdf_folder, new_name):
    files = glob.glob(f'{pdf_folder}\\*') #change slashes when working on mac
    latest_file = max(files, key = os.path.getctime) #find the most recent file by creation time
    if os.path.exists(new_name): os.remove(new_name) #remove old file with the same name
    os.rename(latest_file, new_name) # move to folder with the script with the desired name