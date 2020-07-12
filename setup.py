import sys
import os
from setuptools import setup, find_packages

try:
    from setuptools import setup
    from setuptools import Command
    from setuptools import Extension
except ImportError:
    sys.exit(
        "We need the Python library setuptools to be installed. "
        "Try runnning: python -m ensurepip"
    )


REQUIRES = [
    "py2neo",
    "numpy",
    "pandas",
]


PACKAGES = [
    "tax2graph",
]


EXTENSIONS = [
    Extension(
        "Classeq.KmerCounter._kmer_counter",
        ["Classeq/KmerCounter/_kmer_counter.cpp"]
    ),
]


setup(
    name = 'tax2graph',
    version = '0.0.1',
    description = 'Parse taxonomy database from I4Life to neo4j database.',
    url = 'https://github.com/...',
    author = 'Samuel Galvão Elias',
    author_email = 'sgelias@outlook.com',
    license = 'MIT',
    packages = find_packages(),
    ext_modules = EXTENSIONS,
    install_requires = REQUIRES,
    include_package_data = True, # done via MANIFEST.in under setuptools
    zip_safe = False
)
