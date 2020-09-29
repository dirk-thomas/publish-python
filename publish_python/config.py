# Copyright 2020 Dirk Thomas
# Licensed under the Apache License, Version 2.0

import functools
import pathlib
from collections import OrderedDict
from collections import namedtuple

import yaml


@functools.lru_cache(maxsize=1)
def get_publishings():
    from publish_python.cli import artifact_handlers
    from publish_python.cli import upload_handlers

    config_path = pathlib.Path('publish-python.yaml')
    if not config_path.exists():
        raise RuntimeError(
            'Must be invoked in a directory containing a '
            f"'{config_path}' file")
    data = yaml.safe_load(config_path.read_bytes())
    assert 'artifacts' in data
    assert isinstance(data['artifacts'], list)

    Artifact = namedtuple('Publishing', ['type', 'config', 'uploads'])
    Upload = namedtuple('Upload', ['type', 'config'])

    artifacts = OrderedDict()
    for a in data['artifacts']:
        assert isinstance(a, dict), type(a)
        assert 'type' in a, str(a)
        assert isinstance(a['type'], str), type(a['type'])
        assert a['type'] in artifact_handlers, str(a['type'])
        assert isinstance(a.get('config', {}), dict), type(a['config'])
        assert a['type'] not in artifacts
        artifact = Artifact(
            type=a['type'],
            config=a.get('config', {}),
            uploads=OrderedDict())

        assert 'uploads' in a
        assert isinstance(a['uploads'], list), type(a['uploads'])
        for u in a['uploads']:
            assert 'type' in u
            assert isinstance(u['type'], str), type(u['type'])
            assert u['type'] in upload_handlers, str(u['type'])
            assert isinstance(u.get('config', {}), dict), type(u['config'])

            upload = Upload(type=u['type'], config=u.get('config', {}))

            artifact.uploads[upload.type] = upload
        artifacts[artifact.type] = artifact

    return artifacts
