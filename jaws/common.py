import os
import sys
import json
import pandas as pd

import collections
import pytz
from datetime import datetime, timedelta

###############################################################################

freezing_point_temp = 273.15
pascal_per_millibar = 100
seconds_in_hour = 3600
fillvalue_double = 9.969209968386869e+36
fillvalue_float = 9.96921e+36

###############################################################################

def get_fillvalue(args):
	if args.fll_val_flt:
		return args.fll_val_flt
	return fillvalue_float


def load_dataframe(name, input_file, header_rows, **kwargs):
	path = relative_path('resources/{}/columns.txt'.format(name))
	with open(path) as stream:
		columns = stream.read().split('\n')
	columns = [i.strip() for i in columns if i.strip()]

	return pd.read_csv(
		input_file,
		skiprows=header_rows,
		skip_blank_lines=True,
		header=None,
		names=columns,
		**kwargs)


def get_encoding(name, fillvalue, comp_level):
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
	return data


def load_dataset_attributes(name, ds):
	path = 'resources/{}/ds.json'.format(name)
	attr_dict = read_ordered_json(path)

	ds.attrs = attr_dict.pop('attrs')
	ds.attrs['history'] = '{} {}'.format(datetime.now(), ' '.join(sys.argv))
	ds.attrs['JAWS'] = 'Justified Automatic Weather Station software version 0.4.2 (Homepage = http://github.com/jaws/jaws)'
	for key, value in attr_dict.items():
		ds[key].attrs = value


def read_ordered_json(path):
	path = relative_path(path)
	decoder = json.JSONDecoder(object_pairs_hook=collections.OrderedDict)
	with open(path) as stream:
		return decoder.decode(stream.read())


def log(args, level, message):
	if args.dbg_lvl > level:
		print(message)


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
	dtime_1970 = datetime(1970,1,1)
	dtime_1970 = tz.localize(dtime_1970.replace(tzinfo=None))
	
	return dtime_1970, tz

def get_month_day(year, day, one_based=False):
	if one_based:  # if Jan 1st is 1 instead of 0
		day -= 1
	dt = datetime(year, 1, 1) + timedelta(days=day)
	return dt.month, dt.day


def write_data(args, ds, op_file, encoding):
	if args.format3 == 1:
		ds.to_netcdf(op_file, format = 'NETCDF3_CLASSIC', unlimited_dims={'time':True}, encoding = encoding)
	elif args.format4 == 1:
		ds.to_netcdf(op_file, format = 'NETCDF4', unlimited_dims={'time':True}, encoding = encoding)
	elif args.format5 == 1:
		ds.to_netcdf(op_file, format = 'NETCDF3_64BIT', unlimited_dims={'time':True}, encoding = encoding)
	elif args.format6 == 1:
		ds.to_netcdf(op_file, format = 'NETCDF3_64BIT', unlimited_dims={'time':True}, encoding = encoding)
	elif args.format7 == 1:
		ds.to_netcdf(op_file, format = 'NETCDF4_CLASSIC', unlimited_dims={'time':True}, encoding = encoding)
	else:
		ds.to_netcdf(op_file, unlimited_dims={'time':True}, encoding = encoding)

def relative_path(path):
	"""Get relative path based on the location of this file."""
	this_dir = os.path.dirname(os.path.realpath(__file__))
	return os.path.join(this_dir, path)