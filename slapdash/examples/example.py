import slapdash


class Channel:
    _frequency = 1
    _time = 2

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, value):
        self._frequency = value

    @property
    def time(self):
        return self._time


class Settings:
    _enabled = True

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value

    @property
    def version(self):
        return '1.0'


class Example:
    _voltage = 0.0
    _channels = []
    gpio = [0, 1, 2, 3]

    def __init__(self):
        self.channels = [Channel() for i in range(4)]
        self.settings = Settings()

    def __repr__(self):
        return 'Example'

    @property
    def name(self) -> str:
        '''name of the device'''
        return "Name"

    @property
    def voltage(self) -> float:
        return self._voltage

    @voltage.setter
    def voltage(self, value: float):
        self._voltage = value

    def remote_call(self, x: int, y: int):
        '''remote call'''
        return x+y


if __name__ == '__main__':
    example = Example()
    slapdash.run(example)
