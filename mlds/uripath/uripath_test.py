from mlds.uripath import uripath


def test_uri():
  path = uripath.PureUriPath('gs://bucket/part')

  # PurePath methods
  assert isinstance(path, uripath.GcsPath)
  assert repr(path) == 'GcsPath(\'gs://bucket/part\')'
  assert str(path) == 'gs://bucket/part'
  assert path.parts == ('gs://', 'bucket', 'part')

  assert path.scheme == 'gs'

  # PurePath methods on a child
  sub_path = path / 'other'
  assert isinstance(sub_path, uripath.GcsPath)
  assert repr(sub_path) == 'GcsPath(\'gs://bucket/part/other\')'
  assert str(sub_path) == 'gs://bucket/part/other'
  assert sub_path.parts == ('gs://', 'bucket', 'part', 'other')

  # PurePath methods on a parent
