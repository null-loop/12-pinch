from screens.Enums import Command
from screens.GitScreen import GitScreen
from screens.LifeScreen import LifeScreen
from screens.SnakeScreen import SnakeScreen
from screens.SpotifyScreen import SpotifyScreen
import keyboard
import sys

from utils import matrix


class ScreenController:
    def __init__(self):
        self.__screens = [LifeScreen(),GitScreen(),SnakeScreen(),SpotifyScreen()]
        self.__current_screen_index = 0
        self.__command_queue = []
        self.__paused = False
        self.__powered = True
        keyboard.on_press(lambda key_event: self.key_pressed(key_event.scan_code))

    def current_screen(self):
        return self.__screens[self.__current_screen_index]

    def key_pressed(self, scan_code):
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
        if scan_code == 11: command = Command.PRESET_0
        if scan_code == 113: command = Command.RESET
        ## vol up - 115
        ## vol down - 114
        ## program up - 104
        ## program down - 109
        ## reset - 113
        self.__command_queue.append(command)

    def run(self):
        try:
            print("Press CTRL-C to stop.")
            self.current_screen().focus()
            while True:
                if not self.__paused: self.current_screen().tick()
                self.process_command_queue()

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
            self.__paused = not self.__paused
            if self.__powered:
                self.__powered = False
                matrix.clear()
            else:
                self.__powered = True
                self.current_screen().focus()
        if command == Command.PAUSE_PLAY:
            self.__paused = not self.__paused
        if command == Command.PREVIOUS:
            next_index = self.__current_screen_index - 1
            if self.__current_screen_index == -1: next_index = len(self.__screens) - 1
            self.change_screen(next_index)
        if command == Command.NEXT:
            next_index = self.__current_screen_index + 1
            if self.__current_screen_index == len(self.__screens) - 1: next_index = 0
            self.change_screen(next_index)
        if command == Command.RESET:
            matrix.clear()
            self.current_screen().reset()

    def change_screen(self, index):
        matrix.clear()
        self.__current_screen_index = index
        self.current_screen().focus()