"""Setup script."""

import pathlib
import setuptools

import setup_utils

root_path = pathlib.Path(__file__).parent

# Import the version (without executing `mlds/__init__.py`)
version = setup_utils.import_module_from_path(root_path / 'mlds' / 'version.py')

# Import required packages
install_requires = setup_utils.load_requirements(root_path / 'requirements.txt')
test_requires = setup_utils.load_requirements(
    root_path / 'requirements-dev.txt'
)

setuptools.setup(
    # ----- Base -----
    name='mlds',
    version=version.__version__,

    # ----- Code -----
    packages=setuptools.find_namespace_packages(include=["mlds.*"]),
    install_requires=install_requires,
    extras_require={
        'test': test_requires,
    },
    package_data={},

    # ----- PyPI metadata -----
    description='Python Distribution Utilities',
    long_description=(root_path / 'README.md').read_text(encoding='utf-8'),
    author='Google Inc.',
    author_email='mlds-team+github@google.com',
    keywords=['dataset', 'datasets', 'mlds', 'tfds', 'opends'],
    # All classifiers at: https://pypi.org/classifiers/
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries",
        "Typing :: Typed",
    ],
    # TODO(mlds): Update once documentation is online
    url='https://github.com/opends/mlds',
)
