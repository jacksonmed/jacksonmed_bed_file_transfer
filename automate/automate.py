from pynput import mouse, keyboard
from pynput.mouse import Button, Controller
import pandas as pd
import time
import yaml

stream = open("config.yaml", 'r')
configuration = yaml.load(stream)




class automation:
    mouse_controller = Controller()
    MOVE_TASK = 'move_mouse'
    CLICK_TASK = 'click_mouse'
    KEYBOARD_TASK = 'keystroke'
    automation_cols = ['x', 'y', 'task']
    automation_df = pd.DataFrame(columns=automation_cols)
    automation_loop = True

    def __init__(self, file_transfer):
        self.file_transfer = file_transfer

    def create_automation(self, filename):
        self.automation_loop = True
        self.start_keyboard_listen()

        input("Begin Automation. Press Enter to begin")
        while self.automation_loop:
            print("Move cursor to desired position and click")
            self.start_mouse_listen()
            print("Task added")
        self.automation_df.to_csv(filename, index=False)

    def complete_task(self, x, y, task):
        if task == self.MOVE_TASK:
            self.mouse_controller.position = (x, y)
        elif task == self.CLICK_TASK:
            time.sleep(1.5)
            self.mouse_controller.press(Button.left)
            self.mouse_controller.release(Button.left)
        elif task == self.KEYBOARD_TASK:
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
        print("Task added Successfully")

    def automate(self, instruction_path):

        self.automation_loop = True
        self.start_keyboard_listen()
        while self.automation_loop:
            instructions = pd.read_csv(instruction_path)
            instructions.apply(lambda x: self.complete_task(x.x, x.y, x.task), axis=1)
            self.file_transfer.scp_put()
        return


    def on_move(self, x, y):
        # print('Pointer moved to {0}'.format(
        #     (x, y)))
        return

    def on_click(self, x, y, button, pressed):
        print('{0} at {1}'.format(
            'Pressed' if pressed else 'Released',
            (x, y)))
        if pressed:
            self.add_task(x, y, self.MOVE_TASK)
        else:
            self.add_task(x, y, self.CLICK_TASK)
            return False

    def on_scroll(self, x, y, dx, dy):
        print('Scrolled {0} at {1}'.format(
            'down' if dy < 0 else 'up',
            (x, y)))

    def start_mouse_listen(self):
        # Collect events until released
        with mouse.Listener(
                on_move=self.on_move,
                on_click=self.on_click,
                on_scroll=self.on_scroll) as listener:
            listener.join()

    def on_press(self, key):
        try:
            print('alphanumeric key {0} pressed\n'.format(
                key.char))
        except AttributeError:
            print('special key {0} pressed\n'.format(
                key))

    def on_release(self, key):
        global automation_loop
        print('{0} released\n'.format(
            key))
        if key == keyboard.Key.esc:
            self.automation_loop = False
            # Stop listener
            return False

    def start_keyboard_listen(self):
        # # Collect events until released
        # with keyboard.Listener(
        #         on_press=on_press,
        #         on_release=on_release) as listener:
        #     listener.join()

        # ...or, in a non-blocking fashion:
        listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
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
