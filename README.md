![Shark](./img/shark.jpg?raw=true)


# JAWS: Justified Automated Weather Station
___

## About

JAWS is a scientiﬁc software workﬂow to ingest Level 2 (L2) data in the multiple formats now distributed, harmonize it into a common format, and deliver value-added Level3 (L3) output suitable for distribution by the network operator, analysis by the researcher, and curation by the data center. 

Automated Weather Station (AWS) and AWS-like networks are the primary source of surface-level meteorological data in remote polar regions. These networks have developed organically and independently, and deliver data to researchers in idiosyncratic ASCII formats that hinder automated processing and intercomparison among networks. Moreover, station tilt causes signiﬁcant biases in polar AWS measurements of radiation and wind direction. Researchers, network operators, and data centers would beneﬁt from AWS-like data in a common format, amenable to automated analysis, and adjusted for known biases.

The immediate target recipient elements are polar AWS network managers, users, and data distributors. L2 borehole data suffers from similar interoperability issues, as does non-polar AWS data. Hence our L3 format will be extensible to global AWS and permafrost networks. JAWS will increase *insitu* data accessibility and utility, and enable new derived products.

## Overview

### JAWS consists of:

#### 1) Standardization

Convert L2 data (usually ASCII tables) into a netCDF-based L3 format compliant with metadata conventions (Climate-Forecast and ACDD) that promote automated discovery and
analysis. 

#### 2) Adjustment

Include value-added L3 features like the Retrospective, Iterative, Geometry-Based (RIGB) tilt angle and direction corrections, solar angles, and standardized quality flags. 

#### 3) API

Provide a scriptable API to extend the initial L2-to-L3 conversion to newer AWS-like networks and instruments.

___
## Installation
### 64-bit Linux/unix
#### Requirements:
* writable directory
* installed curl package
* installed unzip package

From within a writable directory, run the following command:
``` html
curl -L http://bit.ly/2j2SZz2 | bash
```

## Running JAWS
### Example Run on Linux
From within the JAWS-master directory, run the following commands:
``` html
$ source env.sh
```
* Should see the following output...
``` html
Adding conda to your path...
Activating jaws conda environment...
All done. Enjoy!
```

``` html
$ python RUNNER.py
```
<!--
* Should see similar log output to the following:
``` html
DEBUG : filemanager     Creating packet: './Example_data/AKUL232'
DEBUG : filemanager     Dropping packet: './Example_data/AKUL232'
DEBUG : filemanager     Creating packet: './Example_data/AKUL232'
DEBUG : filemanager     Creating packet: 1
DEBUG : filemanager     Creating packet: './Example_data/AKUL232.log'
DEBUG : filemanager     Creating packet: './Example_data/AUPA299'
DEBUG : filemanager     Dropping packet: './Example_data/AUPA299'
DEBUG : filemanager     Creating packet: './Example_data/AUPA299'
DEBUG : filemanager     Creating packet: 2
```
-->

___
## Credit

This software is being developed by the University of California under NASA Advanced Information Systems Technology (AIST) Proposal and Project 80NSSC17K0540.



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

