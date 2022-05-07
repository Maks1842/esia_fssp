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
    driver = webdriver.Chrome(
        executable_path="/media/maks/Новый том/Python/lessons/linux_puthon_lessons/parsing_lessons/webdriver/chromedriver_linux64/chromedriver",
        options=options
    )

    # xpath_button = '/html/body/portal-root/header/lib-header/div/div/div[2]/div[2]/div/div/lib-login[2]/a'
    # xpath_enter = '/html/body/esia-root/div/esia-idp/div/div[1]/form/div[3]/button'

    try:
        driver.get("https://esia.gosuslugi.ru")
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
        driver.implicitly_wait(10)

        # cookies
        cookies = driver.get_cookies()
        pickle.dump(cookies, open('cookies_file', 'wb'))

        # Переход по ссылке на главную страницу ЕСИА
        driver.find_element(By.CLASS_NAME, 'btn-gotoback').click()    # нажатие ссылки
        time.sleep(10)

        # Выбор компании
        xpath_company = '/html/body/app-root/main/div/div/div/div/button[2]'
        driver.find_element(By.XPATH, xpath_company).click()
        time.sleep(5)

        # Переход в раздел "Услуги"
        xpath_category = '/html/body/div[1]/div[1]/div[2]/div/div/div/div[2]/div/div[1]/a'
        driver.find_element(By.XPATH, xpath_category).click()
        time.sleep(5)

        # Переход в раздел "Органы власти"
        xpath_structure = '/html/body/div[1]/div[3]/div[1]/div[2]/div/div/div[2]/div/div[2]/div/div[2]/a'
        driver.find_element(By.XPATH, xpath_structure).click()
        time.sleep(5)

        # Переход в раздел "ФССП"
        xpath_fssp = '/html/body/div[1]/div[3]/div[1]/div[2]/div/div/div[3]/div/div[1]/div[2]/div[2]/div/div/a'
        driver.find_element(By.XPATH, xpath_fssp).click()
        time.sleep(5)

        # Выбор услуги по предоставлению инфы об ИП
        xpath_service_ip = '/html/body/div[1]/div[3]/div[1]/div[2]/div/div/div[2]/ng-include/div[2]/a[2]/div[2]/div'
        driver.find_element(By.XPATH, xpath_service_ip).click()
        driver.implicitly_wait(5)

        # Выбор инфы о наличие ИП
        xpath_information_ip = '/html/body/div[1]/div[3]/div[1]/div[2]/div/div/div[2]/div[1]/div[1]/ul/li[4]'
        driver.find_element(By.XPATH, xpath_information_ip).click()
        time.sleep(10)

        # with open("index_selenium.html", "w") as file:    # Сохраняю HTML код страницы в файл !!!! Данный код только для записи HTML кода в файл!!!
        #     file.write(driver.page_source)

        # Проверка наличия шаблона
        page_notifications = driver.page_source
        soup_page_notifications = BeautifulSoup(page_notifications, 'html.parser')
        if 'conf-modal conf-modal--short' in soup_page_notifications:
            xpath_checking_template = '/html/body/div/div/portal-new-sf-player/epgu-constructor-form-player/epgu-cf-ui-main-container/epgu-cf-ui-modal-container/div/div/epgu-cf-ui-cta-modal/div[2]/div[2]/div/div/div[2]/lib-button[1]'
            driver.find_element(By.XPATH, xpath_checking_template).click()
            time.sleep(5)

        # Выбор "Начать"
        xpath_start = '//*[@id="print-page"]/portal-new-sf-player/epgu-constructor-form-player/epgu-cf-ui-main-container/epgu-constructor-screen-resolver/epgu-constructor-info-screen/epgu-cf-ui-screen-container/div/epgu-cf-ui-constructor-screen-pad/epgu-constructor-screen-buttons/lib-button/div'
        driver.find_element(By.XPATH, xpath_start).click()
        time.sleep(5)

        # Выбор "Нет"
        xpath_no_button = '/html/body/div/div/portal-new-sf-player/epgu-constructor-form-player/epgu-cf-ui-main-container/epgu-constructor-screen-resolver/epgu-constructor-question-screen/epgu-cf-ui-screen-container/div/div[2]/epgu-constructor-answer-button[2]/epgu-cf-ui-long-button'
        driver.find_element(By.XPATH, xpath_no_button).click()
        time.sleep(5)

        # Выбор "Верно" ФИО
        xpath_correctly_name = '/html/body/div/div/portal-new-sf-player/epgu-constructor-form-player/epgu-cf-ui-main-container/epgu-constructor-screen-resolver/epgu-constructor-unique-screen/epgu-constructor-component-unique-resolver/epgu-constructor-confirm-personal-user-data/epgu-constructor-default-unique-screen-wrapper/epgu-cf-ui-screen-container/div/div[2]/epgu-constructor-screen-buttons/lib-button/div'
        driver.find_element(By.XPATH, xpath_correctly_name).click()
        time.sleep(5)

        # Выбор "Верно" организация
        xpath_correctly_user = '/html/body/div/div/portal-new-sf-player/epgu-constructor-form-player/epgu-cf-ui-main-container/epgu-constructor-screen-resolver/epgu-constructor-unique-screen/epgu-constructor-component-unique-resolver/epgu-constructor-confirm-personal-user-legal-data/epgu-constructor-default-unique-screen-wrapper/epgu-cf-ui-screen-container/div/div[2]/epgu-constructor-screen-buttons/lib-button/div'
        driver.find_element(By.XPATH, xpath_correctly_user).click()
        time.sleep(5)

        # Выбор "Верно" адрес регистрации
        xpath_correctly_registration = '/html/body/div/div/portal-new-sf-player/epgu-constructor-form-player/epgu-cf-ui-main-container/epgu-constructor-screen-resolver/epgu-constructor-unique-screen/epgu-constructor-component-unique-resolver/epgu-constructor-registration-addr/epgu-constructor-default-unique-screen-wrapper/epgu-cf-ui-screen-container/div/div[2]/epgu-constructor-screen-buttons/lib-button/div'
        driver.find_element(By.XPATH, xpath_correctly_registration).click()
        time.sleep(5)

        # Выбор "Взыскатель"
        xpath_claimer = '/html/body/div/div/portal-new-sf-player/epgu-constructor-form-player/epgu-cf-ui-main-container/epgu-constructor-screen-resolver/epgu-constructor-question-screen/epgu-cf-ui-screen-container/div/div[2]/epgu-constructor-answer-button[2]/epgu-cf-ui-long-button'
        driver.find_element(By.XPATH, xpath_claimer).click()
        time.sleep(5)

        # Выбор "Да"
        xpath_ok_start = '/html/body/div/div/portal-new-sf-player/epgu-constructor-form-player/epgu-cf-ui-main-container/epgu-constructor-screen-resolver/epgu-constructor-question-screen/epgu-cf-ui-screen-container/div/div[2]/epgu-constructor-answer-button[1]/epgu-cf-ui-long-button'
        driver.find_element(By.XPATH, xpath_ok_start).click()
        time.sleep(30)

        # Получение ссылок на ИП
        page_ip = driver.page_source
        soup_page_ip = BeautifulSoup(page_ip, 'html.parser')
        block_ip = soup_page_ip.find_all('div', class_='shadow-container mb-24')
        # body > div > div > div.flex-container.flex-column.flex-1-0.mb-32.mb-md-64 > app-ip-list > div > div > div:nth-child(4)
        # /html/body/div/div/div[1]/app-ip-list/div/div/div[3]
        # /html/body/div/div/div[1]/app-ip-list/div/div/div[4]
        # /html/body/div/div/div[1]/app-ip-list/div/div/div[22]
        print(len(block_ip))
        count = 1
        # for x in range(1, 21):
        xpath_x = '/html/body/div/div/div[1]/app-ip-list/div/div/div[3]'
        driver.find_element(By.XPATH, xpath_x).click()
        time.sleep(5)

        driver.switch_to.window(driver.window_handles[1])
        # count += 1
        time.sleep(5)

        page_data = driver.page_source
        time.sleep(1)
        driver.close()

        soup_data = BeautifulSoup(page_data, 'html.parser')

        number_ep = soup_data.find('h4', class_='main-title mb-16').text.strip()
        current_debt = soup_data.find('span', class_='amount-owed mr-md-24 mb-24 mb-md-0').text.strip()
        border_block = soup_data.find_all('div', class_='border-block mb-24')
        main_debt = border_block[0].find_all('span', class_='text-plain')[0].text
        performance_fee = border_block[0].find_all('span', class_='text-plain')[1].text
        redeemed_part = border_block[0].find_all('span', class_='text-plain')[2].text
        reason = border_block[1].find_all('span', class_='info-text')[0].text
        footing = border_block[1].find_all('span', class_='info-text')[1].text
        debtor = border_block[2].find('p', class_='info-text bold mb-12').text.strip()
        birthday = border_block[2].find_all('span', class_='info-text')[0].text
        place_of_birth = border_block[2].find_all('span', class_='info-text')[1].text
        restriction = border_block[3].find('span', class_='green-frame').text.strip()
        creditor = border_block[4].find('p', class_='info-text bold mb-16').text.strip()
        bailiff = border_block[5].find('p', class_='info-text bold mb-12').text.strip()
        bailiff_tel = border_block[5].find_all('span', class_='info-text')[0].text
        rosp = border_block[5].find_all('span', class_='info-text')[1].text
        address_rosp = border_block[5].find_all('span', class_='info-text')[2].text

        executive_production.append({
            '№ Исполнительного производства': number_ep,
            'Текущая задолженность': current_debt,
            'Основной долг': main_debt,
            'Исполнительский сбор': performance_fee,
            'Погашенная часть': redeemed_part,
            'Причина': reason,
            'Основание': footing,
            'Должник': debtor,
            'Дата рождения': birthday,
            'Место рождения': place_of_birth,
            'Ограничения': restriction,
            'Взыскатель': creditor,
            'Судебный пристав': bailiff,
            'Телефон пристава': bailiff_tel,
            'РОСП': rosp,
            'Адрес РОСП': address_rosp
        })

        print(f'{executive_production = }')




# /html/body/div[1]/div[3]/div[1]/div[2]/div/div/div[2]/div[1]/div[1]/ul/li[3]

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

    return executive_production


# def read_html(html_page):
#     soup = BeautifulSoup(html_page, "lxml")
#     block = soup.find('div', class_='message-wrapper col-3 col-md-6 col-lg-12').text
#     return block

def read_html():
    with open("ep.html") as file:          # Сохраняю файл в переменную, для дальнейшего парсинга
        src = file.read()
    soup = BeautifulSoup(src, "html.parser")

    number_ep = soup.find('h4', class_='main-title mb-16').text.strip()
    current_debt = soup.find('span', class_='amount-owed mr-md-24 mb-24 mb-md-0').text.strip()
    border_block = soup.find_all('div', class_='border-block mb-24')
    main_debt = border_block[0].find_all('span', class_='text-plain')[0].text
    performance_fee = border_block[0].find_all('span', class_='text-plain')[1].text
    redeemed_part = border_block[0].find_all('span', class_='text-plain')[2].text
    reason = border_block[1].find_all('span', class_='info-text')[0].text
    footing = border_block[1].find_all('span', class_='info-text')[1].text
    debtor = border_block[2].find('p', class_='info-text bold mb-12').text.strip()
    birthday = border_block[2].find_all('span', class_='info-text')[0].text
    place_of_birth = border_block[2].find_all('span', class_='info-text')[1].text
    restriction = border_block[3].find('span', class_='green-frame').text.strip()
    creditor = border_block[4].find('p', class_='info-text bold mb-16').text.strip()
    bailiff = border_block[5].find('p', class_='info-text bold mb-12').text.strip()
    bailiff_tel = border_block[5].find_all('span', class_='info-text')[0].text
    rosp = border_block[5].find_all('span', class_='info-text')[1].text
    address_rosp = border_block[5].find_all('span', class_='info-text')[2].text


    # for url_ip in block_ip:
    #     url_ip = 'https://esia.gosuslugi.ru' + url_ip.find('a').get('href')
    #     print(f'{url_ip = }')

def save_file():
    items = esia_parsing()
    with open('data/' + f'fssp.csv', 'w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['№ Исполнительного производства',
        'Текущая задолженность',
        'Основной долг',
        'Исполнительский сбор',
        'Погашенная часть',
        'Причина',
        'Основание',
        'Должник',
        'Дата рождения',
        'Место рождения',
        'Ограничения',
        'Взыскатель',
        'Судебный пристав',
        'Телефон пристава',
        'РОСП',
        'Адрес РОСП'])

    for item in items:
        with open('data/' + f'fssp.csv', 'a') as file:                           #Открываю файл на добавление данных 'a'
            writer = csv.writer(file)
            writer.writerow([item['№ Исполнительного производства'],
                             item['Текущая задолженность'],
                             item['Основной долг'],
                             item['Исполнительский сбор'],
                             item['Погашенная часть'],
                             item['Причина'],
                             item['Основание'],
                             item['Должник'],
                             item['Дата рождения'],
                             item['Место рождения'],
                             item['Ограничения'],
                             item['Взыскатель'],
                             item['Судебный пристав'],
                             item['Телефон пристава'],
                             item['РОСП'],
                             item['Адрес РОСП']])

def main():
    # save_file(esia_input())
    save_file()
    # read_html()

if __name__ == '__main__':
    main()