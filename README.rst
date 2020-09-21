Script to publish Python packages
=================================

The scripts offers a convenient way to:

* build different kinds of artifacts for a Python 3 package and
* upload the artifacts to various services.


Prerequisites
-------------

* Python 3.6 or higher (to run this script, not necessarily for the generated
  package)
* The Python package ``PyYAML``, on Debian / Ubuntu via ``python3-yaml``
* ``git`` command line (optional, to make the produced binary reproducible)


Wheel artifact
^^^^^^^^^^^^^^

* The Python package ``wheel``


Debian artifact
^^^^^^^^^^^^^^^

* The Python package ``stdeb`` (at least version 0.10 for reproducible
  binaries)
* The following Debian packages: ``debhelper``, ``dh-python``, ``fakeroot``,
  ``python3-all``


Upload to PyPI
^^^^^^^^^^^^^^

* The Python package ``twine``, configure the credentials for PyPI
  (see `twine docs <https://twine.readthedocs.io/en/latest/#configuration>`_)


Upload to packagecloud.io
^^^^^^^^^^^^^^^^^^^^^^^^^

* The gem ``package_cloud`` providing a CLI tool, configure the credentials
  (see `package_cloud docs <https://www.rubydoc.info/gems/package_cloud/#installation>`_)


Upload to GitHub release
^^^^^^^^^^^^^^^^^^^^^^^^

* The GitHub CLI tool ``gh``, configure authentication
  (see `gh docs <https://cli.github.com/manual/>`_)


Usage
-----

To build all artifacts configured in the ``publish_python.yaml`` file call:
``bin/publish_python``.
While this also shows the necessary commands to upload the artifacts no upload
is being performed.

To build and also upload all artifacts pass ``--upload``.

The tool will leave the generated build artifacts which can be cleaned
afterwards by calling the tool again with ``--clean-only``.

Instead of creating all configured artifact type and upload destinations the
desired targets can be passed explicitly.
A list of configured targets can be seen by passing ``--list-only``.

For more information about possible command line arguments pass ``--help``.


Configuration
-------------

A configuration file ``publish_python.yaml`` must be present in the root of the
Python package.

On the top level it must contain a key ``artifacts`` containing a list.
Each item of of that list describes an artifact type to be built.

An artifact type is described by:

* The required key ``type`` identifying what artifact to build (e.g. ``wheel``,
  ``stdeb``).
* The optional key ``config`` can contain an arbitrary dictionary specific to
  the artifact type.
* The required key ``uploads`` containing a list where each item describes an
  upload type.

An upload type is described by:

* The required key ``type`` identifying where to upload to (e.g. ``pypi``,
  ``packagecloud``).
* The optional key ``config`` can contain an arbitrary dictionary specific to
  the upload type.
* The required key ``uploads`` containing a list where each item describes an
  upload type.


stdeb configuration
^^^^^^^^^^^^^^^^^^^

stdeb requires its own configuration file ``stdeb.cfg``
(see `stdeb docs <https://github.com/astraw/stdeb#customizing-the-produced-debian-source-package-config-options>`_).


packagecloud.io configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* The required key ``repository`` describes the packagecloud.io repository to
  upload to.
* The optional key ``distributions`` can contain a list of distribution names.
  For Python wheels the correct name is ``python``.
  For Debian packages each name identifies the distribution and version (e.g.
  ``ubuntu/focal``).


GitHub release configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* The optional key ``repository`` describes the org unit and repository name to
  identify the upload destination (e.g. ``dirk-thomas/publish_python``).
  If the invocation is happening in a git repository the location can be
  determined automatically.


Example
^^^^^^^

.. code-block:: yaml

    artifacts:
      - type: wheel
        uploads:
          - type: pypi
          - type: packagecloud
            config:
              repository: dirk-thomas/repo_name
              distributions:
                - python
          - type: github
      - type: stdeb
        uploads:
          - type: packagecloud
            config:
              repository: dirk-thomas/repo_name
              distributions:
                - ubuntu:focal
                - debian:buster
          - type: github
            config:
              repository: dirk-thomas/publish_python
