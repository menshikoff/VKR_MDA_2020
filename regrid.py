import time
import random
from screeninfo import screeninfo
from pynput.mouse import Controller, Button
import math
import numpy as np
import bezier


class coordinate_grid:

    monitor_height = screeninfo.get_monitors()[0].height
    monitor_width = screeninfo.get_monitors()[0].width
    browser_tools_panel = 0
    browser_bottom_panel = 0
    mouse_ = Controller()

    def __init__(self, browser):
        
        # Координата по оси OY верхней видимой части сайта в системе координат монитора:
        self.y_screen_top = browser.get_window_rect()['y'] + self.browser_tools_panel
        
        # Координата по оси OY нижней видимой части сайта в системе координат монитора:
        self.y_screen_bottom = browser.get_window_rect()['y'] + browser.get_window_rect()['height'] - self.browser_bottom_panel
        
        # Координата по оси OY верхней видимой части сайта в системе координат сайта:
        self.y_website_top = 0
        
        # Координата по оси OY нижней видимой части сайта в системе координат сайта:
        self.y_website_bottom = browser.get_window_rect()['height'] - self.browser_tools_panel - self.browser_bottom_panel
        self.y_website_bottom_lim = self.y_website_bottom

        # Координата по оси OX левой видимой части сайта в системе координат монитора:
        self.x_screen_left = browser.get_window_rect()['x']

        # Координата по оси OX правой видимой части сайта в системе координат монитора:
        self.x_screen_left = browser.get_window_rect()['x'] + browser.get_window_rect()['width'] - self.browser_bottom_panel


    def in_focus(self, element):
        """Функция проверяет находится ли элемент, на который необходимо переместить 
        указатель мыши на экране, прокручивает экран до элемента, случайным образом
        опредляет целевую точку на элементе и возвращает координаты экрана определенной точки.

        :param element: WebElement
        :return: возвращает координаты целевой точки
        """

        # В качестве параметра element передается результат работы метода "find_element_by_xpath"
        element_x = element.rect['x']
        element_y = element.rect['y']
        element_height = element.rect['height']
        element_width = element.rect['width']

        while element_y + element_height + random.randrange(30, 100, 10) > self.y_website_bottom:
            self.mouse_.scroll(0, -1)
            self.y_website_top += 53
            self.y_website_bottom += 53
            time.sleep(random.uniform(0.0077, 0.1385))
            element_y = element.rect['y']
     
        while element_y < self.y_website_top:
            self.mouse_.scroll(0, 1)
            self.y_website_top -= (53 if self.y_website_top > 0 else 0)
            self.y_website_bottom -= (53 if self.y_website_bottom > self.y_website_bottom_lim else 0)
            time.sleep(random.uniform(0.0077, 0.1385)) #Параметры установлены на основании статистики по скролингу пользователя.

        point_on_element_x = element_x + random.randint(int(element.rect['width'] * 0.2), 
                                                        int(element.rect['width'] * 0.7))

        point_on_element_y = self.y_screen_bottom - (self.y_website_bottom - element_y) + random.randint(int(element.rect['height'] * 0.2), int(element.rect['height'] * 0.8))

        return point_on_element_x, point_on_element_y
    

    def bezier_path(self, x1, y1, x2, y2):
        """Функция возвращает список координат точек для построения пути указателя мыши
        до целеовой координаты на экране

        :param x1:  координата по оси ОХ текущей позиции указателя мыши
        :param y1:  координата по оси ОY текущей позиции указателя мыши
        :param x2:  координата по оси ОХ целевой точки для указателя мыши
        :param y2:  координата по оси ОY целевой точки для указателя мыши
        :return: список координат точек
        """
        
        k = (y1 - y2) / (x1 - x2)
        b = y2 - k * x2

        x_delta = x2 - x1
        y_delta = y2 - y1

        up_down_direction = random.choice([-1, 1])

        x_inter_1 = x1 + int(x_delta * random.randrange(-15, 40, 3)/100)
        y_inter_1 = k * x_inter_1 + b + up_down_direction * int(y_delta * random.randrange(5, 25, 2) / 100)

        if math.fabs(x_delta) > 100:
            x_inter_2 = x1 + int(x_delta * random.randrange(80, 120, 3)/100)
            y_inter_2 = k * x_inter_2 + b + up_down_direction * (-1) * int(y_delta * random.randrange(5, 25, 2) / 100)
        else:
            x_inter_2 = x2
            y_inter_2 = y2

        nodes1 = np.asfortranarray([
        [x1, x_inter_1, x_inter_2 ,x2],
        [y1, y_inter_1, y_inter_2, y2],])

        curve1 = bezier.Curve(nodes1, degree=3)
        s_vals = np.linspace(0., 1., math.fabs(int(x2 - x1))) 
        points = curve1.evaluate_multi(s_vals)
        points = points.astype(int)

        return points

    def mouse_click_left(self):
        """Функция иммитирует нажатие левой кнопки мыши и ничего не возвращает
        """

        self.mouse_.press(Button.left)
        time.sleep(random.uniform(0.0578, 0.1129))  #Значения установлены на основани статистической информации о скорости клика пользователя
        self.mouse_.release(Button.left)

    def mouse_move_to(self, element):
        """ Функция перемещает курсор мыши от текущей позиции нв экране до целевого элемента на сранице
        :param element: WebElement а который необходимо навести указатель мыши
        :return: None
        """
        element_destination = self.in_focus(element)

        # Строим путь до элемента из точек:
        track_to_element = self.bezier_path(self.mouse_.position[0], 
                            self.mouse_.position[1], 
                            element_destination[0], 
                            element_destination[1])
        
        speed_OX_1 = [(0.18, 0,22), (0.012, 0.017), (0.003, 0.005), (0.0030, 0.0070), (0.0035, 0.0055)]
        speed_OX_2 = [(0.05, 0.19), (0.016, 0.030), (0.016, 0.047),	(0.0108, 0.0211), (0.0044, 0.0082)]

        distance_OX = math.fabs(element_destination[0] - self.mouse_.position[0])
        distance_OY = math.fabs(element_destination[1] - self.mouse_.position[1])

        if distance_OX >= distance_OY:
            speed_choice = speed_OX_1
        else:
            speed_choice = speed_OX_2

        if distance_OX <= 20:
            point_interval = speed_choice[0]
        elif 20 < distance_OX <= 50:
            point_interval = speed_choice[1]
        elif 50 < distance_OX <= 100:
            point_interval = speed_choice[2]
        elif 100 < distance_OX <= 300:
            point_interval = speed_choice[3]
        elif distance_OX > 300:
            point_interval = speed_choice[4]    

        for i in range(len(track_to_element[0])):
            self.mouse_.position = (track_to_element[0][i], track_to_element[1][i])
            time.sleep(random.uniform(point_interval[0], point_interval[1]))
        
        time.sleep(0.4)

    def mouse_scroll(self, direction):
        """Функция осуществляет одно прокручивание колеса мыши по заданному направлению вверз/вниз

        :param direction: для вижения вниз задаем -1 / для движения вверх задаем "1"        
        :return: None
        """
        self.mouse_.scroll(0, direction)
        time.sleep(random.uniform(0.0077, 0.1385))
