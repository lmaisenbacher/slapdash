import slapdash


class ReadonlyDashboard:
    '''This model creates attributes based on properties
    that only have `getter` functions, and thus become
    read-only in the interface. In the interface, they
    should appear grayed out and not settable.'''

    _str_ro = "hello"
    _str_rw = "world"
    _int_ro: int = 0
    _int_rw: int = 0
    _float_ro: float = 1.1
    _float_rw: float = 1.1
    _bool_ro_true: bool = True
    _bool_ro_false: bool = False
    _bool_rw: bool = True

    _metadata = {
        'float_ro': {'units': 'mW'},
        'float_rw': {'units': 'mW'}
    }

    @property
    def str_ro(self):
        return self._str_ro

    @property
    def str_rw(self) -> str:
        return self._str_rw

    @str_rw.setter
    def str_rw(self, value: str) -> None:
        self._str_rw = value

    @property
    def int_ro(self):
        return self._int_ro

    @property
    def int_rw(self) -> int:
        return self._int_rw

    @int_rw.setter
    def int_rw(self, value: int) -> None:
        self._int_rw = value

    @property
    def float_ro(self):
        return self._float_ro

    @property
    def float_rw(self) -> float:
        return self._float_rw

    @float_rw.setter
    def float_rw(self, value: float) -> None:
        self._float_rw = value

    @property
    def bool_ro_true(self):
        return self._bool_ro_true

    @property
    def bool_ro_false(self):
        return self._bool_ro_false

    @property
    def bool_rw(self) -> bool:
        return self._bool_rw

    @bool_rw.setter
    def bool_rw(self, value: bool) -> None:
        self._bool_rw = value


if __name__ == '__main__':
    slapdash.run(ReadonlyDashboard())
