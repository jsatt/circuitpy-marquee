from math import ceil
from random import randint

COLORS = {
    'red': (255, 0, 0),
    'orange': (255, 60, 0),
    'yellow': (255, 128, 0),
    'chartreuse': (220, 255, 0),
    'green': (0, 255, 0),
    'spring_green': (0, 255, 80),
    'cyan': (0, 255, 200),
    'azure': (0, 80, 255),
    'blue': (0, 0, 255),
    'violet': (100, 0, 255),
    'magenta': (255, 0, 255),
    'rose': (255, 0, 80),
    'white': (255, 225, 200),
    'black': (0, 0, 0),
}

class Sequence:
    def __init__(self, length, brightness=100, colors=['white']):
        self.length = length
        self.brightness = brightness / 100
        self.colors = [COLORS.get(color, color) for color in colors]
        self.pixels = self.initial_pixels()
        self.initialize()
        self.step = 0

    def __repr__(self):
        return '<{}: colors={}>'.format(type(self).__name__, self.colors)

    def initialize(self, **kwargs):
        pass

    def tick(self):
        return True

    def apply(self, pixels, brightness):
        pixels.brightness = self.brightness
        pixels[::] = self.pixels
        pixels.show()

    def initial_pixels(self):
        return (self.colors * ceil(self.length / len(self.colors)))[:self.length]

class AnimatedSequence(Sequence):
    def __init__(self, *args, rate=100, reverse=False, **kwargs):
        self.rate = rate / 100
        self.reverse = reverse
        super().__init__(*args, **kwargs)

    def tick(self):
        act = False
        if (self.step % int(1 / self.rate)) == 0:
            act = True
        self.step += 1
        if self.step >= 100:
            self.step = 0
        return act

    def apply(self, *args, **kwargs):
        self.take_step()
        super().apply(*args, **kwargs)

    def take_step(self):
        pass


class Fade(AnimatedSequence):
    def initialize(self):
        self.max_brightness = self.brightness
        self.direction = 'u' if self.reverse else 'd'
        self.brightness = 0 if self.reverse else self.brightness
        self.step_size = (self.max_brightness / 2) * self.rate

    def take_step(self):
        if self.direction == 'd' and self.brightness >= 0:
            self.brightness -= self.step_size
        elif self.direction == 'u' and self.brightness <= self.max_brightness:
            self.brightness += self.step_size

        if self.brightness <= 0:
            self.direction = 'u'
        elif self.brightness >= self.max_brightness:
            self.direction = 'd'


class Rotate(AnimatedSequence):
    def take_step(self):
        if self.reverse:
            self.pixels.insert(0, self.pixels.pop())
        else:
            self.pixels.append(self.pixels.pop(0))


class Cycle(AnimatedSequence):
    def initialize(self):
        self.positions = [idx for idx in range(len(self.colors))]

    def take_step(self):
        self.pixels = [
            self.colors[self.positions[0]]
            if idx % len(self.colors) == self.positions[0]
            else COLORS['black']
            for idx in range(self.length)
        ]
        if self.reverse:
            self.positions.insert(0, self.positions.pop())
        else:
            self.positions.append(self.positions.pop(0))


class Chase(Rotate):
    def __init__(self, *args, instances=1, **kwargs):
        self.instances = instances
        super().__init__(*args, **kwargs)

    def initial_pixels(self):
        pixels = ((self.colors + [COLORS['black']] * (ceil(self.length / self.instances) - len(self.colors))) * self.instances)
        if self.reverse:
            pixels = [pixels[len(pixels) - 1 - idx] for idx in range(len(pixels))]

        return pixels[:self.length]


class Sparkle(AnimatedSequence):
    def __init__(self, *args, instances=1, **kwargs):
        self.instances = instances
        super().__init__(*args, **kwargs)
        self.positions = {}

    def initial_pixels(self):
        return [COLORS['black']] * self.length

    def take_step(self):
        color_count = len(self.colors)
        new_pix = []
        while len(new_pix) < self.instances and (
                self.length - self.instances * color_count) > len(new_pix):
            pixel = randint(0, self.length)
            if pixel not in self.positions:
                new_pix.append(pixel)
        for idx, pixel in enumerate(self.pixels):
            if idx in self.positions:
                if self.positions[idx] + 1 >= color_count:
                    del self.positions[idx]
                    self.pixels[idx] = COLORS['black']
                else:
                    self.positions[idx] += 1
                    self.pixels[idx] = self.colors[self.positions[idx]]
            elif idx in new_pix:
                self.positions[idx] = 0
                self.pixels[idx] = self.colors[0]

SEQUENCES = {
    'solid': {'cls': Sequence, 'args': [],},
    'fade': {'cls': Fade, 'args': ['reverse', 'rate'],},
    'rotate': {'cls': Rotate, 'args': ['reverse', 'rate'],},
    'cycle': {'cls': Cycle, 'args': ['reverse', 'rate'],},
    'chase': {'cls': Chase, 'args': ['instances', 'reverse', 'rate'],},
    'sparkle': {'cls': Sparkle, 'args': ['instances', 'rate'],},
}


def init_sequences(items, length):
    sequences = []
    for item in items:
        seq = SEQUENCES[item['name']]
        cls = seq['cls']
        kwargs = {
            kwarg: item[kwarg]
            for kwarg in ['colors', 'brightness'] + seq['args']
            if kwarg in item
        }
        sequences.append(cls(length, **kwargs))
    return sequences
