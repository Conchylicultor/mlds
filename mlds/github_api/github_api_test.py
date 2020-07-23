"""Github API util tests."""

import contextlib
from unittest import mock

import pytest

from mlds.github_api import github_api

_original_query_github = github_api._PathMetadata._query_github


@pytest.fixture(scope='module', autouse=True)
def assert_no_api_call():
  """Globally disable github API call."""
  with mock.patch.object(
      github_api._PathMetadata,
      '_query_github',
      side_effect=AssertionError('Forbidden API call'),
  ):
    yield


@contextlib.contextmanager
def enable_api_call():
  """Contextmanager which explicitly allow API calls."""
  with mock.patch.object(
      github_api._PathMetadata, '_query_github', _original_query_github
  ):
    yield


def test_parse_github_path():
  url = '/tensorflow/datasets/tree/master/docs/README.md'
  repo, branch, path = github_api._parse_github_path(url)
  assert repo == 'tensorflow/datasets'
  assert branch == 'master'
  assert path == 'docs/README.md'

  url = '/tensorflow/datasets/tree/master'
  repo, branch, path = github_api._parse_github_path(url)
  assert repo == 'tensorflow/datasets'
  assert branch == 'master'
  assert path == ''


def test_invalid_github_path():

  with pytest.raises(ValueError, match='Invalid github path'):
    github_api.GithubPath()

  with pytest.raises(ValueError, match='Invalid github path'):
    github_api.GithubPath('')

  with pytest.raises(ValueError, match='Invalid github path'):
    github_api.GithubPath('/not/a/path')

  with pytest.raises(ValueError, match='Invalid github path'):
    github_api.GithubPath('/tensorflow/tree/master/docs/README.md')

  # `blob` isn't accepted for consistency between paths.
  with pytest.raises(ValueError, match='Invalid github path'):
    github_api.GithubPath('/tensorflow/datasets/blob/master/docs/README.md')

  p = github_api.GithubPath('/tensorflow/datasets/tree/master/docs/README.md')
  p = p.parent  # /docs
  p = p.parent  # /
  with pytest.raises(ValueError, match='Invalid github path'):
    p.parent  # pylint: disable=pointless-statement


def test_github_path_purepath():
  """Tests that pathlib methods works as expected."""
  p = github_api.GithubPath('/tensorflow/datasets/tree/master/')
  sub_p = p / 'some_folder'
  assert isinstance(sub_p, github_api.GithubPath)
  assert str(p) == '/tensorflow/datasets/tree/master'
  assert p == github_api.GithubPath.from_repo('tensorflow/datasets')


def test_github_api_listdir():
  """Test query github API (non-hermetic)."""
  # PurePath ops do not trigger API calls
  p = github_api.GithubPath.from_repo('tensorflow/datasets', 'v3.1.0')
  p = p / 'tensorflow_datasets' / 'testing'

  with enable_api_call():
    sub_dirs = sorted(p.iterdir())

  # `listdir` call cache the filetype of all childs
  all_dir_names = [d.name for d in sub_dirs if d.is_dir()]
  all_file_names = [d.name for d in sub_dirs if d.is_file()]
  all_names = [d.name for d in sub_dirs]

  with pytest.raises(NotADirectoryError):
    list((p / '__init__.py').iterdir())

  assert all_names == [
      '__init__.py',
      'dataset_builder_testing.py',
      'dataset_builder_testing_test.py',
      'fake_data_generation',
      'fake_data_utils.py',
      'generate_archives.sh',
      'metadata',
      'mocking.py',
      'mocking_test.py',
      'test_case.py',
      'test_data',
      'test_utils.py',
      'test_utils_test.py',
  ]
  assert all_dir_names == [
      'fake_data_generation',
      'metadata',
      'test_data',
  ]
  assert all_file_names == [
      '__init__.py',
      'dataset_builder_testing.py',
      'dataset_builder_testing_test.py',
      'fake_data_utils.py',
      'generate_archives.sh',
      'mocking.py',
      'mocking_test.py',
      'test_case.py',
      'test_utils.py',
      'test_utils_test.py',
  ]


def test_github_api_exists():
  """Test query github API (non-hermetic)."""
  p = github_api.GithubPath.from_repo('tensorflow/datasets', 'v3.1.0')
  with enable_api_call():
    assert p.exists()
    assert not (p / 'unnknown_dir').exists()

  readme = p / 'README.md'
  core = p / 'tensorflow_datasets' / 'core'
  with enable_api_call():
    assert readme.is_file()
    assert core.is_dir()

  # Data should have been cached (no API calls required)
  assert not readme.is_dir()
  assert not core.is_file()
  assert readme.exists()
  assert core.exists()
  # Recreating a new Path reuse the cache
  assert (core.parent.parent / 'README.md').is_file()
  assert (core.parent.parent / 'README.md')._metadata is readme._metadata


def test_assert_no_api_call():
  with pytest.raises(AssertionError, match='Forbidden API call'):
    github_api.GithubPath.from_repo('tensorflow/datasets', 'v1.0.0').exists()
