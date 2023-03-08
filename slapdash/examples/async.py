import slapdash
import asyncio


class AsyncExample:

    counter: int
    _enable: bool

    def __init__(self):
        self.counter = 0
        self._enable = False

    def __repr__(self):
        return 'Asynchronous Example'

    @property
    def enable(self) -> bool:
        return self._enable

    @enable.setter
    def enable(self, value: bool):
        self._enable = value
        if value:
            self.counter = 0
            loop = asyncio.new_event_loop()
            loop.run_until_complete(self._start_counter())

    async def _start_counter(self):
        while self._enable:
            self.counter += 1
            await asyncio.sleep(1)


if __name__ == '__main__':
    async_example = AsyncExample()
    slapdash.run(async_example)
