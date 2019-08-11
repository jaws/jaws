from datetime import datetime
import sys

import numpy as np
import pandas as pd
import xarray as xr

try:
    from jaws import common, sunposition
except ImportError:
    import common, sunposition


def init_dataframe(args, input_file):
    """Initialize dataframe with data from input file; convert temperature and pressure to SI units"""
    header_rows = 4

    df, columns = common.load_dataframe('nsidc', input_file, header_rows)

    # Replace missing values with NaN
    df['wspd'].replace(999, np.nan, inplace=True)
    df['visby'].replace(999999, np.nan, inplace=True)
    df['ta'].replace(9999, np.nan, inplace=True)
    df['dpt'].replace(9999, np.nan, inplace=True)
    df['slp'].replace(99999, np.nan, inplace=True)

    temperature_vars = ['ta', 'dpt']
    if not args.celsius:
        df.loc[:, temperature_vars] += common.freezing_point_temp  # Convert units to Kelvin

    pressure_vars = ['slp']
    # Pressure already in hPa
    # if not args.mb:
    #    df.loc[:, pressure_vars] *= common.pascal_per_millibar  # Convert units to millibar/hPa

    df = df.where((pd.notnull(df)), common.get_fillvalue(args))

    return df, temperature_vars, pressure_vars


def get_station(args, input_file, stations):
    """Get latitude, longitude and name for each station"""
    count = 1
    with open(input_file) as stream:
        for line in stream:
            if count == 1:
                name = int(line.split(',')[0][12:])
                lat = float(line.split(',')[1][6:-1])
                lon = float(line.split(',')[2][5:-1])
            if count == 2:
                elevation = int(line.split(',')[0].split('=')[-1][2:7])
                qlty_ctrl = line.split(',')[-1].split('=')[-1].strip()
                break
            count += 1

    return lat, lon, name, elevation, qlty_ctrl


def get_time_and_sza(args, dataframe, longitude, latitude):
    """Calculate additional time related variables"""
    dtime_1970, tz = common.time_common(args.tz)

    num_rows = dataframe['year'].size
    time, time_bounds, sza, day_of_year = ([0] * num_rows for _ in range(4))

    for idx in range(num_rows):
        keys = ('year', 'month', 'day', 'hour', 'minute')
        dtime = datetime(*[dataframe[k][idx] for k in keys])
        dtime = tz.localize(dtime.replace(tzinfo=None))

        day_of_year[idx] = dtime.timetuple().tm_yday

        time[idx] = (dtime - dtime_1970).total_seconds()
        time_bounds[idx] = (time[idx], time[idx])

        dtime = datetime.utcfromtimestamp(time[idx])

        sza[idx] = sunposition.sunpos(dtime, latitude, longitude, 0)[1]

    return time, time_bounds, sza, day_of_year


def nsidc2nc(args, input_file, output_file, stations):
    """Main function to convert NSIDC txt file to netCDF"""
    df, temperature_vars, pressure_vars = init_dataframe(args, input_file)
    ds = xr.Dataset.from_dataframe(df)
    ds = ds.drop('time')

    common.log(args, 2, 'Retrieving latitude, longitude and station name')
    latitude, longitude, station_name, elevation, qlty_ctrl = get_station(args, input_file, stations)

    common.log(args, 3, 'Calculating time and sza')
    time, time_bounds, sza, day_of_year = get_time_and_sza(args, df, latitude, longitude)

    ds['day_of_year'] = 'time', day_of_year
    ds['time'] = 'time', time
    ds['time_bounds'] = ('time', 'nbnd'), time_bounds
    ds['sza'] = 'time', sza
    ds['station_name'] = tuple(), station_name
    ds['latitude'] = tuple(), latitude
    ds['longitude'] = tuple(), longitude
    ds['elevation'] = tuple(), elevation

    comp_level = args.dfl_lvl

    common.load_dataset_attributes('nsidc', ds, args, temperature_vars=temperature_vars, pressure_vars=pressure_vars,
                                   qlty_ctrl=qlty_ctrl)
    encoding = common.get_encoding('nsidc', common.get_fillvalue(args), comp_level, args)

    common.write_data(args, ds, output_file, encoding)
