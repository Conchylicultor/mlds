"""Tests for external datasets."""
import pathlib
import textwrap
from typing import List

from unittest import mock

from mlds import github_api
from mlds.community import export_community_datasets


def _write_dataset_files(
    root_path: pathlib.Path, namespace: str, datasets: List[str]
) -> str:
  """Write the repo content containing the datasets."""
  repo_path = root_path / namespace
  # Create all datasets
  for ds_name in datasets:
    ds_path = repo_path / ds_name / f'{ds_name}.py'
    ds_path.parent.mkdir(parents=True)  # Create the containing dir
    ds_path.touch()  # Create the file

  # Additional noisy files should be ignored
  (repo_path / '__init__.py').touch()
  (repo_path / 'empty_dir').mkdir()
  return str(repo_path)


def test_export_community_datasets(tmp_path):

  # Create the community dataset repositories
  tfg_path = _write_dataset_files(
      tmp_path, namespace='tensorflow_graphics', datasets=['cifar']
  )
  nlp_path = _write_dataset_files(
      tmp_path, namespace='nlp', datasets=['mnist', 'robotnet']
  )

  # Import/export community datasets
  in_path = tmp_path / 'config.toml'
  in_path.write_text(
      textwrap.dedent(
          f"""\
          [Namespaces]
          tensorflow_graphics = '{tfg_path}'
          nlp = '{nlp_path}'
          """
      )
  )
  out_path = tmp_path / 'out.tsv'

  with mock.patch.object(github_api, 'GithubPath', pathlib.Path):
    export_community_datasets.export_community_datasets(in_path, str(out_path))

  # Ensure datasets where correctly exported
  assert out_path.read_text() == textwrap.dedent(
      f"""\
      namespace\tname\tpath
      tensorflow_graphics\tcifar\t{tfg_path}/cifar
      nlp\tmnist\t{nlp_path}/mnist
      nlp\trobotnet\t{nlp_path}/robotnet
      """
  )
