import keyboard

keyboard.hook(lambda key_event:print(f'Name:{key_event.name}, ScanCode:{key_event.scan_code}'))

while True:
    x=1