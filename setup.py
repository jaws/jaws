"""A setuptools based setup module for jaws.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

setup(
    name="jaws",
    version='0.2.6',
    description='Software to convert idiosyncratic ASCII formats to netCDF formats',
    url='https://github.com/jaws/jaws',
    author='Ajay Saini',
    author_email='ajcse1@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    #data_files=[('jaws/resources', ['jaws/resources/stations.txt']),
    #			('jaws/resources/aaws', ['jaws/resources/aaws/columns.txt']),
    #			('jaws/resources/aaws', ['jaws/resources/aaws/ds.json']),
    #			('jaws/resources/aaws', ['jaws/resources/aaws/encoding.json']),
    #			('jaws/resources/gcnet', ['jaws/resources/gcnet/columns.txt']),
    #			('jaws/resources/gcnet', ['jaws/resources/gcnet/ds.json']),
    #			('jaws/resources/gcnet', ['jaws/resources/gcnet/encoding.json']),
    #			('jaws/resources/gcnet', ['jaws/resources/gcnet/quality_control.json']),
    #			('jaws/resources/promice', ['jaws/resources/promice/aliases.txt']),
    #			('jaws/resources/promice', ['jaws/resources/promice/columns.txt']),
    #			('jaws/resources/promice', ['jaws/resources/promice/ds.json']),
    #			('jaws/resources/promice', ['jaws/resources/promice/encoding.json'])],
	platforms=["any"],
    keywords=['xarray', 'netcdf', 'pandas', 'data', 'science', 'network', 'meteorology', 'climate', 'automated', 'weather', 'stations'],
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
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

    install_requires=['pandas', 'numpy', 'xarray', 'pytz', 'matplotlib', 'netcdf4'],

    entry_points = {
        'console_scripts': ['jaws=jaws.jaws:start'],
    }
)