# Copyright 2020 Dirk Thomas
# Licensed under the Apache License, Version 2.0

from publish_python.artifact.wheel import clean_wheel
from publish_python.artifact.wheel import create_wheel
from publish_python.upload.pypi import upload_pypi

artifact_handlers = {}
artifact_cleanups = {}
upload_handlers = {}

# TODO this should be populated by entry points instead
artifact_handlers['wheel'] = create_wheel
artifact_cleanups['wheel'] = clean_wheel

upload_handlers['pypi'] = upload_pypi
