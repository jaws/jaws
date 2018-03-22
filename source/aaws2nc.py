from datetime import datetime

import pandas as pd
import xarray as xr

import common
from sunposition import sunpos


def get_fillvalue(args):
	if args.fillvalue_float:
		return args.fillvalue_float
	return common.fillvalue_float


def init_dataframe(args, input_file):
	df = common.load_dataframe('aaws', input_file, 8)
	df.index.name = 'time'
	df.loc[:, 'air_temp'] += common.freezing_point_temp
	df.loc[:, 'pressure'] *= common.pascal_per_millibar
	df = df.where((pd.notnull(df)), get_fillvalue(args))

	return df


def get_station(args, input_file, stations):
	with open(input_file) as stream:
		stream.readline()
		name = stream.readline()[12:]
	name = name.strip('\n\r')
	lat, lon, new_name = common.parse_station(args, stations[name])
	return lat, lon, new_name or name


def get_time_and_sza(args, input_file, latitude, longitude):
	dtime_1970, tz = common.time_common(args.timezone)
	header_rows = 8

	with open(input_file) as stream:
		lines = stream.readlines()[header_rows:]

	time, bounds, sza = [], [], []
	for line in lines:
		dtime = line.strip().split(",")[0]
		dtime = datetime.strptime(dtime, '%Y-%m-%dT%H:%M:%SZ')
		dtime = tz.localize(dtime.replace(tzinfo=None))

		seconds = (dtime - dtime_1970).total_seconds()
		time.append(seconds)
		bounds.append((seconds - common.seconds_in_hour, seconds))

		sza.append(sunpos(dtime, latitude, longitude, 0)[1])

	return time, bounds, sza


def aaws2nc(args, input_file, output_file, stations):
	df = init_dataframe(args, input_file)
	ds = xr.Dataset.from_dataframe(df)
	ds = ds.drop('time')

	common.log(args, 2, 'Retrieving latitude, longitude and station name')
	latitude, longitude, station_name = get_station(args, input_file, stations)

	common.log(args, 3, 'Calculating time and sza')
	time, time_bounds, sza = get_time_and_sza(
		args, input_file, latitude, longitude)

	ds['time'] = 'time', time
	ds['time_bounds'] = ('time', 'nbnd'), time_bounds
	ds['sza'] = 'time', sza
	ds['station_name'] = tuple(), station_name
	ds['latitude'] = tuple(), latitude
	ds['longitude'] = tuple(), longitude

	common.load_dataset_attributes('aaws', ds)
	encoding = common.get_encoding('aaws', get_fillvalue(args))

	common.write_data(args, ds, output_file, encoding)
