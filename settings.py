import board
import digitalio
import neopixel

DEBUG = False

NEOPIXEL_PIN = board.D5
NEOPIXEL_COUNT = 20
NEOPIXEL_ORDER = neopixel.GRB

SWITCH_1 = board.D7
SWITCH_2 = board.D12
SWITCH_3 = board.D11
SWITCH_4 = board.D10
SWITCH_5 = board.D9
SWITCH_PULL = digitalio.Pull.UP

BRIGHTNESS_PIN = board.A2
BRIGHTNESS_RANGE = (0, .01)
SPEED_PIN = board.A1
SPEED_RANGE = (128, 65520)

TICK_HZ = 50
BRIGHTNESS_MULTIPLIER = 1


SEQUENCES = [
    {
        'name': 'fade',
        'brightness': 50,
        'rate': 50,
        'colors': ['red', 'orange', 'yellow'],
    },
    {
        'name': 'rotate',
        'brightness': 50,
        'rate': 50,
        'colors': ['red', 'violet', 'blue'],
    },
    {
        'name': 'cycle',
        'brightness': 50,
        'rate': 50,
        'colors': ['green', 'cyan', 'blue'],
    },
    {
        'name': 'chase',
        'brightness': 50,
        'rate': 50,
        'instances': 1,
        'colors': ['cyan', 'magenta', 'yellow', 'black'],
    },
    {
        'name': 'sparkle',
        'brightness': 10,
        'rate': 50,
        'reverse': True,
        'instances': 2,
        'colors': ['blue', 'violet', 'white'],
    },
]
