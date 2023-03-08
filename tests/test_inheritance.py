import slapdash


class Parent:
    def func(self, x):
        pass


class Child(Parent):
    pass


def test_function_args():
    child = Child()
    model = slapdash.Model(child)
    assert 'args' in model.props()['func']
