# Clients

Clients allow accessing a dashboard from the command line, a web interface, or python scripts (perhaps from another dashboard :wink:).

To access this dashboard

```python
import slapdash

class Channel:
    value: float = 0.0

class Device:
    _voltage = 0.0
    gpio = [0, 0, 1, 0]

    def __init__(self):
        self.channels = [Channel() for i in range(4)]

    @property
    def voltage(self) -> float:
        return self._voltage

    @voltage.setter
    def voltage(self, value: float):
        print('Setting voltage')
        self._voltage = value

    def calculate(self, x: int, y: int):
        '''remote call'''
        return x + y

slapdash.run(Device(), host=hostname, rpc_port=6001, web_port=8001)
```

slapdash implements clients for the two type of supported servers, `rpc` and `request`

=== "rpc"

    ```python
    from slapdash import Client
    client = Client(hostname, port=6001, client_type='rpc')
    ```

=== "request"

    ```python
    from slapdash import Client
    client = Client(hostname, port=8001, client_type='request')
    ```

And they both provide the same access to the dashboard. The exposed objects in the interface can be nicely accessed as attributes of the client -- and tab completion works too!

## Attributes, properties, objects

```python
>>> client.voltage
0.0
>>> client.voltage = 1.1  # The dashboard shell will print 'Setting voltage'
>>> client.voltage
1.1
```

## List

Objects in the list can be accessed by index, but the returned interface cannot be sliced

```python
>>> client.gpio
[0, 0, 1, 0]
>>> client.gpio[2]
1
>>> client.gpio[0:2]
# this will raise an Error
```

## Classes

Sub-objects are returned as Clients of the same kind, so that their attributes can be accessed the usual way

```python
>>>ch0 = client.channels[0]
>>> type(client)
<class 'slapdash.client.Device'>
>>> type(ch0)
<class 'slapdash.client.channels[0]'>
>>> ch0.value
0.0
```

## Methods

Easy peasy

```python
>>> client.calculate(1, 2)
3
```

# Web interface

The package ships with a default frontend GUI accessible through a web browser, written in JavaScript/React. The GUI is designed to accept and render the dashboard data model, and values are synced among the server (and all clients) through a persistent WebSocket connection. Documentation for a dashboard is auto-generated, and endpoints can be viewed and tested at `http://<server>:<port>/docs`.

A custom GUI folder can be supplied (see arguments of `run`) that will be served to the user. For simple stylistic adjustments, a `custom.css` stylesheet file can be supplied to modify the default GUI styling (see the `custom_css` example). Alternatively, simple extensions or modifications to the frontend can be performed by supplying your own `custom.js` script within the frontend folder, which will be loaded along with the application.
