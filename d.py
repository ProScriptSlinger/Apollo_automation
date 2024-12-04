from utils import * 
from main import login 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

clicker = "arguments[0].click();"

with open('Config.json', 'r') as cfile:
    config = json.load(cfile)

time_limit = config['time_limit']
sleep(5)
def main(driver, url):
    try:
        df = pd.read_csv('Accounts.csv', dtype={'Email':str, 'Password':str, 'File_1':str, 'Status':str}, encoding='utf-8', encoding_errors='ignore')
        for index, row in df.iterrows():
            user = df.loc[index, 'Email']
            pasw = df.loc[index, 'Password']
            files = df.loc[index, 'File_1']
            status = df.loc[index, 'Status']
            if not pd.isna(files) and pd.isna(status):
                driver = login(driver, user, pasw, url)
                sleep(2)
                driver.get('https://app.apollo.io/#/people')
                sleep(2)
                files = files.split(',')
                try:
                    
                    Lists = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//span[contains(text(), "Lists")]')))
                    driver.execute_script(clicker, Lists)

                    create_list = driver.find_element(By.XPATH, '//div[contains(text(), "Select lists...")]')
                    create_list_input = driver.execute_script("return arguments[0].nextElementSibling;", create_list)
                    for file in files:
                        create_list_input.send_keys(file)
                        create_list_input.send_keys(Keys.ENTER)
                        sleep(5)
                    sleep(10)

                    select_all = driver.execute_script("return document.querySelector('button.finder-select-multiple-entities-button')")
                    if select_all is None:
                        driver.execute_script("""document.querySelector('button[aria-label="View more options to select rows"]').click();""")
                        sleep(1)
                        driver.execute_script("""document.querySelector('input[value="all"]').click();""")
                        sleep(1)
                        driver.execute_script("""document.querySelector('button[type="submit"]').click();""")
                        sleep(5)
                        export = driver.find_element(By.XPATH, '//span[contains(text(), "Export")]')
                        driver.execute_script("arguments[0].click(); ", export)
                        sleep(3)
                        driver.execute_script("""document.querySelector('button[data-cy="confirm"]').click();""")
                        sleep(10)
                    else:
                        SELECT_ALL = True
                        while SELECT_ALL:
                            try:
                                driver.execute_script(clicker, select_all)
                                SELECT_ALL = False
                            except:
                                pass 
                            sleep(2)
                            select_all = driver.execute_script("return document.querySelector('button.finder-select-multiple-entities-button')")

                        select_this_page = driver.find_element(By.XPATH, '//a[contains(text(), "Select this page")]')
                        select_all_people = driver.execute_script("return arguments[0].nextElementSibling;", select_this_page)
                        driver.execute_script(clicker, select_all_people)

                        sleep(2)
                        export_button = driver.find_element(By.XPATH, "//button[@data-cy='toolbar-action-export-button']")
                        driver.execute_script(clicker, export_button)
                        sleep(3)
                        confirm = driver.find_element(By.XPATH, "//button[@data-cy='confirm']")
                        driver.execute_script(clicker, confirm)
                        try:
                            download = WebDriverWait(driver, time_limit).until(
                                EC.visibility_of_element_located((By.XPATH, "//button[@data-cy='download-csv']"))
                            )
                        except:
                            pass 

                    # driver.execute_script(clicker, download)

                    # sleep(10)
                    # profile = driver.find_element(By.XPATH, "//button[@data-cy='user-profile']")
                    # driver.execute_script(clicker, profile)
                    # sleep(1)
                    # logout = driver.find_element(By.XPATH, "//div[@data-cy='logout']")
                    # driver.execute_script(clicker, logout)
                    # sleep(2)
                    # updated
                    df.loc[index, 'Status'] = 'Downloaded'
                    df.to_csv('Accounts.csv', index=False)

                    driver.quit()
                    driver = get_browser_d()
                    driver.implicitly_wait(15)
                    driver.maximize_window()
                except Exception as e:
                    print(e)


    except Exception as e:
        print(e)

if __name__ == '__main__':
    driver = get_browser_d()
    driver.implicitly_wait(15)
    driver.maximize_window()
    main(driver, 'https://app.apollo.io/#/people')