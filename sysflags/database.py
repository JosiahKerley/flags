#!/usr/bin/env python
from .strategies import *
from . import utils
import os
import re
import sys
import dpath.util
import pickle
from pathlib import Path
from datetime import datetime
dpath.options.ALLOW_EMPTY_STRING_KEYS = True


class Database:
  scope = None
  namespace = None
  snapshot = None
  strategy = None
  _file_extenstion = None
  _database_file_subpath = '{namespace}/snapshot-{snapshot}.{file_extenstion}'
  _datetime_fmt = "%Y-%m-%d_%H-%M-%S"
  _system_scope_parent_dir = '/etc/flags'
  _user_scope_parent_dir = f'{Path.home()}/.config/flags'
  _directory_scope_parent_dir = f'{os.getcwd()}/.flags'

  def __init__(self, scope='system', snapshot='current', namespace='default', strategy='MergeScopesTopToBottom'):
    self.scope = scope
    self.snapshot = snapshot
    self.namespace = namespace
    if strategy:
      self.strategy = getattr(sys.modules[__name__], strategy)(cls=self, scope=scope, snapshot=snapshot, namespace=namespace)
    self._setup()

  def _get_database_filepath(self, subpath=None):
    if not subpath:
      subpath = self._database_file_subpath.format(
        scope=self.scope,
        namespace=self.namespace,
        snapshot=self.snapshot,
        file_extenstion=self._file_extenstion
      )
    if self.scope == 'system':
      return f'{self._system_scope_parent_dir}/{subpath}'
    elif self.scope == 'user':
      return f'{self._user_scope_parent_dir}/{subpath}'
    elif self.scope == 'directory':
      return f'{self._directory_scope_parent_dir}/{subpath}'
    else:
      raise Exception(f'unknown scope {self.scope}')

  def _get_database_filedir(self):
    return os.path.dirname(self._get_database_filepath())

  def _get_datetime_string_now(self):
    return datetime.now().strftime(self._datetime_fmt)

  def _list_snapshot_filepaths(self):
    if os.path.exists(self._get_database_filedir()):
      return [f for f in os.listdir(self._get_database_filedir()) if re.match(rf'snapshot-.*.{self._file_extenstion}', f)]

  def _bootstrap_empty_file(self, filepath):
    os.mknod(filepath)
    return True

  def _setup_dirs(self):
    try:
      if not os.path.exists(self._get_database_filedir()):
        os.makedirs(self._get_database_filedir())
        utils.eprint(f'Creating directory {self._get_database_filedir()}')
    except:
      utils.eprint(f'Cannot create directory {self._get_database_filedir()}')

  def _setup_files(self):
    if self.snapshot == 'current':
      if not os.path.islink(self._get_database_filepath()) and os.path.exists(self._get_database_filedir()):
        if not self._list_snapshot_filepaths():
          subpath = self._database_file_subpath.format(
            scope=self.scope,
            namespace=self.namespace,
            snapshot=self._get_datetime_string_now(),
            file_extenstion=self._file_extenstion
          )
          empty_snapshot_filepath = self._get_database_filepath(subpath)
          utils.eprint(f'Creating empty db file {empty_snapshot_filepath}')
          assert self._bootstrap_empty_file(empty_snapshot_filepath)
          os.symlink(empty_snapshot_filepath, self._get_database_filepath())
      return True
    else:
      subpath = self._database_file_subpath.format(
        scope=self.scope,
        namespace=self.namespace,
        snapshot=self.snapshot,
        file_extenstion=self._file_extenstion
      )
      return os.path.isfile(self._get_database_filepath(subpath))

  def _setup(self):
    self._setup_dirs()
    self._setup_files()

  def _serialize(self, data: dict):
    return pickle.dumps(data)

  def _deserialize(self, datastr: str) -> dict:
    return pickle.loads(datastr)

  def _read_data(self):
    with open(self._get_database_filepath(), 'r') as f:
      return f.read()

  def _write_data(self, data):
    with open(self._get_database_filepath(), 'w') as f:
      return f.write(data)

  def _get_data(self):
    if self.strategy:
      return self.strategy.get_data()
    else:
      return self._deserialize(self._read_data())

  def _set_data(self, data: dict):
    return self._write_data(self._serialize(data))

  def dump(self):
    return self._get_data()

  def get(self, query: str):
    try:
      return dpath.util.get(self._get_data(), query)
    except:
      return None

  def search(self, query: str):
    return dpath.util.search(self._get_data(), query)

  def values(self, query: str):
    return dpath.util.values(self._get_data(), query)

  def set(self, query: str, value=None, writeback=True, recurse=True):
    if recurse:
      retval = dpath.util.new(self._get_data(), query, value)
    else:
      retval = dpath.util.set(self._get_data(), query, value)
    if writeback:
      self._set_data(retval)
    return retval


class YamlDatabase(Database):
  import yaml
  _file_extenstion = 'yaml'

  def _bootstrap_empty_file(self, filepath):
    with open(filepath, 'w') as f:
      return f.write('{}')

  def _serialize(self, data: dict):
    return self.yaml.dump(data)

  def _deserialize(self, datastr: str) -> dict:
    return self.yaml.load(datastr, Loader=self.yaml.FullLoader)


class JsonDatabase(Database):
  import json
  _file_extenstion = 'json'

  def _bootstrap_empty_file(self, filepath):
    with open(filepath, 'w') as f:
      return f.write('{}')

  def _serialize(self, data: dict):
    return self.json.dumps(data, indent=2)

  def _deserialize(self, datastr: str) -> dict:
    return self.json.loads(datastr)
