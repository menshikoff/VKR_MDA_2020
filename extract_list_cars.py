from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from time import sleep
from pynput.keyboard import Key, Controller
import pyautogui
import time
import re


import my_tools
import par_sing_page
import regrid

def list_page_navi(browser, grid):
    #The idea is to open links by pointing mouse and clicking.

    start_time = time.time()
  
    car_list_data = {}

    #Определяем количество страниц с данными авто по запросу
    pages_numbers = browser.find_elements_by_xpath(
        '//a[@class="Button Button_color_whiteHoverBlue Button_size_s Button_type_link Button_width_default ListingPagination-module__page"]')
    
    try:
        last_page = int(list(map(lambda x: x.text, pages_numbers))[-1])
    except:
        last_page = 1

    #Запускаем цикл для обхода страниц поиска

    for i in range(last_page):
        
        count_items = lambda x,y: x.find_elements_by_xpath(y)
        car_list = count_items(browser, '//div[@class="ListingItem-module__container ListingCars-module__listingItem"]') #Get the list of car_brief on the current page
        sleep(1)
        
    #Запускаем цикл для обхода объявлений на странице
        for car in car_list:
            try:
                grid.in_focus(car)
            except:
                browser.back()

            try:
                link_to_car = car.find_element_by_tag_name('h3').find_element_by_tag_name('a')
                # link_to_car = car.find_element(By.XPATH, '//div[@class="ListingItem-module__thumb"]')
                print(link_to_car)
            except:
                continue
test_search_Wed Feb  5 23:42:22 2020.jsn
            grid.mouse_move_to(link_to_car)
            time.sleep(1)
            
            car_id = re.search(r'\d{10}-.+/', link_to_car.get_attribute('href'))[0][:-1]
            car_list_data.update({car_id: {'Ссылка': link_to_car.get_attribute('href')}})
            
            grid.mouse_click_left()
            
            k = Controller()
            k.press(Key.f11)
            k.release(Key.f11)

            try:
                WebDriverWait(browser, 3).until(EC.number_of_windows_to_be(2))
            except:
                continue

            browser.switch_to.window(browser.window_handles[1])
            
            sleep(2)
            k.press(Key.f11)
            k.release(Key.f11)

            window_grid = regrid.coordinate_grid(browser)
         
            #Блок трай нужен, чтобы закрыть неправильную страницу если случайно перешли на нее
            try:
                car_list_data.get(car_id).update(par_sing_page.extract_car_data(browser, window_grid))
            except:
                pass

            window_grid.y_website_top = 0
            window_grid.y_website_bottom = window_grid.y_website_top + window_grid.y_website_bottom_lim

            browser.close()
            browser.switch_to.window(browser.window_handles[0])

        sleep(1)

        finish_time = time.time()

        car_list_data.update({'Техническая информация': {'Время поиска в секундах': finish_time - start_time, 'Кол-во объявлений': len(car_list_data.keys()), 'Время поиска одного объявления': (finish_time - start_time) / len(car_list_data.keys())}})

        #Сохраняем в файл данные по авто. (Временное решение, т.к. логично будет если сохранение будет прозводиться сразу в базу данных после получения информации о каждом авто)
        my_tools.json_s('test_search_'+ time.ctime(time.time())+'.jsn', car_list_data)
        
        #Переходим на следующую страницу
        try:
            content_panel = browser.find_element_by_xpath('//div[@class="ListingPagination-module__container"]')
            next_button = content_panel.find_element_by_xpath(
                '//a[@class="Button Button_color_white Button_size_s Button_type_link Button_width_default ListingPagination-module__next"]')

            grid.in_focus(content_panel)
            grid.mouse_move_to(next_button)
            grid.mouse_click_left()
        except:
            pass
        
        sleep(4)
        browser.refresh()


        # Ждем прогрузки страницы
        try:
            WebDriverWait(browser, 30).until(EC.presence_of_all_elements_located((By.XPATH,
            '//div[@class="ListingCars-module__container ListingCars-module__list"]')))
        except:
            pass
        
        # Обновляем информацию в переменных сетки координат
        
        for i in range(20):
            grid.mouse_scroll(1)
        
        grid.y_website_top = 0
        grid.y_website_bottom = grid.y_website_top + grid.monitor_height

    return car_list_data

def main(url):

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
    option.add_experimental_option("excludeSwitches", ["enable-automation"])
    option.add_experimental_option('useAutomationExtension', False)

    browser = webdriver.Chrome(chrome_options=option)
    browser.fullscreen_window()
    browser.set_script_timeout(5)

    browser.get(url)
    sleep(7)

    grid_one = regrid.coordinate_grid(browser)

    sleep(2)

    print(list_page_navi(browser, grid_one))

    # list_page_navi(browser)

    # set_the_region(browser, ['Санкт-Петербург', 'Москва'])
    # filter_mark(browser, 'Audi')
    sleep(1)


if __name__ == "__main__":
    
    main('https://auto.ru/sankt-peterburg/cars/used/body-allroad/?sort=cr_date-desc&top_days=1')
        