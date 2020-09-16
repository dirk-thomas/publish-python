# Copyright 2020 Dirk Thomas
# Licensed under the Apache License, Version 2.0

import glob
import os
import shutil
import subprocess
import sys

from publish_python.package import get_package_name_and_version


def create_wheel(*, config):
    pkg = get_package_name_and_version()
    print('\n-- Building sdist and bdist_wheel artifacts of package '
          f"'{pkg.name}' {pkg.version} ...")

    cmd = [sys.executable, 'setup.py', 'sdist', 'bdist_wheel']
    print('$', *cmd)
    subprocess.check_call(cmd)

    tarball = f'dist/{pkg.name}-{pkg.version}.tar.gz'
    assert os.path.exists(tarball), \
        f"Failed to generate source tarball '{tarball}'"

    wheel_pattern = f'dist/{pkg.name.replace("-", "_")}-{pkg.version}-*.whl'
    wheels = glob.glob(wheel_pattern)
    assert wheels, f"Failed to generate wheel '{wheel_pattern}'"
    assert len(wheels) == 1, f'Found more than one wheel: {wheels}'

    return [tarball, wheels[0]]


def clean_wheel():
    pkg = get_package_name_and_version()
    print(f"\n-- Deleting wheel artifacts of package '{pkg.name}' ...")
    subfolders = ['build', 'dist'] + \
        glob.glob(
            f'**/{pkg.name.replace("-", "_")}.egg-info', recursive=True)
    for subfolder in subfolders:
        if os.path.exists(subfolder):
            print("-- Deleting subfolder '%s' ..." % subfolder)
            shutil.rmtree(subfolder)
