#!/usr/bin/env python2

from setuptools import setup, find_packages

setup(
    zip_safe=True,
    name='indy_build_promote',
    version="0.1",
    license='APLv2',
    packages = find_packages(),
    install_requires=[
        'click',
        'requests',
        'ruamel.yaml',
    ],
    # entry_points={
    #     'console_scripts': [
    #         'consolidate-builds = indy_build_promote:promote',
    #         'list-build-files = indy_build_promote:list_build_files'
    #     ],
    # }
)

