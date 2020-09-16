# Copyright 2020 Dirk Thomas
# Licensed under the Apache License, Version 2.0

import configparser
import glob
import os
import shutil
import subprocess
import sys

from publish_python.package import get_package_name_and_version


def create_deb(*, config):
    pkg = get_package_name_and_version()
    source_pkg_name = f'python3-{pkg.name.replace("_", "-")}'

    try:
        print('\n-- Building sdist_dsc and bdist_deb package ...')
        cmd = [
            sys.executable, 'setup.py',
            '--command-packages=stdeb.command',
            'sdist_dsc', '--source', source_pkg_name,
            '--with-python3', 'true',
            '--with-python2', 'false',
            '--force-x-python3-version',
            'bdist_deb']

        config_parser = configparser.RawConfigParser()
        config_parser.read(config.get('stdeb_file', 'stdeb.cfg'))

        add_env = {}
        if config_parser.has_option(pkg.name, 'Setup-Env-Vars'):
            setup_env_vars = config_parser.get(pkg.name, 'Setup-Env-Vars')
            for env_var in setup_env_vars.split(' '):
                key, value = env_var.split('=', 1)
                add_env[key] = value

        print(
            '$', *cmd,
            f'[with {str.join(" ", [f"{k}={v}" for k, v in add_env.items()])}]'
            if add_env else '')

        subprocess.check_call(cmd, env=dict(os.environ, **add_env))
    finally:
        tarball = f'{pkg.name}-{pkg.version}.tar.gz'
        if os.path.isfile(tarball):
            os.unlink(tarball)

    return {
        f'deb_dist/{source_pkg_name}_{pkg.version}.orig.tar.gz',
        f'deb_dist/{source_pkg_name}_{pkg.version}-1.debian.tar.gz',
        f'deb_dist/{source_pkg_name}_{pkg.version}-1.dsc',
        f'deb_dist/{source_pkg_name}_{pkg.version}-1_all.deb'}


def clean_deb():
    pkg = get_package_name_and_version()
    print(f"\n-- Deleting wheel artifacts of package '{pkg.name}' ...")
    subfolders = ['deb_dist', 'dist'] + \
        glob.glob(
            f'**/{pkg.name.replace("-", "_")}.egg-info', recursive=True)
    for subfolder in subfolders:
        if os.path.exists(subfolder):
            print("-- Deleting subfolder '%s' ..." % subfolder)
            shutil.rmtree(subfolder)
