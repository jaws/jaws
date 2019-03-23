import os
import sys
import re
import json
import pandas as pd

import collections
import pytz
from datetime import datetime, timedelta

try:
    from jaws import tilt_angle, fsds_adjust
except ImportError:
    import tilt_angle, fsds_adjust

###############################################################################

freezing_point_temp = 273.15
pascal_per_millibar = 100
seconds_in_hour = 3600
seconds_in_half_hour = 1800
fillvalue_double = 9.969209968386869e+36
fillvalue_float = 9.96921e+36
jaws_version = '0.7.6'

###############################################################################


def log(args, level, message):
    if args.dbg_lvl > level:
        print(message)


def get_fillvalue(args):
    if args.fll_val_flt:
        return args.fll_val_flt
    return fillvalue_float


def relative_path(path):
    """Get relative path based on the location of this file."""
    this_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(this_dir, path)


def read_ordered_json(path):
    path = relative_path(path)
    decoder = json.JSONDecoder(object_pairs_hook=collections.OrderedDict)
    with open(path) as stream:
        return decoder.decode(stream.read())


def load_dataframe(name, input_file, header_rows, **kwargs):

    input_file_vars = [item for sublist in[v for k,v in kwargs.items()] for item in sublist]

    global columns

    if (name == 'gcnet' and header_rows == 54) or (name == 'promice' and len(input_file_vars) == 46) or (
        name == 'aaws' and len(input_file_vars) == 6) or (name == 'imau/ant') or (name == 'imau/grl') or (
        name == 'scar'):

        path = relative_path('resources/{}/columns.txt'.format(name))
        with open(path) as stream:
            columns = stream.read().split('\n')
        columns = [i.strip() for i in columns if i.strip()]

    elif name == 'gcnet':
        path = relative_path('resources/{}/original_columns.json'.format(name))
        org_columns = read_ordered_json(path)
        columns = []

        with open(input_file) as stream:
            stream.readline()
            count = 0
            for line in stream:
                isColumnFoundForThisLine = False
                for column_name, std_name in org_columns.items():
                    if re.search(r'\b' + column_name + r'\b', line):
                        isColumnFoundForThisLine = True
                        columns.append(std_name)

                if not isColumnFoundForThisLine:
                    if '[W m-2]' in line:
                        count += 1
                        if count == 1:
                            columns.append('sw_down_max')
                        elif count == 2:
                            columns.append('sw_up_max')

    elif name == 'promice' or 'aaws':
        path = relative_path('resources/{}/original_columns.json'.format(name))
        org_columns = read_ordered_json(path)
        columns = []
        if name == 'aaws':
            columns.append('timestamp')

        for column_name,std_name in org_columns.items():
            if column_name in input_file_vars:
                columns.append(std_name)

    df = pd.read_csv(
        input_file,
        skiprows=header_rows,
        skip_blank_lines=True,
        header=None,
        names=columns,
        sep=r'\t|\s+|\,',
        engine='python')

    df.index.name = 'time'

    return df, columns


def load_dataset_attributes(name, ds, args, **kwargs):
    global derived_vars, no_drv_tm_vars, rigb_vars
    path = 'resources/{}/ds.json'.format(name)
    attr_dict = read_ordered_json(path)

    ds.attrs = attr_dict.pop('attributes')

    if name == 'scar':
        country = kwargs.pop('country')
        institution = kwargs.pop('institution')

        if country:
            ds.attrs['operated_by'] = country
        if institution:
            ds.attrs['institution'] = institution

    ds.attrs['history'] = '{} {}'.format(datetime.now(), ' '.join(sys.argv))
    ds.attrs['JAWS'] = 'Justified Automated Weather Station software version {} (Homepage = https://github.com/' \
                       'jaws/jaws)'.format(jaws_version)

    derived_vars = ['time', 'time_bounds', 'sza', 'az','station_name', 'latitude', 'longitude',
                    'ice_velocity_GPS_total', 'ice_velocity_GPS_x', 'ice_velocity_GPS_y', 'height']

    no_drv_tm_vars = []

    if not args.no_drv_tm:
        no_drv_tm_vars = ['hour', 'month', 'day', 'day_of_year']

    rigb_vars = []

    if name in ['imau/ant', 'imau/grl', 'gcnet', 'promice']:
        rigb_vars = kwargs.pop('rigb_vars')

    for key, value in attr_dict.items():
        for key1, value1 in value.items():
            if (key1 in columns) or (key1 in derived_vars) or (key1 in no_drv_tm_vars) or (key1 in rigb_vars):
                for key2, value2 in value1.items():
                    if key2 == 'type':
                        pass
                    else:
                        ds[key1].attrs = value2.items()
    for column in columns:
        if column in ('qc1', 'qc9', 'qc17', 'qc25'):
            load_dataset_attributes_gcnet_qltyctrl(name, ds)


def load_dataset_attributes_gcnet_qltyctrl(name, ds):
    path = 'resources/{}/ds_derived.json'.format(name)
    attr_dict = read_ordered_json(path)

    for key, value in attr_dict.items():
        for key1, value1 in value.items():
            for key2, value2 in value1.items():
                if key2 == 'type':
                    pass
                else:
                    try:
                        ds[key1].attrs = value2.items()
                    except KeyError:
                        pass


def get_encoding(name, fillvalue, comp_level, args):
    path = relative_path('resources/{}/encoding.json'.format(name))
    with open(path) as stream:
        data = json.load(stream)

    def recursive_fill(data):
        for k, v in data.items():
            if k == '_FillValue' and v == 'FILL':
                data[k] = fillvalue
            elif k == 'complevel' and v == 'COMP':
                data[k] = comp_level
            elif isinstance(v, dict):
                recursive_fill(v)

    recursive_fill(data)
    masterlist = [columns, derived_vars]
    if not args.no_drv_tm:
        masterlist.append(no_drv_tm_vars)
    if args.rigb:
        masterlist.append(rigb_vars)

    # Get encoding for only those variables present in input file
    masterlist = [item for sublist in masterlist for item in sublist]
    data = {k: data[k] for k in masterlist if k in data.keys()}
    return data


def parse_station(args, station):
    if len(station) == 3:
        latitude, longitude, name = station
    else:
        latitude, longitude = station
        name = None
    if args.stn_nm:
        print('Default station name overrided by user provided station name')
        name = args.stn_nm
    return latitude, longitude, name


def time_common(tzone):
    tz = pytz.timezone(tzone)
    dtime_1970 = datetime(1970, 1, 1)
    dtime_1970 = tz.localize(dtime_1970.replace(tzinfo=None))

    return dtime_1970, tz


def get_month_day(year, day, one_based=False):
    if one_based:  # if Jan 1st is 1 instead of 0
        day -= 1
    dt = datetime(year, 1, 1) + timedelta(days=day)
    return dt.month, dt.day


def get_cleardays_df(station_name, first_date, last_date):
    path_cleardays = relative_path('resources/cleardays.csv')
    clr_df = pd.read_csv(path_cleardays)
    clr_df = clr_df.loc[clr_df['network_name'] == station_name]
    clr_df = clr_df.drop('network_name', 1)
    clr_df = clr_df.loc[(clr_df['date'] >= first_date) & (clr_df['date'] <= last_date)]
    clr_df[['start_hour', 'end_hour']] = clr_df[['start_hour', 'end_hour']].astype(int)

    return clr_df


def call_rigb(args, station_name, first_date, last_date, ds, latitude, longitude, rigb_vars):
    log(args, 6, 'Detecting clear-sky day(s)')
    clr_df = get_cleardays_df(station_name, first_date, last_date)
    if args.dbg_lvl > 6:
        print("Found {} clear-sky day(s)".format(len(clr_df.index)))

    if clr_df.empty:
        if args.dbg_lvl > 6:
            print('Skipping RIGB, since no clear-sky day found')
    else:
        log(args, 7, 'Calculating tilt angle and direction')
        if len(clr_df.index) >= 5:
            print('Tilt correction will take long time')
        ds = tilt_angle.main(ds, latitude, longitude, clr_df, args)

        log(args, 8, 'Calculating corrected_fsds')
        ds = fsds_adjust.main(ds, args)

        rigb_vars = ['tilt_direction', 'tilt_angle', 'fsds_adjusted', 'fsus_adjusted', 'cloud_fraction']

    return ds, rigb_vars


def write_data(args, ds, op_file, encoding):
    if args.format3 == 1:
        ds.to_netcdf(op_file, format='NETCDF3_CLASSIC', unlimited_dims={'time': True}, encoding=encoding)
    elif args.format4 == 1:
        ds.to_netcdf(op_file, format='NETCDF4', unlimited_dims={'time': True}, encoding=encoding)
    elif args.format5 == 1:
        ds.to_netcdf(op_file, format='NETCDF3_64BIT', unlimited_dims={'time': True}, encoding=encoding)
    elif args.format6 == 1:
        ds.to_netcdf(op_file, format='NETCDF3_64BIT', unlimited_dims={'time': True}, encoding=encoding)
    elif args.format7 == 1:
        ds.to_netcdf(op_file, format='NETCDF4_CLASSIC', unlimited_dims={'time': True}, encoding=encoding)
    else:
        ds.to_netcdf(op_file, unlimited_dims={'time': True}, encoding=encoding)
