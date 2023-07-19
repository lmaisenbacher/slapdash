import uvicorn
import asyncio
import signal

from .model import Model
from .web import web_api
from .version import __version__


def run(interface,
        host: str='0.0.0.0',
        port: int=8000,
        enable_web: bool=True,
        servers: list=[],
        loop=None,
        web_settings: dict={},
        *args, **kwargs
        ):
    """
    Start an instance of the Slapdash server.

    Parameters
    ----------
    interface : class
        Class describing device to be controlled.
    host : str, optional
        The host to use for the dashboard server.
        The default is '0.0.0.0', which binds to all interfaces.
    port : int, optional
        The port for the web REST interface of the server. The default is 8000.
    enable_web : bool, optional
        Enable web server. Disable this in case you will only use your own add-in servers.
        The default is True.
    servers : list, optional
        Any number of server factories that produce functions that spawn servers, which will share
        the data model produced from `interface`. These functions should accept arguments
        (data_model, info) and will be passed any additional (*args, **kwargs) supplied to `run()`,
        where `info` will include the data model name, slapdash version, web port, and any supplied
        `web_settings`.
        They should return a server instance with the method `serve()` that mirrors that of
        `uvicorn.Server`.
        The default is [].
    loop : asyncio event loop or None, optional
        Specify an event loop to use to run all servers, in case you would prefer that the dashboard
        not create its own. The default is None, in which case the current event loop is used.
    web_settings : dict, optional
        DESCRIPTION. The default is {}.
    *args : TYPE
        DESCRIPTION.
    **kwargs : TYPE
        DESCRIPTION.

    Optional kwargs used in the web interface
    -------
    frontend : str or None, optional
        An absolute path for a folder containing files to serve on the root '/' endpoint of the web
        interface. Defaults to None, in which case a built in frontend is used.
    css : str or None, optional
        An absolute path for a custom css file to override the styles of the built-in web gui.
    enable_CORS : bool, optional
        Uninhibits cross-origin resource sharing (CORS). CORS is useful for development.
        The defaults is True.
    web_notify_callback : str or None, optional
        The name of a callback function in `interface` that will be called when notifications are
        triggered via the web interface.
    web_settings : dict, optional
        Any settings you would like to make available at the `/info` endpoint of the REST API.

    Returns
    -------
    None.

    """
    data_model = Model(interface)
    info = {
        'name': data_model.name,
        'version': __version__,
        'web_port': port,
        'web_settings': web_settings,
        **kwargs
    }
    if loop is None:
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
    else:
        asyncio.set_event_loop(loop)

    # if wrapped with @Saver, attach DashboardSavingInterface's saving callback to all model changes
    if 'DashboardSavingInterface' in [c.__name__ for c in type(data_model._interface).__mro__]:
        data_model_emit = data_model.emit

        def emit(message):
            data_model_emit(message)
            data_model._interface._trigger_save(message)
        data_model.emit = emit

    addin_servers = []
    try: # accept single server factor or list thereof
        _ = iter(servers)
    except TypeError: # not iterable
        additional_server = servers(data_model, info, *args, **kwargs)
        try:
            additional_server.install_signal_handlers = lambda: None
        except:
            pass
        loop.create_task(additional_server.serve())
        addin_servers.append(additional_server)
    else: # iterable
        for server_factory in servers:
            server = server_factory(data_model, info, *args, **kwargs)
            try:
                server.install_signal_handlers = lambda: None
            except:
                pass
            loop.create_task(server.serve())
            addin_servers.append(server)
    addin_server_info = []
    for i, s in enumerate(addin_servers):
        sn = s.__module__ + '.' + s.__class__.__name__
        addin_server_info.append({'name': sn})
        try: # _host and _port may not exist for all add-in servers
            addin_server_info[i].update({'host': s._host, 'port': s._port})
        except:
            pass
    info['addin_servers'] = addin_server_info
    if enable_web:
        wapi = web_api(data_model=data_model, info=info, *args, **kwargs)
        web_server = uvicorn.Server(uvicorn.Config(wapi, host=host, port=port))
        # overwrite uvicorn's signal handlers, otherwise it will bogart SIGINT and
        # SIGTERM, which makes it impossible to escape out of
        web_server.install_signal_handlers = lambda: None
        loop.create_task(web_server.serve())

    async def stop_loop():
        loop.stop()
        print('Slapdash server shutting down')

    def shutdown():
        try:
            tasks = asyncio.all_tasks(loop)
        except AttributeError:
            # asyncio API change in python3.6
            tasks = asyncio.Task.all_tasks(loop)

        for task in tasks:
            # here creating an exception when trying to shutdown might be dangerous
            # throw out any of these exceptions
            try:
                task.cancel()
            except:  # noqa
                pass
        loop.create_task(stop_loop())

    def custom_exception_handler(loop, context):
        # if any background task creates an unhandled exception, shut down the entire loop
        # it's possible we don't want to do this, maybe make this optional in the future
        loop.default_exception_handler(context)

        # here we exclude most kinds of exceptions from triggering this kind of shutdown
        exc = context['exception']
        if type(exc) not in [RuntimeError, KeyboardInterrupt, asyncio.CancelledError]:
            if enable_web:
                async def emit_exception():
                    await wapi._sio.emit('notify', {'data': {'exception': str(exc),
                                                    'type': exc.__class__.__name__}})
                loop.create_task(emit_exception())
        else:
            shutdown()

    loop.set_exception_handler(custom_exception_handler)

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, shutdown)
        except (NotImplementedError, RuntimeError):
            pass

    print('Starting Slapdash server')
    try:
        loop.run_forever()
    finally:
        try:
            loop.close()
        except:  # noqa
            pass
