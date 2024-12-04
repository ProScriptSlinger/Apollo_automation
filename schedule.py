import json

from utils import *

if not os.path.exists('Data'):
    os.mkdir('Data')

cur_date = datetime.now().strftime("%d_%m_%Y_%M")
clicker = "arguments[0].click();"

with open('Config.json', 'r') as jfile:
    config = json.load(jfile)

limit = config['upload_limit']
up_time = config['uploading_time']

file = os.path.join(os.getcwd(), 'csv-upload')

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

def element_exists(driver, locator_type, locator_value):
    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((locator_type, locator_value))
        )
        return True
    except Exception as e:
        print(f"Element does not exist: {e}")
        return False
    
# Function to send text to an input field
def input_text(driver, locator_type, locator_value, text):
    input_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((locator_type, locator_value))
    )
    
    input_element.clear()
    input_element.send_keys(text)

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

def main(driver, url):
    result = account_selector_schedule()
    try:
        if result:
            user, pasw, index, file_name = result
            driver = login(driver, user, pasw, url)
            print(f"Logged in with account {index}: {user}")
            enrichment_url = "https://app.apollo.io/#/enrichment-status/data-health-center"
            driver.get(enrichment_url)
            click_element(driver, By.CSS_SELECTOR, "button[data-product-tour-id='view-schedule-enrichment-button-selector']")

            # Delete previous jobs
            if element_exists(driver, By.CSS_SELECTOR, "input.zp_zzdNt"):
                click_element(driver, By.CSS_SELECTOR, "input.zp_zzdNt")
                click_element(driver, By.CSS_SELECTOR, ".zp-icon.apollo-icon.apollo-icon-trash.zp_QUSTG.zp_D0r3Q.zp_K7tmh.zp_NGTfw")
                click_element(driver,   By.CSS_SELECTOR, ".zp_qe0Li.zp_FG3Vz.zp_WgYDT.zp_h2EIO:nth-of-type(2)")
            click_element(driver, By.XPATH, "//span[text()='Add new']")

            # Define Object to enrich
            click_element(driver, By.CSS_SELECTOR, ".zp_wBCO3.zp_HkcK4")
            click_element(driver, By.CSS_SELECTOR, ".zp_syGaH.zp_O7waS")
            click_element(driver, By.CSS_SELECTOR, "button[id='save-object']")

            # Select enrichment type
            click_element(driver, By.CSS_SELECTOR, ".zp_wlG4j.zp_y3qeA")
            click_element(driver, By.XPATH, '//div[@class="zp_fzaGw zp_kwjTA"][2]//label')
            click_element(driver, By.CSS_SELECTOR, "button[id='save-action']")

            click_element(driver, By.CSS_SELECTOR, ".zp_wBCO3.zp_HkcK4")
            click_element(driver, By.XPATH, "//div[span[text()='Lists']]")

            input_text(driver, By.CLASS_NAME, "Select-input", file_name)

            click_element(driver, By.CSS_SELECTOR, ".Select-option")
            click_element(driver, By.XPATH, "//button[span[text()='Save']]")

            # Cadence
            click_element(driver, By.CSS_SELECTOR, ".zp_wBCO3.zp_HkcK4")
            click_element(driver, By.CSS_SELECTOR, '.zp_VTl3h.zp_xqxgc')
            click_element(driver, By.CSS_SELECTOR, 'a.zp_lmny2')

            input_text(driver, By.CLASS_NAME, "zp_iw9gb", "999")
            
            click_element(driver, By.CSS_SELECTOR, "button[id='save-cadence']")
            click_element(driver, By.CSS_SELECTOR, "button[id='go-to-settings']")

            input_text(driver, By.CLASS_NAME, "zp_iw9gb", file_name)

            # Finalize the process
            click_element(driver, By.CSS_SELECTOR, "button[id='save-enrichment-job']")

            # # Update Status
            status_updater(index, 'Scheduled')

            # Logout
            # sidebar_element = driver.find_element(By.ID, "sideNavExpanded")
            # aria_hidden_value = sidebar_element.get_attribute('aria-hidden')
            # if aria_hidden_value == "true":
            #     click_element(driver, By.CSS_SELECTOR, '.zp_A4j9S')
            # click_element(driver, By.CSS_SELECTOR, '.zp_qe0Li.zp_VsP8_')
            # click_element(driver, By.XPATH, "//div[span[text()='Log out']]")
        else:
            print("Failed to select an account.")

    except Exception as e:
        print(e)
        status_updater(index, 'Not found')


if __name__ == '__main__':
    df = pd.read_csv('Accounts.csv', dtype={'Email':str}, encoding='utf-8', encoding_errors='ignore')
    for _ in df.iterrows():
        driver = get_browser(headless=False)
        driver.implicitly_wait(30)
        driver.maximize_window()
        try:
            main(driver=driver, url='https://app.apollo.io/#/contacts/import')
        finally:
            driver.quit()