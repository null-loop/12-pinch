from PIL import Image
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

options = RGBMatrixOptions()
options.rows = 64
options.cols = 64
options.chain_length = 4
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'
options.gpio_slowdown = 2
options.limit_refresh_rate_hz = 120
options.brightness = 50
options.disable_hardware_pulsing = True
options.drop_privileges = False

matrix = RGBMatrix(options = options)

def increase_brightness():
    options.brightness = options.brightness + 1
    if options.brightness >= 100:
        options.brightness = 100
    ##__reset_matrix()

def decrease_brightness():
    options.brightness = options.brightness - 1
    if options.brightness <= 0:
        options.brightness = 1
    ##__reset_matrix()

##def __reset_matrix():
  ##  matrix = RGBMatrix(options = options)

def render_image_on_matrix(image: Image):
    # rearrange for rendering...
    top_half = image.crop((0, 0, 128, 64))
    bottom_half = image.crop((0, 64, 128, 128))

    stitched = Image.new('RGB', (256, 64))
    stitched.paste(top_half, (0, 0))
    stitched.paste(bottom_half, (128, 0))

    rgb = stitched.convert('RGB')

    matrix.SetImage(rgb)

def set_matrix_point(x, y, r, g, b):
    t_x = x
    t_y = y
    if t_y >= 64:
        t_x = t_x + 128
        t_y = t_y - 64
    colour = graphics.Color(r, g, b)
    graphics.DrawLine(matrix, t_x, t_y, t_x, t_y, colour)

def clear():
    matrix.Clear()