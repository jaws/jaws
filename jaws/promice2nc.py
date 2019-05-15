from datetime import datetime
import os
import re
import sys
import warnings

import numpy as np
import pandas as pd
import xarray as xr

try:
    from jaws import common, sunposition, clearsky, tilt_angle, fsds_adjust
except ImportError:
    import common, sunposition, clearsky, tilt_angle, fsds_adjust

warnings.filterwarnings("ignore")


def init_dataframe(args, input_file):
    """Initialize dataframe with data from input file; convert current, temperature and pressure to SI units"""
    convert_current = 1000
    check_na = -999

    with open(input_file) as stream:
        for line in stream:
            input_file_vars =[x.strip() for x in line.split(' ') if x]
            break

    df, columns = common.load_dataframe('promice', input_file, 1, input_file_vars=input_file_vars)
    df.replace(check_na, np.nan, inplace=True)

    temperature_vars = ['ta', 'ta_hygroclip', 'ts',
               'tice1', 'tice2', 'tice3', 'tice4',
               'tice5', 'tice6', 'tice7', 'tice8',
               'temp_logger']
    if not args.celsius:
        df.loc[:, temperature_vars] += common.freezing_point_temp  # Convert units to Kelvin

    pressure_vars = ['pa']
    if not args.mb:
        df.loc[:, pressure_vars] *= common.pascal_per_millibar  # Convert units to millibar/hPa

    df.loc[:, ['fan_current']] /= convert_current  # Convert units to Ampere

    df = df.where((pd.notnull(df)), common.get_fillvalue(args))

    return df, temperature_vars, pressure_vars


def get_station(args, input_file, stations):
    """Get latitude, longitude and name for each station"""
    path = 'resources/promice/aliases.txt'
    aliases = {}
    with open(common.relative_path(path)) as stream:
        for line in stream.readlines():
            if not line.strip():
                continue
            bits = re.split('[,:]', line)
            bits = [i.strip() for i in bits if i.strip()]
            for b in bits[:-1]:
                aliases[b] = bits[-1]

    filename = os.path.basename(input_file)
    count = 0
    for key, value in aliases.items():
        if key in filename:
            count += 1
            return common.parse_station(args, stations[value])

    if count == 0:
        print("ERROR: Please check input file name. It should include station name e.g. KAN-B. Note that there is "
              "'-' between KAN and B not '_'. This condition is only for PROMICE stations.")
        sys.exit(1)


def get_time_and_sza(args, dataframe, longitude, latitude):
    """Calculate additional time related variables"""
    dtime_1970, tz = common.time_common(args.tz)

    num_rows = dataframe['year'].size
    time, time_bounds, sza, az = ([0] * num_rows for _ in range(4))
    dates = []

    for idx in range(num_rows):
        keys = ('year', 'month', 'day', 'hour')
        dtime = datetime(*[dataframe[k][idx] for k in keys])
        dtime = tz.localize(dtime.replace(tzinfo=None))

        time[idx] = (dtime - dtime_1970).total_seconds()
        time_bounds[idx] = (time[idx], time[idx] + common.seconds_in_hour)

        # Each timestamp is average of current and next hour values i.e. value at hour=5 is average of hour=5 and hour=6
        # Our 'time' variable will represent values at half-hour i.e. 5.5 in above case, so add 30 minutes to all.
        time[idx] = time[idx] + common.seconds_in_half_hour
        dtime = datetime.utcfromtimestamp(time[idx])
        dates.append(int(dtime.date().strftime("%Y%m%d")))

        solar_angles = sunposition.sunpos(dtime, latitude, longitude, 0)
        az[idx] = solar_angles[0]
        sza[idx] = solar_angles[1]

    first_date = min(dates)
    last_date = max(dates)
    return time, time_bounds, sza, az, first_date, last_date


def get_ice_velocity(args, dataframe, delta_x, delta_y):
    """Calculate GPS-derived ice velocity using Haversine formula"""
    num_rows = dataframe['year'].size
    R = 6373.0  # Approx radius of earth
    fillvalue = common.get_fillvalue(args)

    velocity = []
    for idx in range(num_rows - 1):
        if any(i == fillvalue for i in (
                dataframe['latitude_GPS'][idx],
                dataframe['longitude_GPS'][idx],
                dataframe['latitude_GPS'][delta_x],
                dataframe['longitude_GPS'][delta_y])):
            velocity.append(fillvalue)
        else:
            lat1 = np.radians(dataframe['latitude_GPS'][idx])
            lon1 = np.radians(dataframe['longitude_GPS'][idx])
            lat2 = np.radians(dataframe['latitude_GPS'][delta_x])
            lon2 = np.radians(dataframe['longitude_GPS'][delta_y])

            dlat = lat2 - lat1
            dlon = lon2 - lon1

            a = (np.sin(dlat / 2) ** 2 +
                 np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2)
            c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

            # Multiplied by 1000 to convert km to meters
            distance = (R * c) * 1000
            # Divided by 3600 because time change
            # between 2 records is one hour
            velocity.append(round(distance / common.seconds_in_hour, 4))

        delta_x += 1
        delta_y += 1

    velocity.append(0)
    return velocity


def fill_ice_velocity(args, dataframe, dataset):
    """Calculate total ice velocity and its x, y components"""
    params = (
        ('ice_velocity_GPS_total', 1, 1),
        ('ice_velocity_GPS_x', 0, 1),
        ('ice_velocity_GPS_y', 1, 0))
    for key, x, y in params:
        dataset[key] = 'time', get_ice_velocity(args, dataframe, x, y)


def convert_coordinates(args, dataframe):
    """Convert latitude_GPS and longitude_GPS units from ddmm to degrees"""
    fillvalue = common.get_fillvalue(args)
    # Exclude NAs
    df1 = dataframe[dataframe.latitude_GPS != fillvalue]
    df2 = dataframe[dataframe.longitude_GPS != fillvalue]

    def lat_lon_gps(coords):
        deg = np.floor(coords / 100)
        minutes = np.floor(((coords / 100) - deg) * 100)
        seconds = (((coords / 100) - deg) * 100 - minutes) * 100
        return deg + minutes / 60 + seconds / 3600

    dataframe.latitude_GPS = lat_lon_gps(df1.latitude_GPS)
    dataframe.longitude_GPS = lat_lon_gps(df2.longitude_GPS)


def promice2nc(args, input_file, output_file, stations):
    """Main function to convert PROMICE txt file to netCDF"""
    df, temperature_vars, pressure_vars = init_dataframe(args, input_file)
    ds = xr.Dataset.from_dataframe(df)
    ds = ds.drop('time')

    common.log(args, 2, 'Retrieving latitude, longitude and station name')
    latitude, longitude, station_name = get_station(args, input_file, stations)

    common.log(args, 3, 'Calculating time and sza')
    time, time_bounds, sza, az, first_date, last_date = get_time_and_sza(args, df, longitude, latitude)

    common.log(args, 4, 'Converting lat_GPS and lon_GPS')
    convert_coordinates(args, df)

    common.log(args, 5, 'Calculating ice velocity')
    fill_ice_velocity(args, df, ds)

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

    common.load_dataset_attributes('promice', ds, args, rigb_vars=rigb_vars, temperature_vars=temperature_vars,
                                   pressure_vars=pressure_vars)
    encoding = common.get_encoding('promice', common.get_fillvalue(args), comp_level, args)

    common.write_data(args, ds, output_file, encoding)
