# import epot_poetry_test

# from absl import app
import pkg_resources
import pkgutil
import pathlib
import importlib.resources
"""
print('Hi')

l = list(pkg_resources.iter_entry_points('epottest.test'))

# import sub
# import sub.a
print('aa')
# print(sub.a)

p = list(p for p in pkgutil.iter_modules() if p.name == 'sub123')[0]
print(list(pkgutil.walk_packages([f'{p.module_finder.path}/{p.name}'])))
print(p)
print('ss')
"""


def main(_):
  pass


class A:
  pass


print('\n'.join(dir(A)))
print(A.__module__)

print(importlib.resources.read_text('my_dataset', 'checksums.txt'))
print(
    importlib.resources
    .read_text('my_dataset.data', pathlib.Path('data.json'))
)

# importlib.resources.read_text(get_package(A), 'checksums.txt')
