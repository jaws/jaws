import pandas as pd
import numpy as np
import xarray as xr
from datetime import datetime, timedelta
import pytz
from sunposition import sunpos
from common import write_data, time_common
import common

def get_fillvalue(args):
	if args.fillvalue_float:
		return args.fillvalue_float
	return common.fillvalue_float


def init_dataframe(args, input_file):
	check_na = 999.0

	df = common.load_dataframe('gcnet', input_file, 54, delim_whitespace=True)
	df.index.name = 'time'
	df['qc25'] = df['qc25'].astype(str)  # To avoid 999 values marked as N/A
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
	df = df.where((pd.notnull(df)), get_fillvalue(args))
	df['qc25'] = df['qc25'].astype(int)  # Convert it back to int

	return df

def get_station(args, input_file, stations):
	df = common.load_dataframe('gcnet', input_file, 54, delim_whitespace=True)
	station_number = df['station_number'][0]

	if 30 <= station_number <= 32:
		name = 'gcnet_lar{}'.format(station_number - 29)
		station = stations[name]
	else:
		station = list(stations.values())[station_number]

	return common.parse_station(args, station)



def gcnet2nc(args, op_file, station_dict, station_name):

	freezing_point_temp = common.freezing_point_temp
	pascal_per_millibar = common.pascal_per_millibar
	seconds_in_hour = common.seconds_in_hour
	
	if args.fillvalue_float:
		fillvalue_float = args.fillvalue_float
	else:
		fillvalue_float = common.fillvalue_float

	header_rows = 54
	check_na = 999.0
	hour_conversion = (100/4)		#Divided by 4 because each hour value is a multiple of 4 and then multiplied by 100 to convert decimal to integer
	last_hour = 23

	column_names = ['station_number', 'year', 'julian_decimal_time', 'sw_down', 'sw_up', 'net_radiation', 'temperature_tc_1', 'temperature_tc_2', 'temperature_cs500_1', 'temperature_cs500_2', 'relative_humidity_1', 'relative_humidity_2', 
	'u1_wind_speed', 'u2_wind_speed', 'u_direction_1', 'u_direction_2', 'atmos_pressure', 'snow_height_1', 'snow_height_2', 't_snow_01', 't_snow_02', 't_snow_03', 't_snow_04', 't_snow_05', 't_snow_06', 't_snow_07', 't_snow_08', 't_snow_09', 't_snow_10', 
	'battery_voltage', 'sw_down_max', 'sw_up_max', 'net_radiation_max', 'max_air_temperature_1', 'max_air_temperature_2', 'min_air_temperature_1', 'min_air_temperature_2', 'max_windspeed_u1', 'max_windspeed_u2', 'stdev_windspeed_u1', 'stdev_windspeed_u2', 
	'ref_temperature', 'windspeed_2m', 'windspeed_10m', 'wind_sensor_height_1', 'wind_sensor_height_2', 'albedo', 'zenith_angle', 'qc1', 'qc9', 'qc17', 'qc25']

	
	df = pd.read_csv(args.input_file or args.fl_in, delim_whitespace=True, skiprows=header_rows, skip_blank_lines=True, header=None, names = column_names)
	df.index.name = 'time'
	df['qc25'] = df['qc25'].astype(str)			# To avoid 999 values marked as N/A
	df.replace(check_na, np.nan, inplace=True)
	df.loc[:,['temperature_tc_1', 'temperature_tc_2', 'temperature_cs500_1', 'temperature_cs500_2', 't_snow_01', 't_snow_02', 't_snow_03', 't_snow_04', 't_snow_05', 't_snow_06', 't_snow_07', 't_snow_08', 't_snow_09', 't_snow_10', 'max_air_temperature_1', 'max_air_temperature_2', 'min_air_temperature_1', 'min_air_temperature_2', 'ref_temperature']] += freezing_point_temp
	df.loc[:,'atmos_pressure'] *= pascal_per_millibar
	df = df.where((pd.notnull(df)), fillvalue_float)
	df['qc25'] = df['qc25'].astype(int)			#Convert it back to int

	station_number = df['station_number'][0]
	df.drop('station_number', axis=1, inplace=True)

	ds = xr.Dataset.from_dataframe(df)
	ds = ds.drop('time')
	
	
	# Intializing variables
	num_rows =  df['year'].size
	qc_swdn, qc_swup, qc_netradiation, qc_ttc1, qc_ttc2, qc_tcs1, qc_tcs2, qc_rh1, qc_rh2, qc_u1, qc_u2, qc_ud1, qc_ud2, qc_pressure, qc_snowheight1, qc_snowheight2, qc_tsnow1, qc_tsnow2, qc_tsnow3, qc_tsnow4, qc_tsnow5, qc_tsnow6, qc_tsnow7, qc_tsnow8, qc_tsnow9, qc_tsnow10, qc_battery = ([0]*num_rows for x in range(27))

	hour, month, day, time, time_bounds, sza = ([0]*num_rows for x in range(6))

	
	if args.dbg_lvl > 2:
		print('Retrieving latitude, longitude and station name')

	try:
		if station_number == 30:
			temp_stn = 'gcnet_lar1'
		elif station_number == 31:
			temp_stn = 'gcnet_lar2'
		elif station_number == 32:
			temp_stn = 'gcnet_lar3'
		
		latitude = station_dict.get(temp_stn)[0]
		longitude = station_dict.get(temp_stn)[1]

		if args.station_name:
			print('Default station name overrided by user provided station name')
		else:
			station_name = station_dict.get(temp_stn)[2]

	except:
		latitude = list(station_dict.values())[station_number][0]
		longitude = list(station_dict.values())[station_number][1]

		if args.station_name:
			print('Default station name overrided by user provided station name')
		else:
			station_name = list(station_dict.values())[station_number][2]


	if args.dbg_lvl > 3:
		print('Calculating time and sza')
	
	hour[:] = [int(x) for x in [round((y-int(y)),3)*hour_conversion for y in df['julian_decimal_time']]]
	
	z = 0
	while z < num_rows:
		if hour[z] > last_hour:
			hour[z] = 0
		z += 1

	
	dtime_1970, tz = time_common(args.timezone)
	i = 0

	while i < num_rows:

		try:
			temp_dtime = datetime.strptime("%s %s %s" % (df['year'][i], int(df['julian_decimal_time'][i]), hour[i]), "%Y %j %H")
			temp_dtime = tz.localize(temp_dtime.replace(tzinfo=None))
			time[i] = (temp_dtime-dtime_1970).total_seconds()
		except:
			time[i] = time[i-1] 		#Assign time of previous row, if julian_decimal_time > 366
		
		time_bounds[i] = (time[i]-seconds_in_hour, time[i])
		
		sza[i] = sunpos(temp_dtime,latitude,longitude,0)[1]
		
		i += 1
	

	if args.dbg_lvl > 4:
		print('Calculating quality control variables')

	temp1 = [list(map(int, i)) for i in zip(*map(str, df['qc1']))]
	temp9 = [list(map(int, i)) for i in zip(*map(str, df['qc9']))]
	temp17 = [list(map(int, i)) for i in zip(*map(str, df['qc17']))]
	temp25 = [list(map(int, i)) for i in zip(*map(str, df['qc25']))]

	
	qc_swdn[:] = temp1[0]
	qc_swup[:] = temp1[1]
	qc_netradiation[:] = temp1[2]
	qc_ttc1[:] = temp1[3]
	qc_ttc2[:] = temp1[4]
	qc_tcs1[:] = temp1[5]
	qc_tcs2[:] = temp1[6]
	qc_rh1[:] = temp1[7]
	
	qc_rh2[:] = temp9[0]
	qc_u1[:] = temp9[1]
	qc_u2[:] = temp9[2]
	qc_ud1[:] = temp9[3]
	qc_ud2[:] = temp9[4]
	qc_pressure[:] = temp9[5]
	qc_snowheight1[:] = temp9[6]
	qc_snowheight2[:] = temp9[7]

	qc_tsnow1[:] = temp17[0]
	qc_tsnow2[:] = temp17[1]
	qc_tsnow3[:] = temp17[2]
	qc_tsnow4[:] = temp17[3]
	qc_tsnow5[:] = temp17[4]
	qc_tsnow6[:] = temp17[5]
	qc_tsnow7[:] = temp17[6]
	qc_tsnow8[:] = temp17[7]

	qc_tsnow9[:] = temp25[0]
	qc_tsnow10[:] = temp25[1]
	qc_battery[:] = temp25[2]

	ds['qc_swdn'] = (('time',qc_swdn))
	ds['qc_swup'] = (('time',qc_swup))
	ds['qc_netradiation'] = (('time',qc_netradiation))
	ds['qc_ttc1'] = (('time',qc_ttc1))
	ds['qc_ttc2'] = (('time',qc_ttc2))
	ds['qc_tcs1'] = (('time',qc_tcs1))
	ds['qc_tcs2'] = (('time',qc_tcs2))
	ds['qc_rh1'] = (('time',qc_rh1))
	ds['qc_rh2'] = (('time',qc_rh2))
	ds['qc_u1'] = (('time',qc_u1))
	ds['qc_u2'] = (('time',qc_u2))
	ds['qc_ud1'] = (('time',qc_ud1))
	ds['qc_ud2'] = (('time',qc_ud2))
	ds['qc_pressure'] = (('time',qc_pressure))
	ds['qc_snowheight1'] = (('time',qc_snowheight1))
	ds['qc_snowheight2'] = (('time',qc_snowheight2))
	ds['qc_tsnow1'] = (('time',qc_tsnow1))
	ds['qc_tsnow2'] = (('time',qc_tsnow2))
	ds['qc_tsnow3'] = (('time',qc_tsnow3))
	ds['qc_tsnow4'] = (('time',qc_tsnow4))
	ds['qc_tsnow5'] = (('time',qc_tsnow5))
	ds['qc_tsnow6'] = (('time',qc_tsnow6))
	ds['qc_tsnow7'] = (('time',qc_tsnow7))
	ds['qc_tsnow8'] = (('time',qc_tsnow8))
	ds['qc_tsnow9'] = (('time',qc_tsnow9))
	ds['qc_tsnow10'] = (('time',qc_tsnow10))
	ds['qc_battery'] = (('time',qc_battery))


	
	if args.dbg_lvl > 5 and args.derive_times:
		print('Calculating month and day')
		
	if args.derive_times:
		def get_month_day(year, day, one_based=False):
			if one_based:  # if Jan 1st is 1 instead of 0
				day -= 1
			dt = datetime(year, 1, 1) + timedelta(days=day)
			return dt.month, dt.day

		j = 0
		while j < num_rows:
			month[j] = get_month_day(int(df['year'][j]), int(df['julian_decimal_time'][j]), True)[0]
			day[j] = get_month_day(int(df['year'][j]), int(df['julian_decimal_time'][j]), True)[1]
			j += 1


		ds['hour'] = (('time'),hour)
		ds['month'] = (('time'),month)
		ds['day'] = (('time'),day)


	ds['time'] = (('time'),time)
	ds['time_bounds'] = (('time', 'nbnd'),time_bounds)
	ds['sza'] = (('time'),sza)
	ds['station_number'] = ((),station_number)
	ds['station_name'] = ((),station_name)
	ds['latitude'] = ((),latitude)
	ds['longitude'] = ((),longitude)

	common.load_ds_attrs('gcnet', ds)
	encoding = common.get_encoding('gcnet', fillvalue_float)

	write_data(args, ds, op_file, encoding)
