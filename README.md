# Slapdash

**<https://github.com/cathaychris/slapdash/>**

The Slapdash library lets you create a control dashboard with ease. It takes device driver classes written in simple python and automatically generates

- A web server exposing the class via a RESTful API, that can be accessed with HTTP requests or using the provided clients;
- An automatically generated fronted rendered in a web page that directly connects to the web server for immediate access;
- and modularly permits the bootstrapping of other interfaces such as RPC. Bring-Your-Own-Interface.

For example, it will turn this:

```python
class Device:

    _current = 0.0
    _voltage = 0.0
    _power = False

    @property
    def current(self):
        # run code to get current
        return self._current

    @current.setter
    def current(self, value):
        # run code to set current
        self._current = value

    @property
    def voltage(self):
        # run code to get voltage
        return self._voltage

    @voltage.setter
    def voltage(self, value):
        # run code to set voltage
        self._voltage = value

    @property
    def power(self):
        # run code to get power state
        return self._power

    @power.setter
    def power(self, value):
        # run code to set power state
        self._power = value

    def reset(self):
        self.current = 0.0
        self.voltage = 0.0
```

into this:

![](./docs/images/fast-api-example.png)
