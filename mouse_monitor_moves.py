from pynput import mouse
import time
import logging
import my_tools

grand_dict = {'move0': []}
move_count = 0

def on_move(x, y):
    
    print(f'Pointer moved to {(x, y)} at time: {time.time()}')
    logging.info(f'Mouse: {(x, y)}: Time: {time.time()}')

    global grand_dict
    grand_dict['move' + str(move_count)].append([x, y, float(time.time())])


def on_click(x, y, button, pressed):
    
    if pressed:
        print(f'Pressed at {(x, y)} at time {time.time()}')
        logging.info(f'Button_pressed: {(x, y)}: time: {time.time()}')
    else:
        print(f'Unpresed at {(x, y)} at time {time.time()}')
        logging.info(f'Button_released: {(x, y)}: time: {time.time()}')

        global move_count
        move_count += 1

        global grand_dict
        grand_dict.update({'move' + str(move_count): [x, y, float(time.time())]})
        print(grand_dict)


def save_results():
    
    global grand_dict
    my_tools.s_pickle('mouse_track_'+ str(time.ctime(time.time())), grand_dict)


if __name__ == "__main__":
    logging.basicConfig(format='%(message)s', filename=f'monitor_{time.ctime(time.time())}.log', level=logging.DEBUG)
    
    try:
        with mouse.Listener(
            on_move=on_move,
            on_click=on_click) as listener:
            listener.join()
    except KeyboardInterrupt:  
        save_results()
        print('User killed the process')