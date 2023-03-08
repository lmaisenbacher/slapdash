#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Created: 02/2022
# Author: Carmelo Mordini <cmordini@phys.ethz.ch>

import pytest
import json
from enum import Enum
from slapdash.decorators import Saver


class Sub:
    value = 0.0


class Color(Enum):
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'


class Simple1:
    a_float = 0.0
    a_int = 0
    a_string = "test"
    a_bool = False
    a_enum = Color.RED

    def __init__(self):
        self.array_int = [1, 2, 3, 4]
        self.array_float = [0.1, 0.2, 0.3]
        self.array_bool = [False, False]
        self.array_str = ['this', 'is', 'a', 'test']
        self.array_mix = [0, 0.1, False, 'test']
        self.sub = Sub()


def make_dashboard_with_saver(tmp_path, settings):
    settings_path = tmp_path / 's.json'
    with open(settings_path, 'w') as f:
        json.dump(settings, f)
    return Saver(settings_path)(Simple1)()


def test_saver(tmp_path):

    settings = {
        'a_float': 10.0,
        'a_int': 1,
        'array_int': [11, 12, 13, 14],
        'array_mix': [1, 0.2, True, 'the test'],
        'sub': {
            'value': 1.0,
        },
        'a_enum': 'blue'
    }

    dashboard = make_dashboard_with_saver(tmp_path, settings)
    # testing the effect of the decorator
    assert isinstance(dashboard, Simple1)
    assert type(dashboard).__name__ == 'DashboardSavingInterface'

    assert dashboard.a_float == 10.0
    assert isinstance(dashboard.a_float, float)
    assert dashboard.a_int == 1
    assert isinstance(dashboard.a_int, int)
    assert dashboard.array_int == [11, 12, 13, 14]
    assert dashboard.array_mix == [1, 0.2, True, 'the test']
    assert dashboard.sub.value == 1.0
    assert isinstance(dashboard.sub.value, float)
    assert dashboard.a_enum == Color.BLUE
    assert isinstance(dashboard.a_enum, Enum)


def test_saver_bad_settings(tmp_path):
    # TODO: maybe raise Warning instead of printing, and catch that here
    # non existing param: this prints a logger message at level WARNING
    # bad_settings = {
    #     'some_param': 1.0
    # }
    # with pytest.raises(Exception):  # TODO: make it more explicit
    #     make_dashboard_with_saver(tmp_path, bad_settings)

    # non existing param in children: this prints a logger message at level WARNING
    # bad_settings = {
    #     'sub': {
    #         'another_value': 1
    #     }
    # }
    # with pytest.raises(Exception):  # TODO: make it more explicit
    #     make_dashboard_with_saver(tmp_path, bad_settings)

    # Existing parameter with wrong type
    bad_settings = {
        'a_int': 1.0
    }
    with pytest.raises(TypeError, match='Cannot override class parameter'):
        make_dashboard_with_saver(tmp_path, bad_settings)

    # existing enum, wrong value. Exceptions will be raised by the Enum constructor
    bad_settings = {
        'a_enum': 1.0
    }
    with pytest.raises(ValueError, match=f"is not a valid {type(Simple1.a_enum).__name__}"):
        make_dashboard_with_saver(tmp_path, bad_settings)

    bad_settings = {
        'a_enum': 'yellow'
    }
    with pytest.raises(ValueError, match=f"is not a valid {type(Simple1.a_enum).__name__}"):
        make_dashboard_with_saver(tmp_path, bad_settings)

    bad_settings = {
        'sub': {
            'value': 0
        }
    }
    with pytest.raises(TypeError, match='Cannot override class parameter'):
        make_dashboard_with_saver(tmp_path, bad_settings)
