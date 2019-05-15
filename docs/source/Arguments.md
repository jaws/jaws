# Arguments

## Positional Arguments

* `input`: Path to raw L2 data file for converting to netCDF (or use -i option).

* `output`: Path to save output netCDF file (or use -o option).

Note: `input` is first positional argument and it is required, 
whereas `output` is second (or last) positional argument and it is optional. 
See examples below to understand more about it.

**Case 1**: User provides only input (e.g. *'ABC.txt'*).

Usage:
``` html
$ jaws ABC.txt
```

This will convert *'ABC.txt'* to netCDF format with same name as input file i.e. *'ABC.nc'*.

**Case 2**: User provides both input (e.g. *'ABC.txt'*) and output file name (e.g. *'XYZ.nc'*).

Usage:
``` html
$ jaws ABC.txt XYZ.nc
```

This will convert *'ABC.txt'* to *'XYZ.nc'*.

## Optional Arguments

* `-i, --fl_in, --input`: Path to raw L2 data file for converting to netCDF (or use first positional argument).

    Usage:
    ``` html
    $ jaws -i ABC.txt
    ```
    or
    ``` html
    $ jaws --fl_in ABC.txt
    ```
    or
    ``` html
    $ jaws --input ABC.txt
    ```

* `-o, --fl_out, --output`: Path to save output netCDF file (or use last positional argument).

    Usage:
    ``` html
    $ jaws -i ABC.txt -o XYZ.nc
    ```
    or
    ``` html
    $ jaws -o XYZ.nc -i ABC.txt
    ```

* `-r, --vrs, --version, --revision`: JAWS current version and last modified date.

    Usage:
    ``` html
    $ jaws --version America/Los_Angeles ABC.txt
    ```

* `-c, --cel, --celsius` `--centigrade`: By default, all temperature variables will be in Kelvin (K) in output file 
    (CF convention). Use this option if you want them in Celsius (°C) in output netCDF file. If during analysis step, 
    you find that units are Kelvin and you want the plots in Celsius, first convert the raw file to netCDF using this 
    option and then do the analysis.

    Usage:
    ``` html
    $ jaws --celsius ABC.txt
    ```

* `--mb, --hPa, --millibar`: By default, all pressure variables will be in Pascal (Pa) in output file 
    (CF convention). Use this option if you want them in hPa/millibar in output netCDF file. If during analysis step, 
    you find that units are Pa and you want the plots in hPa, first convert the raw file to netCDF using this 
    option and then do the analysis.

    Usage:
    ``` html
    $ jaws --hPa ABC.txt
    ```

* `--rigb`: Calculate adjusted downwelling shortwave flux, tilt_angle and tilt_direction. 
    This option is only for stations that archive radiometric data.

    Usage:
    ``` html
    $ jaws --rigb ABC.txt
    ```

* `--merra`: Select MERRA dataset for thermodynamic profiles in RIGB calculations. 
    It has to be used in conjunction with *rigb* option.

    Usage:
    ``` html
    $ jaws --rigb --merra ABC.txt
    ```

* `-f, --fll_val_flt, --fillvalue_float`: Override default float _FillValue.

    Usage:
    ``` html
    $ jaws --fll_val_flt 999.99 America/Los_Angeles ABC.txt
    ```

* `-s, --stn_nm, --station_name`: Override default station name.

    Usage:
    ``` html
    $ jaws -s AA ABC.txt
    ```

* `-t, --tz, --timezone`: Change the timezone, default is UTC. A list of all the timezones can be 
    found [here](https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568).

    Usage:
    ``` html
    $ jaws --timezone America/Los_Angeles ABC.txt
    ```

* `-3, --format3, --3, --fl_fmt=classic`: Output file in netCDF3 CLASSIC (32-bit offset) storage format.

    Usage:
    ``` html
    $ jaws -3 ABC.txt
    ```

* `-4, --format4, --4, --netcdf4`: Output file in netCDF4 (HDF5) storage format. This is default.

    Usage:
    ``` html
    $ jaws --format4 ABC.txt
    ```

* `-5, --format5, --5, --fl_fmt=64bit_data`: Output file in netCDF3 64-bit data (i.e., CDF5, PnetCDF) storage format.

    Usage:
    ``` html
    $ jaws --fl_fmt=64bit_data ABC.txt
    ```

* `-6, --format6, --6, --64`: Output file in netCDF3 64-bit offset storage format.

    Usage:
    ``` html
    $ jaws --6 ABC.txt
    ```

* `-7, --format7, --7, --fl_fmt=netcdf4_classic`: Output file in netCDF4 CLASSIC format (3+4=7).

    Usage:
    ``` html
    $ jaws -7 ABC.txt
    ```

* `-L, --dfl_lvl, --dfl, --deflate`: Lempel-Ziv deflation/compression (lvl=0..9) for netCDF4 output.

    Usage:
    ``` html
    $ jaws --dfl_lvl 2 America/Los_Angeles ABC.txt
    ```

* `--flx, --gradient_fluxes`: This method is only for GCNet stations. Calculate gradient fluxes i.e. Sensible and Latent
    Heat Flux based on [Steffen & DeMaria (1996)](http://doi.org/10.1175/1520-0450(1996)035<2067:sefoaw>2.0.co;2). 
    This method is very sensitive to input data quality.

    Usage:
    ``` html
    $ jaws --flx ABC.txt
    ```

* `--no_drv_tm, --no_derive_times`: By default extra time variables (month, day and hour) are derived for further 
    analysis. Use this option to not derive them.

    Usage:
    ``` html
    $ jaws --no_drv_tm ABC.txt
    ```

* `-D, --dbg_lvl, --debug_level`: Debug-level ranging from 1 to 9. It prints what steps are occurring during conversion.

    Usage:
    ``` html
    $ jaws -D 5 ABC.txt
    ```

* `-a, --anl, --analysis`: Plot type e.g.- diurnal, monthly, annual, seasonal.

    Usage:
    ``` html
    $ jaws -a XYZ.nc
    ```

* `-v, --var, --variable`: Variable you want to analyze.

    Usage:
    ``` html
    $ jaws -a -v temperature ABC.txt
    ```

* `-y, --anl_yr, --analysis_year`: Year you want to select for analysis.

    Usage:
    ``` html
    $ jaws -a -v temperature -y 2012 ABC.txt
    ```

* `-m, --anl_mth, --analysis_month`: Month you want to select for analysis.

    Usage:
    ``` html
    $ jaws -a -v temperature -y 2012 -m 5 ABC.txt
    ```
