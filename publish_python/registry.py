# Copyright 2020 Dirk Thomas
# Licensed under the Apache License, Version 2.0

from publish_python.artifact.stdeb import clean_deb
from publish_python.artifact.stdeb import create_deb
from publish_python.artifact.wheel import clean_wheel
from publish_python.artifact.wheel import create_wheel
from publish_python.upload.github import upload_github
from publish_python.upload.packagecloud import upload_packagecloud
from publish_python.upload.pypi import upload_pypi

artifact_handlers = {}
artifact_cleanups = {}
upload_handlers = {}

# TODO this should be populated by entry points instead
artifact_handlers['stdeb'] = create_deb
artifact_cleanups['stdeb'] = clean_deb

artifact_handlers['wheel'] = create_wheel
artifact_cleanups['wheel'] = clean_wheel

upload_handlers['github'] = upload_github
upload_handlers['packagecloud'] = upload_packagecloud
upload_handlers['pypi'] = upload_pypi
