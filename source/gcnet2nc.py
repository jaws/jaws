import pandas as pd
import numpy as np
import xarray as xr
from datetime import datetime, timedelta
import pytz
from sunposition import sunpos
from common import write_data
import common

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

	
	tz = pytz.timezone(args.timezone)
	dtime_1970 = datetime(1970,1,1)
	dtime_1970 = tz.localize(dtime_1970.replace(tzinfo=None))
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


	
	if args.derive_times:
		print('calculating month and day...')
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

	ds.attrs = {'title':'Surface Radiation Data from Greenland Climate Network', 'source':'Surface Observations', 'featureType':'timeSeries', 'institution':'Cooperative Institute for Research in Enviornmental Sciences', 
	'reference':'http://cires.colorado.edu/science/groups/steffen/gcnet/', 'Conventions':'CF-1.7', 'time_convention':"'time: point' variables match the time coordinate values exactly, whereas 'time: mean' variables are valid for the mean time within the time_bounds variable." + " e.g.: battery_voltage is measured once per hour at the time stored in the 'time' coordinate." + 	" On the other hand, temperature_tc_1 is continuously measured and then hourly-mean values are stored for each period contained in the time_bounds variable"}

	ds['station_number'].attrs= {'units':'1', 'long_name':'Station Number'}
	ds['year'].attrs= {'units':'1', 'long_name':'Year'}
	ds['julian_decimal_time'].attrs= {'units':'decimal time', 'long_name':'Julian Decimal Time', 'note':'For each year, time starts at 1.0000 and ends at 365.9999.'}
	ds['sw_down'].attrs= {'units':'watt meter-2', 'long_name':'Shortwave Flux Down', 'standard_name':'downwelling_shortwave_flux_in_air', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['sw_up'].attrs= {'units':'watt meter-2', 'long_name':'Shortwave Flux Up', 'standard_name':'upwelling_shortwave_flux_in_air', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['net_radiation'].attrs= {'units':'watt meter-2', 'long_name':'Net Radiation', 'standard_name':'surface_net_downward_radiative_flux', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['temperature_tc_1'].attrs= {'units':'kelvin', 'long_name':'TC-1 Air Temperature', 'standard_name':'air_temperature', 'note':'air temperature from TC sensor', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['temperature_tc_2'].attrs= {'units':'kelvin', 'long_name':'TC-2 Air Temperature', 'standard_name':'air_temperature', 'note':'air temperature from TC sensor', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['temperature_cs500_1'].attrs= {'units':'kelvin', 'long_name':'CS500-1 Air Temperature', 'standard_name':'air_temperature', 'note':'air temperature from CS500 sensor', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['temperature_cs500_2'].attrs= {'units':'kelvin', 'long_name':'CS500-2 Air Temperature', 'standard_name':'air_temperature', 'note':'air temperature from CS500 sensor', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['relative_humidity_1'].attrs= {'units':'1', 'long_name':'Relative Humidity 1', 'standard_name':'realtive_humidity', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['relative_humidity_2'].attrs= {'units':'1', 'long_name':'Relative Humidity 2', 'standard_name':'realtive_humidity', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['u1_wind_speed'].attrs= {'units':'meter second-1', 'long_name':'U1 Wind Speed', 'standard_name':'wind_speed', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['u2_wind_speed'].attrs= {'units':'meter second-1', 'long_name':'U2 Wind Speed', 'standard_name':'wind_speed', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['u_direction_1'].attrs= {'units':'degree', 'long_name':'U Direction 1', 'standard_name':'wind_from_direction', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['u_direction_2'].attrs= {'units':'degree', 'long_name':'U Direction 2', 'standard_name':'wind_from_direction', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['atmos_pressure'].attrs= {'units':'pascal', 'long_name':'Atmospheric Pressure', 'standard_name':'surface_air_pressure', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['snow_height_1'].attrs= {'units':'meter', 'long_name':'Snow Height 1', 'standard_name':'snow_height', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['snow_height_2'].attrs= {'units':'meter', 'long_name':'Snow Height 2', 'standard_name':'snow_height', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['t_snow_01'].attrs= {'units':'kelvin', 'long_name':'T Snow 1', 'standard_name':'', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['t_snow_02'].attrs= {'units':'kelvin', 'long_name':'T Snow 2', 'standard_name':'', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['t_snow_03'].attrs= {'units':'kelvin', 'long_name':'T Snow 3', 'standard_name':'', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['t_snow_04'].attrs= {'units':'kelvin', 'long_name':'T Snow 4', 'standard_name':'', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['t_snow_05'].attrs= {'units':'kelvin', 'long_name':'T Snow 5', 'standard_name':'', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['t_snow_06'].attrs= {'units':'kelvin', 'long_name':'T Snow 6', 'standard_name':'', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['t_snow_07'].attrs= {'units':'kelvin', 'long_name':'T Snow 7', 'standard_name':'', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['t_snow_08'].attrs= {'units':'kelvin', 'long_name':'T Snow 8', 'standard_name':'', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['t_snow_09'].attrs= {'units':'kelvin', 'long_name':'T Snow 9', 'standard_name':'', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['t_snow_10'].attrs= {'units':'kelvin', 'long_name':'T Snow 10', 'standard_name':'', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['battery_voltage'].attrs= {'units':'volts', 'long_name':'Battery Voltage', 'standard_name':'battery_voltage', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['sw_down_max'].attrs= {'units':'watt meter-2', 'long_name':'Shortwave Flux Down Max', 'standard_name':'maximum_downwelling_shortwave_flux_in_air', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['sw_up_max'].attrs= {'units':'watt meter-2', 'long_name':'Shortwave Flux Up Max', 'standard_name':'maximum_upwelling_shortwave_flux_in_air', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['net_radiation_max'].attrs= {'units':'watt meter-2', 'long_name':'Net Radiation Max', 'standard_name':'maximum_net_radiation', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['max_air_temperature_1'].attrs= {'units':'kelvin', 'long_name':'Max Air Temperature 1', 'standard_name':'air_temperature', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['max_air_temperature_2'].attrs= {'units':'kelvin', 'long_name':'Max Air Temperature 2', 'standard_name':'air_temperature', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['min_air_temperature_1'].attrs= {'units':'kelvin', 'long_name':'Min Air Temperature 1', 'standard_name':'air_temperature', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['min_air_temperature_2'].attrs= {'units':'kelvin', 'long_name':'Min Air Temperature 2', 'standard_name':'air_temperature', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['max_windspeed_u1'].attrs= {'units':'meter second-1', 'long_name':'Max Windspeed-U1', 'standard_name':'wind_speed', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['max_windspeed_u2'].attrs= {'units':'meter second-1', 'long_name':'Max Windspeed-U2', 'standard_name':'wind_speed', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['stdev_windspeed_u1'].attrs= {'units':'meter second-1', 'long_name':'StdDev Windspeed-U1', 'standard_name':'wind_speed', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['stdev_windspeed_u2'].attrs= {'units':'meter second-1', 'long_name':'StdDev Windspeed-U2', 'standard_name':'wind_speed', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['ref_temperature'].attrs= {'units':'kelvin', 'long_name':'Reference Temperature', 'standard_name':'Need to ask network manager about long name', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['windspeed_2m'].attrs= {'units':'meter second-1', 'long_name':'Windspeed@2m', 'standard_name':'wind_speed', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['windspeed_10m'].attrs= {'units':'meter second-1', 'long_name':'Windspeed@10m', 'standard_name':'wind_speed', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['wind_sensor_height_1'].attrs= {'units':'meter', 'long_name':'Wind Sensor Height 1', 'standard_name':'', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['wind_sensor_height_2'].attrs= {'units':'meter', 'long_name':'Wind Sensor Height 2', 'standard_name':'', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['albedo'].attrs= {'units':'1', 'long_name':'Albedo', 'standard_name':'surface_albedo', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['zenith_angle'].attrs= {'units':'degree', 'long_name':'Zenith Angle', 'standard_name':'solar_zenith_angle', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['qc1'].attrs= {'units':'1', 'long_name':'Quality Control variables 01-08', 'coordinates':'longitude latitude'}
	ds['qc9'].attrs= {'units':'1', 'long_name':'Quality Control variables 09-16', 'coordinates':'longitude latitude'}
	ds['qc17'].attrs= {'units':'1', 'long_name':'Quality Control variables 17-24', 'coordinates':'longitude latitude'}
	ds['qc25'].attrs= {'units':'1', 'long_name':'Quality Control variables 25-27', 'coordinates':'longitude latitude'}
	ds['qc_swdn'].attrs= {'units':'1', 'long_name':'Quality Control flag for Shortwave Flux Down'}
	ds['qc_swup'].attrs= {'units':'1', 'long_name':'Quality Control flag for Shortwave Flux Up'}
	ds['qc_netradiation'].attrs= {'units':'1', 'long_name':'Quality Control flag for Net Radiation'}
	ds['qc_ttc1'].attrs= {'units':'1', 'long_name':'Quality Control flag for TC-1 Air Temperature'}
	ds['qc_ttc2'].attrs= {'units':'1', 'long_name':'Quality Control flag for TC-2 Air Temperature'}
	ds['qc_tcs1'].attrs= {'units':'1', 'long_name':'Quality Control flag for CS500-1 Air Temperature'}
	ds['qc_tcs2'].attrs= {'units':'1', 'long_name':'Quality Control flag for CS500-2 Air Temperature'}
	ds['qc_rh1'].attrs= {'units':'1', 'long_name':'Quality Control flag for Relative Humidity 1'}
	ds['qc_rh2'].attrs= {'units':'1', 'long_name':'Quality Control flag for Relative Humidity 2'}
	ds['qc_u1'].attrs= {'units':'1', 'long_name':'Quality Control flag for U1 Wind Speed'}
	ds['qc_u2'].attrs= {'units':'1', 'long_name':'Quality Control flag for U2 Wind Speed'}
	ds['qc_ud1'].attrs= {'units':'1', 'long_name':'Quality Control flag for U Direction 1'}
	ds['qc_ud2'].attrs= {'units':'1', 'long_name':'Quality Control flag for U Direction 2'}
	ds['qc_pressure'].attrs= {'units':'1', 'long_name':'Quality Control flag for Atmospheric Pressure'}
	ds['qc_snowheight1'].attrs= {'units':'1', 'long_name':'Quality Control flag for Snow Height 1'}
	ds['qc_snowheight2'].attrs= {'units':'1', 'long_name':'Quality Control flag for Snow Height 2'}
	ds['qc_tsnow1'].attrs= {'units':'1', 'long_name':'Quality Control flag for T Snow 1'}
	ds['qc_tsnow2'].attrs= {'units':'1', 'long_name':'Quality Control flag for T Snow 2'}
	ds['qc_tsnow3'].attrs= {'units':'1', 'long_name':'Quality Control flag for T Snow 3'}
	ds['qc_tsnow4'].attrs= {'units':'1', 'long_name':'Quality Control flag for T Snow 4'}
	ds['qc_tsnow5'].attrs= {'units':'1', 'long_name':'Quality Control flag for T Snow 5'}
	ds['qc_tsnow6'].attrs= {'units':'1', 'long_name':'Quality Control flag for T Snow 6'}
	ds['qc_tsnow7'].attrs= {'units':'1', 'long_name':'Quality Control flag for T Snow 7'}
	ds['qc_tsnow8'].attrs= {'units':'1', 'long_name':'Quality Control flag for T Snow 8'}
	ds['qc_tsnow9'].attrs= {'units':'1', 'long_name':'Quality Control flag for T Snow 9'}
	ds['qc_tsnow10'].attrs= {'units':'1', 'long_name':'Quality Control flag for T Snow 10'}
	ds['qc_battery'].attrs= {'units':'1', 'long_name':'Quality Control flag for Battery Voltage'}
	ds['time'].attrs= {'units':'seconds since 1970-01-01 00:00:00', 'long_name':'time of measurement',	'standard_name':'time', 'bounds':'time_bounds', 'calendar':'leap'}
	ds['sza'].attrs= {'units':'degree', 'long_name':'Solar Zenith Angle', 'standard_name':'solar_zenith_angle', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['station_name'].attrs= {'long_name':'Station Name', 'cf_role':'timeseries_id'}
	ds['latitude'].attrs= {'units':'degrees_north', 'standard_name':'latitude'}
	ds['longitude'].attrs= {'units':'degrees_east', 'standard_name':'longitude'}
	

	encoding = {'station_number': {'dtype': 'i2'},
				'year': {'dtype': 'i2'},
				'julian_decimal_time': {'_FillValue': False, 'dtype': 'f4'},
				'sw_down': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				'sw_up': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				'net_radiation': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				'temperature_tc_1': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				'temperature_tc_2': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				'temperature_cs500_1': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				'temperature_cs500_2': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				'relative_humidity_1': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				'relative_humidity_2': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				'u1_wind_speed': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				'u2_wind_speed': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				'u_direction_1': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				'u_direction_2': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				'atmos_pressure': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				'snow_height_1': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				'snow_height_2': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				't_snow_01': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				't_snow_02': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				't_snow_03': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				't_snow_04': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				't_snow_05': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				't_snow_06': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				't_snow_07': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				't_snow_08': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				't_snow_09': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				't_snow_10': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				'battery_voltage': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				'sw_down_max': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				'sw_up_max': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				'net_radiation_max': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				'max_air_temperature_1': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				'max_air_temperature_2': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				'min_air_temperature_1': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				'min_air_temperature_2': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				'max_windspeed_u1': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				'max_windspeed_u2': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				'stdev_windspeed_u1': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				'stdev_windspeed_u2': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				'ref_temperature': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				'windspeed_2m': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				'windspeed_10m': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				'wind_sensor_height_1': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				'wind_sensor_height_2': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				'albedo': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				'zenith_angle': {'_FillValue': fillvalue_float, 'dtype': 'f4'},
				'qc1': {'dtype': 'i4'},
				'qc9': {'dtype': 'i4'},
				'qc17': {'dtype': 'i4'},
				'qc25': {'dtype': 'i4'},
				'qc_swdn': {'dtype': 'i1'},
				'qc_swup': {'dtype': 'i1'},
				'qc_netradiation': {'dtype': 'i1'},
				'qc_ttc1': {'dtype': 'i1'},
				'qc_ttc2': {'dtype': 'i1'},
				'qc_tcs1': {'dtype': 'i1'},
				'qc_tcs2': {'dtype': 'i1'},
				'qc_rh1': {'dtype': 'i1'},
				'qc_rh2': {'dtype': 'i1'},
				'qc_u1': {'dtype': 'i1'},
				'qc_u2': {'dtype': 'i1'},
				'qc_ud1': {'dtype': 'i1'},
				'qc_ud2': {'dtype': 'i1'},
				'qc_pressure': {'dtype': 'i1'},
				'qc_snowheight1': {'dtype': 'i1'},
				'qc_snowheight2': {'dtype': 'i1'},
				'qc_tsnow1': {'dtype': 'i1'},
				'qc_tsnow2': {'dtype': 'i1'},
				'qc_tsnow3': {'dtype': 'i1'},
				'qc_tsnow4': {'dtype': 'i1'},
				'qc_tsnow5': {'dtype': 'i1'},
				'qc_tsnow6': {'dtype': 'i1'},
				'qc_tsnow7': {'dtype': 'i1'},
				'qc_tsnow8': {'dtype': 'i1'},
				'qc_tsnow9': {'dtype': 'i1'},
				'qc_tsnow10': {'dtype': 'i1'},
				'qc_battery': {'dtype': 'i1'},
				'time': {'_FillValue': False},
				'time_bounds': {'_FillValue': False},
				'sza': {'_FillValue': False},
				'latitude': {'_FillValue': False},
				'longitude': {'_FillValue': False}
				}


	write_data(args, ds, op_file, encoding)