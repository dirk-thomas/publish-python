# Copyright 2020 Dirk Thomas
# Licensed under the Apache License, Version 2.0

import subprocess


def upload_pypi(*, artifacts, upload, config):
    if upload:
        print('-- Uploading package to PyPI ...')
    else:
        print('-- Skip uploading package to PyPI, pass --upload to actually '
              'upload artifacts')
    cmd = ['twine', 'upload', '-s', *artifacts]
    print('$', *cmd)
    if upload:
        subprocess.check_call(cmd)
