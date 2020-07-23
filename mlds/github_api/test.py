import functools
import contextlib
import subprocess
import pathlib


p = pathlib.Path()
p2 = pathlib.Path('abc')
print(p, p2, p / p2)

p = pathlib.Path('/abc/def')
p2 = pathlib.Path('/ghe/ijk')
print(p, p2, p / p2)

p = pathlib.Path('/abc/def')
p2 = pathlib.Path('abc/def')
print(p, p2, p / p2)
