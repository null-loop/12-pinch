import sys
import time
from datetime import datetime, timedelta

import matrix
from gitScreen import GitScreen
from lifeScreen import LifeScreen
from snakeScreen import SnakeScreen
from spotifyScreen import SpotifyScreen

try:
    print("Press CTRL-C to stop.")
    screens = [LifeScreen(),GitScreen(),SnakeScreen(),SpotifyScreen()]
    current_screen_index = 0
    current_screen = screens[0]
    screen_cycle_interval_seconds = 2 * 60 # how long until we switch to next screen
    last_screen_cycle_time = datetime.now()
    while True:
        if datetime.now() > last_screen_cycle_time + timedelta(0, screen_cycle_interval_seconds):
            last_screen_cycle_time = datetime.now()
            current_screen_index = current_screen_index + 1
            if current_screen_index == len(screens):
                current_screen_index = 0
            current_screen = screens[current_screen_index]
            if not current_screen.render_as_image:
                current_screen.fresh_render()

        if current_screen.render_as_image:
            image = current_screen.render()
            if not image is None:
                matrix.render_image_on_matrix(image)
        else:
            current_screen.render()

        if current_screen.update_interval_seconds > 0:
            time.sleep(current_screen.update_interval_seconds)

except KeyboardInterrupt:
    sys.exit(0)