import keyboard

keyboard.on_press(lambda key_event:print(f'Name:{key_event.name}, ScanCode:{key_event.scan_code}'))

while True:
    x=1

# Recorded scan codes

# Power - 116
# Rewind - 168
# Fastforward - 208
# Previous - 165
# Next - 163
# Pause / Play - 164
# 1 to 0 - 2 to 11 (n+1)