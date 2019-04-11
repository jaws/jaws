.. jaws documentation master file, created by
   sphinx-quickstart on Fri Mar  1 15:10:31 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Justified Automated Weather Station (JAWS) Software
===================================================


.. image:: http://jaws.ess.uci.edu/jaws/img/nasa.png
   :width: 200 px

.. image:: http://jaws.ess.uci.edu/jaws/img/yopp_logo.png
   :width: 300 px


.. toctree::
   :maxdepth: 2
   :hidden:

   Networks
   Overview
   Installation
   Example
   Arguments
   RIGB
   Analysis
   Modification
   License

JAWS is a scientific software workflow to ingest Level 2 (L2) data in the multiple
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
intercomparison among networks. Moreover, station tilt causes significant biases in
polar AWS measurements of radiation and wind direction. Researchers, network operators,
and data centers would benefit from AWS-like data in a common format, amenable to
automated analysis, and adjusted for known biases.

The immediate target recipient elements are polar AWS network managers, users, and
data distributors. L2 borehole data suffers from similar interoperability issues,
as does non-polar AWS data. Hence our L3 format will be extensible to global AWS and
permafrost networks. JAWS will increase in situ data accessibility and utility, and
enable new derived products.
