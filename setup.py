#!/usr/bin/env python
import os
from setuptools import setup
from setuptools import find_packages

def get_package_data(package):
  walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
          for dirpath, dirnames, filenames in os.walk(package)
          if not os.path.exists(os.path.join(dirpath, '__init__.py'))]
  filepaths = []
  for base, filenames in walk:
    filepaths.extend([os.path.join(base, filename)
                      for filename in filenames])
  return {package: filepaths}


os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
with open('requirements.txt', 'r') as f:
    requirements = f.read().rstrip().split('\n')

setup(
  name             = 'flags',
  version          = '0.0.1',
  description      = 'TBD',
  author           = 'Josiah Kerley',
  author_email     = 'josiahkerley.@gmail.com',
  url              = 'https://github.com/JosiahKerley/flags',
  zip_safe         = False,
  install_requires = requirements,
  packages=find_packages(),
  package_data=get_package_data('flags'),
  entry_points = {
    "console_scripts": [
      "flags=sysflags:console"
    ]
  }
)