"""A setuptools based setup module for jaws.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
from jaws.common import jaws_version

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name="jaws",
    version='{}'.format(jaws_version),
    description='Software to convert idiosyncratic ASCII formats to netCDF formats',
    long_description=long_description,
    url='https://github.com/jaws/jaws',
    author='Ajay Saini',
    author_email='ajcse1@gmail.com',
    license='Apache License, Version 2.0',
    packages=find_packages(),
    include_package_data=True,
    platforms=["any"],
    keywords=['xarray', 'netcdf', 'pandas', 'data', 'science', 'network', 'meteorology', 'climate', 'automated', 'weather', 'stations'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: OS Independent"],

    install_requires=['pandas', 'numpy >= 1.11', 'xarray', 'pytz', 'matplotlib', 'netcdf4'],

    entry_points = {
        'console_scripts': ['jaws=jaws.jaws:start'],
    }
)