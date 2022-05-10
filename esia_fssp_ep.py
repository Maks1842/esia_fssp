'''
Парсинга сайта Госуслуги.
Раздел ФССП - сведения о наличие ИП.
'''

from bs4 import BeautifulSoup
import requests
import fake_useragent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys     # Модуль для нажатия кнопки Enter (например при авторизации)
import pickle
import time
from auth_data import esia_di_login, esia_di_password
import csv


def esia_parsing():
    executive_production = []

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
        print('login')
        driver.implicitly_wait(5)

        # cookies
        cookies = driver.get_cookies()
        pickle.dump(cookies, open('cookies_file', 'wb'))

        # Переход по ссылке на главную страницу ЕСИА
        xpath_esia = 'btn-gotoback'
        driver.find_element(By.CLASS_NAME, xpath_esia).click()    # нажатие ссылки
        print('esia')
        time.sleep(5)
        # driver.implicitly_wait(5)

        # Выбор компании
        xpath_company = '//div[@class="grid-row"]/button[2]'
        driver.find_element(By.XPATH, xpath_company).click()
        print('company')
        time.sleep(5)
        # driver.implicitly_wait(5)

        # Переход в раздел "Услуги"
        xpath_category = '//div[@class="flex-container justify-end"]/div[1]'
        driver.find_element(By.XPATH, xpath_category).click()
        print('category')
        time.sleep(5)
        # driver.implicitly_wait(5)

        # Переход в раздел "Органы власти"
        xpath_structure = '//div[@class="limiter"]/div[2]'
        driver.find_element(By.XPATH, xpath_structure).click()
        print('structure')
        time.sleep(5)
        # driver.implicitly_wait(10)

        # Переход в раздел "ФССП"
        xpath_fssp = '//div[@class="popular-structure"]/div[2]/div[2]'
        driver.find_element(By.XPATH, xpath_fssp).click()
        print('fssp')
        time.sleep(5)
        # driver.implicitly_wait(10)

        # Выбор услуги по предоставлению инфы об ИП
        xpath_service_ip = '//div[@class="structure-passport-list ng-scope"]/a[2]'
        driver.find_element(By.XPATH, xpath_service_ip).click()
        print('service_ip')
        time.sleep(5)
        # driver.implicitly_wait(10)

        # Выбор инфы о наличие ИП
        xpath_information_ip = '//li[@data-ng-if="!service.hideAfterFilter"][2]'
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
        # driver.implicitly_wait(60)

        # Получение ссылок на ИП
        xpath_xx = '//div[@class="shadow-container mb-24"]|//div[@class="shadow-container"]'
        items = driver.find_elements(By.XPATH, xpath_xx)
        print(len(items))
        count = 1
        for item in items:
            xpath_x = f'//div[@class="shadow-container mb-24"][{count}]/h3/a|//div[@class="shadow-container"][1]/h3/a'
            driver.find_element(By.XPATH, xpath_x).click()
            time.sleep(5)
            print('загрузка ИП')

            page_notifications = driver.page_source
            number_ep = driver.find_element(By.XPATH, '//h4[@class="main-title mb-16"]').text
            print(f'{number_ep = }')
            if '"gray-text mb-8"' in page_notifications:
                start_date = driver.find_element(By.XPATH, '//p[@class="gray-text mb-8"]').text
                print(f'{start_date = }')
                end_date = driver.find_element(By.XPATH, '//p[@class="gray-text"]').text
                print(f'{end_date = }')
            else:
                start_date = driver.find_element(By.XPATH, '//p[@class="gray-text"]').text
                print(f'{start_date = }')
                end_date = '-'
                print(f'{end_date = }')

            # Проверка наличия задолженности
            if '"amount-owed mr-md-24 mb-24 mb-md-0"' in page_notifications:
                current_debt = driver.find_element(By.XPATH, '//span[@class="amount-owed mr-md-24 mb-24 mb-md-0"]').text
                print(f'{current_debt = }')
                xpath_details_click = '//div[@class="toggle-link mb-24"]'
                driver.find_element(By.XPATH, xpath_details_click).click()
                time.sleep(1)

                page2_notifications = driver.page_source
                if 'Исполнительский сбор' in page2_notifications and 'Погашенная часть' in page2_notifications:
                    main_debt = driver.find_element(By.XPATH, '//div[@class="flex-container flex-column mb-16"][1]/span[2]').text
                    print(f'{main_debt = }')
                    performance_fee = driver.find_element(By.XPATH, '//div[@class="flex-container flex-column mb-16"][2]/span[2]').text
                    print(f'{performance_fee = }')
                    repaid_debt = driver.find_element(By.XPATH, '//div[@class="flex-container flex-column mb-16"][3]/span[2]').text
                    print(f'{repaid_debt = }')
                elif 'Исполнительский сбор' in page2_notifications and not 'Погашенная часть' in page2_notifications:
                    main_debt = driver.find_element(By.XPATH, '//div[@class="flex-container flex-column mb-16"][1]/span[2]').text
                    print(f'{main_debt = }')
                    performance_fee = driver.find_element(By.XPATH, '//div[@class="flex-container flex-column mb-16"][2]/span[2]').text
                    print(f'{performance_fee = }')
                    repaid_debt = '-'
                    print(f'{repaid_debt = }')
                else:
                    main_debt = driver.find_element(By.XPATH, '//div[@class="flex-container flex-column mb-16"][1]/span[2]').text
                    print(f'{main_debt = }')
                    performance_fee = '-'
                    print(f'{performance_fee = }')
                    repaid_debt = driver.find_element(By.XPATH, '//div[@class="flex-container flex-column mb-16"][2]/span[2]').text
                    print(f'{repaid_debt = }')
            else:
                current_debt = driver.find_element(By.XPATH, '//span[@class="amount-owed mr-md-24 mb-24 mb-md-0 gray-amount"]').text
                print(f'{current_debt = }')
                xpath_details_click = '//div[@class="toggle-link mb-24"]'
                driver.find_element(By.XPATH, xpath_details_click).click()
                time.sleep(1)
                main_debt = driver.find_element(By.XPATH, '//div[@class="flex-container flex-column mb-16"][1]/span[2]').text
                print(f'{main_debt = }')
                performance_fee = '-'
                print(f'{performance_fee = }')
                repaid_debt = driver.find_element(By.XPATH, '//div[@class="flex-container flex-column mb-16"][2]/span[2]').text
                print(f'{repaid_debt = }')

            if 'Причина' in page_notifications:
                reason = driver.find_element(By.XPATH, '//div[@class="border-block mb-24"][2]/div[1]/span[2]').text
                print(f'{reason = }')
                footing = driver.find_element(By.XPATH, '//div[@class="border-block mb-24"][2]/div[2]/span[2]').text
                print(f'{footing = }')
            else:
                reason = '-'
                print(f'{reason = }')
                footing = driver.find_element(By.XPATH, '//div[@class="border-block mb-24"][2]/div[1]/span[2]').text
                print(f'{footing = }')

            debtor = driver.find_element(By.XPATH, '//div[@class="border-block mb-24"][3]/p').text
            print(f'{debtor = }')
            birthday = driver.find_element(By.XPATH, '//div[@class="border-block mb-24"][3]/div[1]/span[2]').text
            print(f'{birthday = }')
            place_of_birth = driver.find_element(By.XPATH, '//div[@class="border-block mb-24"][3]/div[2]/span[2]').text
            print(f'{place_of_birth = }')
            # restriction = driver.find_element(By.XPATH, '//div[@class="border-block mb-24"][4]/div/div/span').text
            # print(f'{restriction = }')
            # driver.implicitly_wait(5)
            creditor = driver.find_element(By.XPATH, '//div[@class="border-block mb-24"][5]/p').text
            print(f'{creditor = }')
            bailiff = driver.find_element(By.XPATH, '//div[@class="border-block mb-24"][6]/p').text
            print(f'{bailiff = }')
            bailiff_tel = driver.find_element(By.XPATH, '//div[@class="border-block mb-24"][6]/div[1]/span[2]').text
            print(f'{bailiff_tel = }')
            rosp = driver.find_element(By.XPATH, '//div[@class="border-block mb-24"][6]/div[2]/span[2]').text
            print(f'{rosp = }')
            address_rosp = driver.find_element(By.XPATH, '//div[@class="border-block mb-24"][6]/div[3]/span[2]').text
            print(f'{address_rosp = }')

            executive_production.append({
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
            print(str(count) + '_' + '#' * 40)

            count += 1

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

    return executive_production


## Для проверки html кода
# def read_html():
#     with open("ep.html") as file:          # Сохраняю файл в переменную, для дальнейшего парсинга
#         src = file.read()
#     soup = BeautifulSoup(src, "html.parser")
#
#     number_ep = soup.find('h4', class_='main-title mb-16').text.strip()
#     current_debt = soup.find('span', class_='amount-owed mr-md-24 mb-24 mb-md-0').text.strip()
#     border_block = soup.find_all('div', class_='border-block mb-24')
#     main_debt = border_block[0].find_all('span', class_='text-plain')[0].text
#     performance_fee = border_block[0].find_all('span', class_='text-plain')[1].text
#     redeemed_part = border_block[0].find_all('span', class_='text-plain')[2].text
#     reason = border_block[1].find_all('span', class_='info-text')[0].text
#     footing = border_block[1].find_all('span', class_='info-text')[1].text
#     debtor = border_block[2].find('p', class_='info-text bold mb-12').text.strip()
#     birthday = border_block[2].find_all('span', class_='info-text')[0].text
#     place_of_birth = border_block[2].find_all('span', class_='info-text')[1].text
#     restriction = border_block[3].find('span', class_='green-frame').text.strip()
#     creditor = border_block[4].find('p', class_='info-text bold mb-16').text.strip()
#     bailiff = border_block[5].find('p', class_='info-text bold mb-12').text.strip()
#     bailiff_tel = border_block[5].find_all('span', class_='info-text')[0].text
#     rosp = border_block[5].find_all('span', class_='info-text')[1].text
#     address_rosp = border_block[5].find_all('span', class_='info-text')[2].text

def save_file():
    items = esia_parsing()
    with open('data/' + f'fssp.csv', 'w') as file:                 # Создаю файл .csv с заголовками
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['№ Исполнительного производства',
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

    for item in items:
        with open('data/' + f'fssp.csv', 'a') as file:                           #Открываю файл на добавление данных: 'a'
            writer = csv.writer(file)
            writer.writerow([item['№ Исполнительного производства'],
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
    save_file()
    # read_html()

if __name__ == '__main__':
    main()