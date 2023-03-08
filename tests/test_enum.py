import pytest
from tiqi_rpc import plugin_server, PluginClient
from tiqi_rpc.error import RPCResponseError
from enum import Enum, auto
import slapdash
from slapdash.testing import create_server


class SomeRepr:
    def __repr__(self):
        return "I am a talking object!"


class Some:
    pass


class Color(Enum):
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'


class Auto(Enum):
    A = auto()
    B = auto()
    C = auto()


class Mixed(Enum):
    value_int = 10
    value_int_alias = 10
    value_float = 1.65
    value_bool = True
    value_bool_alias = 1
    value_str = 'some string'
    value_class = Some
    value_instance = SomeRepr()
    value_bad_instance = Some()


class EnumPlugin:
    color = Color.GREEN
    _col = Color.GREEN

    @property
    def color_prop(self):
        return self._col

    @color_prop.setter
    def color_prop(self, value):
        self._col = value

    auto = Auto.A
    mix = Mixed.value_int


def test_enum():
    '''Test enum and enum props with clients'''

    plugin = EnumPlugin()
    with create_server(plugin, port=8003, servers=plugin_server('0.0.0.0', 6003)):
        import time
        time.sleep(0.5)
        rpc_client = slapdash.Client(port=6003, client_type=PluginClient)
        web_client = slapdash.Client(port=8003)

        rpc_client.color = 'red'
        assert plugin.color == Color.RED
        assert rpc_client.color == 'red'
        assert web_client.color_prop == 'green'

        web_client.color_prop = 'blue'
        assert plugin.color_prop == Color.BLUE
        assert rpc_client.color_prop == 'blue'
        assert web_client.color == 'red'


def test_enum_names():
    '''setting the prop via a Client with the enum name will raise a KeyError'''

    plugin = EnumPlugin()
    with create_server(plugin, enable_web=False, servers=plugin_server('0.0.0.0', 6022)):
        client = slapdash.Client(port=6022, client_type=PluginClient)

        with pytest.raises(RPCResponseError, match='KeyError'):
            client.color = 'RED'


def test_enum_values():
    '''you can get/set the prop with the str version of its value'''

    plugin = EnumPlugin()
    with create_server(plugin, enable_web=False, servers=plugin_server('0.0.0.0', 6023)):
        client = slapdash.Client(port=6023, client_type=PluginClient)

        client.color = 'red'
        assert plugin.color == Color.RED
        assert client.color == 'red'

        assert plugin.auto == Auto.A
        assert client.auto == '1'


def test_mixed_enum():
    '''test improbable enum with mixed-type values'''

    plugin = EnumPlugin()
    with create_server(plugin, enable_web=False, servers=plugin_server('0.0.0.0', 6024)):
        client = slapdash.Client(port=6024, client_type=PluginClient)

        client.mix = '1.65'
        # the plugin attribute is set with the true enum object
        assert plugin.mix == Mixed.value_float
        # the client returns str(enum.value)
        assert client.mix == '1.65'

        client.mix = '10'
        assert plugin.mix == Mixed.value_int
        assert plugin.mix == Mixed.value_int_alias  # this alias is OK
        assert client.mix == '10'

        client.mix = 'True'
        assert plugin.mix == Mixed.value_bool
        assert client.mix == 'True'

        client.mix = 'some string'
        assert plugin.mix == Mixed.value_str

        # this works, because str(Some) = "<class '__main__.Some'>" is reproducible
        client.mix = str(Some)
        assert plugin.mix == Mixed.value_class
        assert client.mix == f"<class '{__name__}.Some'>"

        # this works, because str(SomeRepr()) = "I am a talking object!" is reproducible
        client.mix = str(SomeRepr())
        assert plugin.mix == Mixed.value_instance
        assert client.mix == "I am a talking object!"

        # This is a nasty case... the object has a valid str representation like
        # '<__main__.Some object at 0x7f8f95c0d430>' (or some other id, you can read it in the web interface)
        # so it goes in the plugin and is shown in the combobox, but I have no way to set it from a Client
        # unless I can read the id of the particular object in the Enum class,
        with pytest.raises(RPCResponseError, match='KeyError'):
            # trying to set it in this naive way will fail with KeyError
            client.mix = str(Some())

        with pytest.raises(RPCResponseError, match='KeyError'):
            client.mix = '1'  # boolean alias fails because it is "hidden" by True
