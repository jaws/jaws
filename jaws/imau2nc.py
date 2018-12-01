from datetime import datetime
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


def get_time_and_sza(args, dataframe, longitude, latitude):
    # Divided by 4 because each hour value is a multiple of 4
    # and then multiplied by 100 to convert decimal to integer
    hour_conversion = 100 / 4
    last_hour = 23
    seconds_in_hour = common.seconds_in_hour
    num_rows = dataframe['year'].size

    month, day, minutes, time, time_bounds, sza, az = ([0] * num_rows for _ in range(7))

    hour = dataframe['day_of_year']
    hour = [round(i - int(i), 3) * hour_conversion for i in hour]
    hour = [int(h) if int(h) <= last_hour else 0 for h in hour]

    dtime_1970, tz = common.time_common(args.tz)

    for idx in range(num_rows):
        time_year = dataframe['year'][idx]
        time_j = int(dataframe['day_of_year'][idx])
        time_hour = hour[idx]

        if time_j <= 366:
            temp_dtime = '{} {} {}'.format(time_year, time_j, time_hour)
            temp_dtime = datetime.strptime(temp_dtime, "%Y %j %H")
            temp_dtime = tz.localize(temp_dtime.replace(tzinfo=None))

            time[idx] = (temp_dtime - dtime_1970).total_seconds()
        else:
            # Assign time of previous row, if day_of_year > 366
            time[idx] = time[idx - 1]

        time_bounds[idx] = (time[idx] - seconds_in_hour, time[idx])

        time[idx] = time[idx] - common.seconds_in_half_hour
        temp_dtime = datetime.utcfromtimestamp(time[idx])

        solar_angles = sunposition.sunpos(temp_dtime, latitude, longitude, 0)
        az[idx] = solar_angles[0]
        sza[idx] = solar_angles[1]

    return month, day, hour, minutes, time, time_bounds, sza, az


def derive_times(dataframe, month, day):
    num_rows = dataframe['year'].size
    for idx in range(num_rows):
        month[idx], day[idx] = common.get_month_day(
            int(dataframe['year'][idx]),
            int(dataframe['day_of_year'][idx]),
            True)


def grl_time(args, dataframe, longitude, latitude):
    seconds_in_15min = 15*60
    # dtime_1970, tz = common.time_common(args.tz)
    num_rows = dataframe['year'].size

    month, day, time, time_bounds, sza, az = ([0] * num_rows for _ in range(6))

    hour = (dataframe['hour_mult_100']/100).astype(int)
    minutes = (((dataframe['hour_mult_100']/100) % 1) * 100).astype(int)
    temp_dtime = pd.to_datetime(dataframe['year']*1000 + dataframe['day_of_year'].astype(int), format='%Y%j')

    dataframe['hour'] = hour
    dataframe['minutes'] = minutes
    dataframe['dtime'] = temp_dtime

    dataframe['dtime'] = pd.to_datetime(dataframe.dtime)
    dataframe['dtime'] += pd.to_timedelta(dataframe.hour, unit='h')
    dataframe['dtime'] += pd.to_timedelta(dataframe.minutes, unit='m')

    time = (dataframe['dtime'] - datetime(1970, 1, 1)) / np.timedelta64(1, 's') - seconds_in_15min
    time_bounds = [(i-seconds_in_15min, i+seconds_in_15min) for i in time]

    month = pd.DatetimeIndex(dataframe['dtime']).month.values
    day = pd.DatetimeIndex(dataframe['dtime']).day.values

    for idx in range(num_rows):
        solar_angles = sunposition.sunpos(dataframe['dtime'][idx], latitude, longitude, 0)
        az[idx] = solar_angles[0]
        sza[idx] = solar_angles[1]

    return month, day, hour, minutes, time, time_bounds, sza, az


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

    if sub_type == 'imau/grl':
        month, day, hour, minutes, time, time_bounds, sza, az = grl_time(
            args, df, longitude, latitude)

    elif sub_type == 'imau/ant':
        common.log(args, 3, 'Calculating time and sza')
        month, day, hour, minutes, time, time_bounds, sza, az = get_time_and_sza(
            args, df, longitude, latitude)

        common.log(args, 5, 'Calculating month and day')
        derive_times(df, month, day)
    
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

    if args.rigb:
        clr_df = clearsky.main(ds, args)
        if not clr_df.empty:
            ds = tilt_angle.main(ds, latitude, longitude, clr_df)

        ds = fsds_adjust.main(ds, args)

    comp_level = args.dfl_lvl

    common.load_dataset_attributes(sub_type, ds, args)
    encoding = common.get_encoding(sub_type, common.get_fillvalue(args), comp_level)

    common.write_data(args, ds, output_file, encoding)
