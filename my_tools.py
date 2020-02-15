import pickle
import json
from screeninfo import screeninfo
import math
import csv

def file_s(f_name, obj):
    with open(f_name, 'w') as output:
        output.write(obj)

def json_s(f_name, obj):
    with open(f_name, 'w') as output:
        json.dump(obj, output)

def json_l(f_name):
    with open(f_name, 'r') as input_:
        obj = json.load(input_)
    return obj


def s_pickle(f_name, obj):
    with open(f_name, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output)

def l_pickle(f_name):
    with open(f_name, 'rb') as input_:
        obj = pickle.load(input_)

    return obj

def monitor_res():

    monitor_list = {}

    for m in screeninfo.get_monitors():
        
        monitor_list.update({m.name: (m.height, m.width)})
        m_name = list(monitor_list.keys())

    return monitor_list[m_name[0]]

def csv_writer(data, path):

    with open(path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            writer.writerow(line)

def mouse_moves_calcs(_dict):

    result_dict = {}

    for move in _dict:
        
        dict_of_points = _dict.get(move)

        start_point = list(dict_of_points.keys())[0]
        finish_point = list(dict_of_points.keys())[-1]

        start_x = dict_of_points.get(start_point)[0]
        start_y = dict_of_points.get(start_point)[1]
        start_t = dict_of_points.get(start_point)[2]
        
        finish_x = dict_of_points.get(finish_point)[0]
        finish_y = dict_of_points.get(finish_point)[1]
        finish_t = dict_of_points.get(finish_point)[2]

        distance_OX = math.fabs(finish_x - start_x)
        distance_OY = math.fabs(finish_y - start_y)

        try:
            speed_two_points = (((finish_x - start_x) ** 2 + (finish_y - start_y) ** 2) ** 0.5) / (finish_t - start_t)
        except:
            pass

        try:
            speed_OX = ((finish_x - start_x) ** 2) ** 0.5 / (finish_t - start_t)
        except:
            pass
        
        try:
            speed_OY = ((finish_y - start_y) ** 2) ** 0.5 / (finish_t - start_t)
        except:
            pass

        result_dict.update({move: [distance_OX, distance_OY, speed_two_points, speed_OX, speed_OY, finish_t - start_t]})
    
    return result_dict

if __name__ == "__main__":
    dict_ = json_l('test_search_Thu Feb  6 03:44:52 2020.jsn')

    print(dict_['Техническая информация'])