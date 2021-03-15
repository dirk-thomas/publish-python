# Copyright 2020 Dirk Thomas
# Licensed under the Apache License, Version 2.0

import hashlib
import os
import subprocess
import urllib.error
import urllib.request


def upload_packagecloud(*, artifacts, upload, config):
    if upload:
        print('-- Uploading package to packagecloud.io ...')
    else:
        print('-- Skip uploading package to packagecloud.io, pass --upload to '
              'actually upload artifacts')

    repository = config.get('repository')
    assert isinstance(repository, str), type(repository)
    for distribution in config.get('distributions', [None]):
        version = ''
        if distribution is not None:
            version = f'/{distribution.replace(":", "/")}'
        destination = f'{repository}{version}'
        for artifact in artifacts:
            ext = os.path.splitext(artifact)[1]
            if ext not in ('.deb', '.dsc', '.whl'):
                continue

            basename = os.path.basename(artifact)
            url = f'https://packagecloud.io/{repository}/packages{version}' + \
                f'/{basename}'
            try:
                with urllib.request.urlopen(url) as h:
                    metadata_html = h.read()
            except urllib.error.HTTPError:
                pass
            else:
                with open(artifact, 'rb') as h:
                    artifact_data = h.read()
                m = hashlib.sha256()
                m.update(artifact_data)
                if m.hexdigest().encode() in metadata_html:
                    print(
                        '\nExisting packagecloud.io package matches the '
                        f"artifact '{basename}', skipping the upload\n")
                    continue
                print(
                    '\nExisting packagecloud.io package differs from the '
                    f"artifact '{basename}'\n")

            cmd = ['package_cloud', 'push', destination, artifact]
            print('$', *cmd)
            if upload:
                subprocess.check_call(cmd)
