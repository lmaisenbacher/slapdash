from slapdash import Model


class Simple:
    def __init__(self):
        self.b = 0
        self.a = 1

    @property
    def d(self):
        return 2

    @property
    def c(self):
        return 3


def test_simple():
    simple = Simple()
    model = Model(simple)

    assert list(model.props().keys()) == ['b', 'a', 'd', 'c']
