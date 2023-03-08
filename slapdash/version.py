import os
import json

parent_dir_path = os.path.dirname(os.path.realpath(__file__))
version_filename = os.path.join(parent_dir_path, 'version.json')
with open(version_filename) as version_file:
    version = json.load(version_file)

__major__ = version['major']
__minor__ = version['minor']
__patch__ = version['patch']
__version__ = f"{__major__}.{__minor__}.{__patch__}"

# This uses Semantic Versioning 2.0.0

# Given a version number MAJOR.MINOR.PATCH, increment the:
# 1. MAJOR version when you make incompatible API changes,
# 2. MINOR version when you add functionality in a backwards compatible manner, and
# 3. PATCH version when you make backwards compatible bug fixes.
# Additional labels for pre-release and build metadata are available as extensions to the MAJOR.MINOR.PATCH format.

# The version update should always accompany a merge into the master branch
