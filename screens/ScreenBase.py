from datetime import datetime, timedelta
from utils.matrix import ScreenMatrix


class ImageScreenBase:
    update_interval_seconds = 60
    def __init__(self, matrix: ScreenMatrix):
        self.__matrix = matrix
        self.__last_refreshed = datetime.now()
        self.__last_image = None

    def tick(self):
        if datetime.now() > self.__last_refreshed + timedelta(0, self.update_interval_seconds):
            self.__refresh_and_render()

    def __refresh_and_render(self):
        self.__last_refreshed = datetime.now()
        self.__last_image = self.render()
        self.__draw_image()

    def __draw_image(self):
        if not self.__last_image is None:
            self.__matrix.render_image(self.__last_image)

    def render(self):
        return None

    def focus(self):
        self.__draw_image()

    def reset(self):
        self.__refresh_and_render()

    def preset(self, index):
        a = None # no-op