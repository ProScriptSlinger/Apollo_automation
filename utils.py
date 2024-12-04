from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv, re, os, json
from time import sleep
from datetime import datetime
import pandas as pd

import undetected_chromedriver as uc
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def account_selector():
    acc_list = []
    df = pd.read_csv('Accounts.csv', dtype={'Email':str, 'Password':str, 'File_1':str, 'File_2':str}, encoding='utf-8', encoding_errors='ignore')
    for index, row in df.iterrows():
        user = df.loc[index, 'Email']
        pasw = df.loc[index, 'Password']
        file_name = df.loc[index, 'File_1']
        yield user, pasw, index

def account_selector_schedule():
    try:
        # Read the CSV file
        df = pd.read_csv('Accounts.csv', dtype={'Email':str, 'Password':str, 'File_1':str, 'File_2':str, 'Status':str}, encoding='utf-8', encoding_errors='ignore')
        
        # Iterate over DataFrame rows
        for index, row in df.iterrows():
            user = row['Email']
            pasw = row['Password']
            file_name = row['File_1']
            status = row['Status']
            
            # Check if Status is empty
            if pd.isna(status):
                return user, pasw, index, file_name
        
        # If no suitable account is found, raise an exception or return None
        print("No accounts with an empty status found.")
        return None
    
    except FileNotFoundError:
        print("Accounts.csv file not found.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def status_updater(index, status):
    try:
        # Read the CSV file
        df = pd.read_csv('Accounts.csv', dtype={'Email': str, 'Password': str, 'File_1': str, 'File_2': str, 'Status': str}, encoding='utf-8', encoding_errors='ignore')
        # Check and update the Status column
        if index >= len(df) or index < 0:
            print("Index out of bounds. Please ensure the provided index is valid.")
            return
        if pd.isna(df.loc[index, 'Status']):
            df.loc[index, 'Status'] = status
        else:
            df.loc[index, 'Status'] = df.loc[index, 'Status'] + "," + status
        # Write back to the CSV file
        with open('Accounts.csv', 'w', newline='', encoding='utf-8', errors='ignore') as file:
            df.to_csv(file, index=False)
        
        print("Status updated successfully.")
        
    except PermissionError:
        print("Permission denied. Please close any programs using the file, check permissions, or try running as an administrator.")
    except FileNotFoundError:
        print("File not found. Please ensure 'Accounts.csv' exists in the specified directory.")
    except IndexError:
        print("Index out of bounds. Please ensure the provided index is valid.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def file_updater(index, file_name):
    df = pd.read_csv('Accounts.csv', dtype={'Email': str, 'Password': str, 'File_1': str, 'File_2': str, 'Status': str}, encoding='utf-8', encoding_errors='ignore')
    if pd.isna(df.loc[index, 'File_1']):
        df.loc[index, 'File_1'] = file_name
    else:
        df.loc[index, 'File_1'] = df.loc[index, 'File_1'] + "," + file_name
    df.to_csv('Accounts.csv', index=False)


def get_files_in_directory(directory):
    file_paths = []
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            file_paths.append(file_path)
    return file_paths




def get_browser(headless=False, sel=False):
    download_directory = os.path.join(os.getcwd(), "Data")
    agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/116.0.1216.0 Safari/537.2'
    s = Service(executable_path=ChromeDriverManager().install())
    # s = Service(executable_path='chromedriver.exe')
    chrome_option = webdriver.ChromeOptions()
    if headless:
        chrome_option.add_argument('--headless')
        chrome_option.add_argument("--no-sandbox")
        chrome_option.add_argument("--disable-dev-shm-usage")
    chrome_option.add_argument(f'user-agent={agent}')
    chrome_option.add_argument('--log-level=3')
    chrome_option.page_load_strategy = 'eager'
    chrome_option.add_argument('--ignore-certificate-errors')
    chrome_option.add_argument('--ignore-ssl-errors')
    chrome_option.add_argument('--ignore-certificate-errors-spki-list')
    chrome_option.add_argument('--incognito')
    chrome_option.add_argument("--disable-blink-features=AutomationControlled")
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_option.add_experimental_option("prefs", prefs)
    chrome_option.add_experimental_option("useAutomationExtension", False)
    chrome_option.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(service=s, options=chrome_option)
    return driver


def get_browser_d(headless=False, sel=False):
    download_directory = os.path.join(os.getcwd(), "Data")
    agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/116.0.1216.0 Safari/537.2'
    # s = Service(executable_path=ChromeDriverManager().install())#"
    s = Service(executable_path='chromedriver.exe')
    chrome_option = webdriver.ChromeOptions()
    if headless:
        chrome_option.add_argument('--headless')
        chrome_option.add_argument("--no-sandbox")
        chrome_option.add_argument("--disable-dev-shm-usage")
        chrome_option.add_argument(f'user-agent={agent}')
    chrome_option.add_argument('--log-level=3')
    chrome_option.page_load_strategy = 'eager'
    chrome_option.add_argument('--ignore-certificate-errors')
    chrome_option.add_argument('--ignore-ssl-errors')
    chrome_option.add_argument('--ignore-certificate-errors-spki-list')
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_option.add_experimental_option("prefs", prefs)
    chrome_option.add_experimental_option("useAutomationExtension", False)
    chrome_option.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_option.add_experimental_option("prefs", {
        "download.default_directory": download_directory,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    
    driver = webdriver.Chrome(service=s, options=chrome_option)
    return driver








