import os
from sunposition import sunpos
from datetime import date, datetime
from math import sin, cos, sqrt, atan2, radians
import warnings

warnings.filterwarnings("ignore")

def promice2nc(args, op_file, root_grp, station_name, latitude, longitude, time, time_bounds, sza, station_dict):

	#Global Attributes
	root_grp.title = 'Weather Station Data'
	root_grp.source = 'Surface Observations'
	root_grp.featureType = 'timeSeries'
	root_grp.institution = 'Programme for Monitoring of the Greenland Ice Sheet'
	root_grp.reference = 'http://www.promice.dk/home.html'
	root_grp.Conventions = 'CF-1.7'
	root_grp.time_convention = "'time: point' variables match the time coordinate values exactly, whereas 'time: mean' variables are valid for the mean time within the time_bounds variable." + " e.g.: sensor_height is measured once per hour at the time stored in the 'time' coordinate." + " On the other hand, air_temperature is continuously measured and then hourly-mean values are stored for each period contained in the time_bounds variable"

	# variables
	year = root_grp.createVariable('year', 'i4', ('time',))
	month = root_grp.createVariable('month', 'i4', ('time',))
	day = root_grp.createVariable('day', 'i4', ('time',))
	hour = root_grp.createVariable('hour', 'i4', ('time',))
	day_of_year = root_grp.createVariable('day_of_year', 'i4', ('time',))
	day_of_century = root_grp.createVariable('day_of_century', 'i4', ('time',))
	air_pressure = root_grp.createVariable('air_pressure', 'f4', ('time',), fill_value = -999)
	air_temperature = root_grp.createVariable('air_temperature', 'f4', ('time',), fill_value = -999)
	air_temperature_hygroclip = root_grp.createVariable('air_temperature_hygroclip', 'f4', ('time',), fill_value = -999)
	relative_humidity_wrtwater = root_grp.createVariable('relative_humidity_wrtwater', 'f4', ('time',), fill_value = -999)
	relative_humidity = root_grp.createVariable('relative_humidity', 'f4', ('time',), fill_value = -999)
	wind_speed = root_grp.createVariable('wind_speed', 'f4', ('time',), fill_value = -999)
	wind_direction = root_grp.createVariable('wind_direction', 'f4', ('time',), fill_value = -999)
	shortwave_radiation_down = root_grp.createVariable('shortwave_radiation_down', 'f4', ('time',), fill_value = -999)
	shortwave_radiation_down_cor = root_grp.createVariable('shortwave_radiation_down_cor', 'f4', ('time',), fill_value = -999)
	shortwave_radiation_up = root_grp.createVariable('shortwave_radiation_up', 'f4', ('time',), fill_value = -999)
	shortwave_radiation_up_cor = root_grp.createVariable('shortwave_radiation_up_cor', 'f4', ('time',), fill_value = -999)
	albedo_theta = root_grp.createVariable('albedo_theta', 'f4', ('time',), fill_value = -999)
	longwave_radiation_down = root_grp.createVariable('longwave_radiation_down', 'f4', ('time',), fill_value = -999)
	longwave_radiation_up = root_grp.createVariable('longwave_radiation_up', 'f4', ('time',), fill_value = -999)
	cloudcover = root_grp.createVariable('cloudcover', 'f4', ('time',), fill_value = -999)
	surface_temp = root_grp.createVariable('surface_temp', 'f4', ('time',), fill_value = -999)
	height_sensor_boom = root_grp.createVariable('height_sensor_boom', 'f4', ('time',), fill_value = -999)
	height_stakes = root_grp.createVariable('height_stakes', 'f4', ('time',), fill_value = -999)
	depth_pressure_transducer = root_grp.createVariable('depth_pressure_transducer', 'f4', ('time',), fill_value = -999)
	depth_pressure_transducer_cor = root_grp.createVariable('depth_pressure_transducer_cor', 'f4', ('time',), fill_value = -999)
	ice_temp_01 = root_grp.createVariable('ice_temp_01', 'f4', ('time',), fill_value = -999)
	ice_temp_02 = root_grp.createVariable('ice_temp_02', 'f4', ('time',), fill_value = -999)
	ice_temp_03 = root_grp.createVariable('ice_temp_03', 'f4', ('time',), fill_value = -999)
	ice_temp_04 = root_grp.createVariable('ice_temp_04', 'f4', ('time',), fill_value = -999)
	ice_temp_05 = root_grp.createVariable('ice_temp_05', 'f4', ('time',), fill_value = -999)
	ice_temp_06 = root_grp.createVariable('ice_temp_06', 'f4', ('time',), fill_value = -999)
	ice_temp_07 = root_grp.createVariable('ice_temp_07', 'f4', ('time',), fill_value = -999)
	ice_temp_08 = root_grp.createVariable('ice_temp_08', 'f4', ('time',), fill_value = -999)
	tilt_east = root_grp.createVariable('tilt_east', 'f4', ('time',), fill_value = -999)
	tilt_north = root_grp.createVariable('tilt_north', 'f4', ('time',), fill_value = -999)
	time_GPS = root_grp.createVariable('time_GPS', 'i4', ('time',), fill_value = -999)
	latitude_GPS = root_grp.createVariable('latitude_GPS', 'f4', ('time',), fill_value = -999)
	longitude_GPS = root_grp.createVariable('longitude_GPS', 'f4', ('time',), fill_value = -999)
	elevation = root_grp.createVariable('elevation', 'f4', ('time',), fill_value = -999)
	hor_dil_prec = root_grp.createVariable('hor_dil_prec', 'f4', ('time',), fill_value = -999)
	logger_temp = root_grp.createVariable('logger_temp', 'f4', ('time',), fill_value = -999)
	fan_current = root_grp.createVariable('fan_current', 'f4', ('time',), fill_value = -999)
	battery_voltage = root_grp.createVariable('battery_voltage', 'f4', ('time',), fill_value = -999)
	ice_velocity_GPS_total = root_grp.createVariable('ice_velocity_GPS_total', 'f4', ('time',), fill_value = -999)
	ice_velocity_GPS_x = root_grp.createVariable('ice_velocity_GPS_x', 'f4', ('time',), fill_value = -999)
	ice_velocity_GPS_y = root_grp.createVariable('ice_velocity_GPS_y', 'f4', ('time',), fill_value = -999)
	
	year.units = '1'
	year.long_name = 'Year'

	month.units = '1'
	month.long_name = 'Month of Year'
	
	day.units = '1'
	day.long_name = 'Day of Month'
	
	hour.units = '1'
	hour.long_name = 'Hour of Day(UTC)'
	
	day_of_year.units = '1'
	day_of_year.long_name = 'Day of Year'
	
	day_of_century.units = '1'
	day_of_century.long_name = 'Day of Century'
	
	air_pressure.units = 'pascal'
	air_pressure.long_name = 'Air Pressure'
	air_pressure.standard_name = 'air_pressure'
	air_pressure.coordinates = 'longitude latitude'
	air_pressure.cell_methods = 'time: mean'

	air_temperature.units = 'kelvin'
	air_temperature.long_name = 'Air Temperature'
	air_temperature.standard_name = 'air_temperature'
	air_temperature.coordinates = 'longitude latitude'
	air_temperature.cell_methods = 'time: mean'
	
	air_temperature_hygroclip.units = 'kelvin'
	air_temperature_hygroclip.long_name = 'Air Temperature HygroClip'
	air_temperature_hygroclip.standard_name = 'air_temperature'
	air_temperature_hygroclip.coordinates = 'longitude latitude'
	air_temperature_hygroclip.cell_methods = 'time: mean'

	relative_humidity_wrtwater.units = '1'
	relative_humidity_wrtwater.long_name = 'Relative Humidity wrt Water'
	relative_humidity_wrtwater.standard_name = 'relative_humidity'
	relative_humidity_wrtwater.coordinates = 'longitude latitude'
	relative_humidity_wrtwater.cell_methods = 'time: mean'

	relative_humidity.units = '1'
	relative_humidity.long_name = 'Relative Humidity'
	relative_humidity.standard_name = 'relative_humidity'
	relative_humidity.coordinates = 'longitude latitude'
	relative_humidity.cell_methods = 'time: mean'

	wind_speed.units = 'meter second-1'
	wind_speed.long_name = 'Wind Speed'
	wind_speed.standard_name = 'wind_speed'
	wind_speed.coordinates = 'longitude latitude'
	wind_speed.cell_methods = 'time: mean'

	wind_direction.units = 'degree'
	wind_direction.long_name = 'Wind Direction'
	wind_direction.standard_name = 'wind_from_direction'
	wind_direction.coordinates = 'longitude latitude'
	wind_direction.cell_methods = 'time: mean'

	shortwave_radiation_down.units = 'watt meter-2'
	shortwave_radiation_down.long_name = 'Shortwave Radiation Down'
	shortwave_radiation_down.standard_name = 'downwelling_shortwave_flux_in_air'
	shortwave_radiation_down.coordinates = 'longitude latitude'
	shortwave_radiation_down.cell_methods = 'time: mean'

	shortwave_radiation_down_cor.units = 'watt meter-2'
	shortwave_radiation_down_cor.long_name = 'Shortwave Radiation Down Cor'
	shortwave_radiation_down_cor.standard_name = 'downwelling_shortwave_flux_in_air'
	shortwave_radiation_down_cor.coordinates = 'longitude latitude'
	shortwave_radiation_down_cor.cell_methods = 'time: mean'

	shortwave_radiation_up.units = 'watt meter-2'
	shortwave_radiation_up.long_name = 'Shortwave Radiation Up'
	shortwave_radiation_up.standard_name = 'upwelling_shortwave_flux_in_air'
	shortwave_radiation_up.coordinates = 'longitude latitude'
	shortwave_radiation_up.cell_methods = 'time: mean'

	shortwave_radiation_up_cor.units = 'watt meter-2'
	shortwave_radiation_up_cor.long_name = 'Shortwave Radiation Up Cor'
	shortwave_radiation_up_cor.standard_name = 'upwelling_shortwave_flux_in_air'
	shortwave_radiation_up_cor.coordinates = 'longitude latitude'
	shortwave_radiation_up_cor.cell_methods = 'time: mean'

	albedo_theta.units = '1'
	albedo_theta.long_name = 'Albedo_theta<70d'
	albedo_theta.standard_name = 'surface_albedo'
	albedo_theta.coordinates = 'longitude latitude'
	albedo_theta.cell_methods = 'time: mean'

	longwave_radiation_down.units = 'watt meter-2'
	longwave_radiation_down.long_name = 'Longwave Radiation Down'
	longwave_radiation_down.standard_name = 'downwelling_longwave_flux_in_air'
	longwave_radiation_down.coordinates = 'longitude latitude'
	longwave_radiation_down.cell_methods = 'time: mean'

	longwave_radiation_up.units = 'watt meter-2'
	longwave_radiation_up.long_name = 'Longwave Radiation Up'
	longwave_radiation_up.standard_name = 'upwelling_longwave_flux_in_air'
	longwave_radiation_up.coordinates = 'longitude latitude'
	longwave_radiation_up.cell_methods = 'time: mean'

	cloudcover.units = '1'
	cloudcover.long_name = 'Cloud Cover'
	#cloudcover.standard_name = ''
	cloudcover.coordinates = 'longitude latitude'
	cloudcover.cell_methods = 'time: mean'

	surface_temp.units = 'kelvin'
	surface_temp.long_name = 'Surface Temperature'
	surface_temp.standard_name = 'surface_temperature'
	surface_temp.coordinates = 'longitude latitude'
	surface_temp.cell_methods = 'time: mean'

	height_sensor_boom.units = 'meter'
	height_sensor_boom.long_name = 'Height Sensor Boom'
	#height_sensor_boom.standard_name = ''
	height_sensor_boom.coordinates = 'longitude latitude'
	height_sensor_boom.cell_methods = 'time: point'

	height_stakes.units = 'meter'
	height_stakes.long_name = 'Height Stakes'
	#height_stakes.standard_name = ''
	height_stakes.coordinates = 'longitude latitude'
	height_stakes.cell_methods = 'time: point'

	depth_pressure_transducer.units = 'meter'
	depth_pressure_transducer.long_name = 'Depth Pressure Transducer'
	#depth_pressure_transducer.standard_name = ''
	depth_pressure_transducer.coordinates = 'longitude latitude'
	depth_pressure_transducer.cell_methods = 'time: point'

	depth_pressure_transducer_cor.units = 'meter'
	depth_pressure_transducer_cor.long_name = 'Depth Pressure Transducer Cor'
	#depth_pressure_transducer_cor.standard_name = ''
	depth_pressure_transducer_cor.coordinates = 'longitude latitude'
	depth_pressure_transducer_cor.cell_methods = 'time: point'

	ice_temp_01.units = 'kelvin'
	ice_temp_01.long_name = 'Ice Temperature 1'
	ice_temp_01.standard_name = 'land_ice_temperature'
	ice_temp_01.coordinates = 'longitude latitude'
	ice_temp_01.cell_methods = 'time: mean'

	ice_temp_02.units = 'kelvin'
	ice_temp_02.long_name = 'Ice Temperature 2'
	ice_temp_02.standard_name = 'land_ice_temperature'
	ice_temp_02.coordinates = 'longitude latitude'
	ice_temp_02.cell_methods = 'time: mean'
	
	ice_temp_03.units = 'kelvin'
	ice_temp_03.long_name = 'Ice Temperature 3'
	ice_temp_03.standard_name = 'land_ice_temperature'
	ice_temp_03.coordinates = 'longitude latitude'
	ice_temp_03.cell_methods = 'time: mean'
	
	ice_temp_04.units = 'kelvin'
	ice_temp_04.long_name = 'Ice Temperature 4'
	ice_temp_04.standard_name = 'land_ice_temperature'
	ice_temp_04.coordinates = 'longitude latitude'
	ice_temp_04.cell_methods = 'time: mean'

	ice_temp_05.units = 'kelvin'
	ice_temp_05.long_name = 'Ice Temperature 5'
	ice_temp_05.standard_name = 'land_ice_temperature'
	ice_temp_05.coordinates = 'longitude latitude'
	ice_temp_05.cell_methods = 'time: mean'

	ice_temp_06.units = 'kelvin'
	ice_temp_06.long_name = 'IceTemperature6'
	ice_temp_06.standard_name = 'land_ice_temperature'
	ice_temp_06.coordinates = 'longitude latitude'
	ice_temp_06.cell_methods = 'time: mean'

	ice_temp_07.units = 'kelvin'
	ice_temp_07.long_name = 'Ice Temperature 7'
	ice_temp_07.standard_name = 'land_ice_temperature'
	ice_temp_07.coordinates = 'longitude latitude'
	ice_temp_07.cell_methods = 'time: mean'

	ice_temp_08.units = 'kelvin'
	ice_temp_08.long_name = 'Ice Temperature 8'
	ice_temp_08.standard_name = 'land_ice_temperature'
	ice_temp_08.coordinates = 'longitude latitude'
	ice_temp_08.cell_methods = 'time: mean'

	tilt_east.units = 'degree'
	tilt_east.long_name = 'Tilt to East'
	#tilt_east.standard_name = ''
	tilt_east.coordinates = 'longitude latitude'
	tilt_east.cell_methods = 'time: point'

	tilt_north.units = 'degree'
	tilt_north.long_name = 'Tilt to North'
	#tilt_north.standard_name = ''
	tilt_north.coordinates = 'longitude latitude'
	tilt_north.cell_methods = 'time: point'

	time_GPS.units = 'UTC'
	time_GPS.long_name = 'Time GPS(hhmmssUTC)'
	time_GPS.standard_name = 'time'

	latitude_GPS.units = 'degrees_north'
	latitude_GPS.long_name = 'Latitude GPS'
	latitude_GPS.standard_name = 'latitude'

	longitude_GPS.units = 'degrees_east'
	longitude_GPS.long_name = 'Longitude GPS'
	longitude_GPS.standard_name = 'longitude'

	elevation.units = 'meter'
	elevation.long_name = 'Elevation GPS'
	#elevation.standard_name = ''
	elevation.coordinates = 'longitude latitude'
	elevation.cell_methods = 'time: point'

	hor_dil_prec.units = '1'
	hor_dil_prec.long_name = 'Horizontal Dilution of Precision GPS'
	#hor_dil_prec.standard_name = ''
	hor_dil_prec.coordinates = 'longitude latitude'
	hor_dil_prec.cell_methods = 'time: point'

	logger_temp.units = 'kelvin'
	logger_temp.long_name = 'Logger Temperature'
	#logger_temp.standard_name = ''
	logger_temp.coordinates = 'longitude latitude'
	logger_temp.cell_methods = 'time: point'

	fan_current.units = 'ampere'
	fan_current.long_name = 'Fan Current'
	#fan_current.standard_name = ''
	fan_current.coordinates = 'longitude latitude'
	fan_current.cell_methods = 'time: point'

	battery_voltage.units = 'volts'
	battery_voltage.long_name = 'Battery Voltage'
	battery_voltage.standard_name = 'battery_voltage'
	battery_voltage.coordinates = 'longitude latitude'
	battery_voltage.cell_methods = 'time: point'

	ice_velocity_GPS_total.units = 'meter second-1'
	ice_velocity_GPS_total.long_name = 'Ice velocity derived from GPS Lat and Long'
	ice_velocity_GPS_total.coordinates = 'longitude latitude'
	ice_velocity_GPS_total.cell_methods = 'time: mean'

	ice_velocity_GPS_x.units = 'meter second-1'
	ice_velocity_GPS_x.long_name = 'x-component of Ice velocity derived from GPS Lat and Long'
	ice_velocity_GPS_x.standard_name = 'land_ice_surface_x_velocity'
	ice_velocity_GPS_x.coordinates = 'longitude latitude'
	ice_velocity_GPS_x.cell_methods = 'time: mean'

	ice_velocity_GPS_y.units = 'meter second-1'
	ice_velocity_GPS_y.long_name = 'y-component of Ice velocity derived from GPS Lat and Long'
	ice_velocity_GPS_y.standard_name = 'land_ice_surface_y_velocity'
	ice_velocity_GPS_y.coordinates = 'longitude latitude'
	ice_velocity_GPS_y.cell_methods = 'time: mean'


	print("converting data...")

	def time_calc_promice():
		delta = datetime(year[j], month[j], day[j], hour[j])-datetime(1970, 1, 1)
		return delta.total_seconds()

	def lat_lon_gps(col_index):
		return (round(float(int(columns[col_index])-((int(columns[col_index])/100)*100))/60, 2) + (int(columns[col_index])/100))

	num_lines =  sum(1 for line in open(args.input_file or args.fl_in) if len(line.strip()) != 0) - 1
	#1 is the number of lines before the data starts in input file

	j = 0
	convert_temp = 273.15
	convert_press = 100
	convert_current = 1000
	check_na = 999.0

	idx_year, idx_month, idx_day, idx_hour, idx_dayofyear, idx_dayofcentury, idx_airpress, idx_airtemp, idx_airtemphygro, idx_rhwrtwater, idx_rh, idx_windspd, idx_winddir, idx_swdn, idx_swdncor = range(15)
	idx_swup, idx_swupcor, idx_albedo, idx_lwdn, idx_lwup, idx_cloudcover, idx_surfacetemp, idx_htsensor, idx_htstakes, idx_depthpress, idx_depthpresscor, idx_icetemp1, idx_icetemp2, idx_icetemp3, idx_icetemp4 = range(15,30)
	idx_icetemp5, idx_icetemp6, idx_icetemp7, idx_icetemp8, idx_tilteast, idx_tiltnorth, idx_timegps, idx_latgps, idx_longps, idx_elevation, idx_hordil, idx_loggertemp, idx_fancurrent, idx_batvolt = range(30, 44)


	ip_file = open(str(args.input_file or args.fl_in), 'r')
	ip_file.readline()

	for line in ip_file:

		if len(line.strip()) == 0:
			continue
		
		else:
			line = line.strip()
			columns = line.split()
			columns = [float(x) for x in columns]
			
			year[j] = columns[idx_year]
			month[j] = columns[idx_month]
			day[j] = columns[idx_day]
			hour[j] = columns[idx_hour]
			day_of_year[j] = columns[idx_dayofyear]
			day_of_century[j] = columns[idx_dayofcentury]

			if columns[idx_airpress] == check_na:
				air_pressure[j] = columns[idx_airpress]
			else:
				air_pressure[j] = columns[idx_airpress] * convert_press

			if columns[idx_airtemp] == check_na:
				air_temperature[j] = columns[idx_airtemp]
			else:
				air_temperature[j] = columns[idx_airtemp] + convert_temp

			if columns[idx_airtemphygro] == check_na:
				air_temperature_hygroclip[j] = columns[idx_airtemphygro]
			else:
				air_temperature_hygroclip[j] = columns[idx_airtemphygro] + convert_temp

			relative_humidity_wrtwater[j] = columns[idx_rhwrtwater]
			relative_humidity[j] = columns[idx_rh]
			wind_speed[j] = columns[idx_windspd]
			wind_direction[j] = columns[idx_winddir]
			shortwave_radiation_down[j] = columns[idx_swdn]
			shortwave_radiation_down_cor[j] = columns[idx_swdncor]
			shortwave_radiation_up[j] = columns[idx_swup]
			shortwave_radiation_up_cor[j] = columns[idx_swupcor]
			albedo_theta[j] = columns[idx_albedo]
			longwave_radiation_down[j] = columns[idx_lwdn]
			longwave_radiation_up[j] = columns[idx_lwup]
			cloudcover[j] = columns[idx_cloudcover]

			if columns[idx_surfacetemp] == check_na:
				surface_temp[j] = columns[idx_surfacetemp]
			else:
				surface_temp[j] = columns[idx_surfacetemp] + convert_temp

			height_sensor_boom[j] = columns[idx_htsensor]
			height_stakes[j] = columns[idx_htstakes]
			depth_pressure_transducer[j] = columns[idx_depthpress]
			depth_pressure_transducer_cor[j] = columns[idx_depthpresscor]

			if columns[idx_icetemp1] == check_na:
				ice_temp_01[j] = columns[idx_icetemp1]
			else:
				ice_temp_01[j] = columns[idx_icetemp1] + convert_temp

			if columns[idx_icetemp2] == check_na:
				ice_temp_02[j] = columns[idx_icetemp2]
			else:
				ice_temp_02[j] = columns[idx_icetemp2] + convert_temp

			if columns[idx_icetemp3] == check_na:
				ice_temp_03[j] = columns[idx_icetemp3]
			else:
				ice_temp_03[j] = columns[idx_icetemp3] + convert_temp

			if columns[idx_icetemp4] == check_na:
				ice_temp_04[j] = columns[idx_icetemp4]
			else:
				ice_temp_04[j] = columns[idx_icetemp4] + convert_temp

			if columns[idx_icetemp5] == check_na:
				ice_temp_05[j] = columns[idx_icetemp5]
			else:
				ice_temp_05[j] = columns[idx_icetemp5] + convert_temp

			if columns[idx_icetemp6] == check_na:
				ice_temp_06[j] = columns[idx_icetemp6]
			else:
				ice_temp_06[j] = columns[idx_icetemp6] + convert_temp

			if columns[idx_icetemp7] == check_na:
				ice_temp_07[j] = columns[idx_icetemp7]
			else:
				ice_temp_07[j] = columns[idx_icetemp7] + convert_temp

			if columns[idx_icetemp8] == check_na:
				ice_temp_08[j] = columns[idx_icetemp8]
			else:
				ice_temp_08[j] = columns[idx_icetemp8] + convert_temp

			tilt_east[j] = columns[idx_tilteast]
			tilt_north[j] = columns[idx_tiltnorth]
			time_GPS[j] = columns[idx_timegps]
			
			if columns[idx_latgps] == check_na:
				latitude_GPS[j] = columns[idx_latgps]
			else:
				latitude_GPS[j] = lat_lon_gps(idx_latgps)

			if columns[idx_longps] == check_na:
				longitude_GPS[j] = columns[idx_longps]
			else:
				longitude_GPS[j] == lat_lon_gps(idx_longps)
			
			elevation[j] = columns[idx_elevation]
			hor_dil_prec[j] = columns[idx_hordil]

			if columns[idx_loggertemp] == check_na:
				logger_temp[j] = columns[idx_loggertemp]
			else:
				logger_temp[j] = columns[idx_loggertemp] + convert_temp

			if columns[idx_fancurrent] == check_na:
				fan_current[j] = columns[idx_fancurrent]
			else:
				fan_current[j] = columns[idx_fancurrent] / convert_current

			battery_voltage[j] = columns[idx_batvolt]

			time[j] = time_calc_promice()
		j += 1


		if ('EGP') in os.path.basename(args.input_file or args.fl_in):
			temp_stn = 'promice_egp'
		elif ('KAN_B') in os.path.basename(args.input_file or args.fl_in):
			temp_stn = 'promice_kanb'
		elif ('KAN_L') in os.path.basename(args.input_file or args.fl_in):
			temp_stn = 'promice_kanl'
		elif ('KAN_M') in os.path.basename(args.input_file or args.fl_in):
			temp_stn = 'promice_kanm'
		elif ('KAN_U') in os.path.basename(args.input_file or args.fl_in):
			temp_stn = 'promice_kanu'
		elif ('KPC_L') in os.path.basename(args.input_file or args.fl_in):
			temp_stn = 'promice_kpcl'
		elif ('KPC_U') in os.path.basename(args.input_file or args.fl_in):
			temp_stn = 'promice_kpcu'
		elif ('MIT') in os.path.basename(args.input_file or args.fl_in):
			temp_stn = 'promice_mit'
		elif ('NUK_K') in os.path.basename(args.input_file or args.fl_in):
			temp_stn = 'promice_nukk'
		elif ('NUK_L') in os.path.basename(args.input_file or args.fl_in):
			temp_stn = 'promice_nukl'
		elif ('NUK_N') in os.path.basename(args.input_file or args.fl_in):
			temp_stn = 'promice_nukn'
		elif ('NUK_U') in os.path.basename(args.input_file or args.fl_in):
			temp_stn = 'promice_nuku'
		elif ('QAS_A') in os.path.basename(args.input_file or args.fl_in):
			temp_stn = 'promice_qasa'
		elif ('QAS_L') in os.path.basename(args.input_file or args.fl_in):
			temp_stn = 'promice_qasl'
		elif ('QAS_M') in os.path.basename(args.input_file or args.fl_in):
			temp_stn = 'promice_qasm'
		elif ('QAS_U') in os.path.basename(args.input_file or args.fl_in):
			temp_stn = 'promice_qasu'
		elif ('SCO_L') in os.path.basename(args.input_file or args.fl_in):
			temp_stn = 'promice_scol'
		elif ('SCO_U') in os.path.basename(args.input_file or args.fl_in):
			temp_stn = 'promice_scou'
		elif ('TAS_A') in os.path.basename(args.input_file or args.fl_in):
			temp_stn = 'promice_tasa'
		elif ('TAS_L') in os.path.basename(args.input_file or args.fl_in):
			temp_stn = 'promice_tasl'
		elif ('TAS_U') in os.path.basename(args.input_file or args.fl_in):
			temp_stn = 'promice_tasu'
		elif ('THU_L') in os.path.basename(args.input_file or args.fl_in):
			temp_stn = 'promice_thul'
		elif ('THU_U') in os.path.basename(args.input_file or args.fl_in):
			temp_stn = 'promice_thuu'
		elif ('UPE_L') in os.path.basename(args.input_file or args.fl_in):
			temp_stn = 'promice_upel'
		elif ('UPE_U') in os.path.basename(args.input_file or args.fl_in):
			temp_stn = 'promice_upeu'
		elif ('CEN') in os.path.basename(args.input_file or args.fl_in):
			temp_stn = 'promice_cen'

	latitude[0] = (station_dict.get(temp_stn)[0])
	longitude[0] = (station_dict.get(temp_stn)[1])

	if args.station_name:
		print('Default station name overrided by user provided station name')
	else:
		for y in range(0, len(station_dict.get(temp_stn)[2])): station_name[y] = (station_dict.get(temp_stn)[2])[y]


	
	l = 0
	while l < num_lines:
		time_bounds[l] = (time[l], time[l]+3600)
		
		temp_date = datetime(year[l], month[l], day[l], hour[l])
		sza[l] = sunpos(temp_date,latitude[0],longitude[0],0)[1]
		l += 1

#Calculating GPS-derived ice velocity
	'''m,n = 0,1
	R = 6373.0		#Approx radius of earth
	while n < num_lines:
		if (latitude_GPS[m] == -999 or latitude_GPS[m+1] == -999 or longitude_GPS[m] == -999 or longitude_GPS[m+1] == -999):
			m += 1
		else:
			lat1 = radians(latitude_GPS[m])
			lon1 = radians(longitude_GPS[m])
			lat2 = radians(latitude_GPS[m+1])
			lon2 = radians(longitude_GPS[m+1])

			dlat = lat2 - lat1
			dlon = lon2 - lon1

			a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
			c = 2 * atan2(sqrt(a), sqrt(1 - a))

			distance = (R*c)*1000		#Multiplied by 1000 to convert km to meters

			ice_velocity_GPS[m] = str(round(distance/3600, 4))		#Divided by 3600 because time change between 2 records is one hour
			m += 1

		n += 1'''

	def ice_velocity(n,o):
		m,p = 0,1
		velocity = [0]*num_lines
		R = 6373.0		#Approx radius of earth
		while p < num_lines:
			if (latitude_GPS[m] == -999 or longitude_GPS[m] == -999 or latitude_GPS[n] == -999 or longitude_GPS[o] == -999):
				pass
			else:
				lat1 = radians(latitude_GPS[m])
				lon1 = radians(longitude_GPS[m])
				lat2 = radians(latitude_GPS[n])
				lon2 = radians(longitude_GPS[o])

				dlat = lat2 - lat1
				dlon = lon2 - lon1

				a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
				c = 2 * atan2(sqrt(a), sqrt(1 - a))

				distance = (R*c)*1000		#Multiplied by 1000 to convert km to meters

				velocity[m] = str(round(distance/3600, 4))		#Divided by 3600 because time change between 2 records is one hour

			m += 1
			n += 1
			o += 1
			p += 1

		return velocity[:]

	ice_velocity_GPS_total[:] = ice_velocity(1,1)
	ice_velocity_GPS_x[:] = ice_velocity(0,1)
	ice_velocity_GPS_y[:] = ice_velocity(1,0)

	root_grp.close()
