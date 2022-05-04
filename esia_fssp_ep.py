'''
Парсинга сайта Госуслуги.
Раздел ФССП - сведения о наличие ИП.
'''

from bs4 import BeautifulSoup
import fake_useragent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys     # Модуль для нажатия кнопки Enter (например при авторизации)
import pickle
import time
from auth_data import esia_di_login, esia_di_password
import csv


def esia_input():
    list_result = []

    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36")
    driver = webdriver.Chrome(
        executable_path="/media/maks/Новый том/Python/lessons/linux_puthon_lessons/parsing_lessons/webdriver/chromedriver_linux64/chromedriver",
        options=options
    )

    xpath_button = '/html/body/portal-root/header/lib-header/div/div/div[2]/div[2]/div/div/lib-login[2]/a'
    xpath_enter = '/html/body/esia-root/div/esia-idp/div/div[1]/form/div[3]/button'

    try:
        driver.get("https://esia.gosuslugi.ru")
        time.sleep(2)

        login = driver.find_element(By.ID, "login")
        login.clear()                                  # Очистка поля от данных
        time.sleep(1)
        password = driver.find_element(By.ID, "password")
        password.clear()                                  # Очистка поля от данных
        time.sleep(1)


        login.send_keys(esia_di_login)                    # ввод логина и пароля
        password.send_keys(esia_di_password)
        password.send_keys(Keys.ENTER)                    # вход по нажатии Enter, после ввода пароля
        time.sleep(3)

        # driver.get_cookies()     # разобраться для чего данная конструкция

        driver.find_element(By.CLASS_NAME, 'btn-gotoback').click()    # нажатие ссылки
        time.sleep(5)

        xpath_company = '/html/body/app-root/main/div/div/div/div/button[2]'
        driver.find_element(By.XPATH, xpath_company).click()
        time.sleep(10)


        # xpath_filter = '/html/body/lk-root/main/lk-notifications/div/div[2]/div[1]/div/div/div[1]/lk-feeds-filter/div'
        # driver.find_element(By.XPATH, xpath_filter).click()
        # time.sleep(2)
        # xpath_gosmail = '/html/body/lk-root/main/lk-notifications/div/div[2]/div[1]/div/div/div[1]/lk-feeds-filter/div/div[2]/ul/li[9]'
        # driver.find_element(By.XPATH, xpath_gosmail).click()
        # time.sleep(2)
        #
        # page_notifications = driver.page_source
        #
        # soup = BeautifulSoup(page_notifications, 'lxml')
        #
        # notifications = soup.find_all('div', class_='status status-inbox feed-status')
        # print(f'Количество элементов_{len(notifications)}')
        #
        # count = 1
        # for i in notifications[:3]:
        #     xpath_mail = f'/html/body/lk-root/main/lk-notifications/div/div[2]/div[1]/div/lib-feeds/a[{count}]'
        #     driver.find_element(By.XPATH, xpath_mail).click()
        #     print(f'Control_{count}')
        #     time.sleep(3)
        #
        #     # with open(f'index_page_{count}.html', 'w') as file:                   # Сохраняю HTML код страницы в файл !!!! Данный код только для записи HTML кода в файл!!!
        #     #     file.write(driver.page_source)
        #
        #     html_page = driver.page_source
        #     result = read_html(html_page)
        #     list_result.append(result)
        #
        #     time.sleep(3)
        #     driver.back()             # возврат на предыдущую страницу
        #     time.sleep(3)
        #     count += 1


    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

    return list_result


def read_html(html_page):
    soup = BeautifulSoup(html_page, "lxml")
    block = soup.find('div', class_='message-wrapper col-3 col-md-6 col-lg-12').text
    return block

def save_file(items):
    # print(items)
    with open('data/' + f'TEST.csv', 'w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['Госпочта'])

    for item in items:
        with open('data/' + f'TEST.csv', 'a') as file:                           #Открываю файл на добавление данных 'a'
            writer = csv.writer(file)
            writer.writerow([item])

def main():
    # save_file(esia_input())
    esia_input()
    # read_html()

if __name__ == '__main__':
    main()