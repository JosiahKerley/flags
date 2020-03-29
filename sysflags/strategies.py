#!/usr/bin/env python
import dpath.util

class Strategy:
  def __init__(self, *args, **kwargs):
    self.args = args
    self.kwargs = kwargs
    self._setup()

  def _setup(self):
    pass


class MergeStrategy(Strategy):
  def get_data(self):
    return {}

  def _setup(self):
    self._cls = self.kwargs['cls'].__class__
    self._scope = self.kwargs['scope']
    self._snapshot = self.kwargs['snapshot']
    self._namespace = self.kwargs['namespace']
    self.system = self._cls(scope='system', snapshot=self._snapshot, namespace=self._namespace, strategy=None)
    self.user = self._cls(scope='user', snapshot=self._snapshot, namespace=self._namespace, strategy=None)
    self.directory = self._cls(scope='directory', snapshot=self._snapshot, namespace=self._namespace, strategy=None)
    try:
      self.system = self.system._get_data()
    except:
      self.system = {}
    try:
      self.user = self.user._get_data()
    except:
      self.user = {}
    try:
      self.directory = self.directory._get_data()
    except:
      self.directory = {}


class MergeScopesTopToBottom(MergeStrategy):
  def get_data(self):
    return dpath.util.merge(
      self.system, dpath.util.merge(
        self.user, self.directory
      )
    )
