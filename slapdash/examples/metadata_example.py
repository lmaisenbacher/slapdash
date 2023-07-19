#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Created: 07/2021
# Author: Carmelo Mordini <cmordini@phys.ethz.ch>

'''
https://stackoverflow.com/a/48717971
'''

import slapdash
import matplotlib.pyplot as plt
import base64
from io import BytesIO

from typing import List


class Device:
    current = 0.0
    voltage = 0.0


class MetadataDashboard:
    '''This model demonstrates the kinds of metadata properties that may be assigned
    to model attributes.
    - The `renderAs` property assigned to `image` causes it to be
    rendered as an image based on a base64 string.
    '''
    bool_prop: bool = True
    bool_prop2: bool = False
    int_prop: int = 5
    string_prop: str = "hello"
    _float_prop: float = 0.35
    _image_data = [list(range(3)) for _ in range(3)]
    image: str = ""
    list_prop: List[float] = []
    free_float_prop: float = 0.05

    _metadata = {
        'float_prop': {'min': 0, 'max': 'a', 'step': 0.01, 'units': 'MHz'},
        'free_float_prop': {'units': 'GHz'},
        'extra_float': {'step': 0.01, 'units': 'MHz2'},
        'list_prop': {'units': 'kg', 'step': 0.1},
        'int_prop': {'units': 'mol'},
        'string_prop': {'units': 'ciao', 'meta': 1},
        'image': {'renderAs': 'image', 'min': 0},
        'bool_prop': {'mapping': ['HEALTHY', 'FAILING']},
        'device': {'collapsed': True},
        'asds': {},
    }

    def __init__(self):
        self.list_prop = [1.0, 2.0]
        self.extra_float = 3.6
        self.device = Device()
        self.plot()

    @property
    def float_prop(self):
        return self._float_prop

    @float_prop.setter
    def float_prop(self, value):
        self._float_prop = value

    def plot(self):
        fig, ax = plt.subplots(figsize=(2, 2))
        ax.imshow(self._image_data)
        # encode your plot
        tmpfile = BytesIO()
        fig.savefig(tmpfile, format='png')
        self.image = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
        plt.close(fig)


if __name__ == '__main__':
    slapdash.run(MetadataDashboard())
