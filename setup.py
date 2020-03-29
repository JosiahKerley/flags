#!/usr/bin/env python
from setuptools import setup, find_packages
with open('requirements.txt', 'r') as f:
    requirements = f.read.rstrip().split('\n')
setup(
    name='sysflags',
    version='0.0.1',
    description='A system database for storing flags as structured key value pairs.',
    url='https://github.com/JosiahKerley/flags',
    author='Josiah Kerley',
    author_email='josiahkerley@gmail.com',
    keywords='system database utilities',
    package_dir={'': 'sysflags'},
    packages=find_packages(where='sysflags'),
    python_requires='>2.*, <4.*',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'flags=sysflags:cli',
        ],
    },
    project_urls={
        'Source': 'https://github.com/JosiahKerley/flags',
    },
)
