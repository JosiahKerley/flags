#!/usr/bin/env python
from __future__ import print_function
import sys
import json
import yaml

def eprint(*args, **kwargs):
  print(*args, file=sys.stderr, **kwargs)

def print_formatted_message(data, format='json', pretty=False):
  if type(data) == type(''):
    print(data)
  elif format == 'json':
    if pretty:
      print(json.dumps(data, indent=2))
    else:
      print(json.dumps(data, indent=2))
  elif format == 'yaml':
    print(yaml.dump(data))
