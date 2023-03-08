import slapdash

metadata = dict(min=0., max=1., step=0.1)
metadata2 = dict(min=-5, max=5, step=1)

class Subclass:
    '''This subclass has a docstring.'''
    
    f = 1

class Simple:
    _value = 0.5
    s = Subclass()

    attribute_value = 1.234
    '''This attribute value can be used to generate documentation following PEP 257. But actually not.'''

    @slapdash.metadata(metadata)
    @property
    def a(self):
        '''This property `a` has a docstring.'''
        return self._value



    @slapdash.metadata(metadata)
    def b(self):
        '''This method `b` has a docstring.'''
        return self._value



    @slapdash.metadata(metadata)
    @property
    def c(self):
        '''This property `c` has a getter docstring.'''
        return self._value

    @c.setter
    def c(self, value):
        '''This property `c` has a setter docstring that will be ignored.'''
        self._value = value


    @property
    @slapdash.metadata(metadata)
    def c2(self):
        '''This property `c2` has a getter docstring.'''
        return self._value

    @c2.setter
    def c2(self, value):
        '''This property `c2` has a setter docstring that will be ignored.'''
        self._value = value


    @property
    def c3(self):
        '''This property `c3` has a getter docstring.'''
        return self._value

    @c3.setter
    def c3(self, value):
        '''This property `c3` has a setter docstring that will be ignored.'''
        self._value = value



    @property
    def d(self):
        '''This property `d` has a getter docstring.'''
        return self._value

    @slapdash.metadata(metadata)
    @d.setter
    def d(self, value):
        '''This property `d` has a setter docstring that will be ignored.'''
        self._value = value



    @slapdash.metadata(metadata)
    @property
    def e(self):
        '''This property `e` has a getter docstring.'''
        return self._value

    @slapdash.metadata(metadata2)
    @e.setter
    def e(self, value):
        '''This property `e` has a setter docstring that will be ignored.
        Wrapping with metadata here will overwrite the getter metadata.'''
        self._value = value



def test_function_wrapping():
    interface = Simple()
    model = slapdash.Model(interface)
    assert model.props()['a']['metadata'] == metadata
    assert model.props()['a']['doc'] == 'This property `a` has a docstring.'
    assert model.props()['b']['doc'] == 'This method `b` has a docstring.'
    assert model.props()['c']['doc'] == 'This property `c` has a getter docstring.'
    assert model.props()['c2']['doc'] == 'This property `c2` has a getter docstring.'
    assert model.props()['c3']['doc'] == 'This property `c3` has a getter docstring.'
    assert model.props()['d']['doc'] == 'This property `d` has a getter docstring.'
    assert model.props()['e']['doc'] == 'This property `e` has a getter docstring.'
    assert model.props()['e']['metadata'] == metadata2
    # assert model.props()['attribute_value']['doc'] == 'This attribute value can be used to generate documentation following PEP 257.'
    assert model.props()['s']['doc'] == 'This subclass has a docstring.'


if __name__ == '__main__':
    test_function_wrapping()