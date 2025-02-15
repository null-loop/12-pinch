from PIL import Image
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

class ScreenMatrix:
    def __init__(self):
        self.__options = RGBMatrixOptions()
        self.__options.rows = 64
        self.__options.cols = 64
        self.__options.chain_length = 4
        self.__options.parallel = 1
        self.__options.hardware_mapping = 'adafruit-hat'
        self.__options.gpio_slowdown = 2
        self.__options.limit_refresh_rate_hz = 120
        self.__options.brightness = 50
        self.__options.disable_hardware_pulsing = True
        self.__options.drop_privileges = False
        self.__matrix = RGBMatrix(options=self.__options)
        self.__next_canvas = None

    def start_new_canvas(self):
        self.__next_canvas = self.__matrix.CreateFrameCanvas()

    def finish_canvas(self):
        self.__matrix.SwapOnVSync(self.__next_canvas)
        self.__next_canvas = None

    def render_image(self, image: Image):
        # rearrange for rendering...
        top_half = image.crop((0, 0, 128, 64))
        bottom_half = image.crop((0, 64, 128, 128))

        stitched = Image.new('RGB', (256, 64))
        stitched.paste(top_half, (0, 0))
        stitched.paste(bottom_half, (128, 0))

        rgb = stitched.convert('RGB')
        if self.__next_canvas is not None:
            self.__next_canvas.SetImage(rgb)
        else:
            canvas = self.__matrix.CreateFrameCanvas()
            canvas.SetImage(rgb)
            self.__matrix.SwapOnVSync(canvas)

    def set_pixel(self, x, y, r, g, b):
        t_x = x
        t_y = y
        if t_y >= 64:
            t_x = t_x + 128
            t_y = t_y - 64
        if self.__next_canvas is not None:
            self.__next_canvas.SetPixel(t_x, t_y, r, g, b)
        else:
            self.__matrix.SetPixel(t_x, t_y, r, g, b)

    def clear(self):
        self.__matrix.Clear()

    def increase_brightness(self):
        n = self.__matrix.brightness + 20
        if n <= 0:
            n = 1
        self.__matrix.brightness = n

    def decrease_brightness(self):
        n = self.__matrix.brightness - 20
        if n <= 0:
            n = 1
        self.__matrix.brightness = n
