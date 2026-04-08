import evdev
from evdev import InputDevice, categorize, ecodes
from picrawler import Picrawler


def normalize_direction(val):
    max_val = 32768.0
    normalized = val / max_val
    return max(-1, min(1, normalized))


def joystick_movements(x, y, rx, ry):
    deadzone = 0.85

    if rx < -deadzone:
        return 'turn left'
    
    elif rx > deadzone:
        return 'turn right'
    
    elif y < -deadzone:
        return 'forward'
    
    elif y > deadzone:
        return 'backward'
    
    elif (abs(x) < deadzone) and (abs(y) < deadzone) and (abs(rx) < deadzone) and (abs(ry) < deadzone):
        return ''
    
    return ''


def connect_controller():
    gamepad = InputDevice('/dev/input/event3')
    print(gamepad)
    crawler = Picrawler()
    speed = 80

    aBTN   = 589825
    bBTN   = 589826
    xBTN   = 589827
    yBTN   = 589828
    selectBTN = 589831
    startBTN  = 589832

    x, y, rx, ry = 0, 0, 0, 0
    current_direction = ''
    last_msc_code = None
    gamepad.grab()

    try:
        while True:
            event = gamepad.read_one()

            while event:
                if event.type == ecodes.EV_MSC:
                    last_msc_code = event.value

                    if event.value == aBTN:
                        current_direction = 'backward'

                    elif event.value == yBTN:
                        current_direction = 'forward'

                    elif event.value == bBTN:
                        current_direction = 'turn right'

                    elif event.value == xBTN:
                        current_direction = 'turn left'

                    elif event.value == selectBTN:
                        current_direction = 'sit'

                    elif event.value == startBTN:
                        current_direction = 'stand'

                elif event.type == ecodes.EV_KEY:
                    if event.value == 0:
                        current_direction = ''

                elif event.type == ecodes.EV_ABS:
                    if event.code == ecodes.ABS_X:
                        x = normalize_direction(event.value)

                    elif event.code == ecodes.ABS_Y:
                        y = normalize_direction(event.value)

                    elif event.code == ecodes.ABS_RX:
                        rx = normalize_direction(event.value)

                    elif event.code == ecodes.ABS_RY:
                        ry = normalize_direction(event.value)
                        
                    current_direction = joystick_movements(x, y, rx, ry)

                event = gamepad.read_one()

            if current_direction in ('sit', 'stand'):
                crawler.do_step(current_direction, 1, speed)
            elif current_direction == '':
                continue
            else:
                crawler.do_action(current_direction, 1, speed)

    except KeyboardInterrupt:
        print("\nBye!")
        crawler.do_step('sit', 1, 90)


if __name__ == "__main__":
    connect_controller()