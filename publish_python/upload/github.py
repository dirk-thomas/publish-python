# Copyright 2020 Dirk Thomas
# Licensed under the Apache License, Version 2.0

import json
import os
import subprocess

from publish_python.package import get_package_name_and_version


def upload_github(*, artifacts, upload, config):
    if upload:
        print('-- Uploading package to GitHub release ...')
    else:
        print('-- Skip uploading package to GitHub release, pass --upload to '
              'actually upload artifacts')

    pkg = get_package_name_and_version()
    repository = config.get('repository')
    if not repository:
        if not os.path.isdir('.git'):
            raise RuntimeError(
                'Config must specify a repository for GitHub uploads if '
                'invoked outside a git repository')
        repository = ':owner/:repo'

    # query if a release for the tag exists
    cmd = ['gh', 'api', f'/repos/{repository}/releases/tags/{pkg.version}']
    print('$', *cmd)
    output = None
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        # if not create a release for the tag
        print(
            f"\nA GitHub release for tag '{pkg.version}' doesn't exist yet\n")
        cmd = [
            'gh', 'api', f'/repos/{repository}/releases', '--field',
            f'tag_name={pkg.version}']
        print('$', *cmd)
        if upload:
            try:
                output = subprocess.check_output(
                    cmd, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                raise RuntimeError(
                    'Unable to create a GitHub release for tag '
                    f"'{pkg.version}'")
            print(f"\nCreated a GitHub release for tag '{pkg.version}'\n")

    # extract upload_url from response
    if output is not None:
        response = json.loads(output)
        if isinstance(response, list):
            assert len(response) == 1, \
                f"More than one GitHub releases for the tag '{pkg.version}' " \
                'exists'
            response = response[0]
        upload_url = response['upload_url'].split('{', 1)[0]
    else:
        upload_url = '<upload_url>'

    # use the upload_url from the last response to upload artifacts
    for artifact in artifacts:
        ext = os.path.splitext(artifact)[1]
        if ext not in ('.deb', '.whl'):
            continue

        cmd = [
            'gh', 'api', upload_url + f'?name={os.path.basename(artifact)}',
            '--header', 'Content-Type: application/octet-stream',
            '--input', artifact]
        print('$', *[f'"{c}"' if ' ' in c else c for c in cmd])
        if upload:
            try:
                subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                raise RuntimeError(
                    'Failed to upload artifact '
                    f"'{os.path.basename(artifact)}' to GitHub release")
            print(
                f"\nUploaded artifact '{os.path.basename(artifact)}' to "
                'GitHub release\n')
