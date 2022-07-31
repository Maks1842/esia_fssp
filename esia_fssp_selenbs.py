'''
!!!ОСНОВНОЙ МОДУЛЬ ДЛЯ ПАРСИНГА ЕСИА!!!

Парсинга сайта Госуслуги.
Раздел ФССП - сведения о наличие ИП.

Авторизация с помощью selenium, парсинг - BeautifulSoup
'''
import os
import logging
import gc         # Сборщик мусора

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys     # Модуль для нажатия кнопки (например при авторизации)
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import pickle
import time
from datetime import date
# import datetime
from auth_data import esia_di_login, esia_di_password
import csv

logging.basicConfig(filename='example.log', filemode='w', level=logging.INFO)

def esia_parsing():

    # options = webdriver.ChromeOptions()
    # options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36")

    options = webdriver.FirefoxOptions()
    options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0")


    options.add_argument('--headless')     # Бот работает в фоновом режиме

    # # Драйвер для Chrome
    # driver = webdriver.Chrome(
    #     executable_path="/media/maks/Новый том/Python/work/esia_fssp/webdriver/chromedriver_linux64/chromedriver",
    #     options=options
    # )

    # Драйвер для Firefox
    driver = webdriver.Firefox(
        executable_path="/media/maks/Новый том/Python/work/esia_fssp/firefoxdriver/geckodriver-v0.31.0-linux64/geckodriver",
        options=options
    )

    driver.implicitly_wait(60)


    # driver.set_window_size(1920, 1080)
    driver.set_window_size(1800, 1000)

    try:
        driver.get("https://esia.gosuslugi.ru")
        print('start')

        login = driver.find_element(By.ID, "login")
        login.clear()
        password = driver.find_element(By.ID, "password")
        password.clear()

        login.send_keys(esia_di_login)                    # ввод логина и пароля
        password.send_keys(esia_di_password)
        password.send_keys(Keys.ENTER)                    # вход по нажатии Enter, после ввода пароля
        # print('login')
        time.sleep(3)

        # # cookies
        # cookies = driver.get_cookies()
        # pickle.dump(cookies, open('cookies_file', 'wb'))

        # Переход на страницу ЛК
        xpath_personal_account = 'btn-gotoback'
        driver.find_element(By.CLASS_NAME, xpath_personal_account).click()    # нажатие ссылки
        # print('personal_account')
        time.sleep(5)



        current_date = date.today()
        today = current_date.strftime("%d-%m-%Y")
        files = os.listdir()
        url_file = ''
        for file_url in files:
            if file_url == f'{today}.txt':
                url_file = file_url
                print(f'{url_file = }')

        if url_file != '':
            with open(url_file, 'r') as file:
                url_page_ip = file.read()
            driver.get(url_page_ip)
            time.sleep(5)
        else:
            # Выбор компании
            xpath_company = '//div[@class="grid-row"]/button[2]'
            # driver.implicitly_wait(10)
            driver.find_element(By.XPATH, xpath_company).click()
            print('company')
            time.sleep(3)


            # Переход на главную страницу Госуслуг
            xpath_esia = '//*[@id="header"]/div[2]/div/div/div/div/div/div[1]/a'
            # driver.implicitly_wait(10)
            driver.find_element(By.XPATH, xpath_esia).click()
            print('esia')
            time.sleep(3)


            # Переход в раздел "Услуги"
            # xpath_category = '//div[@class="flex-container justify-end"]/div[1]'
            xpath_category = '//a[@data-ng-href="/catalog?from=lmain"]'
            # driver.implicitly_wait(10)
            driver.find_element(By.XPATH, xpath_category).click()
            print('category')
            time.sleep(3)

            # Переход в раздел "Органы власти"
            xpath_structure = '//div[@class="limiter"]/div[2]'
            # driver.implicitly_wait(10)
            driver.find_element(By.XPATH, xpath_structure).click()
            print('structure')
            time.sleep(3)

            # Переход в раздел "ФССП"
            xpath_fssp = '//div[@class="popular-structure"]/div[2]/div[2]'
            # driver.implicitly_wait(10)
            driver.find_element(By.XPATH, xpath_fssp).click()
            print('fssp')
            time.sleep(3)

            # Выбор услуги по предоставлению инфы об ИП
            xpath_service_ip = '//div[@class="structure-passport-list ng-scope"]/a[2]'
            driver.find_element(By.XPATH, xpath_service_ip).click()
            print('service_ip')
            time.sleep(3)

            # Выбор инфы о наличие ИП
            xpath_information_ip = '//li[@data-ng-if="!service.hideAfterFilter"][2]'
            driver.find_element(By.XPATH, xpath_information_ip).click()
            print('information_ip')
            time.sleep(4)

            # Проверка наличия шаблона
            page_notifications = driver.page_source
            if 'conf-modal conf-modal--short' in page_notifications:
                driver.find_element(By.XPATH, '//div[@class="conf-modal__controls"]/lib-button[1]').click()
                print('проверка шаблона')
                time.sleep(4)

            # Выбор "Начать"
            xpath_start = '//div[@class="button-container"]'
            driver.find_element(By.XPATH, xpath_start).click()
            print('начать')
            time.sleep(4)

            # Выбор "Нет"
            xpath_no_button = '//epgu-constructor-answer-button[@class="quiz__item"][2]/epgu-cf-ui-long-button[@class="answer-btn"]'
            driver.find_element(By.XPATH, xpath_no_button).click()
            print('no_button')
            time.sleep(4)

            # Выбор "Верно" ФИО
            xpath_correctly_name = '//div[@class="button-container"]'
            driver.find_element(By.XPATH, xpath_correctly_name).click()
            print('correctly_name')
            time.sleep(4)

            # Выбор "Верно" организация
            xpath_correctly_user = '//div[@class="button-container"]'
            driver.find_element(By.XPATH, xpath_correctly_user).click()
            print('user')
            time.sleep(4)

            # Выбор "Верно" адрес регистрации
            xpath_correctly_registration = '//div[@class="button-container"]'
            driver.find_element(By.XPATH, xpath_correctly_registration).click()
            print('registration')
            time.sleep(4)

            # Выбор "Взыскатель"
            xpath_claimer = '//epgu-constructor-answer-button[@class="quiz__item"][2]/epgu-cf-ui-long-button[@class="answer-btn"]'
            driver.find_element(By.XPATH, xpath_claimer).click()
            print('claimer')
            time.sleep(4)

            # Выбор "Да"
            xpath_ok_start = '//epgu-constructor-answer-button[@class="quiz__item"][1]/epgu-cf-ui-long-button[@class="answer-btn"]'
            driver.find_element(By.XPATH, xpath_ok_start).click()
            print('загрузка должников')
            time.sleep(20)
            current_url = driver.current_url
            print(current_url)

            with open(f'{today}.txt', 'w') as file:
                file.write(current_url)
                file.close()


        # Подгрузка всех страниц с ИП
        print(f'start_pars')
        count_page = 1
        count = 0

        # Блок используется для возобновления парсинга с указанного места
        # for i in range(1, 2):                                          # Вторая цифра указывает номер страницы с которой надо возобновить парсинг (пока меняется в ручную)
        #     show1_more = '//div[@class="button-container"]'
        #     driver.find_element(By.XPATH, show1_more).click()
        #     print(f'Показать ещё (предварительно): стр_{count_page}')
        #     count_page += 1
        #     time.sleep(1)
        # count = count_page * 20


        create_file()

        while 'white button font-' in driver.page_source:
            executive_production = []
            if count > 18:
                show_more = '//div[@class="button-container"]'
                driver.find_element(By.XPATH, show_more).click()
                print(f'Показать ещё: стр_{count_page}')
                count_page += 1
                time.sleep(5)


            # Получение ссылок на ИП
            xpath_xx = '//div[@class="content-container"]|//div[@class="mb-24"]'
            items = driver.find_elements(By.XPATH, xpath_xx)
            number_items = len(items)
            logging.info(f'Количество ИП_{number_items}')
            print(f'count = {count}: Количество ИП_{number_items}')

            for i in range(count, number_items):
                print(f'ИП {count + 1}')
                logging.info(f'ИП {count + 1}')
                xpath_x = f'//app-fssp-list-item[{count + 1}]//div[@class="shadow-container"]/h3/a'
                driver.find_element(By.XPATH, xpath_x).click()
                time.sleep(1)
                # print('загрузка ИП')

                xpath_details_click = '//div[@class="toggle-link mb-24"]'
                driver.find_element(By.XPATH, xpath_details_click).click()
                time.sleep(0.5)


                html_page = driver.page_source
                result = read_html(count_page, count, html_page)

                executive_production.append(result)

                driver.back()
                time.sleep(0.5)
                count += 1
            save_file(executive_production)
            gc.collect()          # Сборщик мусора

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def read_html(count_page, count, html_page):
    # with open('data/fssp6.html', 'r') as file:
    #     html_page = file.read()
    soup = BeautifulSoup(html_page, "html.parser")

    number_ep = soup.find('h4', class_="main-title mb-16").text.strip()
    print(f'{number_ep = }')
    logging.info(f'{number_ep = }')
    if soup.find('p', class_="gray-text mb-8"):
        start_date = soup.find_all('p')[0].text.strip()
        # print(f'{start_date = }')
        end_date = soup.find_all('p')[1].text.strip()
        # print(f'{end_date = }')
    else:
        start_date = soup.find('p', class_="gray-text").text.strip()
        # print(f'{start_date = }')
        end_date = '-'
        # print(f'{end_date = }')

    main_debt_all = soup.find_all('div', class_="flex-container flex-column mb-16")
    # Проверка наличия задолженности
    if soup.find('span', class_="amount-owed mr-md-24 mb-24 mb-md-0"):
        current_debt = soup.find('span', class_="amount-owed mr-md-24 mb-24 mb-md-0").text.strip()
        # print(f'{current_debt = }')

        if 'Основной долг' in soup.text and 'Исполнительский сбор' in soup.text and 'Погашенная часть' in soup.text:
            main_debt = main_debt_all[0].find('span', class_="text-plain").text.strip()
            performance_fee = main_debt_all[1].find('span', class_="text-plain").text.strip()
            repaid_debt = main_debt_all[2].find('span', class_="text-plain").text.strip()
        elif 'Основной долг' in soup.text and 'Исполнительский сбор' in soup.text and not 'Погашенная часть' in soup.text:
            main_debt = main_debt_all[0].find('span', class_="text-plain").text.strip()
            performance_fee = main_debt_all[1].find('span', class_="text-plain").text.strip()
            repaid_debt = '-'
        elif 'Основной долг' in soup.text and not 'Исполнительский сбор' in soup.text and not 'Погашенная часть' in soup.text:
            main_debt = main_debt_all[0].find('span', class_="text-plain").text.strip()
            performance_fee = '-'
            repaid_debt = '-'
        elif 'Основной долг' in soup.text and not 'Исполнительский сбор' in soup.text and 'Погашенная часть' in soup.text:
            main_debt = main_debt_all[0].find('span', class_="text-plain").text.strip()
            performance_fee = '-'
            repaid_debt = main_debt_all[1].find('span', class_="text-plain").text.strip()
        else:
            main_debt = '-'
            performance_fee = '-'
            repaid_debt = '-'
    else:
        current_debt = soup.find('span', class_="amount-owed mr-md-24 mb-24 mb-md-0 gray-amount").text.strip()
        main_debt = main_debt_all[0].find('span', class_="text-plain").text.strip()
        performance_fee = '-'
        repaid_debt = main_debt_all[1].find('span', class_="text-plain").text.strip()

    border_block_all = soup.find_all('div', class_="border-block mb-24")
    if 'Причина' in soup.text:
        reason = border_block_all[1].find_all('div')[0].find('span', class_="info-text").text.strip()
        footing = border_block_all[1].find_all('div')[1].find('span', class_="info-text").text.strip()
    else:
        reason = '-'
        footing = border_block_all[1].find_all('div')[0].find('span', class_="info-text").text.strip()

    debtor = border_block_all[2].find('p').text.strip()
    birthday = border_block_all[2].find_all('div')[0].find('span', class_="info-text").text.strip()
    if 'Место рождения' in soup.text:
        place_of_birth = border_block_all[2].find_all('div')[1].find('span', class_="info-text").text.strip()
    else:
        place_of_birth = ''
    # restriction = soup.find(By.XPATH, '//div[@class="border-block mb-24"][4]/div/div/span').text.strip()
    # print(f'{restriction = }')
    creditor =border_block_all[4].find('p').text.strip()
    bailiff = border_block_all[5].find('p').text.strip()
    bailiff_tel = border_block_all[5].find_all('div')[0].find('span', class_="info-text").text.strip()
    rosp = border_block_all[5].find_all('div')[1].find('span', class_="info-text").text.strip()
    address_rosp = border_block_all[5].find_all('div')[2].find('span', class_="info-text").text.strip()

    result = {
        '№ Страницы': count_page,
        '№ ПП': count + 1,
        '№ Исполнительного производства': number_ep,
        'Начало ИП': start_date,
        'Окончание ИП': end_date,
        'Текущая задолженность': current_debt,
        'Основной долг': main_debt,
        'Исполнительский сбор': performance_fee,
        'Погашенная часть': repaid_debt,
        'Причина': reason,
        'Основание': footing,
        'Должник': debtor,
        'Дата рождения': birthday,
        'Место рождения': place_of_birth,
        # 'Ограничения': restriction,
        'Взыскатель': creditor,
        'Судебный пристав': bailiff,
        'Телефон пристава': bailiff_tel,
        'РОСП': rosp,
        'Адрес РОСП': address_rosp
    }

    return result


def create_file():
    current_date = date.today()
    today = current_date.strftime("%d-%m-%Y")
    with open(f'data/fssp_{today}.csv', 'w', encoding='utf-8') as file:                 # Создаю файл .csv с заголовками
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['№ Страницы',
                         '№ ПП',
                         '№ Исполнительного производства',
                         'Начало ИП',
                         'Окончание ИП',
                         'Текущая задолженность',
                         'Основной долг',
                         'Исполнительский сбор',
                         'Погашенная часть',
                         'Причина',
                         'Основание',
                         'Должник',
                         'Дата рождения',
                         'Место рождения',
                         # 'Ограничения',
                         'Взыскатель',
                         'Судебный пристав',
                         'Телефон пристава',
                         'РОСП',
                         'Адрес РОСП'])


def save_file(items):
    current_date = date.today()
    today = current_date.strftime("%d-%m-%Y")
    for item in items:
        with open(f'data/fssp_{today}.csv', 'a', encoding='utf-8') as file:                           #Открываю файл на добавление данных: 'a'
            writer = csv.writer(file)
            writer.writerow([item['№ Страницы'],
                             item['№ ПП'],
                             item['№ Исполнительного производства'],
                             item['Начало ИП'],
                             item['Окончание ИП'],
                             item['Текущая задолженность'],
                             item['Основной долг'],
                             item['Исполнительский сбор'],
                             item['Погашенная часть'],
                             item['Причина'],
                             item['Основание'],
                             item['Должник'],
                             item['Дата рождения'],
                             item['Место рождения'],
                             # item['Ограничения'],
                             item['Взыскатель'],
                             item['Судебный пристав'],
                             item['Телефон пристава'],
                             item['РОСП'],
                             item['Адрес РОСП']])

def main():
    esia_parsing()
    # read_html()

if __name__ == '__main__':
    main()