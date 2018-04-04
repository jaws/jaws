![Shark](http://grele.ess.uci.edu/jaws/img/shark.jpg)


# Justified Automated Weather Station (JAWS) Software 

[![Build Status](https://travis-ci.org/jaws/jaws.svg?branch=master)](https://travis-ci.org/jaws/jaws)
[![Build status](https://ci.appveyor.com/api/projects/status/gt0r8jlo5iarqv55?svg=true)](https://ci.appveyor.com/project/ajcse1/jaws)
___
## News

2017/10/23: Version 0.1 released: Original scripts from Wenshan

2018/01/22: Version 0.2 released: Conversion of GCNet, PROMICE and AAWS networks complete

## About

JAWS is a scientiﬁc software workﬂow to ingest Level 2 (L2) data in the multiple formats now distributed, harmonize it into a common format, and deliver value-added Level 3 (L3) output suitable for distribution by the network operator, analysis by the researcher, and curation by the data center. NASA has funded JAWS (project [summary](http://dust.ess.uci.edu/prp/prp_aist/prp_aist_smr.pdf)) from 20171001&ndash;20190930.

Automated Weather Station (AWS) and AWS-like networks are the primary source of surface-level meteorological data in remote polar regions. These networks have developed organically and independently, and deliver data to researchers in idiosyncratic ASCII formats that hinder automated processing and intercomparison among networks. Moreover, station tilt causes signiﬁcant biases in polar AWS measurements of radiation and wind direction. Researchers, network operators, and data centers would beneﬁt from AWS-like data in a common format, amenable to automated analysis, and adjusted for known biases.

The immediate target recipient elements are polar AWS network managers, users, and data distributors. L2 borehole data suffers from similar interoperability issues, as does non-polar AWS data. Hence our L3 format will be extensible to global AWS and permafrost networks. JAWS will increase *in situ* data accessibility and utility, and enable new derived products.

## Overview

### JAWS consists of:

#### 1) Standardization

Convert L2 data (usually ASCII tables) into a netCDF-based L3 format compliant with metadata conventions (Climate-Forecast and ACDD) that promote automated discovery and analysis. 

#### 2) Adjustment

Include value-added L3 features like the Retrospective, Iterative, Geometry-Based (RIGB) tilt angle and direction corrections, solar zenith angle, standardized quality flags, GPS-derived ice velocity, and turbulent fluxes.

#### 3) API

Provide a scriptable API to extend the initial L2-to-L3 conversion to newer AWS-like networks and instruments.

___
<!--
## Installation
### Linux/unix/win
#### Requirements:
* writable directory
* anaconda/miniconda
* installed unzip package

From within a writable directory, run the following command:
``` html
$ conda install -c conda-forge jaws
```
-->

## Obtaining and Running JAWS

First-time users can execute this to copy JAWS to their local machines:

``` html
$ git clone https://github.com/jaws/jaws.git
```

Those with GitHub accounts who wish to contribute to JAWS should clone via SSH instead:

``` html
$ git clone git@github.com:/jaws/jaws.git
```

Users should periodically update their local repositories to the current version:

``` html
$ git pull
```

### Pre-requisites 

JAWS works with any Python distribution, and especially well with Anaconda and [Miniconda](https://conda.io/miniconda.html)
* matplotlib: Install with `conda install matplotlib` or as instructed [here](http://matplotlib.org)
* netCDF4: Install with `conda install netcdf4` or as instructed [here](http://unidata.github.io/netcdf4-python)
* pandas: Install with `conda install pandas` or as instructed [here](http://pandas.pydata.org)
* xarray: Install with `conda install xarray` or as instructed [here](http://xarray.pydata.org)

### Example

The current version can translate L2 ASCII data from the GCNet, PROMICE and AAWS networks to netCDF format. The user provides the input file path. By default, the output file will be stored within the current directory with the network name (e.g. promice.nc). The user can optionally give their own output path/name. Execute this from the JAWS `source` directory:

``` html
$ python jaws.py ../sample_data/PROMICE_EGP_20160501.txt
```

or from anywhere, by specifying longer paths, and with options:

``` html
$ python ~/jaws/source/jaws.py -4 -o ~/PROMICE_EGP_20160501.nc ~/jaws/sample_data/PROMICE_EGP_20160501.txt
$ python ~/jaws/source/jaws.py -4 -o ~/GCNET_Summit_20140601.nc ~/jaws/sample_data/GCNET_Summit_20140601.txt
$ python ~/jaws/source/jaws.py -4 -o ~/AAWS_AGO-4_20161130.nc ~/jaws/sample_data/AAWS_AGO-4_20161130.txt
```

where the argument to the optional `-o` is the user-defined output filename

#### Analysis Example

Currently, JAWS can be used to analyse the data for GCNet in multiple ways such as:

i. Plotting monthly diurnal cycle to see hourly changes for any variable throughout the month.

The user provides input file path, variable name (on which analysis needs to be done) and plot type (i.e. diurnal, monthly, annual or seasonal). Year and month are optional arguments. If the input file contains data for only single year, then the user doesn't  need to provide the '-y' argument. Similar is the case for '-m' argument.

```
$ python analysis.py file.nc temperature_tc_1 diurnal -y 2002 -m 5
```

![diurnal](http://grele.ess.uci.edu/jaws/img/diurnal.png)

ii. Avg, max and min values for each day of a month for any variable

```
$ python analysis.py file.nc temperature_cs500_1 monthly -y 2013 -m 2
```

![monthly](http://grele.ess.uci.edu/jaws/img/monthly.png)

iii. Annual cycle with daily mean, max and min

Since it is annual plot, user shouldn't provide the '-m' argument

```
$ python analysis.py file.nc temperature_tc_1 annual -y 2016
```

![annual](http://grele.ess.uci.edu/jaws/img/annual.jpg)

iv. Climatological seasonal cycle showing variation for each month through multiple years

Since it is seasonal plot, user shouldn't provide both '-y', '-m' argument.

```
$ python analysis.py file.nc temperature_tc_1 seasonal
```

![seasonal](http://grele.ess.uci.edu/jaws/img/seasonal.png)


<!--
Storing AWS-like data using DSG convention:
``` html
$ jaws --L2=gcnet --featureType L2.ascii L3.nc
```
Unit-test to verify data:
``` html
$ jaws --L2=gcnet --kelvin sample_L2.ascii sample_L3.nc
```
Annotate L2b netCDF with CF and ACDD variable and global metadata:
``` html
$ jaws --L2=imau --creator_email=’janedoe@summit.com’ --L2.ascii L3.nc
```
Derive value-added data and metadata:
``` html
$ jaws --L2=gcnet --solar_zenith_angles L2.ascii L3.nc
```
-->

___
## Credit

This software is being developed by the University of California Irvine under NASA Advanced Information Systems Technology (AIST) Proposal and Project 80NSSC17K0540.

## Resources

* [API Reference](https://github.com/jaws/jaws/blob/master/API.md)
* [Release Notes](https://github.com/jaws/jaws/releases)
* [Gallery](https://github.com/jaws/jaws/wiki/Gallery)
* [Examples](https://)


## Full Documentation

See the [Wiki](https://github.com/jaws/jaws/wiki/) for full documentation, examples, operational details and other information.

## Bugs and Feedback

For bugs, questions and discussions please use the [GitHub Issues](https://github.com/jaws/jaws/issues).
 
## Copyright and License

Copyright (C) 2017--2018 Regents of the University of California.
You may redistribute and/or modify JAWS under the terms of the Apache License, Version 2.0.
