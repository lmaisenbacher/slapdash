import inspect
import slapdash
from slapdash.testing import create_server
# from rpc import plugin_server, PluginClient


class Functions:
    def no_arg(self):
        return 0

    def one_arg(self, x: int) -> int:
        return x

    def two_arg(self, x: float, y: float) -> float:
        return x + y

    def no_return(self, x: int) -> None:
        return None

    def no_annotate(self, x, y):
        return x + y


# def test_client():
#     '''Test method signatures as seen by a custom client'''
#     with create_server(Functions(), enable_web=False, servers=plugin_server('0.0.0.0', 6001)):

#         funcs = Functions()
#         client_funcs = slapdash.Client(port=6001, client_type=PluginClient)
#         assert inspect.signature(funcs.no_arg).parameters == inspect.signature(
#             client_funcs.no_arg).parameters
#         assert inspect.signature(funcs.one_arg).parameters == inspect.signature(
#             client_funcs.one_arg).parameters
#         assert inspect.signature(funcs.two_arg).parameters == inspect.signature(
#             client_funcs.two_arg).parameters
#         assert inspect.signature(funcs.no_return).parameters == inspect.signature(
#             client_funcs.no_return).parameters
#         assert inspect.signature(funcs.no_annotate).parameters == inspect.signature(
#             client_funcs.no_annotate).parameters
