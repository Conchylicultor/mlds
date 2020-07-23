"""Uri util path."""

import abc
import pathlib
from typing import ClassVar, Dict


class PureUriPath(pathlib.PurePosixPath, abc.ABC):
  """Path representing an URI."""

  SCHEME: ClassVar[str]

  _subclasses: Dict[str, 'PureUriPath'] = {}

  def __init_subclass__(cls, **kwargs):
    """Dynamically register subclasses."""
    super().__init_subclass__(**kwargs)
    if cls.SCHEME in cls._subclasses:
      raise ValueError(
          f'Conflict: Same scheme "{cls.SCHEME}" registered twice: '
          f'{cls} and {cls._subclasses[cls.SCHEME]}'
      )
    cls._subclasses[cls.SCHEME] = cls

  def __new__(cls, *args):
    """Create a new URI instance."""
    # 1: Find which subclass
    # TODO(perf): Lookup should be optimized (how ?).
    p = super().__new__(cls, *args)
    scheme = p.parts[0]
    subclass = cls._subclasses[scheme.rstrip(':')]
    # 2. Create the child
    # To avoid circular __new__, the new path is created by
    # calling the parent __new__.
    # This means subclasses aren't notified when they are
    # created.
    # We should have a way of forwarding state & cie to childs
    uri_path = pathlib.PurePosixPath.__new__(subclass, '/', *p.parts[1:])
    return uri_path

  def __str__(self) -> str:
    # TODO(perf): Could cache the result
    s = super().__str__()
    return f'{self.SCHEME}:/{s}'


class PureAbstractPath(pathlib.PurePosixPath):
  """Path which is extensible."""


class GcsPath(PureUriPath):
  SCHEME = 'gs'


class S3Path(PureUriPath):
  SCHEME = 's3'
