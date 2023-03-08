#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Created: 01/2022
# Author: Carmelo Mordini <cmordini@phys.ethz.ch>
import argparse
import runpy
import pkg_resources
from pathlib import Path

examples = Path(pkg_resources.resource_filename('slapdash', 'examples'))


def list_examples():
    examples_list = [f"- {p.stem}" for p in examples.iterdir() if p.suffix == '.py']
    examples_list.sort()
    print("Available examples")
    print("\n".join(examples_list))


def run_example(path):
    runpy.run_path((examples / path).with_suffix('.py'), run_name='__main__')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("example", nargs="?", default="")
    args = parser.parse_args()
    if args.example:
        run_example(args.example)
    else:
        list_examples()
