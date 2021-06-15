from pynput import mouse, keyboard
from pynput.mouse import Button
from pynput.mouse import Controller as Controller_Mouse
from pynput.keyboard import Controller as Controller_Keyboard
from src.file.parser import get_latest_frame, save_df_csv
import pandas as pd
import time
import yaml
import os

file = os.path.abspath("../config.yaml")
stream = open(file, 'r')
configuration = yaml.load(stream)


class Automation:
    mouse_controller = Controller_Mouse()
    keyboard_controller = Controller_Keyboard()
    MOVE_TASK = 'move_mouse'
    CLICK_TASK = 'click_mouse'
    KEYBOARD_TASK = 'keystroke'
    DATA_FILE_PATH = configuration["HOST"]["SOURCE_PATH"]
    SAVE_PATH = os.path.abspath("../transfer_data/data.csv")
    AUTOMATION_PATH = os.path.abspath("../automations/temp.pkl")
    automation_cols = ['x', 'y', 'task']
    automation_df = pd.DataFrame(columns=automation_cols)
    automation_loop = True

    def __init__(self, file_transfer):
        self.file_transfer = file_transfer

    def automate(self):
        self.automation_loop = True
        self.start_keyboard_listen_automation()
        while self.automation_loop:
            instructions = pd.read_pickle(self.AUTOMATION_PATH)
            instructions.apply(lambda x: self.complete_task(x.x, x.y, x.task), axis=1)
            df = get_latest_frame(self.DATA_FILE_PATH)
            save_df_csv(df, self.SAVE_PATH)
            self.file_transfer.scp_put()
        return

    def create_automation(self):
        self.automation_loop = True

        input("Begin Automation. Press Enter to begin")
        time.sleep(1)
        print("Move cursor to desired position and click or type")
        self.start_keyboard_listen()
        self.start_mouse_listen()
        while self.automation_loop:
            time.sleep(0.1)
        self.automation_df.to_pickle(self.AUTOMATION_PATH)
        print("Not working")

    def complete_task(self, x, y, task):
        if task == self.MOVE_TASK:
            self.mouse_controller.position = (x, y)
        elif task == self.CLICK_TASK:
            time.sleep(1.5)
            self.mouse_controller.press(Button.left)
            self.mouse_controller.release(Button.left)
        elif task == self.KEYBOARD_TASK:
            self.keyboard_controller.press(x)
            self.keyboard_controller.release(x)
            if x == keyboard.Key.enter:
                time.sleep(1.5)
            return
        else:
            print('Invalid instruction: ' + task)
        return

    def add_task(self, x, y, task):
        new_task = {
            'x': x,
            'y': y,
            'task': task
        }
        temp = pd.DataFrame(data=new_task, index=[0])
        self.automation_df = self.automation_df.append(temp, ignore_index=True)
        print("{} task added Successfully".format(task))

    def on_click(self, x, y, button, pressed):
        if not self.automation_loop:
            return False
        if pressed:
            self.add_task(x, y, self.MOVE_TASK)
        else:
            self.add_task(x, y, self.CLICK_TASK)

    def on_release(self, key):
        if key != keyboard.Key.esc:
            self.add_task(key, 0, self.KEYBOARD_TASK)
        else:
            self.automation_loop = False
            # Stop listener
            return False

    def on_release_automation(self, key):
        if key == keyboard.Key.esc:
            self.automation_loop = False
            # Stop listener
            return False

    def start_mouse_listen(self):
        # Collect events until released
        # with mouse.Listener(
        #         on_click=self.on_click
        # ) as listener:
        #     listener.join()

        listener = mouse.Listener(
            on_click=self.on_click)
        listener.start()

    def start_keyboard_listen(self):
        listener = keyboard.Listener(
            on_release=self.on_release)
        listener.start()
        # # Collect events until released
        # with keyboard.Listener(
        #         on_press=on_press,
        #         on_release=on_release) as listener:
        #     listener.join()

        # ...or, in a non-blocking fashion:

    def start_keyboard_listen_automation(self):
        listener = keyboard.Listener(
            on_release=self.on_release_automation)
        listener.start()

# Read pointer position
# print('The current pointer position is {0}'.format(
#     mouse.position))

# Set pointer position
# mouse.position = (43, 65)
# print('Now we have moved it to {0}'.format(
#     mouse.position))

# # Move pointer relative to current position
# mouse.move(5, -5)
#
# Press and release
# mouse.press(Button.left)
# mouse.release(Button.left)
#
# # Double click; this is different from pressing and releasing
# # twice on macOS
# mouse.click(Button.left, 2)
#
# # Scroll two steps down
# mouse.scroll(0, 2)
