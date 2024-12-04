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

def get_next_valid_account(acc, oldIndex):
    while True:
        try:
            user, pasw, index = next(acc)
            if index > oldIndex:
                return user, pasw, index
        except StopIteration:
            # Handle the case where there are no more valid accounts.
            # You might want to raise an exception, return None, etc.
            return None

def main(driver, url, oldIndex = -1):
    schedule_remover = True
    file_name = str()
    acc = account_selector()
    result = get_next_valid_account(acc, oldIndex)
    if result:
        user, pasw, index = result
        # Process the valid account here
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
                        status_updater(index, "Failed")
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
                    status_updater(index, "Failed")
                    pass 
                submit = driver.find_element(By.XPATH, "//button[@type='submit']")
                driver.execute_script(clicker, submit)
                # print('3')
                sleep(up_time)
                # while driver.current_url == "https://app.apollo.io/#/contacts/import":
                #     sleep(2)
                # print('3')
                
                sleep(5)
                file_updater(index, file_name)
                status_updater(index, "Uploaded")
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
            status_updater(index, "Failed")
            driver = get_browser(headless=False)
            driver.implicitly_wait(30)
            driver.maximize_window()
            main(driver=driver, url='https://app.apollo.io/#/contacts/import', oldIndex=index)
            print(e)
    else:
        print("No valid account found.")


if __name__ == '__main__':
    driver = get_browser(headless=False)
    driver.implicitly_wait(30)
    driver.maximize_window()
    main(driver=driver, url='https://app.apollo.io/#/contacts/import')