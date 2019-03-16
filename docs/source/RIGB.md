# RIGB

RIGB (Retrospective, Iterative, Geometry-Based) is a method that corrects tilt angle and 
direction for AWS with solar radiometry. Unattended AWS are subject to tilt, especially 
when anchored in snow and ice. This tilt can alter the AWS-retrieved albedo from a the 
expected “smiley face” diurnal profile to almost a frown. 

The tilt angle at South Dome station was β ≈ 15◦ in 2008, 
enough to bias retrieved albedo by 0.05–0.10.

The RIGB tilt-correction algorithm advanced the state-of-the-art in removing 
surface shortwave biases from AWS. It reduces solar biases by 11Wm−2 averaged over 
Greenland from May–Sept (Wang et al., 2016), enough to melt 0.24m snow water equivalent. 

To run RIGB, user needs to specify “--rigb” option as below:

``` html
$ jaws ~/Downloads/gcnet_summit_20120817.txt --rigb
```

*Note: Active internet connection is needed when running RIGB, 
as RRTM and CERES files will be downloaded for calculations, 
they will be deleted however upon completion.*

RIGB uses [climlab](https://github.com/brian-rose/climlab)’s radiative transfer model to simulate clear-sky radiation.

RIGB relies on three external datasets:

1. **AIRS**: for thermodynamic profiles (2002-present)
2. **MERRA**: for thermodynamic profiles (1995-present)
3. **CERES**: for cloud fractions 

AIRS is the default dataset used for thermodynamic profiles in JAWS but AIRS data is 
available only since 2002. So, users working on pre-2002 datasets, 
please choose MERRA as following:

``` html
$ jaws ~/Downloads/gcnet_summit_20120817.txt --rigb --merra
```

It is to be noted here that user needs to use ‘--merra’ option in conjunction with ‘--rigb’.
