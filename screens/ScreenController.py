import sys

import keyboard

from screens.Enums import Command
from screens.GitScreen import GitScreen
from screens.LifeScreen import LifeScreen
from screens.SnakeScreen import SnakeScreen
from screens.SpotifyScreen import SpotifyScreen
from utils import matrix
from utils.matrix import ScreenMatrix


class ScreenController:
    def __init__(self):
        self.__matrix = ScreenMatrix()
        self.__screens = [LifeScreen(self.__matrix),GitScreen(self.__matrix),SnakeScreen(self.__matrix),SpotifyScreen(self.__matrix)]
        self.__current_screen_index = 0
        self.__command_queue = []
        self.__paused = False
        self.__powered = True
        self.__step_once = False
        keyboard.on_press(lambda key_event: self.key_pressed(key_event.scan_code, key_event.name))

    def current_screen(self):
        return self.__screens[self.__current_screen_index]

    def key_pressed(self, scan_code, name):
        print(f'Scan_Code:{scan_code}')
        command = Command.NONE
        if scan_code == 116: command = Command.POWER
        if scan_code == 168: command = Command.REWIND
        if scan_code == 208: command = Command.FAST_FORWARD
        if scan_code == 165: command = Command.PREVIOUS
        if scan_code == 163: command = Command.NEXT
        if scan_code == 164: command = Command.PAUSE_PLAY
        if scan_code == 2: command = Command.PRESET_1
        if scan_code == 3: command = Command.PRESET_2
        if scan_code == 4: command = Command.PRESET_3
        if scan_code == 5: command = Command.PRESET_4
        if scan_code == 6: command = Command.PRESET_5
        if scan_code == 7: command = Command.PRESET_6
        if scan_code == 8: command = Command.PRESET_7
        if scan_code == 9: command = Command.PRESET_8
        if scan_code == 10: command = Command.PRESET_9
        if scan_code == 11: command = Command.PRESET_10
        if scan_code == 113: command = Command.RESET
        if scan_code == 115: command = Command.BRIGHTNESS_UP
        if scan_code == 114: command = Command.BRIGHTNESS_DOWN
        if scan_code == 104: command = Command.PROGRAM_UP
        if scan_code == 109: command = Command.PROGRAM_DOWN
        self.__command_queue.append(command)

    def run(self):
        try:
            print("Press CTRL-C to stop.")
            self.__focus_current()
            while True:
                self.process_command_queue()
                if self.__paused:
                    if self.__step_once:
                        self.__step_once = False
                        self.current_screen().tick()
                else:
                    self.current_screen().tick()

        except KeyboardInterrupt:
            sys.exit(0)

    def process_command_queue(self):
        # continue while there's work in the queue
        while len(self.__command_queue) > 0:
            # pop the first command and process it
            command = self.__command_queue.pop(0)
            self.process_command(command)

    def process_command(self, command:Command):
        print(f'Command:{command}')
        if command == Command.POWER:
            if self.__powered:
                self.__paused = True
                self.__powered = False
                self.__matrix.clear()
            else:
                self.__paused = False
                self.__powered = True
                self.__focus_current()
        if command == Command.PAUSE_PLAY:
            self.__paused = not self.__paused
        if command == Command.PREVIOUS:
            next_index = self.__current_screen_index - 1
            if self.__current_screen_index == 0: next_index = len(self.__screens) - 1
            self.__change_screen(next_index)
        if command == Command.NEXT:
            next_index = self.__current_screen_index + 1
            if self.__current_screen_index == len(self.__screens) - 1: next_index = 0
            self.__change_screen(next_index)
        if command == Command.RESET:
            self.__reset_current()
        if command == Command.FAST_FORWARD:
            self.__step_once = True
        if command == Command.BRIGHTNESS_DOWN:
            self.__matrix.decrease_brightness()
            self.__focus_current()
        if command == Command.BRIGHTNESS_UP:
            self.__matrix.increase_brightness()
            self.__focus_current()
        if command == Command.PROGRAM_UP:
            self.__matrix.start_new_canvas()
            self.current_screen().program_up()
            self.__matrix.finish_canvas()
        if command == Command.PROGRAM_DOWN:
            self.__matrix.start_new_canvas()
            self.current_screen().program_down()
            self.__matrix.finish_canvas()
        if command >= Command.PRESET_1:
            preset = command - Command.PRESET_1 + 1
            self.__preset_current(preset)

    def __focus_current(self):
        self.__matrix.start_new_canvas()
        self.current_screen().focus()
        self.__matrix.finish_canvas()

    def __reset_current(self):
        self.__matrix.start_new_canvas()
        self.current_screen().reset()
        self.__matrix.finish_canvas()

    def __preset_current(self, preset_index:int):
        self.__matrix.start_new_canvas()
        self.current_screen().preset(preset_index)
        self.__matrix.finish_canvas()

    def __change_screen(self, index):
        self.__matrix.clear()
        print(f'Setting screen index to {index}')
        self.__current_screen_index = index

        self.__focus_current()
        print(f'Focused screen {self.current_screen().label}')