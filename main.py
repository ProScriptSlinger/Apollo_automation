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
print("File Directory: ", file)

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
    schedule_remover = True
    file_name = str()
    acc = account_selector()
    user, pasw, index, file_name = next(acc)
    try:
        driver = login(driver, user, pasw, url)
        files = get_files_in_directory(file)

        counter = 0
        for index_, i in enumerate(files, start=1):
            driver.get('https://app.apollo.io/#/contacts/import')
            sleep(2)
            success = False
            while success is False:
                try:
                    file_name = i.rsplit('.', maxsplit=1)[0].rsplit('\\',maxsplit=1)[-1]
                    print("File Name: ", file_name)
                    csv_input = driver.find_element(By.TAG_NAME, 'input')
                    if csv_input.get_attribute('type') == 'text':
                        driver.find_elements(By.TAG_NAME, 'input')[1].send_keys(i)
                    elif csv_input.get_attribute('type') == 'file':
                        driver.find_elements(By.TAG_NAME, 'input')[0].send_keys(i)
                    # print('looping')
                    sleep(2)
                    success = True
                except Exception as e:
                    pass 

            # print('1')
            try:
                create_list = driver.find_element(By.XPATH, '//div[contains(text(), "Enter or create lists...")]')
                create_list_input = driver.execute_script("return arguments[0].nextElementSibling;", create_list)
                create_list_input.send_keys(file_name)
                # print('2')
                sleep(1)
                create_list_input.send_keys(Keys.SPACE)
                sleep(1)
                create_list_input.send_keys(Keys.ENTER)
                sleep(1)
            except Exception as e:
                pass 
            submit = driver.find_element(By.XPATH, "//button[@type='submit']")
            driver.execute_script(clicker, submit)
            # print('3')
            sleep(up_time)
            # while driver.current_url == "https://app.apollo.io/#/contacts/import":
            #     sleep(2)
            # print('3')
            driver.get('https://app.apollo.io/#/enrichment-status/data-health-center?page=1')
            schedule = driver.find_element(By.XPATH, '//*[contains(text(), "Schedule enrichment")]')
            driver.execute_script(clicker, schedule)
            # # checking existing schedule

            schedure_flag = True
            try:
                driver.implicitly_wait(5)
                driver.find_element(By.XPATH, '//span[contains(text(), "Nothing scheduled yet!")]')
                schedure_flag = False
            except Exception as e:
                pass
            if schedule_remover:
                if schedure_flag:
                    sleep(1)
                    trash_items = driver.execute_script("return document.querySelectorAll('.apollo-icon-trash').length")
                    for trash in range(trash_items):
                        try:
                            driver.execute_script(f"document.querySelector('.apollo-icon-trash').click();")
                            sleep(2)
                            delete = driver.find_elements(By.XPATH, "//*[contains(text(), 'Delete')]")[1]
                            driver.execute_script(clicker, delete)
                            sleep(6)
                            driver.execute_script("document.querySelectorAll('i.mdi-close')[1].click();")
                            sleep(2)
                            schedule = driver.find_element(By.XPATH, '//*[contains(text(), "Schedule enrichment")]')
                            driver.execute_script(clicker, schedule)
                            sleep(1)
                        except:
                            pass
                        schedule_remover = False

            add_new = driver.find_element(By.XPATH, '//*[contains(text(), "Add new")]')
            driver.execute_script(clicker, add_new)
            sleep(1)
            driver.execute_script("document.querySelectorAll('.input-container input')[1].click();")
            driver.execute_script("document.querySelector('.zp_Mjo7b button').click();")
            sleep(1)
            driver.execute_script("document.querySelector('a.zp-menu-item').click();")
            driver.find_element(By.XPATH, '//input[@name="creditLimit"]').send_keys('999')
            sleep(1)
            submit = driver.find_element(By.XPATH, "//button[@data-cy='confirm']")
            driver.execute_script(clicker, submit)
            sleep(1)
            driver.find_element(By.XPATH, '//input[@name="enrichmentName"]').send_keys(file_name)
            add_filter = driver.find_element(By.XPATH, "//*[contains(text(), 'Add filters')]")
            driver.execute_script(clicker, add_filter)
            sleep(2)
            driver.execute_script("""
            const elements = document.querySelectorAll('.zp-accordion-header.zp_r3aQ1');
            elements.forEach(function(element) {
                if (element.textContent.includes('Lists')) {
                    element.click();
                }
            });
        """)

            sleep(1)
            # driver.find_elements(By.TAG_NAME, 'input')[5].send_keys(file_name)
            # sleep(1)
            # driver.find_elements(By.TAG_NAME, 'input')[5].send_keys(Keys.ENTER)
            driver.find_element(By.CSS_SELECTOR, ".Select-control .Select-input").send_keys(file_name)
            sleep(2)

            # Attempt to trigger file upload
            driver.find_element(By.CSS_SELECTOR, ".Select-control .Select-input").send_keys(Keys.ENTER)
            sleep(1)
            apply_filter = driver.find_element(By.XPATH, '//*[contains(text(), "Apply Filters")]')
            driver.execute_script(clicker, apply_filter)
            sleep(2)
            print('Apply')
            schedule_ = driver.find_element(By.XPATH, "//button[@data-cy='confirm']")
            driver.execute_script(clicker, schedule_)
            sleep(5)
            file_updater(index, file_name)
            counter += 1
            print("Index: ",counter)
            if counter == limit:
                counter = 0
                # print('4')
                driver.quit()
                driver = get_browser()
                driver.implicitly_wait(30)
                driver.maximize_window()
                user, pasw, index = next(acc)
                driver = login(driver, user, pasw, url)
                schedule_remover = True
                
            driver.refresh()
            # print('5')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    driver = get_browser(headless=False)
    driver.implicitly_wait(30)
    driver.maximize_window()
    main(driver=driver, url='https://app.apollo.io/#/contacts/import')