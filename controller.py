import evdev
from evdev import InputDevice, categorize, ecodes
from picrawler import Picrawler


gamepad = InputDevice('/dev/input/event3')
crawler = Picrawler()


# do i even need this?
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
        return 'stop'

    return 'stop'


def main():
    speed = 80
    aBTN = 304
    bBTN = 305
    xBTN = 307
    yBTN = 308
    selectBTN = 314
    startBTN = 315
    x, y, rx, ry = 0, 0, 0, 0
    current_direction = 'stop'
    gamepad.grab()

    while True:
        event = gamepad.read_one()
        while event:
            if event.type == ecodes.EV_KEY:
                if event.value == 1:
                    if event.code == aBTN:
                        current_direction = 'backward'

                    elif event.code == yBTN:
                        current_direction = 'forward'

                    elif event.code == bBTN:
                        current_direction = 'turn right'

                    elif event.code == xBTN:
                        current_direction = 'turn left'

                    elif event.code == selectBTN:
                        current_direction = 'sit'

                    elif event.code == startBTN:
                        current_direction = 'stand'

                elif event.value == 0:
                    current_direction = 'stop'

            elif event.type == ecodes.EV_ABS:

                if event.code == ecodes.ABS_X:
                    x = normalize_direction(event.value)

                elif event.code == ecodes.ABS_Y:
                    y = normalize_direction(event.value)

                elif event.code == ecodes.ABS_RX:
                    rx = normalize_direction(event.value)

                elif event.code == ecodes.ABS_RY:
                    ry = normalize_direction(event.value)

                new_direction = joystick_movements(x, y, rx, ry)
                current_direction = new_direction

            event = gamepad.read_one()

        if current_direction != 'stop':
            if current_direction == 'sit':
                crawler.do_step(current_direction, 1, speed)
            elif current_direction == 'stand':
                crawler.do_step(current_direction, 1, speed)
            else:
                crawler.do_action(current_direction, 1, speed)

        else:
            crawler.do_action('stop', 1, speed)


try:
    main()
except KeyboardInterrupt:
    print("\nBye!")
    crawler.do_step('sit', 1, 90)
