import threading
import socket
from contextlib import closing
import asyncio
from .main import run


class create_server:
    # TODO: fix failure to spin up multiple servers when called from pytest
    def __init__(self, interface, **kwargs):
        self.__loop = asyncio.new_event_loop()
        self.__thread = threading.Thread(
            target=run, args=(interface,), kwargs={'loop': self.__loop, **kwargs}, daemon=True)

    def __enter__(self):
        self.__thread.start()

    def __exit__(self, exc_type, exc_value, traceback):
        for task in asyncio.all_tasks(self.__loop):
            task.cancel()
        self.__loop.call_soon_threadsafe(self.__loop.stop)
        self.__thread.join()
        self.__loop.close()


def get_random_port():
    # https://stackoverflow.com/a/45690594
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('localhost', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]
