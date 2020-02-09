from pynput import mouse
import time
import statistics as stat

import my_tools

click_dict = {'click0': []}
click_count = 0

def on_click(x, y, button, pressed):
    
    global click_dict, click_count
    current_click = click_dict['click' + str(click_count)]

    if pressed:
        # print(f'Pressed at {(x, y)} at time {time.time()}')
        current_click.append(time.time())

    else:
        # print(f'Unpresed at {(x, y)} at time {time.time()}')
        current_click.append(time.time())
        current_click.append(current_click[1] - current_click[0])
        
        click_count += 1
        click_dict.update({'click' + str(click_count): []})


def click_statistic():

    global click_dict

    total_clicks = list(click_dict.keys())
    total_clicks.pop()

    clicks_time = [round(click_dict[i][2], 4) for i in total_clicks]

    return {'total_clicks': len(clicks_time),
            'min_time': min(clicks_time),
            'max_time': max(clicks_time),
            'mean_time': round(stat.mean(clicks_time), 4),
            'stadard_deviation': round(stat.stdev(clicks_time), 4)}


if __name__ == "__main__":
    
    try:
        with mouse.Listener(
            on_click=on_click) as listener:
            listener.join()
    except KeyboardInterrupt:  
        # save_results()
        print(click_statistic())
        # my_tools.json_s('mouse_click_stat', click_statistic())
        print('User killed the process')