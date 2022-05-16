'''
Парсинга сайта Госуслуги.
Раздел ФССП - сведения о наличие ИП.
'''
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys     # Модуль для нажатия кнопки (например при авторизации)
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
import pickle
import time
from datetime import date
# import datetime
from auth_data import esia_di_login, esia_di_password
import csv


def esia_parsing():


    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36")

    options.add_argument('--headless')     # Бот работает в фоновом режиме

    driver = webdriver.Chrome(
        executable_path="/media/maks/Новый том/Python/lessons/linux_puthon_lessons/parsing_lessons/webdriver/chromedriver_linux64/chromedriver",
        options=options
    )

    try:
        driver.get("https://esia.gosuslugi.ru")
        print('start')
        driver.implicitly_wait(5)

        login = driver.find_element(By.ID, "login")
        login.clear()                                   # Очистка поля от данных
        driver.implicitly_wait(5)
        password = driver.find_element(By.ID, "password")
        password.clear()                                  # Очистка поля от данных
        driver.implicitly_wait(5)

        login.send_keys(esia_di_login)                    # ввод логина и пароля
        password.send_keys(esia_di_password)
        password.send_keys(Keys.ENTER)                    # вход по нажатии Enter, после ввода пароля
        # print('login')
        driver.implicitly_wait(5)

        # cookies
        cookies = driver.get_cookies()
        pickle.dump(cookies, open('cookies_file', 'wb'))

        # Переход на страницу ЛК
        xpath_personal_account = 'btn-gotoback'
        driver.find_element(By.CLASS_NAME, xpath_personal_account).click()    # нажатие ссылки
        # print('personal_account')
        time.sleep(5)
        # driver.implicitly_wait(5)



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
            driver.implicitly_wait(10)
            xpath_company = '//div[@class="grid-row"]/button[2]'
            driver.find_element(By.XPATH, xpath_company).click()
            print('company')
            time.sleep(5)
            # driver.implicitly_wait(5)

            # Переход на главную страницу Госуслуг
            xpath_esia = '//*[@id="header"]/div[2]/div/div/div/div/div/div[1]/a'
            driver.find_element(By.XPATH, xpath_esia).click()
            print('esia')
            # time.sleep(5)
            # driver.implicitly_wait(5)

            # Переход в раздел "Услуги"

            # xpath_category = '//div[@class="flex-container justify-end"]/div[1]'
            xpath_category = '//a[@data-ng-href="/catalog?from=lmain"]'
            driver.implicitly_wait(10)
            driver.find_element(By.XPATH, xpath_category).click()
            print('category')
            # time.sleep(5)
            # driver.implicitly_wait(5)

            # Переход в раздел "Органы власти"

            xpath_structure = '//div[@class="limiter"]/div[2]'
            driver.implicitly_wait(10)
            driver.find_element(By.XPATH, xpath_structure).click()
            print('structure')
            # time.sleep(5)
            # driver.implicitly_wait(10)

            # Переход в раздел "ФССП"
            xpath_fssp = '//div[@class="popular-structure"]/div[2]/div[2]'
            driver.implicitly_wait(10)
            driver.find_element(By.XPATH, xpath_fssp).click()
            print('fssp')
            # time.sleep(5)
            # driver.implicitly_wait(10)

            # Выбор услуги по предоставлению инфы об ИП
            xpath_service_ip = '//div[@class="structure-passport-list ng-scope"]/a[2]'
            driver.implicitly_wait(10)
            driver.find_element(By.XPATH, xpath_service_ip).click()
            print('service_ip')
            # time.sleep(5)
            # driver.implicitly_wait(10)

            # Выбор инфы о наличие ИП
            xpath_information_ip = '//li[@data-ng-if="!service.hideAfterFilter"][2]'
            driver.implicitly_wait(10)
            driver.find_element(By.XPATH, xpath_information_ip).click()
            print('information_ip')
            time.sleep(10)
            # driver.implicitly_wait(10)

            # Проверка наличия шаблона
            page_notifications = driver.page_source
            if 'conf-modal conf-modal--short' in page_notifications:
                driver.find_element(By.XPATH, '//div[@class="conf-modal__controls"]/lib-button[1]').click()
                print('проверка шаблона')
                time.sleep(5)
                # driver.implicitly_wait(5)

            # Выбор "Начать"
            driver.find_element(By.XPATH, '//div[@class="button-container"]').click()
            print('начать')
            time.sleep(5)
            # driver.implicitly_wait(10)

            # Выбор "Нет"
            xpath_no_button = '//epgu-constructor-answer-button[@class="quiz__item"][2]/epgu-cf-ui-long-button[@class="answer-btn"]'
            driver.find_element(By.XPATH, xpath_no_button).click()
            print('no_button')
            time.sleep(5)
            # driver.implicitly_wait(5)

            # Выбор "Верно" ФИО
            xpath_correctly_name = '//div[@class="button-container"]'
            driver.find_element(By.XPATH, xpath_correctly_name).click()
            print('correctly_name')
            time.sleep(5)
            # driver.implicitly_wait(5)

            # Выбор "Верно" организация
            xpath_correctly_user = '//div[@class="button-container"]'
            driver.find_element(By.XPATH, xpath_correctly_user).click()
            print('user')
            time.sleep(5)
            # driver.implicitly_wait(5)

            # Выбор "Верно" адрес регистрации
            xpath_correctly_registration = '//div[@class="button-container"]'
            driver.find_element(By.XPATH, xpath_correctly_registration).click()
            print('registration')
            time.sleep(5)
            # driver.implicitly_wait(5)

            # Выбор "Взыскатель"
            xpath_claimer = '//epgu-constructor-answer-button[@class="quiz__item"][2]/epgu-cf-ui-long-button[@class="answer-btn"]'
            driver.find_element(By.XPATH, xpath_claimer).click()
            print('claimer')
            time.sleep(5)
            # driver.implicitly_wait(5)

            # Выбор "Да"
            xpath_ok_start = '//epgu-constructor-answer-button[@class="quiz__item"][1]/epgu-cf-ui-long-button[@class="answer-btn"]'
            driver.find_element(By.XPATH, xpath_ok_start).click()
            print('загрузка должников')
            time.sleep(30)
            current_url = driver.current_url
            print(current_url)
            # driver.implicitly_wait(60)

            with open(f'{today}.txt', 'w') as file:
                file.write(current_url)
                file.close()




        # Подгрузка всех страниц с ИП
        print(f'start_pars')
        count_page = 1
        count = 0

        ## Блок используется для возобновления парсинга с указанного места
        # for i in range(1, 53):                                          # Вторая цифра указывает номер страницы с которой надо возобновить парсинг (пока меняется в ручную)
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
                # print(f'Показать ещё: стр_{count_page}')
                count_page += 1
                time.sleep(5)


            # Получение ссылок на ИП
            xpath_xx = '//div[@class="shadow-container mb-24"]|//div[@class="shadow-container"]'
            driver.implicitly_wait(10)
            items = driver.find_elements(By.XPATH, xpath_xx)
            number_items = len(items)
            # print(f'count = {count}: Количество ИП_{number_items}')

            for i in range(count, number_items):
                print(f'ИП {count + 1}')
                xpath_x = f'//div[@class="shadow-container mb-24"][{count + 1}]/h3/a|//div[@class="shadow-container"][1]/h3/a'
                driver.implicitly_wait(10)
                driver.find_element(By.XPATH, xpath_x).click()
                time.sleep(3)
                # print('загрузка ИП')

                page_notifications = driver.page_source
                driver.implicitly_wait(10)
                number_ep = driver.find_element(By.XPATH, '//h4[@class="main-title mb-16"]').text
                print(f'{number_ep = }')
                if '"gray-text mb-8"' in page_notifications:
                    start_date = driver.find_element(By.XPATH, '//p[@class="gray-text mb-8"]').text
                    # print(f'{start_date = }')
                    end_date = driver.find_element(By.XPATH, '//p[@class="gray-text"]').text
                    # print(f'{end_date = }')
                else:
                    start_date = driver.find_element(By.XPATH, '//p[@class="gray-text"]').text
                    # print(f'{start_date = }')
                    end_date = '-'
                    # print(f'{end_date = }')

                # Проверка наличия задолженности
                if '"amount-owed mr-md-24 mb-24 mb-md-0"' in page_notifications:
                    current_debt = driver.find_element(By.XPATH, '//span[@class="amount-owed mr-md-24 mb-24 mb-md-0"]').text
                    # print(f'{current_debt = }')
                    xpath_details_click = '//div[@class="toggle-link mb-24"]'
                    driver.find_element(By.XPATH, xpath_details_click).click()
                    time.sleep(1)

                    page2_notifications = driver.page_source
                    if 'Основной долг' in page2_notifications and 'Исполнительский сбор' in page2_notifications and 'Погашенная часть' in page2_notifications:
                        driver.implicitly_wait(10)
                        main_debt = driver.find_element(By.XPATH, '//div[@class="flex-container flex-column mb-16"][1]/span[2]').text
                        # print(f'{main_debt = }')
                        performance_fee = driver.find_element(By.XPATH, '//div[@class="flex-container flex-column mb-16"][2]/span[2]').text
                        # print(f'{performance_fee = }')
                        repaid_debt = driver.find_element(By.XPATH, '//div[@class="flex-container flex-column mb-16"][3]/span[2]').text
                        # print(f'{repaid_debt = }')
                    elif 'Основной долг' in page2_notifications and 'Исполнительский сбор' in page2_notifications and not 'Погашенная часть' in page2_notifications:
                        driver.implicitly_wait(10)
                        main_debt = driver.find_element(By.XPATH, '//div[@class="flex-container flex-column mb-16"][1]/span[2]').text
                        # print(f'{main_debt = }')
                        performance_fee = driver.find_element(By.XPATH, '//div[@class="flex-container flex-column mb-16"][2]/span[2]').text
                        # print(f'{performance_fee = }')
                        repaid_debt = '-'
                        # print(f'{repaid_debt = }')
                    elif 'Основной долг' in page2_notifications and not 'Исполнительский сбор' in page2_notifications and not 'Погашенная часть' in page2_notifications:
                        driver.implicitly_wait(10)
                        main_debt = driver.find_element(By.XPATH, '//div[@class="flex-container flex-column mb-16"][1]/span[2]').text
                        performance_fee = '-'
                        repaid_debt = '-'
                    elif 'Основной долг' in page2_notifications and not 'Исполнительский сбор' in page2_notifications and 'Погашенная часть' in page2_notifications:
                        driver.implicitly_wait(10)
                        main_debt = driver.find_element(By.XPATH, '//div[@class="flex-container flex-column mb-16"][1]/span[2]').text
                        # print(f'{main_debt = }')
                        performance_fee = '-'
                        # print(f'{performance_fee = }')
                        repaid_debt = driver.find_element(By.XPATH, '//div[@class="flex-container flex-column mb-16"][2]/span[2]').text
                        # print(f'{repaid_debt = }')
                    else:
                        main_debt = '-'
                        performance_fee = '-'
                        repaid_debt = '-'
                else:
                    driver.implicitly_wait(10)
                    current_debt = driver.find_element(By.XPATH, '//span[@class="amount-owed mr-md-24 mb-24 mb-md-0 gray-amount"]').text
                    # print(f'{current_debt = }')
                    xpath_details_click = '//div[@class="toggle-link mb-24"]'
                    driver.find_element(By.XPATH, xpath_details_click).click()
                    time.sleep(1)
                    main_debt = driver.find_element(By.XPATH, '//div[@class="flex-container flex-column mb-16"][1]/span[2]').text
                    # print(f'{main_debt = }')
                    performance_fee = '-'
                    # print(f'{performance_fee = }')
                    repaid_debt = driver.find_element(By.XPATH, '//div[@class="flex-container flex-column mb-16"][2]/span[2]').text
                    # print(f'{repaid_debt = }')

                if 'Причина' in page_notifications:
                    driver.implicitly_wait(10)
                    reason = driver.find_element(By.XPATH, '//div[@class="border-block mb-24"][2]/div[1]/span[2]').text
                    # print(f'{reason = }')
                    footing = driver.find_element(By.XPATH, '//div[@class="border-block mb-24"][2]/div[2]/span[2]').text
                    # print(f'{footing = }')
                else:
                    reason = '-'
                    # print(f'{reason = }')
                    footing = driver.find_element(By.XPATH, '//div[@class="border-block mb-24"][2]/div[1]/span[2]').text
                    # print(f'{footing = }')

                driver.implicitly_wait(10)
                debtor = driver.find_element(By.XPATH, '//div[@class="border-block mb-24"][3]/p').text
                # print(f'{debtor = }')
                birthday = driver.find_element(By.XPATH, '//div[@class="border-block mb-24"][3]/div[1]/span[2]').text
                # print(f'{birthday = }')
                if 'Место рождения' in page_notifications:
                    driver.implicitly_wait(10)
                    place_of_birth = driver.find_element(By.XPATH, '//div[@class="border-block mb-24"][3]/div[2]/span[2]').text
                else:
                    place_of_birth = ''
                # restriction = driver.find_element(By.XPATH, '//div[@class="border-block mb-24"][4]/div/div/span').text
                # print(f'{restriction = }')
                # driver.implicitly_wait(5)
                driver.implicitly_wait(10)
                creditor = driver.find_element(By.XPATH, '//div[@class="border-block mb-24"][5]/p').text
                # print(f'{creditor = }')
                bailiff = driver.find_element(By.XPATH, '//div[@class="border-block mb-24"][6]/p').text
                # print(f'{bailiff = }')
                driver.implicitly_wait(10)
                bailiff_tel = driver.find_element(By.XPATH, '//div[@class="border-block mb-24"][6]/div[1]/span[2]').text
                # print(f'{bailiff_tel = }')
                rosp = driver.find_element(By.XPATH, '//div[@class="border-block mb-24"][6]/div[2]/span[2]').text
                # print(f'{rosp = }')
                address_rosp = driver.find_element(By.XPATH, '//div[@class="border-block mb-24"][6]/div[3]/span[2]').text
                # print(f'{address_rosp = }')

                executive_production.append({
                    '№ Страницы': count_page,
                    '№ ПП': count,
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
                })

                driver.back()
                time.sleep(3)
                # print(str(count) + '_' + '#' * 40)
                count += 1
            save_file(executive_production)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def create_file():
    current_date = date.today()
    today = current_date.strftime("%d-%m-%Y")
    with open(f'data/fssp_{today}.csv', 'w') as file:                 # Создаю файл .csv с заголовками
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
        with open(f'data/fssp_{today}.csv', 'a') as file:                           #Открываю файл на добавление данных: 'a'
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