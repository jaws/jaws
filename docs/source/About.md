# About

JAWS is a scientiﬁc software workﬂow to ingest Level 2 (L2) data in the multiple 
formats now distributed, harmonize it into a common format, and deliver value-added 
Level 3 (L3) output suitable for distribution by the network operator, analysis by 
the researcher, and curation by the data center. 
NASA has funded JAWS 
([project summary](http://dust.ess.uci.edu/prp/prp_aist/prp_aist_smr.pdf)) 
from 20171001 to 20190930.

Automated Weather Station (AWS) and AWS-like networks are the primary source 
of surface-level meteorological data in remote polar regions. 
These networks have developed organically and independently, and deliver data to 
researchers in idiosyncratic ASCII formats that hinder automated processing and 
intercomparison among networks. Moreover, station tilt causes signiﬁcant biases in 
polar AWS measurements of radiation and wind direction. Researchers, network operators, 
and data centers would beneﬁt from AWS-like data in a common format, amenable to 
automated analysis, and adjusted for known biases.

The immediate target recipient elements are polar AWS network managers, users, and 
data distributors. L2 borehole data suffers from similar interoperability issues, 
as does non-polar AWS data. Hence our L3 format will be extensible to global AWS and 
permafrost networks. JAWS will increase in situ data accessibility and utility, and 
enable new derived products.

## Supported AWS Networks

The current version can translate L2 ASCII data from the following networks to netCDF format: 

* *Antarctic Automatic Weather Stations* ([**AAWS**](https://amrc.ssec.wisc.edu/)): 
Sample raw file can be downloaded from 
[here](http://jaws.ess.uci.edu/jaws/sample_data/AAWS_AGO-4_20161130.txt). 
Right click on the link and select "Save link as".

* *Greenland Climate Network* ([**GCNet**](http://cires1.colorado.edu/steffen/gcnet/)): 
Sample raw file can be downloaded from 
[here](http://jaws.ess.uci.edu/jaws/sample_data/GCNet_Summit_20120817.txt)

* *Institute for Marine and Atmospheric Research* ([**IMAU**](http://www.projects.science.uu.nl/iceclimate/aws/)): 
Sample raw file for Antarctic stations can be downloaded from 
[here](http://jaws.ess.uci.edu/jaws/sample_data/ant_aws17IMAU_20150101.txt) 
and for Greenland stations can be downloaded from 
[here](http://jaws.ess.uci.edu/jaws/sample_data/grl_aws05IMAU_20151008.txt)

* *The Polar Earth Observing Network* ([**POLENET**](http://polenet.org/)): 
Sample raw file can be downloaded from 
[here](http://jaws.ess.uci.edu/jaws/sample_data/polenet_FoynPoint_20100208.dat)

* *Programme for Monitoring of the Greenland Ice Sheet* ([**PROMICE**](http://www.promice.org/home.html)): 
Sample raw file can be downloaded from 
[here](http://jaws.ess.uci.edu/jaws/sample_data/PROMICE_EGP_20160503.txt)

* *Scientific Committee on Antarctic Research* ([**SCAR**](https://legacy.bas.ac.uk/met/jds/met/SCAR_oma.htm)): 
Sample raw file can be downloaded from 
[here](http://jaws.ess.uci.edu/jaws/sample_data/SCAR_Sofiab_aws.dat)


**Total number of stations handled by JAWS: 378**

**Total number of station-years of data handled by JAWS: 3600**

![](http://jaws.ess.uci.edu/jaws/img/map_ant.png)

![](http://jaws.ess.uci.edu/jaws/img/map_grl.png)


If your network is not in the above list and you would like it to be supported by **JAWS**, please open an issue 
on [Github](https://github.com/jaws/jaws/issues) or contact *Charlie Zender* at <zender@uci.edu>
