from setuptools import setup, find_packages

import os
import json

parent_dir_path = os.path.dirname(os.path.realpath(__file__))
version_filename = os.path.join(parent_dir_path, 'slapdash', 'version.json')
with open(version_filename) as version_file:
    version = json.load(version_file)


setup(name='slapdash',
      version=f"{version['major']}.{version['minor']}.{version['patch']}",
      description='Create device and application control dashboards instantly',
      url='https://github.com/cathaychris/slapdash',
      author='Matt Grau',
      author_email='graum@phys.ethz.ch',
      python_requires='>=3.7',
      install_requires=[
          'requests',
          'fastapi',
          'uvicorn',
          'aiofiles',
          'python-socketio<5',
          'websockets',
      ],
      extras_require={
          'dev': [
              'pylint',
              'autopep8',
              'pytest',
              'pytest-cov'
          ],
          'docs': [
              'mkdocs',
              'mkdocs-material',
              'mkdocs-include-markdown-plugin',
              'mkdocs-gen-files',
              'mkdocstrings'
          ]
      },
      package_data={'slapdash': ['frontend/*', 'examples/*', 'version.json']},
      packages=find_packages())
