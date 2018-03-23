import pandas as pd
import numpy as np
import xarray as xr
import os
from datetime import datetime
import pytz
from sunposition import sunpos
from math import sin, cos, sqrt, atan2, radians
from common import write_data, time_common
import common
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


def promice2nc(args, op_file, station_dict, station_name):

	freezing_point_temp = common.freezing_point_temp
	pascal_per_millibar = common.pascal_per_millibar
	seconds_in_hour = common.seconds_in_hour
	
	if args.fillvalue_float:
		fillvalue_float = args.fillvalue_float
	else:
		fillvalue_float = common.fillvalue_float
	
	header_rows = 1
	convert_current = 1000
	check_na = -999

	column_names = ['year', 'month', 'day', 'hour', 'day_of_year', 'day_of_century', 'air_pressure', 'air_temperature', 'air_temperature_hygroclip', 'relative_humidity_wrtwater', 'relative_humidity', 'wind_speed', 'wind_direction', 
	'shortwave_radiation_down', 'shortwave_radiation_down_cor', 'shortwave_radiation_up', 'shortwave_radiation_up_cor', 'albedo_theta', 'longwave_radiation_down', 'longwave_radiation_up', 'cloudcover', 'surface_temp', 'height_sensor_boom', 
	'height_stakes', 'depth_pressure_transducer', 'depth_pressure_transducer_cor', 'ice_temp_01', 'ice_temp_02', 'ice_temp_03', 'ice_temp_04', 'ice_temp_05', 'ice_temp_06', 'ice_temp_07', 'ice_temp_08', 'tilt_east', 'tilt_north', 
	'time_GPS', 'latitude_GPS', 'longitude_GPS', 'elevation', 'hor_dil_prec', 'logger_temp', 'fan_current', 'battery_voltage']

	df = pd.read_csv(args.input_file or args.fl_in, delim_whitespace=True, skiprows=header_rows, skip_blank_lines=True, header=None, names = column_names)
	df.index.name = 'time'
	df.replace(check_na, np.nan, inplace=True)
	df.loc[:,['air_temperature','air_temperature_hygroclip','surface_temp','ice_temp_01','ice_temp_02','ice_temp_03','ice_temp_04','ice_temp_05','ice_temp_06','ice_temp_07','ice_temp_08','logger_temp']] += freezing_point_temp
	df.loc[:,['air_pressure']] *= pascal_per_millibar
	df.loc[:,['fan_current']] /= convert_current
	df =  df.where((pd.notnull(df)), fillvalue_float)

	ds = xr.Dataset.from_dataframe(df)
	ds = ds.drop('time')
	
	
	# Intializing variables
	num_rows =  df['year'].size
	time, time_bounds, sza, velocity, ice_velocity_GPS_total, ice_velocity_GPS_x, ice_velocity_GPS_y = ([0]*num_rows for x in range(7))

	
	if args.dbg_lvl > 2:
		print('Retrieving latitude, longitude and station name')

	promice_dict = dict.fromkeys(['EGP'], 'promice_egp')
	promice_dict.update(dict.fromkeys(['KAN-B', 'Kangerlussuaq-B'], 'promice_kanb'))
	promice_dict.update(dict.fromkeys(['KAN-L', 'Kangerlussuaq-L'], 'promice_kanl'))
	promice_dict.update(dict.fromkeys(['KAN-M', 'Kangerlussuaq-M'], 'promice_kanm'))
	promice_dict.update(dict.fromkeys(['KAN-U', 'Kangerlussuaq-U'], 'promice_kanu'))
	promice_dict.update(dict.fromkeys(['KPC-L', 'KronprinsChristianland-L'], 'promice_kpcl'))
	promice_dict.update(dict.fromkeys(['KPC-U', 'KronprinsChristianland-U'], 'promice_kpcu'))
	promice_dict.update(dict.fromkeys(['MIT'], 'promice_mit'))
	promice_dict.update(dict.fromkeys(['NUK-K', 'Nuuk-K'], 'promice_nukk'))
	promice_dict.update(dict.fromkeys(['NUK-L', 'Nuuk-L'], 'promice_nukl'))
	promice_dict.update(dict.fromkeys(['NUK-N', 'Nuuk-N'], 'promice_nukn'))
	promice_dict.update(dict.fromkeys(['NUK-U', 'Nuuk-U'], 'promice_nuku'))
	promice_dict.update(dict.fromkeys(['QAS-A', 'Qassimiut-A'], 'promice_qasa'))
	promice_dict.update(dict.fromkeys(['QAS-L', 'Qassimiut-L'], 'promice_qasl'))
	promice_dict.update(dict.fromkeys(['QAS-M', 'Qassimiut-M'], 'promice_qasm'))
	promice_dict.update(dict.fromkeys(['QAS-U', 'Qassimiut-U'], 'promice_qasu'))
	promice_dict.update(dict.fromkeys(['SCO-L', 'Scoresbysund-L'], 'promice_scol'))
	promice_dict.update(dict.fromkeys(['SCO-U', 'Scoresbysund-U'], 'promice_scou'))
	promice_dict.update(dict.fromkeys(['TAS-A', 'Tasiilaq-A'], 'promice_tasa'))
	promice_dict.update(dict.fromkeys(['TAS-L', 'Tasiilaq-L'], 'promice_tasl'))
	promice_dict.update(dict.fromkeys(['TAS-U', 'Tasiilaq-U'], 'promice_tasu'))
	promice_dict.update(dict.fromkeys(['THU-L', 'ThuleAirbase-L'], 'promice_thul'))
	promice_dict.update(dict.fromkeys(['THU-U', 'ThuleAirbase-U'], 'promice_thuu'))
	promice_dict.update(dict.fromkeys(['UPE-L', 'Upernavik-L'], 'promice_upel'))
	promice_dict.update(dict.fromkeys(['UPE-U', 'Upernavik-U'], 'promice_upeu'))
	promice_dict.update(dict.fromkeys(['CEN'], 'promice_cen'))

	k = os.path.basename(args.input_file or args.fl_in).split('_')[1]
	k = os.path.splitext(k)[0]
	temp_stn = promice_dict[k]
	
	latitude = (station_dict.get(temp_stn)[0])
	longitude = (station_dict.get(temp_stn)[1])

	if args.station_name:
		print('Default station name overrided by user provided station name')
	else:
		station_name = station_dict.get(temp_stn)[2]


	if args.dbg_lvl > 3:
		print('Calculating time and sza')
	
	dtime_1970, tz = time_common(args.timezone)
	i = 0

	while i < num_rows:
		
		temp_dtime = datetime(df['year'][i], df['month'][i], df['day'][i], df['hour'][i])
		temp_dtime = tz.localize(temp_dtime.replace(tzinfo=None))		
		time[i] = (temp_dtime-dtime_1970).total_seconds()
		
		time_bounds[i] = (time[i], time[i]+seconds_in_hour)

		sza[i] = sunpos(temp_dtime,latitude,longitude,0)[1]

		i += 1

	
	if args.dbg_lvl > 4:
		print('Converting lat_GPS and lon_GPS')
	
	def lat_lon_gps(coords):
		deg = np.floor(coords / 100)
		minutes = np.floor(((coords / 100) - deg) * 100)
		seconds = (((coords / 100) - deg) * 100 - minutes) * 100
		return deg + minutes / 60 + seconds / 3600

	# Exclude NAs
	logic1 = df.latitude_GPS != fillvalue_float
	logic2 = df.longitude_GPS != fillvalue_float
	df1 = df[logic1]
	df2 = df[logic2]

	df.latitude_GPS = lat_lon_gps(df1.latitude_GPS)
	df.longitude_GPS = lat_lon_gps(df2.longitude_GPS)
	

	if args.dbg_lvl > 5:
		print('Calculating ice velocity')

	def ice_velocity(n,o):
		m,p = 0,1
		R = 6373.0		#Approx radius of earth
		while p < num_rows:
			if (df['latitude_GPS'][m] == fillvalue_float or df['longitude_GPS'][m] == fillvalue_float or df['latitude_GPS'][n] == fillvalue_float or df['longitude_GPS'][o] == fillvalue_float):
				velocity[m] = fillvalue_float
			else:
				lat1 = radians(df['latitude_GPS'][m])
				lon1 = radians(df['longitude_GPS'][m])
				lat2 = radians(df['latitude_GPS'][n])
				lon2 = radians(df['longitude_GPS'][o])

				dlat = lat2 - lat1
				dlon = lon2 - lon1

				a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
				c = 2 * atan2(sqrt(a), sqrt(1 - a))

				distance = (R*c)*1000		#Multiplied by 1000 to convert km to meters

				velocity[m] = round(distance/seconds_in_hour, 4)		#Divided by 3600 because time change between 2 records is one hour

			m += 1
			n += 1
			o += 1
			p += 1

		return velocity[:]

	
	ice_velocity_GPS_total[:] = ice_velocity(1,1)
	ice_velocity_GPS_x[:] = ice_velocity(0,1)
	ice_velocity_GPS_y[:] = ice_velocity(1,0)

	ds['ice_velocity_GPS_total'] = (('time'),ice_velocity_GPS_total)
	ds['ice_velocity_GPS_x'] = (('time'),ice_velocity_GPS_x)
	ds['ice_velocity_GPS_y'] = (('time'),ice_velocity_GPS_y)
	ds['time'] = (('time'),time)
	ds['time_bounds'] = (('time', 'nbnd'),time_bounds)
	ds['sza'] = (('time'),sza)
	ds['station_name'] = ((),station_name)
	ds['latitude'] = ((),latitude)
	ds['longitude'] = ((),longitude)
	
	common.load_ds_attrs('promice', ds)
	encoding = common.get_encoding('promice', fillvalue_float)

	write_data(args, ds, op_file, encoding)
