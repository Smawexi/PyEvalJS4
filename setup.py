from setuptools import setup, find_packages
from pyevaljs4.__version__ import version


NAME = 'pyevaljs4'
URL = "https://github.com/Smawexi/PyEvalJS4"
EMAIL = '1281722462@qq.com'
AUTHOR = 'Samwe'
REQUIRES_PYTHON = '>=3.7.0'
DESCRIPTION = 'A high-performance Python library that relies on nodejs to execute JavaScript'
LONG_DESCRIPTION = open('README.md', encoding="utf-8").read()

setup(
    name=NAME,
    version=version,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(where=".", exclude=('tests',)),
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: Implementation :: CPython',
        'License :: OSI Approved :: MIT License'
    ],
    python_requires=REQUIRES_PYTHON
)
