# Example

JAWS is a command-line tool. 
Linux/Unix users can run JAWS from terminal and Windows users from Anaconda Prompt. 

The only required argument that a user has to provide is the input file path. 
The following minimalist command converts the input file (using default options):

``` html
$ jaws PROMICE_EGP_20160503.txt
```

By default, the output file will be stored within the current working directory 
with same name as of input file 
(e.g. PROMICE_EGP_20160503.txt will be converted to PROMICE_EGP_20160503.nc).

The user can optionally give their own output path/filename using `-o` option as following:

``` html
$ jaws -o ~/Desktop/EGP_20160503.nc PROMICE_EGP_20160503.txt
```

or

``` html
$ jaws -o ~/Desktop/EGP_20160501.nc ~/Downloads/PROMICE_EGP_20160503.txt
```

where the first argument i.e. after `-o` is the user-defined output filename and 
the last argument is input filename

All options are explained in detail in the next section.


The current version can translate L2 ASCII data from the following networks to netCDF format: 

* Antarctic Automatic Weather Stations (**AAWS**): 
Sample raw file can be downloaded from 
[here](http://jaws.ess.uci.edu/jaws/sample_data/AAWS_AGO-4_20161130.txt). 
Right click on the link and select "Save link as".

* Greenland Climate Network (**GCNet**): 
Sample raw file can be downloaded from 
[here](http://jaws.ess.uci.edu/jaws/sample_data/GCNet_Summit_20120817.txt)

* Institute for Marine and Atmospheric Research (**IMAU**): 
Sample raw file for Antarctic stations can be downloaded from 
[here](http://jaws.ess.uci.edu/jaws/sample_data/ant_aws17IMAU_20150101.txt) 
and for Greenland stations can be downloaded from 
[here](http://jaws.ess.uci.edu/jaws/sample_data/grl_aws05IMAU_20151008.txt)

* The Polar Earth Observing Network (**POLENET**): 
Sample raw file can be downloaded from 
[here](http://jaws.ess.uci.edu/jaws/sample_data/polenet_FoynPoint_20100208.dat)

* Programme for Monitoring of the Greenland Ice Sheet (**PROMICE**): 
Sample raw file can be downloaded from 
[here](http://jaws.ess.uci.edu/jaws/sample_data/PROMICE_EGP_20160503.txt)

* Scientific Committee on Antarctic Research (**SCAR**): 
Sample raw file can be downloaded from 
[here](http://jaws.ess.uci.edu/jaws/sample_data/SCAR_Sofiab_aws.dat)

```
Important Note:

For PROMICE, input file name must contain station name. 
e.g. 'PROMICE_KAN-B.txt' or 'KAN-B.txt' or 'Kangerlussuaq-B_abc.txt', etc.

For IMAU, input file name must start with network type(i.e. 'ant' or 'grl'), 
followed by a underscore and then station number. 
e.g. 'ant_aws01.txt' or 'ant_aws15_123.txt' or 'grl_aws21abc.txt', etc.

For SCAR, input file name must end with '_aws.dat'.
e.g. 'Sofiab_aws.dat' or '123abc_aws.dat', etc.

For POLENET, input file name must start with 'polenet_'.
e.g. 'polenet_FoynPoint.txt' or 'polenet_FoynPoint_20100208.dat', etc.

```
