# Copyright 2020 Dirk Thomas
# Licensed under the Apache License, Version 2.0

import argparse
import collections
import functools
import os
import subprocess
import sys

from publish_python.config import get_publishings
from publish_python.package import get_package_name_and_version
from publish_python.registry import artifact_cleanups
from publish_python.registry import artifact_handlers
from publish_python.registry import upload_handlers


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description='Package a Python package and upload the artifacts.')
    parser.add_argument(
        'targets', nargs='*', action=TargetAction, default=get_targets(),
        metavar='TARGET',
        help='The list of targets to publish to (default all: %s).' %
        ' '.join(get_targets()))
    parser.add_argument(
        '--upload', action='store_true', default=False,
        help='Perform upload steps (default: only build the artifacts')
    parser.add_argument(
        '--clean-only', action='store_true', default=False,
        help='Only delete previously generated artifacts')
    parser.add_argument(
        '--list-only', action='store_true', default=False,
        help='Only list the configured publishing')

    args = parser.parse_args(argv)

    print('== Determine available publishings')
    for artifact in get_publishings().values():
        for upload in artifact.uploads.values():
            print(f'* {artifact.type}:{upload.type}')

    if args.list_only:
        return

    package = get_package_name_and_version()
    print('\n== Determine package name and version')
    print(f'Package: {package.name}')
    print(f'Version: {package.version}')

    # try to get timestamp of tag to make builds reproducible
    try:
        timestamp = subprocess.check_output(
            ['git', 'log', '-1', '--format=%at', package.version])
    except subprocess.CalledProcessError:
        pass
    else:
        timestamp = timestamp.rstrip().decode()
        os.environ['SOURCE_DATE_EPOCH'] = timestamp
        print(
            f'\n== Set SOURCE_DATE_EPOCH={timestamp} for reproducible builds')

    # create target hierarchy mapping from an artifact to uploads
    targets = collections.OrderedDict()
    for target in args.targets:
        artifact_type, upload_type = target.split(':')
        uploads = targets.setdefault(artifact_type, [])
        uploads.append(upload_type)

    for artifact_type, upload_types in targets.items():
        if args.clean_only:
            artifact_cleanups[artifact_type]()
            continue

        print(f"\n== Creating '{artifact_type}' artifacts ...")
        artifact = get_publishings()[artifact_type]
        artifacts = artifact_handlers[artifact_type](config=artifact.config)

        for upload_type in upload_types:
            print(f"\n== Uploading artifacts to '{upload_type}' ...")
            upload = artifact.uploads[upload_type]
            upload_handlers[upload_type](
                artifacts=artifacts, upload=args.upload, config=upload.config)


class TargetAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        targets = get_targets()
        for value in (values or []):
            if value not in targets:
                raise argparse.ArgumentError(
                    self,
                    f'invalid choice: {value} (choose from: '
                    f'{str.join(" ", targets)})')
        if len(values) > len(set(values)):
            duplicates = [
                v for v, count in collections.Counter(values).items()
                if count > 1]
            raise argparse.ArgumentError(
                self, f'duplicate choices: {str.join(" ", duplicates)}')
        setattr(namespace, self.dest, values)


@functools.lru_cache(maxsize=1)
def get_targets():
    return [
        f'{artifact.type}:{upload.type}'
        for artifact in get_publishings().values()
        for upload in artifact.uploads.values()]
