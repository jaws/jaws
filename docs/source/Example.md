# Example

JAWS is a command-line tool. 
Linux/Unix users can run JAWS from terminal and Windows users from Anaconda Prompt. 

The only required argument that a user has to provide is the input file path. 
The following minimalist command converts the input ASCII file to netCDF format (using default options):

``` html
$ jaws PROMICE_EGP_20160503.txt
```

By default, the output file will be stored within the current working directory 
with same name as of input file 
(e.g. PROMICE_EGP_20160503.txt will be converted to PROMICE_EGP_20160503.nc).

The user can optionally give their own output path/filename using `-o` option as following:

``` html
$ jaws -o ~/Desktop/PROMICE_EGP_20160503.nc PROMICE_EGP_20160503.txt
```

where the first argument i.e. after `-o` is the user-defined path to output file and 
the last argument is path to input file.

All options are explained in detail in the [Arguments](Arguments.md) section.

```
Important Note:

For PROMICE, input file name must contain station name. 
e.g. 'PROMICE_KAN-B.txt' or 'KAN-B.txt' or 'Kangerlussuaq-B_abc.txt', etc.

For IMAU, input file name must start with network type(i.e. 'ant' or 'grl'), 
followed by a underscore and then station number. 
e.g. 'ant_aws01.txt' or 'ant_aws15_123.txt' or 'grl_aws21abc.txt', etc.

```
