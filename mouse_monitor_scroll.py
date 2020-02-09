from pynput import mouse
import time
import statistics as stat

import my_tools

scrolling_time = []

def on_scroll(x, y, dx, dy):
    print('Scrolled {0} at {1} by {2}'.format(
        'down' if dy < 0 else 'up',
        (x, y), (dx, dy)))
    
    global scrolling_time

    scrolling_time.append(round(time.time(), 4))

    if dy < 0:
        pass
    else:
        pass

def scroll_statistic():
    time_sleep_intervals = []

    global scrolling_time

    for i in range(1, len(scrolling_time)):
        time_sleep_intervals.append(round(scrolling_time[i] - scrolling_time[i - 1], 4))

    return {'total_scroll_intervals': len(time_sleep_intervals),
            'min_time': min(time_sleep_intervals),
            'max_time': max(time_sleep_intervals),
            'mean_time': round(stat.mean(time_sleep_intervals), 4),
            'stadard_deviation': round(stat.stdev(time_sleep_intervals), 4)}

def main():
    
    try:
        with mouse.Listener(
            on_scroll=on_scroll) as listener:
            listener.join()
    except KeyboardInterrupt:
        
        # my_tools.json_s('scroll_time_intervals', scroll_statistic())
        print(scroll_statistic())
        print('User killed the process')


if __name__ == "__main__":
    main()