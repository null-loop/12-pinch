import sys
import time
from datetime import datetime, timedelta

import matrix
from gitScreen import GitScreen
from spotifyScreen import SpotifyScreen

try:
    print("Press CTRL-C to stop.")
    screens = [SpotifyScreen(),GitScreen()]
    current_screen_index = 0
    current_screen = screens[0]
    screen_cycle_interval_seconds = 5 * 60 # how long until we switch to next screen
    last_screen_cycle_time = datetime.now()
    while True:
        if datetime.now() > last_screen_cycle_time + timedelta(0, screen_cycle_interval_seconds):
            last_screen_cycle_time = datetime.now()
            current_screen_index = current_screen_index + 1
            if current_screen_index == len(screens):
                current_screen_index = 0
            current_screen = screens[current_screen_index]
        image = current_screen.render()
        if not image is None:
            matrix.render_image_on_matrix(image)

        time.sleep(current_screen.update_interval_seconds)

except KeyboardInterrupt:
    sys.exit(0)