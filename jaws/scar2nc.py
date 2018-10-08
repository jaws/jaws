from datetime import datetime

import numpy as np
import pandas as pd
import xarray as xr

try:
    from jaws import common, sunposition
except:
    import common, sunposition


def init_dataframe(args, input_file):

    knot_to_ms = 0.514444
    header_rows = 0
    with open(input_file) as stream:
        for line in stream:
            header_rows += 1
            if len(line.strip()) == 0:
                break

    count = 0
    with open(input_file) as stream:
        for line in stream:
            if count == 0:
                stn_name = line.strip()
            if count == 1:
                country = line[12:].strip()
            if count == 2:
                parts = line.split(' ')
                lat = float(parts[1])
                lon = float(parts[3])
                height = float(parts[5].strip()[:-1])
            if count == 3:
                input_file_vars = [x.split('(')[0].strip() for x in line[16:].split(',')]
            if count == 4:
                check_na = int(line.strip().split(' ')[-1])
            if count == 5:
                institution = line[16:].strip().lstrip('the ')

            count += 1

            if count == 6:
                break

    df, columns = common.load_dataframe('scar', input_file, header_rows, input_file_vars=input_file_vars)
    df.index.name = 'time'
    df.replace(check_na, np.nan, inplace=True)
    df.loc[:, 'air_temp'] += common.freezing_point_temp
    df.loc[:, 'wind_spd'] *= knot_to_ms
    df = df.where((pd.notnull(df)), common.get_fillvalue(args))

    return df, stn_name, lat, lon, height, country, institution


def get_time_and_sza(args, dataframe, longitude, latitude):
    dtime_1970, tz = common.time_common(args.tz)

    num_rows = dataframe['year'].size
    time, time_bounds, sza, day_of_year = ([0] * num_rows for _ in range(4))

    for idx in range(num_rows):
        keys = ('year', 'month', 'day', 'hour', 'minute')
        dtime = datetime(*[dataframe[k][idx] for k in keys])
        dtime = tz.localize(dtime.replace(tzinfo=None))

        time[idx] = (dtime - dtime_1970).total_seconds()
        time_bounds[idx] = (time[idx], time[idx] + common.seconds_in_hour)

        sza[idx] = sunposition.sunpos(dtime, latitude, longitude, 0)[1]

        day_of_year[idx] = dtime.timetuple().tm_yday

    return time, time_bounds, sza, day_of_year


def scar2nc(args, input_file, output_file):
    df, station_name, latitude, longitude, height, country, institution = init_dataframe(args, input_file)
    ds = xr.Dataset.from_dataframe(df)
    ds = ds.drop('time')

    common.log(args, 2, 'Calculating time and sza')
    time, time_bounds, sza, day_of_year = get_time_and_sza(
        args, df, latitude, longitude)

    ds['day_of_year'] = 'time', day_of_year

    ds['time'] = 'time', time
    ds['time_bounds'] = ('time', 'nbnd'), time_bounds
    ds['sza'] = 'time', sza
    ds['station_name'] = tuple(), station_name
    ds['latitude'] = tuple(), latitude
    ds['longitude'] = tuple(), longitude
    ds['height'] = tuple(), height

    comp_level = args.dfl_lvl

    common.load_dataset_attributes('scar', ds, args, country = country, institution = institution)
    encoding = common.get_encoding('scar', common.get_fillvalue(args), comp_level)

    common.write_data(args, ds, output_file, encoding)
