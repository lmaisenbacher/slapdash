import slapdash


class Channel:
    value: float = 0.0


class Device:
    _voltage = 0.0
    gpio = [0, 0, 1, 0]

    def __init__(self):
        self.channels = [Channel() for i in range(4)]

    @property
    def voltage(self) -> float:
        return self._voltage

    @voltage.setter
    def voltage(self, value: float):
        print('Setting voltage')
        self._voltage = value

    def calculate(self, x: int, y: int):
        '''remote call'''
        return x + y


if __name__ == "__main__":
    hostname = 'localhost'
    slapdash.run(Device(), host=hostname, port=8001)
