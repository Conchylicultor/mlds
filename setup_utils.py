"""Utils for `setup.py`."""

import importlib
import pathlib
import sys
import types
from typing import List


def import_module_from_path(path: pathlib.Path) -> types.ModuleType:
  """Import a file directly without executing the `__init__.py`.

  Based on:
  https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly

  Args:
    path: Path of the module to import

  Returns:
    Loaded module
  """
  module_path = pathlib.Path(path).resolve()
  module_name = module_path.stem  # 'path/x.py' -> 'x'
  spec = importlib.util.spec_from_file_location(module_name, module_path)
  module = importlib.util.module_from_spec(spec)
  sys.modules[module_name] = module
  spec.loader.exec_module(module)
  return module


def _is_valid_requirement(requirement: str) -> bool:
  """Returns True is the `requirement.txt` line is valid."""
  is_invalid = (
      not requirement or  # Empty line
      requirement.startswith('#') or  # Comment
      requirement.startswith('-r ')  # Filter the `-r requirement.txt`
  )
  return not is_invalid


def load_requirements(path: pathlib.Path) -> List[str]:
  """Loads the requirement.

  Args:
    path: Path to the `requirements.txt` file

  Returns:
    The list of packages
  """
  requirements = pathlib.Path(path).resolve().read_text().splitlines()
  return [req for req in requirements if _is_valid_requirement(req)]
