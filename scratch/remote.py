import keyboard

keyboard.hook(lambda key_event:print(key_event.name))

while True:
    x=1