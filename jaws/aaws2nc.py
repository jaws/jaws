from datetime import datetime

import pandas as pd
import xarray as xr

try:
    from jaws import common, sunposition
except ImportError:
    import common, sunposition


def init_dataframe(args, input_file):

    with open(input_file) as stream:
        stream.readline()
        stream.readline()
        for line in stream:
            input_file_vars =[x.strip() for x in line[11:].split(',')]
            break

    header_rows = 0
    with open(input_file) as stream:
        for line in stream:
            if line.startswith('#'):
                header_rows += 1
            else:
                break

    df, columns = common.load_dataframe('aaws', input_file, header_rows, input_file_vars=input_file_vars)
    df.loc[:, 'air_temp'] += common.freezing_point_temp
    df.loc[:, 'pressure'] *= common.pascal_per_millibar
    df = df.where((pd.notnull(df)), common.get_fillvalue(args))

    return df


def get_station(args, input_file, stations):
    with open(input_file) as stream:
        stream.readline()
        name = stream.readline()[12:]
    name = name.strip('\n\r')
    lat, lon, new_name = common.parse_station(args, stations[name])
    return lat, lon, new_name or name


def get_time_and_sza(args, input_file, latitude, longitude, dataframe):
    num_rows = dataframe['timestamp'].size
    year, month, day, hour, day_of_year = ([0] * num_rows for _ in range(5))
    idx = 0

    dtime_1970, tz = common.time_common(args.tz)
    header_rows = 8

    with open(input_file) as stream:
        lines = stream.readlines()[header_rows:]

    time, bounds, sza = [], [], []
    for line in lines:
        dtime = line.strip().split(",")[0]
        dtime = datetime.strptime(dtime, '%Y-%m-%dT%H:%M:%SZ')
        dtime = tz.localize(dtime.replace(tzinfo=None))

        if args.no_drv_tm:
            pass
        else:
            year[idx] = dtime.year
            month[idx] = dtime.month
            day[idx] = dtime.day
            hour[idx] = dtime.hour
            day_of_year[idx] = dtime.timetuple().tm_yday

            idx += 1

        seconds = (dtime - dtime_1970).total_seconds()
        time.append(seconds)
        bounds.append((seconds - common.seconds_in_hour, seconds))

        sza.append(sunposition.sunpos(dtime, latitude, longitude, 0)[1])

    return time, bounds, sza, year, month, day, hour, day_of_year


def aaws2nc(args, input_file, output_file, stations):
    df = init_dataframe(args, input_file)
    ds = xr.Dataset.from_dataframe(df)
    ds = ds.drop('time')

    common.log(args, 2, 'Retrieving latitude, longitude and station name')
    latitude, longitude, station_name = get_station(args, input_file, stations)

    common.log(args, 3, 'Calculating time and sza')
    time, time_bounds, sza = get_time_and_sza(
        args, input_file, latitude, longitude, df)[:3]

    if args.no_drv_tm:
        pass
    else:
        common.log(args, 5, 'Calculating month and day')
        year, month, day, hour, day_of_year = get_time_and_sza(
        args, input_file, latitude, longitude, df)[3:]
        ds['year'] = 'time', year
        ds['month'] = 'time', month
        ds['day'] = 'time', day
        ds['hour'] = 'time', hour
        ds['day_of_year'] = 'time', day_of_year

    ds['time'] = 'time', time
    ds['time_bounds'] = ('time', 'nbnd'), time_bounds
    ds['sza'] = 'time', sza
    ds['station_name'] = tuple(), station_name
    ds['latitude'] = tuple(), latitude
    ds['longitude'] = tuple(), longitude

    comp_level = args.dfl_lvl

    common.load_dataset_attributes('aaws', ds, args)
    encoding = common.get_encoding('aaws', common.get_fillvalue(args), comp_level)

    common.write_data(args, ds, output_file, encoding)
