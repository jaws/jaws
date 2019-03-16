import os

import numpy as np
import pandas as pd
import xarray as xr

try:
    from jaws import common, sunposition, clearsky, tilt_angle, fsds_adjust
except ImportError:
    import common, sunposition, clearsky, tilt_angle, fsds_adjust


def init_dataframe(args, input_file, sub_type):
    check_na = -9999

    df, columns = common.load_dataframe(sub_type, input_file, 0)
    df.replace(check_na, np.nan, inplace=True)

    if sub_type == 'imau/ant':
        temperature_keys = ['temp_cnr1', 'air_temp',
                            'snow_temp_1a', 'snow_temp_2a', 'snow_temp_3a', 'snow_temp_4a', 'snow_temp_5a',
                            'snow_temp_1b', 'snow_temp_2b', 'snow_temp_3b', 'snow_temp_4b', 'snow_temp_5b',
                            'temp_logger']

    elif sub_type == 'imau/grl':
        temperature_keys = ['temp_cnr1', 'air_temp2', 'air_temp6',
                            'snow_temp_1', 'snow_temp_2', 'snow_temp_3', 'snow_temp_4', 'snow_temp_5',
                            'datalogger']

    df.loc[:, temperature_keys] += common.freezing_point_temp
    df.loc[:, 'air_pressure'] *= common.pascal_per_millibar
    df = df.where((pd.notnull(df)), common.get_fillvalue(args))

    return df


def get_station(args, input_file, stations):
    filename = os.path.basename(input_file)
    name = filename[:9]
    lat, lon, new_name = common.parse_station(args, stations[name])
    return lat, lon, new_name


def get_time_and_sza(args, dataframe, longitude, latitude, sub_type):
    seconds_in_30min = 30*60
    seconds_in_15min = 15*60
    dtime_1970, tz = common.time_common(args.tz)
    num_rows = dataframe['year'].size

    month, day, minutes, time, time_bounds, sza, az = ([0] * num_rows for _ in range(7))

    hour = (dataframe['hour_mult_100']/100).astype(int)
    temp_dtime = pd.to_datetime(dataframe['year']*1000 + dataframe['day_of_year'].astype(int), format='%Y%j')

    dataframe['hour'] = hour
    dataframe['dtime'] = temp_dtime

    dataframe['dtime'] = pd.to_datetime(dataframe.dtime)
    dataframe['dtime'] = [tz.localize(i.replace(tzinfo=None)) for i in dataframe['dtime']]
    dataframe['dtime'] += pd.to_timedelta(dataframe.hour, unit='h')

    if sub_type == 'imau/ant':
        time = (dataframe['dtime'] - dtime_1970) / np.timedelta64(1, 's') - seconds_in_30min
        time_bounds = [(i-seconds_in_30min, i+seconds_in_30min) for i in time]
    elif sub_type == 'imau/grl':
        minutes = (((dataframe['hour_mult_100']/100) % 1) * 100).astype(int)
        dataframe['minutes'] = minutes
        dataframe['dtime'] += pd.to_timedelta(dataframe.minutes, unit='m')

        time = (dataframe['dtime'] - dtime_1970) / np.timedelta64(1, 's') - seconds_in_15min
        time_bounds = [(i-seconds_in_15min, i+seconds_in_15min) for i in time]

    month = pd.DatetimeIndex(dataframe['dtime']).month.values
    day = pd.DatetimeIndex(dataframe['dtime']).day.values
    dates = list(pd.DatetimeIndex(dataframe['dtime']).date)
    dates = [int(d.strftime("%Y%m%d")) for d in dates]
    first_date = min(dates)
    last_date = max(dates)

    for idx in range(num_rows):
        solar_angles = sunposition.sunpos(dataframe['dtime'][idx], latitude, longitude, 0)
        az[idx] = solar_angles[0]
        sza[idx] = solar_angles[1]

    return month, day, hour, minutes, time, time_bounds, sza, az, first_date, last_date


def imau2nc(args, input_file, output_file, stations):
    with open(input_file) as stream:
        line = stream.readline()
        var_count = len(line.split(','))

    errmsg = 'Unknown sub-type of IMAU network. Antarctic stations have 31 columns while Greenland stations have 35. ' \
             'Your dataset has {} columns.'.format(var_count)
    if var_count == 31:
        sub_type = 'imau/ant'
    elif var_count == 35:
        sub_type = 'imau/grl'
    else:
        raise RuntimeError(errmsg)

    df = init_dataframe(args, input_file, sub_type)
    ds = xr.Dataset.from_dataframe(df)
    ds = ds.drop('time')

    common.log(args, 2, 'Retrieving latitude, longitude and station name')
    latitude, longitude, station_name = get_station(args, input_file, stations)

    common.log(args, 3, 'Calculating time and sza')
    month, day, hour, minutes, time, time_bounds, sza, az, first_date, last_date = get_time_and_sza(
        args, df, longitude, latitude, sub_type)

    ds['month'] = 'time', month
    ds['day'] = 'time', day
    ds['hour'] = 'time', hour
    ds['minutes'] = 'time', minutes
    ds['time'] = 'time', time
    ds['time_bounds'] = ('time', 'nbnd'), time_bounds
    ds['sza'] = 'time', sza
    ds['az'] = 'time', az
    ds['station_name'] = tuple(), station_name
    ds['latitude'] = tuple(), latitude
    ds['longitude'] = tuple(), longitude

    rigb_vars = []
    if args.rigb:
        ds, rigb_vars = common.call_rigb(
            args, station_name, first_date, last_date, ds, latitude, longitude, rigb_vars)

    comp_level = args.dfl_lvl

    common.load_dataset_attributes(sub_type, ds, args, rigb_vars=rigb_vars)
    encoding = common.get_encoding(sub_type, common.get_fillvalue(args), comp_level, args)

    common.write_data(args, ds, output_file, encoding)
