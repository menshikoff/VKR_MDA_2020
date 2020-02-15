from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
import random

def extr_element_text(elem, browser):
    """Возвращает текст, содержащийся в искомом элементе
    
    :param elem:    WebElement
    :param browser: WebDriver
    :return: строку
    """

    try:
        output = browser.find_element_by_xpath(elem).text
    except:
        output = 'нет данных'

    return output


def extract_car_data(browser, grid):
    """Возвращает словарь с данными об автомобиле
    
    :param browser: WebDriver
    :param grid:    экземпляр класса 'coordinate_grid'
    :return: словарь с данными ободном автомобиле
    """

    sleep(2)
 
    # Основные данные на странице находится в блоке '//ul[@class="CardInfo"]'. Находим данный блок и проходимся по всем элементам 'span'
    # Словарь с параметрами автомобиля
    car_data = {}

    # Проходим по содержимому блоку и формируем список, где каждый 1-й элемент название параметра, а каждый 2-й элемент значение данного параметра 
    car_table_data = list(map(lambda x: x.text, browser.find_element_by_xpath('//ul[@class="CardInfo"]').find_elements_by_xpath(
        '//span[@class="CardInfo__cell"]')))

    # Добавляем в словать параметры автомобиля
    x = 0
    while x < len(car_table_data):
        car_data.update({car_table_data[x]: car_table_data[x+1]})
        x = x + 2

    # Информация о двигателе представлена одной строкой. Создаем список характеристик двигателя
    car_engine_data = map(lambda i: i.strip(), car_table_data[9].split('/'))
    
    # Дополняем словарь с данными автомобяли отдельными характеристиками двигателя
    for i in ['Объем двигателя', 'Мощность двигателя', 'Тип топлива']:
        car_data.update({i: next(car_engine_data)})

    # Блок действий пользователя
    thumbnails = browser.find_elements_by_xpath('//div[@class="image-gallery-thumbnail-container"]')
    
    for i in range(random.randrange(2, 6, 1)):
        try:
            item = random.choice(thumbnails[0: 9])
            grid.in_focus(item)
            grid.mouse_move_to(item)
        except:
            pass
    
    # Get the phone number
    try:
        button = browser.find_element_by_xpath('//div[@class="CardPhone-module__phone CardPhone-module__preview"]')

        grid.in_focus(button)
        grid.mouse_move_to(button)
        grid.mouse_click_left()
   
    # Ожидание появления элемента с номером телефона
        try:
            element = WebDriverWait(browser, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="CardPhone-module__phone-title"]'))
            )
        except:
            pass
    except:
        return

    main_info = map(extr_element_text,
    [
        '//div[@id="app"]/div[2]/div[3]/div[2]/div/div[2]/div/div/div/div/div',                 #1 - Model of vehicle
        '//div[@id="app"]/div[2]/div[3]/div[2]/div/div[2]/div/div/div/div[2]/div/div[2]/div',   #2 - Price of the vehile
        '//div[@class="CardSellerNamePlace__name"]',                                            #3 - Name of owner
        '//div[@class="CardSellerNamePlace__address"]',                                         #4 - Address
        '//div[@class="CardPhone-module__phone-title"]'                                         #5 - Phone number
    ], [browser, browser, browser, browser, browser]
    )

    for ii in ['Модель автомобиля', 'Цена автомобиля', 'Имя продавца', 'Адрес продавца', 'Номер телефона']:
        car_data.update({ii: next(main_info)})
    
    sleep(2)

    return car_data


if __name__ == "__main__":
    
    option = webdriver.ChromeOptions()

    prefs = {"profile.managed_default_content_settings.images":0,
            "profile.default_content_setting_values.notifications":0,
            "profile.managed_default_content_settings.stylesheets":0,
            "profile.managed_default_content_settings.cookies":0,
            "profile.managed_default_content_settings.javascript":1,
            "profile.managed_default_content_settings.plugins":1,
            "profile.managed_default_content_settings.popups":0,
            "profile.managed_default_content_settings.geolocation":2,
            "profile.managed_default_content_settings.media_stream":0,
            }
    option.add_experimental_option("prefs", prefs)

    browser = webdriver.Chrome(chrome_options=option)

    browser.get('https://auto.ru/cars/used/sale/toyota/alphard/1082941210-095e4f81/?sort=cr_date-desc')
    sleep(4)
