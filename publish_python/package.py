# Copyright 2020 Dirk Thomas
# Licensed under the Apache License, Version 2.0

import functools
import os
import subprocess
import sys
from collections import namedtuple


@functools.lru_cache(maxsize=1)
def get_package_name_and_version():
    if not os.path.exists('setup.py'):
        raise RuntimeError(
            "Must be invoked in a directory containing a 'setup.py' file")
    output = subprocess.check_output(
        [sys.executable, 'setup.py', '--name', '--version'])
    lines = output.decode('ascii').splitlines()
    assert len(lines) == 2
    Package = namedtuple('Package', ['name', 'version'])
    return Package(lines[0], lines[1])
