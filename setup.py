#!/usr/bin/env python2

from setuptools import setup, find_packages

setup(
    zip_safe=True,
    name='indy_build_promote',
    version="0.1",
    long_description="This is a utility for promoting content in the Indy package repository manager",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Public License",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Utilities",
    ],
    keywords='indy maven build java',
    author='John Casey',
    author_email='jdcasey@commonjava.org',
    url='https://github.com/Commonjava/indy_build_promote',
    license='APLv2',
    packages = find_packages(),
    install_requires=[
        'click',
        'requests',
        'ruamel.yaml',
    ],
    entry_points={
        'console_scripts': [
            'consolidate-builds = indy_build_promote:promote',
            'list-build-files = indy_build_promote:list_build_files'
        ],
    }
)

