#!/usr/bin/env python
import argparse
from .database import YamlDatabase as DB
from . import utils

def cli():
  parser = argparse.ArgumentParser()
  parser.add_argument('-S', '--scope',  default='directory',     help="flag scope")
  parser.add_argument('-F', '--output-format', default='yaml', dest='format', help="output format")
  parser.add_argument('-g', '--get', help="get a value")
  parser.add_argument('-s', '--set', help="set a value")
  parser.add_argument('-v', '--value', help="set a value")
  parser.add_argument('-d', '--dump', action="store_true", help="dump the database")
  args = parser.parse_args()

  db = DB(scope=args.scope)
  if args.get:
    utils.print_formatted_message(db.get(query=args.get), format=args.format)
  elif args.set:
    utils.print_formatted_message(db.set(query=args.set, value=args.value), format=args.format)
  elif args.dump:
    utils.print_formatted_message(db.dump(), format=args.format)

