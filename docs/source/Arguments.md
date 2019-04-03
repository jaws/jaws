# Arguments

## Positional Arguments

* `input`: Path to raw L2 data file for converting to netCDF (or use -i option)

* `output`: Path to save output netCDF file (or use -o option)

Note: `input` is first positional argument and it is required, 
whereas `output` is second (or last) positional argument and it is optional. 
See examples below to understand more about it.

**Case 1**: User provides only input (e.g. *'ABC.txt'*), then the command would be
``` html
$ jaws ABC.txt
```

This will convert *'ABC.txt'* to netCDF format with same name as input file i.e. *'ABC.nc'*.

**Case 2**: User provides both input (e.g. *'ABC.txt'*) and output file name (e.g. *'XYZ.nc'*), then the command would be
``` html
$ jaws ABC.txt XYZ.nc
```

This will convert *'ABC.txt'* to *'XYZ.nc'*.

## Optional Arguments

* `-i, --fl_in, --input`: Path to raw L2 data file for converting to netCDF (or use first positional argument)

* `-o, --fl_out, --output`: Path to save output netCDF file (or use last positional argument)

* `-3, --format3, --3, --fl_fmt=classic`: Output file in netCDF3 CLASSIC (32-bit offset) storage format

* `-4, --format4, --4, --netcdf4`: Output file in netCDF4 (HDF5) storage format. This is default.

* `-5, --format5, --5, --fl_fmt=64bit_data`: Output file in netCDF3 64-bit data (i.e., CDF5, PnetCDF) storage format

* `-6, --format6, --6, --64`: Output file in netCDF3 64-bit offset storage format

* `-7, --format7, --7, --fl_fmt=netcdf4_classic`: Output file in netCDF4 CLASSIC format (3+4=7)

* `--rigb`: Calculate adjusted downwelling shortwave flux, tilt_angle and tilt_direction. This option is only for stations that archive radiometric data.

* `-s, --stn_nm, --station_name`: Override default station name

* `-t, --tz, --timezone`: Change the timezone, default is UTC. A list of all the timezones can be found [here](https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568).

* `-f, --fll_val_flt, --fillvalue_float`: Override default float _FillValue

* `-r, --vrs, --version, --revision`: JAWS current version and last modified date

* `-L, --dfl_lvl, --dfl, --deflate`: Lempel-Ziv deflation/compression (lvl=0..9) for netCDF4 output

* `-a, --anl, --analysis`: plot type e.g.- diurnal, monthly, annual, seasonal

* `-v, --var, --variable`: variable you want to analyse 

* `-y, --anl_yr, --analysis_year`: Year you want to select for analysis

* `-m, --anl_mth, --analysis_month`: Month you want to select for analysis

* `--no_drv_tm, --no_derive_times`: By default extra variables ('month', 'day' and 'hour') are derived for further analysis. Select this flag to not derive them

* `-D, --dbg_lvl, --debug_level`: Debug-level ranging from 1 to 9. It is used to print what steps are occurring during conversion. It is used as following:
``` html
$ jaws -D 5 ABC.txt
```
