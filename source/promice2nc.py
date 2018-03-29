from datetime import datetime

import os
import re
from math import sin, cos, sqrt, atan2, radians

import numpy as np
import pandas as pd
import xarray as xr

import common
from sunposition import sunpos

import warnings

warnings.filterwarnings("ignore")

def get_fillvalue(args):
	if args.fillvalue_float:
		return args.fillvalue_float
	return common.fillvalue_float


def init_dataframe(args, input_file):
	convert_current = 1000
	check_na = -999

	df = common.load_dataframe('promice', input_file, 1, delim_whitespace=True)
	df.index.name = 'time'
	df.replace(check_na, np.nan, inplace=True)
	df.loc[:, ['air_temperature', 'air_temperature_hygroclip', 'surface_temp',
			   'ice_temp_01', 'ice_temp_02', 'ice_temp_03', 'ice_temp_04',
			   'ice_temp_05', 'ice_temp_06', 'ice_temp_07', 'ice_temp_08',
			   'logger_temp']] += common.freezing_point_temp
	df.loc[:, ['air_pressure']] *= common.pascal_per_millibar
	df.loc[:, ['fan_current']] /= convert_current
	df = df.where((pd.notnull(df)), get_fillvalue(args))

	return df


def get_station(args, input_file, stations):
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
	for key, value in aliases.items():
		if key in filename:
			return common.parse_station(args, stations[value])


def get_time_and_sza(args, dataframe, longitude, latitude):
	dtime_1970, tz = common.time_common(args.timezone)

	num_rows = dataframe['year'].size
	time, time_bounds, sza = ([0] * num_rows for _ in range(3))

	for idx in range(num_rows):
		keys = ('year', 'month', 'day', 'hour')
		dtime = datetime(*[dataframe[k][idx] for k in keys])
		dtime = tz.localize(dtime.replace(tzinfo=None))

		time[idx] = (dtime - dtime_1970).total_seconds()
		time_bounds[idx] = (time[idx], time[idx] + common.seconds_in_hour)

		sza[idx] = sunpos(dtime, latitude, longitude, 0)[1]

	return time, time_bounds, sza


def get_ice_velocity(args, dataframe, delta_x, delta_y):
	num_rows = dataframe['year'].size
	R = 6373.0  # Approx radius of earth
	fillvalue = get_fillvalue(args)

	velocity = []
	for idx in range(num_rows - 1):
		if any(i == fillvalue for i in (
				dataframe['latitude_GPS'][idx],
				dataframe['longitude_GPS'][idx],
				dataframe['latitude_GPS'][delta_x],
				dataframe['longitude_GPS'][delta_y])):
			velocity.append(fillvalue)
		else:
			lat1 = radians(dataframe['latitude_GPS'][idx])
			lon1 = radians(dataframe['longitude_GPS'][idx])
			lat2 = radians(dataframe['latitude_GPS'][delta_x])
			lon2 = radians(dataframe['longitude_GPS'][delta_y])

			dlat = lat2 - lat1
			dlon = lon2 - lon1

			a = (sin(dlat / 2) ** 2 +
				 cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2)
			c = 2 * atan2(sqrt(a), sqrt(1 - a))

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
	params = (
		('ice_velocity_GPS_total', 1, 1),
		('ice_velocity_GPS_x', 0, 1),
		('ice_velocity_GPS_y', 1, 0))
	for key, x, y in params:
		dataset[key] = 'time', get_ice_velocity(args, dataframe, x, y)


def convert_coordinates(args, dataframe):
	# Exclude NAs
	fillvalue = get_fillvalue(args)
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
	df = init_dataframe(args, input_file)
	ds = xr.Dataset.from_dataframe(df)
	ds = ds.drop('time')

	common.log(args, 2, 'Retrieving latitude, longitude and station name')
	latitude, longitude, station_name = get_station(args, input_file, stations)

	common.log(args, 3, 'Calculating time and sza')
	time, time_bounds, sza = get_time_and_sza(args, df, longitude, latitude)

	common.log(args, 4, 'Converting lat_GPS and lon_GPS')
	convert_coordinates(args, df)

	common.log(args, 5, 'Calculating ice velocity')
	fill_ice_velocity(args, df, ds)

	ds['time'] = 'time', time
	ds['time_bounds'] = ('time', 'nbnd'), time_bounds
	ds['sza'] = 'time', sza
	ds['station_name'] = tuple(), station_name
	ds['latitude'] = tuple(), latitude
	ds['longitude'] = tuple(), longitude

	comp_level = args.dfl_lvl
	
	common.load_dataset_attributes('promice', ds)
	encoding = common.get_encoding('promice', get_fillvalue(args), comp_level)

	common.write_data(args, ds, output_file, encoding)
