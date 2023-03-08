# Plugin components

Every object inside the plugin interface gets exposed by the server(s) according to its type.

Although Python is not statically typed, which is a good thing, the plugin uses the type information to build the input boxes in the web frontend, and sends it to clients that could require it (e.g. because _they_ are statically typed, like Ionizer (C++) or the web frontend itself (Typescript)).
Therefore we recommend using [type hints](https://docs.python.org/3/library/typing.html).

## Class and instance attributes

Attributes of four `BASE_TYPES`: `int`, `str`, `bool`, and `float`, are rendered into input boxes or buttons (for bools), and their value can be changed or toggled from the frontend.

=== "interface"

    ```python
    class Simple:
        a_float: float = 0.0 # class attribute with hint
        a_int = 1
        _hidden = 42

        def __init__(self):
            self.a_bool = True  # instance attribute without hint
            self.a_string = "hello"
            self._hidden2 = "you can't see me"
    ```

=== "web"

    Put some image here

### Hidden attributes

Attributes named with a leading underscore (e.g. `_hidden`) are never rendered by the plugin. This is useful to implement internal functionalities.

## Properties

Properties that do not implement a setter are read-only, they are rendered but cannot be modified from the frontend. Otherwise, they behave like normal attributes. The main use for them is to trigger function calls when their values are changed. For the proper way of implementing cascaded parameter updates, use the [`trigger_update`](/features/decorators/#trigger_update) decorator.

=== "interface"

    ```python
    class Channel:
        _frequency = 1
        _time = 2

        @property
        def frequency(self):
            return self._frequency

        @frequency.setter
        def frequency(self, value):
            self._do_something_with(value)
            self._frequency = value

        @property
        def time(self):
            return self._time
    ```

=== "web"

    Put some image here

## Lists

Lists are rendered with multiple boxes. Lists with object of different types are possible, but are discouraged (and will perhaps be prohibited in a future release). Although they can be handled by Clients, the web frontend will not behave correctly and they won't pass metadata sanity checks.

=== "interface"

    ```python
    from typing import List
    class Simple:
        list1: List[float] = [0.0, 1.0]
        list2: List[int] = [2, 3]
        weird_list = [5.0, True]

    ```

=== "web"

    Put some image here

## Dicts

Dictionaries cannot be exposed by the server, hence they are not allowed inside a plugin (if not hidden). The preferred way to obtain a nested structure with named attributes is to define a class for it.

## Classes

Nested interfaces are rendered accordingly.

=== "interface"

    ```python
    class Sub:
        a = 1
        b = 2

    class Top:
        a = "top"
        sub = Sub()
    ```

=== "web"

    Put some image here

## Methods

Interface methods have buttons if no arguments, or more complicated boxes otherwise. Please, hint exposed methods or the web frontend will complain when executing them.

=== "interface"

    ```python
    class Simple:
        def function1(self):
            print("hello")

        def function2(self, x: int) -> None:
            print(x)

        def _hidden_method(self):
            print("You can do whatever here")
    ```

=== "web"

    Put some image here
