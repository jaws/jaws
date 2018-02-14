import pandas as pd
import numpy as np
import xarray as xr
import os
from datetime import datetime
from pytz import timezone
from sunposition import sunpos
from math import sin, cos, sqrt, atan2, radians
import warnings

warnings.filterwarnings("ignore")

def promice2nc(args, op_file, station_dict, station_name):

	header_lines = 1
	convert_temp = 273.15
	convert_press = 100
	convert_current = 1000
	check_na = -999
	seconds_in_hour = 3600

	column_names = ['year', 'month', 'day', 'hour', 'day_of_year', 'day_of_century', 'air_pressure', 'air_temperature', 'air_temperature_hygroclip', 'relative_humidity_wrtwater', 'relative_humidity', 'wind_speed', 'wind_direction', 
	'shortwave_radiation_down', 'shortwave_radiation_down_cor', 'shortwave_radiation_up', 'shortwave_radiation_up_cor', 'albedo_theta', 'longwave_radiation_down', 'longwave_radiation_up', 'cloudcover', 'surface_temp', 'height_sensor_boom', 
	'height_stakes', 'depth_pressure_transducer', 'depth_pressure_transducer_cor', 'ice_temp_01', 'ice_temp_02', 'ice_temp_03', 'ice_temp_04', 'ice_temp_05', 'ice_temp_06', 'ice_temp_07', 'ice_temp_08', 'tilt_east', 'tilt_north', 
	'time_GPS', 'latitude_GPS', 'longitude_GPS', 'elevation', 'hor_dil_prec', 'logger_temp', 'fan_current', 'battery_voltage']

	df = pd.read_csv(args.input_file or args.fl_in, delim_whitespace=True, skiprows=header_lines, skip_blank_lines=True, header=None, names = column_names)
	df.index.name = 'time'
	df.replace(check_na, np.nan, inplace=True)
	df.loc[:,['air_temperature','air_temperature_hygroclip','surface_temp','ice_temp_01','ice_temp_02','ice_temp_03','ice_temp_04','ice_temp_05','ice_temp_06','ice_temp_07','ice_temp_08','logger_temp']] += convert_temp
	df.loc[:,['air_pressure']] *= convert_press
	df.loc[:,['fan_current']] /= convert_current
	df =  df.where((pd.notnull(df)), check_na)

	ds = xr.Dataset.from_dataframe(df)
	ds = ds.drop('time')
	
	num_lines =  sum(1 for line in open(args.input_file or args.fl_in) if len(line.strip()) != 0) - header_lines
	
	# Intializing variables
	time, time_bounds, sza, velocity, ice_velocity_GPS_total, ice_velocity_GPS_x, ice_velocity_GPS_y = ([0]*num_lines for x in range(7))

	
	print('retrieving lat and lon...')
	k = os.path.basename(args.input_file or args.fl_in)

	if ('EGP') in k:
		temp_stn = 'promice_egp'
	elif ('KAN_B') or ('Kangerlussuaq-B') in k:
		temp_stn = 'promice_kanb'
	elif ('KAN_L') or ('Kangerlussuaq-L') in k:
		temp_stn = 'promice_kanl'
	elif ('KAN_M') or ('Kangerlussuaq-M') in k:
		temp_stn = 'promice_kanm'
	elif ('KAN_U') or ('Kangerlussuaq-U') in k:
		temp_stn = 'promice_kanu'
	elif ('KPC_L') or ('KronprinsChristianland-L') in k:
		temp_stn = 'promice_kpcl'
	elif ('KPC_U') or ('KronprinsChristianland-U') in k:
		temp_stn = 'promice_kpcu'
	elif ('MIT') in k:
		temp_stn = 'promice_mit'
	elif ('NUK_K') or ('Nuuk-K') in k:
		temp_stn = 'promice_nukk'
	elif ('NUK_L') or ('Nuuk-L') in k:
		temp_stn = 'promice_nukl'
	elif ('NUK_N') or ('Nuuk-N') in k:
		temp_stn = 'promice_nukn'
	elif ('NUK_U') or ('Nuuk-U') in k:
		temp_stn = 'promice_nuku'
	elif ('QAS_A') or ('Qassimiut-A') in k:
		temp_stn = 'promice_qasa'
	elif ('QAS_L') or ('Qassimiut-L') in k:
		temp_stn = 'promice_qasl'
	elif ('QAS_M') or ('Qassimiut-M') in k:
		temp_stn = 'promice_qasm'
	elif ('QAS_U') or ('Qassimiut-U') in k:
		temp_stn = 'promice_qasu'
	elif ('SCO_L') or ('Scoresbysund-L') in k:
		temp_stn = 'promice_scol'
	elif ('SCO_U') or ('Scoresbysund-U') in k:
		temp_stn = 'promice_scou'
	elif ('TAS_A') or ('Tasiilaq-A') in k:
		temp_stn = 'promice_tasa'
	elif ('TAS_L') or ('Tasiilaq-L') in k:
		temp_stn = 'promice_tasl'
	elif ('TAS_U') or ('Tasiilaq-U') in k:
		temp_stn = 'promice_tasu'
	elif ('THU_L') or ('ThuleAirbase-L') in k:
		temp_stn = 'promice_thul'
	elif ('THU_U') or ('ThuleAirbase-U') in k:
		temp_stn = 'promice_thuu'
	elif ('UPE_L') or ('Upernavik-L') in k:
		temp_stn = 'promice_upel'
	elif ('UPE_U') or ('Upernavik-U') in k:
		temp_stn = 'promice_upeu'
	elif ('CEN') in k:
		temp_stn = 'promice_cen'

	latitude = (station_dict.get(temp_stn)[0])
	longitude = (station_dict.get(temp_stn)[1])

	if args.station_name:
		print('Default station name overrided by user provided station name')
	else:
		station_name = station_dict.get(temp_stn)[2]


	print('converting lat_GPS and lon_GPS...')
	
	def lat_lon_gps(coords):
		deg = np.floor(coords / 100)
		minutes = np.floor(((coords / 100) - deg) * 100)
		seconds = (((coords / 100) - deg) * 100 - minutes) * 100
		return deg + minutes / 60 + seconds / 3600

	# Exclude NAs
	logic1 = df.latitude_GPS != check_na
	logic2 = df.longitude_GPS != check_na
	df1 = df[logic1]
	df2 = df[logic2]

	df.latitude_GPS = lat_lon_gps(df1.latitude_GPS)
	df.longitude_GPS = lat_lon_gps(df2.longitude_GPS)
	

	print('calculating time and sza...')
	
	i = 0

	while i < num_lines:
		
		temp_dtime = datetime(df['year'][i], df['month'][i], df['day'][i], df['hour'][i]).replace(tzinfo = timezone(args.timezone))
		time[i] = (temp_dtime-(datetime(1970,1,1)).replace(tzinfo = timezone(args.timezone))).total_seconds()
		time_bounds[i] = (time[i], time[i]+seconds_in_hour)

		sza[i] = sunpos(temp_dtime,latitude,longitude,0)[1]

		i += 1

	
	print('calculating ice velocity...')
	def ice_velocity(n,o):
		m,p = 0,1
		R = 6373.0		#Approx radius of earth
		while p < num_lines:
			if (df['latitude_GPS'][m] == check_na or df['longitude_GPS'][m] == check_na or df['latitude_GPS'][n] == check_na or df['longitude_GPS'][o] == check_na):
				velocity[m] = check_na
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
	
	ds.attrs = {'title':'Weather Station Data', 'source':'Surface Observations', 'featureType':'timeSeries', 'institution':'Programme for Monitoring of the Greenland Ice Sheet', 
	'reference':'http://www.promice.dk/home.html', 'Conventions':'CF-1.7', 'time_convention':"'time: point' variables match the time coordinate values exactly, whereas 'time: mean' variables are valid for the mean time within the time_bounds variable." + " e.g.: elevation is measured once per hour at the time stored in the 'time' coordinate." + 	" On the other hand, air_temperature is continuously measured and then hourly-mean values are stored for each period contained in the time_bounds variable"}

	ds['year'].attrs = {'units':'1', 'long_name':'Year'}
	ds['month'].attrs = {'units':'1', 'long_name':'Month of Year'}
	ds['day'].attrs = {'units':'1', 'long_name':'Day of Month'}
	ds['hour'].attrs = {'units':'1', 'long_name':'Hour of Day(UTC)'}
	ds['day_of_year'].attrs = {'units':'1', 'long_name':'Day of Year'}
	ds['day_of_century'].attrs = {'units':'1', 'long_name':'Day of Century'}
	ds['air_pressure'].attrs = {'units':'pascal', 'long_name':'Air Pressure', 'standard_name':'air_pressure', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['air_temperature'].attrs = {'units':'kelvin', 'long_name':'Air Temperature', 'standard_name':'air_temperature', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['air_temperature_hygroclip'].attrs = {'units':'kelvin', 'long_name':'Air Temperature HygroClip', 'standard_name':'air_temperature', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['relative_humidity_wrtwater'].attrs = {'units':'1', 'long_name':'Relative Humidity wrt Water', 'standard_name':'relative_humidity', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['relative_humidity'].attrs = {'units':'1', 'long_name':'Relative Humidity', 'standard_name':'relative_humidity', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['wind_speed'].attrs = {'units':'meter second-1', 'long_name':'Wind Speed', 'standard_name':'wind_speed', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['wind_direction'].attrs = {'units':'degree', 'long_name':'Wind Direction', 'standard_name':'wind_from_direction', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['shortwave_radiation_down'].attrs = {'units':'watt meter-2', 'long_name':'Shortwave Radiation Down', 'standard_name':'downwelling_shortwave_flux_in_air', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['shortwave_radiation_down_cor'].attrs = {'units':'watt meter-2', 'long_name':'Shortwave Radiation Down Cor', 'standard_name':'downwelling_shortwave_flux_in_air', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['shortwave_radiation_up'].attrs = {'units':'watt meter-2', 'long_name':'Shortwave Radiation Up', 'standard_name':'upwelling_shortwave_flux_in_air', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['shortwave_radiation_up_cor'].attrs = {'units':'watt meter-2', 'long_name':'Shortwave Radiation Up Cor', 'standard_name':'upwelling_shortwave_flux_in_air', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['albedo_theta'].attrs = {'units':'1', 'long_name':'Albedo_theta<70d', 'standard_name':'surface_albedo', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['longwave_radiation_down'].attrs = {'units':'watt meter-2', 'long_name':'Longwave Radiation Down', 'standard_name':'downwelling_longwave_flux_in_air', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['longwave_radiation_up'].attrs = {'units':'watt meter-2', 'long_name':'Longwave Radiation Up', 'standard_name':'upwelling_longwave_flux_in_air', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['cloudcover'].attrs = {'units':'1', 'long_name':'Cloud Cover', 'standard_name':'', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['surface_temp'].attrs = {'units':'kelvin', 'long_name':'Surface Temperature', 'standard_name':'surface_temperature', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['height_sensor_boom'].attrs = {'units':'meter', 'long_name':'Height Sensor Boom', 'standard_name':'', 'coordinates':'longitude latitude', 'cell_methods':'time: point'}
	ds['height_stakes'].attrs = {'units':'meter', 'long_name':'Height Stakes', 'standard_name':'', 'coordinates':'longitude latitude', 'cell_methods':'time: point'}
	ds['depth_pressure_transducer'].attrs = {'units':'meter', 'long_name':'Depth Pressure Transducer', 'standard_name':'', 'coordinates':'longitude latitude', 'cell_methods':'time: point'}
	ds['depth_pressure_transducer_cor'].attrs = {'units':'meter', 'long_name':'Depth Pressure Transducer Cor', 'standard_name':'', 'coordinates':'longitude latitude', 'cell_methods':'time: point'}
	ds['ice_temp_01'].attrs = {'units':'kelvin', 'long_name':'Ice Temperature 1', 'standard_name':'land_ice_temperature', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['ice_temp_02'].attrs = {'units':'kelvin', 'long_name':'Ice Temperature 2', 'standard_name':'land_ice_temperature', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['ice_temp_03'].attrs = {'units':'kelvin', 'long_name':'Ice Temperature 3', 'standard_name':'land_ice_temperature', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['ice_temp_04'].attrs = {'units':'kelvin', 'long_name':'Ice Temperature 4', 'standard_name':'land_ice_temperature', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['ice_temp_05'].attrs = {'units':'kelvin', 'long_name':'Ice Temperature 5', 'standard_name':'land_ice_temperature', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['ice_temp_06'].attrs = {'units':'kelvin', 'long_name':'Ice Temperature 6', 'standard_name':'land_ice_temperature', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['ice_temp_07'].attrs = {'units':'kelvin', 'long_name':'Ice Temperature 7', 'standard_name':'land_ice_temperature', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['ice_temp_08'].attrs = {'units':'kelvin', 'long_name':'Ice Temperature 8', 'standard_name':'land_ice_temperature', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['tilt_east'].attrs = {'units':'degree', 'long_name':'Tilt to East', 'standard_name':'', 'coordinates':'longitude latitude', 'cell_methods':'time: point'}
	ds['tilt_north'].attrs = {'units':'degree', 'long_name':'Tilt to North', 'standard_name':'', 'coordinates':'longitude latitude', 'cell_methods':'time: point'}
	ds['time_GPS'].attrs = {'units':'UTC', 'long_name':'Time GPS(hhmmssUTC)', 'standard_name':'time'}
	ds['latitude_GPS'].attrs = {'units':'degrees_north', 'long_name':'Latitude GPS', 'standard_name':'latitude'}
	ds['longitude_GPS'].attrs = {'units':'degrees_east', 'long_name':'Longitude GPS', 'standard_name':'longitude'}
	ds['elevation'].attrs = {'units':'meter', 'long_name':'Elevation GPS', 'standard_name':'', 'coordinates':'longitude latitude', 'cell_methods':'time: point'}
	ds['hor_dil_prec'].attrs = {'units':'1', 'long_name':'Horizontal Dilution of Precision GPS', 'standard_name':'', 'coordinates':'longitude latitude', 'cell_methods':'time: point'}
	ds['logger_temp'].attrs = {'units':'kelvin', 'long_name':'Logger Temperature', 'standard_name':'', 'coordinates':'longitude latitude', 'cell_methods':'time: point'}
	ds['fan_current'].attrs = {'units':'ampere', 'long_name':'Fan Current', 'standard_name':'', 'coordinates':'longitude latitude', 'cell_methods':'time: point'}
	ds['battery_voltage'].attrs = {'units':'volts', 'long_name':'Battery Voltage', 'standard_name':'battery_voltage', 'coordinates':'longitude latitude', 'cell_methods':'time: point'}
	ds['ice_velocity_GPS_total'].attrs = {'units':'meter second-1', 'long_name':'Ice velocity derived from GPS Lat and Long', 'standard_name':'', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['ice_velocity_GPS_x'].attrs = {'units':'meter second-1', 'long_name':'x-component of Ice velocity derived from GPS Lat and Long', 'standard_name':'land_ice_surface_x_velocity', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['ice_velocity_GPS_y'].attrs = {'units':'meter second-1', 'long_name':'y-component of Ice velocity derived from GPS Lat and Long', 'standard_name':'land_ice_surface_y_velocity', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['time'].attrs= {'units':'seconds since 1970-01-01 00:00:00', 'long_name':'time of measurement',	'standard_name':'time', 'bounds':'time_bounds', 'calendar':'noleap'}
	ds['sza'].attrs= {'units':'degree', 'long_name':'Solar Zenith Angle', 'standard_name':'solar_zenith_angle', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['station_name'].attrs= {'long_name':'Station Name', 'cf_role':'timeseries_id'}
	ds['latitude'].attrs= {'units':'degrees_north', 'standard_name':'latitude'}
	ds['longitude'].attrs= {'units':'degrees_east', 'standard_name':'longitude'}
	

	encoding = {'year': {'_FillValue': False},
				'month': {'_FillValue': False},
				'day': {'_FillValue': False},
				'hour': {'_FillValue': False},
				'day_of_year': {'_FillValue': False},
				'day_of_century': {'_FillValue': False},
				'air_pressure': {'_FillValue': check_na},
				'air_temperature': {'_FillValue': check_na},
				'air_temperature_hygroclip': {'_FillValue': check_na},
				'relative_humidity_wrtwater': {'_FillValue': check_na},
				'relative_humidity': {'_FillValue': check_na},
				'wind_speed': {'_FillValue': check_na},
				'wind_direction': {'_FillValue': check_na},
				'shortwave_radiation_down': {'_FillValue': check_na},
				'shortwave_radiation_down_cor': {'_FillValue': check_na},
				'shortwave_radiation_up': {'_FillValue': check_na},
				'shortwave_radiation_up_cor': {'_FillValue': check_na},
				'albedo_theta': {'_FillValue': check_na},
				'longwave_radiation_down': {'_FillValue': check_na},
				'longwave_radiation_up': {'_FillValue': check_na},
				'cloudcover': {'_FillValue': check_na},
				'surface_temp': {'_FillValue': check_na},
				'height_sensor_boom': {'_FillValue': check_na},
				'height_stakes': {'_FillValue': check_na},
				'depth_pressure_transducer': {'_FillValue': check_na},
				'depth_pressure_transducer_cor': {'_FillValue': check_na},
				'ice_temp_01': {'_FillValue': check_na},
				'ice_temp_02': {'_FillValue': check_na},
				'ice_temp_03': {'_FillValue': check_na},
				'ice_temp_04': {'_FillValue': check_na},
				'ice_temp_05': {'_FillValue': check_na},
				'ice_temp_06': {'_FillValue': check_na},
				'ice_temp_07': {'_FillValue': check_na},
				'ice_temp_08': {'_FillValue': check_na},
				'tilt_east': {'_FillValue': check_na},
				'tilt_north': {'_FillValue': check_na},
				'time_GPS': {'_FillValue': check_na},
				'latitude_GPS': {'_FillValue': check_na},
				'longitude_GPS': {'_FillValue': check_na},
				'elevation': {'_FillValue': check_na},
				'hor_dil_prec': {'_FillValue': check_na},
				'logger_temp': {'_FillValue': check_na},
				'fan_current': {'_FillValue': check_na},
				'battery_voltage': {'_FillValue': check_na},
				'ice_velocity_GPS_total': {'_FillValue': check_na},
				'ice_velocity_GPS_x': {'_FillValue': check_na},
				'ice_velocity_GPS_y': {'_FillValue': check_na},
				'time': {'_FillValue': False},
				'time_bounds': {'_FillValue': False},
				'sza': {'_FillValue': False},
				'latitude': {'_FillValue': False},
				'longitude': {'_FillValue': False}
				}


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
