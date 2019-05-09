# About

JAWS is a scientific software workflow to ingest Level 2 (L2) data in the multiple
formats now distributed, harmonize it into a common format, and deliver value-added
Level 3 (L3) output suitable for distribution by the network operator, analysis by
the researcher, and curation by the data center.
NASA has funded JAWS [project summary](http://dust.ess.uci.edu/prp/prp_aist/prp_aist_smr.pdf) from 20171001 to 20190930.

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

## Components

**1) Standardization**: Convert L2 data (usually ASCII tables) into a netCDF-based L3 format compliant with metadata conventions (Climate-Forecast and ACDD) that promote automated discovery and analysis.

**2) Adjustment**: Include value-added L3 features like the Retrospective, Iterative, Geometry-Based (RIGB) tilt angle and direction corrections, solar zenith angle, standardized quality flags, GPS-derived ice velocity, and turbulent fluxes.

**3) Analysis**: Perform analysis on input variables and generate plots to identify trends.

**4) API**: Provide a scriptable API to extend the initial L2-to-L3 conversion to newer AWS-like networks and instruments.
