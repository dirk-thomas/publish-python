# Copyright 2020 Dirk Thomas
# Licensed under the Apache License, Version 2.0

import os
import subprocess


def upload_packagecloud(*, artifacts, upload, config):
    if upload:
        print('-- Uploading package to packagecloud.io ...')
    else:
        print('-- Skip uploading package to packagecloud.io, pass --upload to '
              'actually upload artifacts')

    repository = config.get('repository')
    assert isinstance(repository, str), type(repository)
    for distribution in config.get('distributions', [None]):
        destination = f'{repository}'
        if distribution is not None:
            destination += f'/{distribution.replace(":", "/")}'
        for artifact in artifacts:
            ext = os.path.splitext(artifact)[1]
            if ext not in ('.deb', '.whl'):
                continue
            cmd = ['package_cloud', 'push', destination, artifact]
            print('$', *cmd)
            if upload:
                subprocess.check_call(cmd)
