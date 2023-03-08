import slapdash
from slapdash.testing import create_server, get_random_port
# from rpc import plugin_server, PluginClient

# The following tests require a custom server and client pair.

# def test_repr1():
#     class Simple1:
#         a = 0.0

#     port = get_random_port()
#     with create_server(Simple1(), enable_web=False, servers=plugin_server('0.0.0.0', port)):
#         simple = slapdash.Client(port=port, client_type=PluginClient)
#         assert simple.__class__.__name__ == 'Simple1'


# def test_repr2():
#     class Simple2:
#         def __repr__(self):
#             return 'SimpleClass'
#         a = 0.0

#     port = get_random_port()
#     with create_server(Simple2(), enable_web=False, servers=plugin_server('0.0.0.0', port)):
#         simple = slapdash.Client(port=port, client_type=PluginClient)
#         assert simple.__class__.__name__ == 'SimpleClass'


# def test_repr3():
#     @slapdash.refresh('a')
#     class Simple3:
#         a = 0.0

#     port = get_random_port()
#     with create_server(Simple3(), enable_web=False, servers=plugin_server('0.0.0.0', port)):
#         simple = slapdash.Client(port=port, client_type=PluginClient)
#         assert simple.__class__.__name__ == 'Simple3'


# def test_repr4():
#     @slapdash.refresh('a')
#     class Simple4:
#         def __repr__(self):
#             return 'SimpleClass4'
#         a = 0.0

#     port = get_random_port()
#     with create_server(Simple4(), enable_web=False, servers=plugin_server('0.0.0.0', port)):
#         simple = slapdash.Client(port=port, client_type=PluginClient)
#         assert simple.__class__.__name__ == 'SimpleClass4'
