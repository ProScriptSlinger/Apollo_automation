import json
import pyautogui
from utils import *

user_home = os.path.expanduser('~')
downloads_path = os.path.join(user_home, 'Downloads')

def wait_for_downloads(download_path, timeout=60):
    """ Waits for a download to complete by monitoring the download directory """
    seconds_waited = 0
    while True:
        # Check for any files in the download directory
        if any(file.endswith('.crdownload') for file in os.listdir(download_path)):
            sleep(1)
            seconds_waited += 1
            if seconds_waited > timeout:
                raise Exception("Download timed out")
        else:
            break

clicker = "arguments[0].click();"

# Function to perform actions with explicit wait for clickable elements
def click_element(driver, locator_type, locator_value):
    try:
        # Wait until the element is clickable
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((locator_type, locator_value))
        )
        # Click the element
        element.click()
    except Exception as e:
        # Print or log exception if element is not found/clickable
        print(f"Element not found or not clickable: {e}")

def login(driver, user, pasw, url):
    try:
        driver.get(url)
        driver.find_element(By.XPATH, '//input[@name="email"]').send_keys(user)
        driver.find_element(By.XPATH, '//input[@name="password"]').send_keys(pasw)
        sleep(0.5)
        submit = driver.find_element(By.XPATH, '//button[@data-cy="login-button"]')
        driver.execute_script(clicker, submit)
        sleep(5)
        return  driver
    except:
        pass

def main(driver, url, user, pasw, index):
    try:
        driver = login(driver, user, pasw, url)
        print(f"Logged in with account {index}: {user}")
        download_url = "https://app.apollo.io/#/settings/imports-and-exports/exports"
        driver.get(download_url)
        click_element(driver, By.CSS_SELECTOR, ".zp-icon.apollo-icon.apollo-icon-download.zp_mMqLX.zp_YicAV.zp_EASSb")
        sleep(3)
        pyautogui.press('enter')
        sleep(2)
        wait_for_downloads(downloads_path)
        

    except Exception as e:
        print(e)
        # status_updater(index, 'Not found')


if __name__ == '__main__':
    df = pd.read_csv('Accounts.csv', dtype={'Email':str}, encoding='utf-8', encoding_errors='ignore')
    for user, pasw, index in account_selector():
        driver = get_browser(headless=False)
        driver.implicitly_wait(30)
        driver.maximize_window()
        try:
            main(driver=driver, url='https://app.apollo.io/#/contacts/import', user = user, pasw = pasw, index = index)
        finally:
            driver.quit()