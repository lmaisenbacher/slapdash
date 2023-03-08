#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Created: 01/2022
# Author: Carmelo Mordini <cmordini@phys.ethz.ch>
import mkdocs_gen_files
from slapdash.metadata import METADATA_SPECS


with mkdocs_gen_files.open("features/metadata.md", "a") as f:
    for name, specs in METADATA_SPECS.items():
        docs = f"### {name}\n"
        for key, value in specs.items():
            docs += f"- **{key}**: {', '.join(value) if isinstance(value, list) else value}\n"
        print(docs, file=f)
