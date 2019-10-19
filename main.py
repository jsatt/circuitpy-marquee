import analogio
import digitalio
import math
import time

import neopixel

import settings
from sequences import init_sequences

switch1 = digitalio.DigitalInOut(settings.SWITCH_1)
switch1.direction = digitalio.Direction.INPUT
switch1.pull = settings.SWITCH_PULL
switch2 = digitalio.DigitalInOut(settings.SWITCH_2)
switch2.direction = digitalio.Direction.INPUT
switch2.pull = settings.SWITCH_PULL
switch3 = digitalio.DigitalInOut(settings.SWITCH_3)
switch3.direction = digitalio.Direction.INPUT
switch3.pull = settings.SWITCH_PULL
switch4 = digitalio.DigitalInOut(settings.SWITCH_4)
switch4.direction = digitalio.Direction.INPUT
switch4.pull = settings.SWITCH_PULL
switch5 = digitalio.DigitalInOut(settings.SWITCH_5)
switch5.direction = digitalio.Direction.INPUT
switch5.pull = settings.SWITCH_PULL
brightness = analogio.AnalogIn(settings.BRIGHTNESS_PIN)
brightness_range = settings.BRIGHTNESS_RANGE
speed = analogio.AnalogIn(settings.SPEED_PIN)
speed_range = settings.SPEED_RANGE
sequences = init_sequences(settings.SEQUENCES, settings.NEOPIXEL_COUNT)


state = {
    'switches': [None] * 5,
    'current_switch': 0,
    'sequence': sequences[0],
    'speed': 1,
    'brightness': 1,
}


def get_switch_values():
    return [
        switch_value(switch1),
        switch_value(switch2),
        switch_value(switch3),
        switch_value(switch4),
        switch_value(switch5),
    ]

def update_state():
    switches = get_switch_values()
    current_switch = state['current_switch']
    sequence = state['sequence']

    if not switches[current_switch]:
        for idx, val in enumerate(switches):
            if val:
                try:
                    current_switch = idx
                    sequence = sequences[idx]
                except IndexError:
                    pass

    state.update({
        'switches': switches,
        'current_switch': current_switch,
        'sequence': sequence,
        'speed': max(speed.value - speed_range[0], 0) / (speed_range[1] - speed_range[0]),
        'brightness': max(brightness.value - brightness_range[0], 0) / (brightness_range[1] - brightness_range[0]),
    })


def switch_value(switch):
    return switch.value is (settings.SWITCH_PULL is digitalio.Pull.DOWN)


with neopixel.NeoPixel(settings.NEOPIXEL_PIN,
                       settings.NEOPIXEL_COUNT,
                       pixel_order=settings.NEOPIXEL_ORDER,
                       auto_write=False) as pixels:
    while True:
        update_state()
        seq = state['sequence']
        if seq.tick():
            seq.apply(pixels, state['brightness'])
        if settings.DEBUG:
            print(state)
        time.sleep(state['speed'] / settings.TICK_HZ)
