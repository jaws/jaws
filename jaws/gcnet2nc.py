from datetime import datetime

import numpy as np
import pandas as pd
import xarray as xr

try:
    from jaws import common, sunposition, clearsky, tilt_angle
except ImportError:
    import common, sunposition, clearsky, tilt_angle


def init_dataframe(args, input_file):
    check_na = 999.0

    global header_rows
    header_rows = 0
    with open(input_file) as stream:
        for line in stream:
            header_rows += 1
            if len(line.strip()) == 0 :
                break

    df, columns = common.load_dataframe('gcnet', input_file, header_rows)

    # Convert only if this column is present in input file
    try:
        df['qc25'] = df['qc25'].astype(str)  # To avoid 999 values marked as N/A
    except Exception:
        pass

    df.replace(check_na, np.nan, inplace=True)

    temperature_keys = [
        'temperature_tc_1', 'temperature_tc_2', 'temperature_cs500_1',
        'temperature_cs500_2', 't_snow_01', 't_snow_02', 't_snow_03',
        't_snow_04', 't_snow_05', 't_snow_06', 't_snow_07', 't_snow_08',
        't_snow_09', 't_snow_10', 'max_air_temperature_1',
        'max_air_temperature_2', 'min_air_temperature_1',
        'min_air_temperature_2', 'ref_temperature']
    df.loc[:, temperature_keys] += common.freezing_point_temp
    df.loc[:, 'atmos_pressure'] *= common.pascal_per_millibar
    df = df.where((pd.notnull(df)), common.get_fillvalue(args))

    try:
        df['qc25'] = df['qc25'].astype(int)  # Convert it back to int
    except Exception:
        pass

    return df


def get_station(args, input_file, stations):
    df, columns = common.load_dataframe('gcnet', input_file, header_rows)
    station_number = df['station_number'][0]

    if 30 <= station_number <= 32:
        name = 'gcnet_lar{}'.format(station_number - 29)
        station = stations[name]
    else:
        station = list(stations.values())[station_number]

    return common.parse_station(args, station)


def fill_dataset_quality_control(dataframe, dataset, input_file):
    temp_df, columns = common.load_dataframe('gcnet', input_file, header_rows)

    keys = common.read_ordered_json('resources/gcnet/quality_control.json')
    for key, attributes in keys.items():
        # Check if qc variables are present in input file
        if key in columns:
            values = [list(map(int, i)) for i in zip(*map(str, dataframe[key]))]
            for attr, value in zip(attributes, values):
                dataset[attr] = 'time', value


def get_time_and_sza(args, dataframe, longitude, latitude):
    # Divided by 4 because each hour value is a multiple of 4
    # and then multiplied by 100 to convert decimal to integer
    hour_conversion = 100 / 4
    last_hour = 23
    seconds_in_hour = common.seconds_in_hour
    num_rows = dataframe['year'].size

    month, day, time, time_bounds, sza = ([0] * num_rows for _ in range(5))

    hour = dataframe['julian_decimal_time']
    hour = [round(i - int(i), 3) * hour_conversion for i in hour]
    hour = [int(h) if int(h) <= last_hour else 0 for h in hour]

    dtime_1970, tz = common.time_common(args.tz)

    for idx in range(num_rows):
        time_year = dataframe['year'][idx]
        time_j = int(dataframe['julian_decimal_time'][idx])
        time_hour = hour[idx]

        if time_j <= 366:
            temp_dtime = '{} {} {}'.format(time_year, time_j, time_hour)
            temp_dtime = datetime.strptime(temp_dtime, "%Y %j %H")
            temp_dtime = tz.localize(temp_dtime.replace(tzinfo=None))

            time[idx] = (temp_dtime - dtime_1970).total_seconds()
        else:
            # Assign time of previous row, if julian_decimal_time > 366
            time[idx] = time[idx - 1]

        time_bounds[idx] = (time[idx] - seconds_in_hour, time[idx])

        time[idx] = time[idx] - common.seconds_in_half_hour
        temp_dtime = datetime.utcfromtimestamp(time[idx])

        sza[idx] = sunposition.sunpos(temp_dtime, latitude, longitude, 0)[1]

    return hour, month, day, time, time_bounds, sza


def derive_times(dataframe, month, day):
    num_rows = dataframe['year'].size
    for idx in range(num_rows):
        month[idx], day[idx] = common.get_month_day(
            int(dataframe['year'][idx]),
            int(dataframe['julian_decimal_time'][idx]),
            True)


def extrapolate_temp(dataframe):
    ht1 = dataframe['wind_sensor_height_1']
    ht2 = dataframe['wind_sensor_height_2']
    temp_ht1 = dataframe['temperature_tc_1']
    temp_ht2 = dataframe['temperature_tc_2']

    surface_temp = temp_ht1 - (((temp_ht2 - temp_ht1)/(ht2 - ht1))*ht1)
    return surface_temp


def gcnet2nc(args, input_file, output_file, stations):
    df = init_dataframe(args, input_file)
    station_number = df['station_number'][0]
    df.drop('station_number', axis=1, inplace=True)

    ds = xr.Dataset.from_dataframe(df)
    ds = ds.drop('time')

    surface_temp = extrapolate_temp(df)

    common.log(args, 2, 'Retrieving latitude, longitude and station name')
    latitude, longitude, station_name = get_station(args, input_file, stations)

    common.log(args, 3, 'Calculating time and sza')
    hour, month, day, time, time_bounds, sza = get_time_and_sza(
        args, df, longitude, latitude)

    common.log(args, 4, 'Calculating quality control variables')
    fill_dataset_quality_control(df, ds, input_file)

    if args.no_drv_tm:
        pass
    else:
        common.log(args, 5, 'Calculating month and day')
        derive_times(df, month, day)
        ds['hour'] = 'time', hour
        ds['month'] = 'time', month
        ds['day'] = 'time', day

    ds['time'] = 'time', time
    ds['time_bounds'] = ('time', 'nbnd'), time_bounds
    ds['sza'] = 'time', sza
    ds['station_number'] = tuple(), station_number
    ds['station_name'] = tuple(), station_name
    ds['latitude'] = tuple(), latitude
    ds['longitude'] = tuple(), longitude
    ds['surface_temp'] = 'time', surface_temp

    if args.rigb:
        clr_df = clearsky.main(ds)
        if not clr_df.empty:
            ds = tilt_angle.main(ds, latitude, longitude, clr_df)

    comp_level = args.dfl_lvl

    common.load_dataset_attributes('gcnet', ds, args)
    encoding = common.get_encoding('gcnet', common.get_fillvalue(args), comp_level)

    common.write_data(args, ds, output_file, encoding)
