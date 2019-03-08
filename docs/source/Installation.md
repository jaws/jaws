Installation
============

#### Requirements:
 * Python 2.7, 3.6, or 3.7 (as of JAWS version 0.7)

#### Installing pre-built binaries with conda (Linux, Mac OSX, and Windows)

By far the simplest and recommended way to install `JAWS` is using [conda](https://conda.io/docs/) (which is the wonderful package manager that comes with [Anaconda](https://conda.io/docs/user-guide/install/index.html) or [Miniconda](https://conda.io/miniconda.html) distribution).

To avoid dependencies version mismatch, it is recommended to create separate conda environment as following:
```html
$ conda  create --name jaws_env python=3.7
$ source activate jaws_env
```

You can then install `JAWS` and all its dependencies with:
``` html
$ conda install -c conda-forge jaws
```

#### Installing from source

If you do not use conda, you can install `JAWS` from source with:
``` html
$ pip install jaws
```
(which will download the latest stable release from the [PyPI repository](https://pypi.org/) and trigger the build process.)

pip defaults to installing Python packages to a system directory (such as /usr/local/lib/python2.7). This requires root access.

If you don't have root/administrative access, you can install `JAWS` using:
``` html
$ pip install jaws --user
```
`--user` makes pip install packages in your home directory instead, which doesn't require any special privileges.

#### Update

Users should periodically update JAWS to the latest version using:
```html
$ conda update -c conda-forge jaws
```
or

```html
$ pip install jaws --upgrade
```
