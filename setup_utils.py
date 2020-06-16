"""Utils for `setup.py`."""

import importlib
import pathlib
import sys
import types


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
