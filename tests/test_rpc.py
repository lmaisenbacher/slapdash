import pytest
import slapdash
from slapdash.testing import create_server
# from rpc import plugin_server, PluginClient

RPCPORT = 6021
# rpc = plugin_server('0.0.0.0', RPCPORT)

class Simple:
    a = 0.0
    b = 1
    c = "test"
    d = False
    mylist = [0, 1]

# The followings tests require a custom server and client pair.

# def test_client():
#     with create_server(Simple(), enable_web=False, servers=[rpc,]):
#         simple = slapdash.Client(port=6021, client_type=PluginClient)

#         assert simple.a == 0.0
#         assert simple.b == 1
#         assert simple.c == 'test'
#         assert simple.d is False
#         assert simple.mylist == [0, 1]

#         simple.a = 1.0
#         assert simple.a == 1.0
#         simple.b = 2
#         assert simple.b == 2
#         simple.c = 'new'
#         assert simple.c == 'new'
#         simple.d = True
#         assert simple.d is True
#         simple.mylist = [2, 3]
#         assert simple.mylist == [2, 3]

#         with pytest.raises(AttributeError):
#             assert simple.e == 'e'


# def test_multiple_servers():
#     with create_server(Simple(), enable_web=False, servers=[plugin_server('0.0.0.0', 6022), plugin_server('0.0.0.0', 6023)]):
#         simple = slapdash.Client(hostname='0.0.0.0', port=6022, client_type=PluginClient, timeout=1)
#         simple2 = slapdash.Client(hostname='0.0.0.0', port=6023, client_type=PluginClient, timeout=1)

#         assert simple.a == 0.0
#         assert simple.b == 1
#         assert simple.c == 'test'
#         assert simple.d is False
#         assert simple.mylist == [0, 1]

#         simple.a = 1.0
#         assert simple.a == 1.0
#         assert simple2.a == 1.0
#         simple2.a = 1.5
#         assert simple.a == 1.5
#         assert simple2.a == 1.5
#         simple.b = 2
#         assert simple.b == 2
#         assert simple2.b == 2
#         simple2.b = 3
#         assert simple.b == 3
#         assert simple2.b == 3
#         simple.c = 'new'
#         assert simple.c == 'new'
#         assert simple2.c == 'new'
#         simple2.c = 'newer'
#         assert simple.c == 'newer'
#         assert simple2.c == 'newer'
#         simple.d = True
#         assert simple.d is True
#         assert simple2.d is True
#         simple2.d = False
#         assert simple.d is False
#         assert simple2.d is False
#         simple.mylist = [2, 3]
#         assert simple.mylist == [2, 3]
#         assert simple2.mylist == [2, 3]
#         simple2.mylist = [4, 5]
#         assert simple.mylist == [4, 5]
#         assert simple2.mylist == [4, 5]

#         with pytest.raises(AttributeError):
#             assert simple.e == 'e'

#         with pytest.raises(AttributeError):
#             assert simple2.f == 'f'