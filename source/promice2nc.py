from netCDF4 import Dataset
from datetime import date
import os

def promice2nc(args):

	# NC file setup
	op_file = str((os.path.basename(args.input)).split('.')[0])+'.nc'
	
	if args.output:
		op_file = str(args.output)

	if args.format3 == 1:
		root_grp = Dataset(op_file, 'w', format='NETCDF3_CLASSIC')
	elif args.format4 == 1:
		root_grp = Dataset(op_file, 'w', format='NETCDF4')
	elif args.format5 == 1:
		root_grp = Dataset(op_file, 'w', format='NETCDF3_64BIT_DATA')
	elif args.format6 == 1:
		root_grp = Dataset(op_file, 'w', format='NETCDF3_64BIT_OFFSET')
	elif args.format7 == 1:
		root_grp = Dataset(op_file, 'w', format='NETCDF4_CLASSIC')
	else:
		root_grp = Dataset(op_file, 'w', format='NETCDF4')
	
	root_grp.station_name = os.path.basename(args.input)[0:5]
	root_grp.title = 'Weather Station Data'
	root_grp.source = 'Surface Observations'
	root_grp.institution = 'Programme for Monitoring of the Greenland Ice Sheet'
	root_grp.reference = 'http://www.promice.dk/home.html'
	root_grp.Conventions = 'CF-1.6'

	# dimension
	#root_grp.createDimension('station', 1)
	root_grp.createDimension('time', None)
	root_grp.createDimension('nbnd', 2)
	
	# variables
	#station_name = root_grp.createVariable('station_name', 'S20', ('station',))
	latitude = root_grp.createVariable('latitude', 'f4')
	longitude = root_grp.createVariable('longitude', 'f4')
	time = root_grp.createVariable('time', 'i4', ('time',))
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
	time_bounds = root_grp.createVariable('time_bounds', 'i4', ('time','nbnd'))
	
	#station_name.long_name = 'name of station'
	#station_name.cf_role = 'timeseries_id'

	latitude.units = 'degrees_north'
	latitude.standard_name = 'latitude'

	longitude.units = 'degrees_east'
	longitude.standard_name = 'longitude'

	time.units = 'seconds since 2007-01-01 00:00:00'
	time.long_name = 'time of measurement'
	time.standard_name = 'time'
	time.bounds = 'time_bounds'
	time.calendar = 'standard'
	
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

	air_temperature.units = 'kelvin'
	air_temperature.long_name = 'Air Temperature'
	air_temperature.standard_name = 'air_temperature'
	
	air_temperature_hygroclip.units = 'kelvin'
	air_temperature_hygroclip.long_name = 'Air Temperature HygroClip'
	air_temperature_hygroclip.standard_name = 'air_temperature'

	relative_humidity_wrtwater.units = '1'
	relative_humidity_wrtwater.long_name = 'Relative Humidity wrt Water'
	relative_humidity_wrtwater.standard_name = 'relative_humidity'

	relative_humidity.units = '1'
	relative_humidity.long_name = 'Relative Humidity'
	relative_humidity.standard_name = 'relative_humidity'

	wind_speed.units = 'meter second-1'
	wind_speed.long_name = 'Wind Speed'
	wind_speed.standard_name = 'wind_speed'

	wind_direction.units = 'degree'
	wind_direction.long_name = 'Wind Direction'
	wind_direction.standard_name = 'wind_from_direction'

	shortwave_radiation_down.units = 'watt meter-2'
	shortwave_radiation_down.long_name = 'Shortwave Radiation Down'
	shortwave_radiation_down.standard_name = 'downwelling_shortwave_flux_in_air'

	shortwave_radiation_down_cor.units = 'watt meter-2'
	shortwave_radiation_down_cor.long_name = 'Shortwave Radiation Down Cor'
	shortwave_radiation_down_cor.standard_name = 'downwelling_shortwave_flux_in_air'

	shortwave_radiation_up.units = 'watt meter-2'
	shortwave_radiation_up.long_name = 'Shortwave Radiation Up'
	shortwave_radiation_up.standard_name = 'upwelling_shortwave_flux_in_air'

	shortwave_radiation_up_cor.units = 'watt meter-2'
	shortwave_radiation_up_cor.long_name = 'Shortwave Radiation Up Cor'
	shortwave_radiation_up_cor.standard_name = 'upwelling_shortwave_flux_in_air'

	albedo_theta.units = '1'
	albedo_theta.long_name = 'Albedo_theta<70d'
	albedo_theta.standard_name = 'surface_albedo'

	longwave_radiation_down.units = 'watt meter-2'
	longwave_radiation_down.long_name = 'Longwave Radiation Down'
	longwave_radiation_down.standard_name = 'downwelling_longwave_flux_in_air'

	longwave_radiation_up.units = 'watt meter-2'
	longwave_radiation_up.long_name = 'Longwave Radiation Up'
	longwave_radiation_up.standard_name = 'upwelling_longwave_flux_in_air'

	cloudcover.units = '1'
	cloudcover.long_name = 'Cloud Cover'
	#cloudcover.standard_name = ''

	surface_temp.units = 'kelvin'
	surface_temp.long_name = 'Surface Temperature'
	surface_temp.standard_name = 'surface_temperature'

	height_sensor_boom.units = 'meter'
	height_sensor_boom.long_name = 'Height Sensor Boom'
	#height_sensor_boom.standard_name = ''

	height_stakes.units = 'meter'
	height_stakes.long_name = 'Height Stakes'
	#height_stakes.standard_name = ''

	depth_pressure_transducer.units = 'meter'
	depth_pressure_transducer.long_name = 'Depth Pressure Transducer'
	#depth_pressure_transducer.standard_name = ''

	depth_pressure_transducer_cor.units = 'meter'
	depth_pressure_transducer_cor.long_name = 'Depth Pressure Transducer Cor'
	#depth_pressure_transducer_cor.standard_name = ''

	ice_temp_01.units = 'kelvin'
	ice_temp_01.long_name = 'Ice Temperature 1'
	ice_temp_01.standard_name = 'land_ice_temperature'

	ice_temp_02.units = 'kelvin'
	ice_temp_02.long_name = 'Ice Temperature 2'
	ice_temp_02.standard_name = 'land_ice_temperature'
	
	ice_temp_03.units = 'kelvin'
	ice_temp_03.long_name = 'Ice Temperature 3'
	ice_temp_03.standard_name = 'land_ice_temperature'
	
	ice_temp_04.units = 'kelvin'
	ice_temp_04.long_name = 'Ice Temperature 4'
	ice_temp_04.standard_name = 'land_ice_temperature'

	ice_temp_05.units = 'kelvin'
	ice_temp_05.long_name = 'Ice Temperature 5'
	ice_temp_05.standard_name = 'land_ice_temperature'

	ice_temp_06.units = 'kelvin'
	ice_temp_06.long_name = 'IceTemperature6'
	ice_temp_06.standard_name = 'land_ice_temperature'

	ice_temp_07.units = 'kelvin'
	ice_temp_07.long_name = 'Ice Temperature 7'
	ice_temp_07.standard_name = 'land_ice_temperature'

	ice_temp_08.units = 'kelvin'
	ice_temp_08.long_name = 'Ice Temperature 8'
	ice_temp_08.standard_name = 'land_ice_temperature'

	tilt_east.units = 'degree'
	tilt_east.long_name = 'Tilt to East'
	#tilt_east.standard_name = ''

	tilt_north.units = 'degree'
	tilt_north.long_name = 'Tilt to North'
	#tilt_north.standard_name = ''

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

	hor_dil_prec.units = '1'
	hor_dil_prec.long_name = 'Hor Dil of Prec GPS'
	#hor_dil_prec.standard_name = ''

	logger_temp.units = 'kelvin'
	logger_temp.long_name = 'Logger Temperature'
	#logger_temp.standard_name = ''

	fan_current.units = 'ampere'
	fan_current.long_name = 'Fan Current'
	#fan_current.standard_name = ''

	battery_voltage.units = 'volts'
	battery_voltage.long_name = 'Battery Voltage'
	battery_voltage.standard_name = 'battery_voltage'


	ip_file = open(str(args.input), 'r')
	ip_file.readline()

	print "converting data..."

	j = 0

	for line in ip_file:

		if len(line.strip()) == 0:
			continue
		
		else:
			line = line.strip()
			columns = line.split()
			
			year[j] = columns[0]
			month[j] = columns[1]
			day[j] = columns[2]
			hour[j] = columns[3]
			day_of_year[j] = columns[4]
			day_of_century[j] = columns[5]

			if columns[6] == '-999':
				air_pressure[j] = columns[6]
			else:
				air_pressure[j] = float(columns[6]) * 100

			if columns[7] == '-999':
				air_temperature[j] = columns[7]
			else:
				air_temperature[j] = float(columns[7]) + 273.15

			if columns[8] == '-999':
				air_temperature_hygroclip[j] = columns[8]
			else:
				air_temperature_hygroclip[j] = float(columns[8]) + 273.15

			relative_humidity_wrtwater[j] = columns[9]
			relative_humidity[j] = columns[10]
			wind_speed[j] = columns[11]
			wind_direction[j] = columns[12]
			shortwave_radiation_down[j] = columns[13]
			shortwave_radiation_down_cor[j] = columns[14]
			shortwave_radiation_up[j] = columns[15]
			shortwave_radiation_up_cor[j] = columns[16]
			albedo_theta[j] = columns[17]
			longwave_radiation_down[j] = columns[18]
			longwave_radiation_up[j] = columns[19]
			cloudcover[j] = columns[20]

			if columns[21] == '-999':
				surface_temp[j] = columns[21]
			else:
				surface_temp[j] = float(columns[21]) + 273.15

			height_sensor_boom[j] = columns[22]
			height_stakes[j] = columns[23]
			depth_pressure_transducer[j] = columns[24]
			depth_pressure_transducer_cor[j] = columns[25]

			if columns[26] == '-999':
				ice_temp_01[j] = columns[26]
			else:
				ice_temp_01[j] = float(columns[26]) + 273.15

			if columns[27] == '-999':
				ice_temp_02[j] = columns[27]
			else:
				ice_temp_02[j] = float(columns[27]) + 273.15

			if columns[28] == '-999':
				ice_temp_03[j] = columns[28]
			else:
				ice_temp_03[j] = float(columns[28]) + 273.15

			if columns[29] == '-999':
				ice_temp_04[j] = columns[29]
			else:
				ice_temp_04[j] = float(columns[29]) + 273.15

			if columns[30] == '-999':
				ice_temp_05[j] = columns[30]
			else:
				ice_temp_05[j] = float(columns[30]) + 273.15

			if columns[31] == '-999':
				ice_temp_06[j] = columns[31]
			else:
				ice_temp_06[j] = float(columns[31]) + 273.15

			if columns[32] == '-999':
				ice_temp_07[j] = columns[32]
			else:
				ice_temp_07[j] = float(columns[32]) + 273.15

			if columns[33] == '-999':
				ice_temp_08[j] = columns[33]
			else:
				ice_temp_08[j] = float(columns[33]) + 273.15

			tilt_east[j] = columns[34]
			tilt_north[j] = columns[35]
			time_GPS[j] = columns[36]
			
			if columns[37] == '-999':
				latitude_GPS[j] = columns[37]
			else:
				columns[37] = float(columns[37])
				latitude_GPS[j] = (round(float(int(columns[37])-((int(columns[37])/100)*100))/60, 2) + (int(columns[37])/100))

			if columns[38] == '-999':
				longitude_GPS[j] = columns[38]
			else:
				columns[38] = float(columns[38])
				longitude_GPS[j] == (round(float(int(columns[38])-((int(columns[38])/100)*100))/60, 2) + (int(columns[38])/100))
			
			elevation[j] = columns[39]
			hor_dil_prec[j] = columns[40]

			if columns[41] == '-999':
				logger_temp[j] = columns[41]
			else:
				logger_temp[j] = float(columns[41]) + 273.15

			if columns[42] == '-999':
				fan_current[j] = columns[42]
			else:
				fan_current[j] = float(columns[42] ) / 1000

			battery_voltage[j] = columns[43]
		j += 1


	#station_name = args.input[0:5]
	if os.path.basename(args.input)[0:5] == 'EGP_h':
		latitude[0] = 75.6247
		longitude[0] = 35.9748
	elif os.path.basename(args.input)[0:5] == 'KAN_B':
		latitude[0] = 67.1252
		longitude[0] = 50.1832
	elif os.path.basename(args.input)[0:5] == 'KAN_L':
		latitude[0] = 67.0955
		longitude[0] = 49.9513
	elif os.path.basename(args.input)[0:5] == 'KAN_M':
		latitude[0] =  67.0670
		longitude[0] = 48.8355
	elif os.path.basename(args.input)[0:5] == 'KAN_U':
		latitude[0] = 67.0003
		longitude[0] = 47.0253
	elif os.path.basename(args.input)[0:5] == 'KPC_L':
		latitude[0] = 79.9108
		longitude[0] = 24.0828
	elif os.path.basename(args.input)[0:5] == 'KPC_U':
		latitude[0] = 79.8347
		longitude[0] = 25.1662
	elif os.path.basename(args.input)[0:5] == 'MIT_h':
		latitude[0] =  65.6922
		longitude[0] =  37.8280
	elif os.path.basename(args.input)[0:5] == 'NUK_K':
		latitude[0] = 64.1623
		longitude[0] = 51.3587
	elif os.path.basename(args.input)[0:5] == 'NUK_L':
		latitude[0] = 64.4822
		longitude[0] = 49.5358
	elif os.path.basename(args.input)[0:5] == 'NUK_N':
		latitude[0] = 64.9452
		longitude[0] = 49.8850
	elif os.path.basename(args.input)[0:5] == 'NUK_U':
		latitude[0] = 64.5108
		longitude[0] = 49.2692
	elif os.path.basename(args.input)[0:5] == 'QAS_A':
		latitude[0] =  61.2430
		longitude[0] = 46.7328
	elif os.path.basename(args.input)[0:5] == 'QAS_L':
		latitude[0] = 61.0308
		longitude[0] =  46.8493
	elif os.path.basename(args.input)[0:5] == 'QAS_M':
		latitude[0] = 61.0998
		longitude[0] = 46.8330
	elif os.path.basename(args.input)[0:5] == 'QAS_U':
		latitude[0] = 61.1753
		longitude[0] = 46.8195
	elif os.path.basename(args.input)[0:5] == 'SCO_L':
		latitude[0] =  72.2230
		longitude[0] =  26.8182
	elif os.path.basename(args.input)[0:5] == 'SCO_U':
		latitude[0] = 72.3933
		longitude[0] = 27.2333
	elif os.path.basename(args.input)[0:5] == 'TAS_A':
		latitude[0] = 65.7790
		longitude[0] = 38.8995
	elif os.path.basename(args.input)[0:5] == 'TAS_L':
		latitude[0] = 65.6402
		longitude[0] =  38.8987
	elif os.path.basename(args.input)[0:5] == 'TAS_U':
		latitude[0] =  65.6978
		longitude[0] = 38.8668
	elif os.path.basename(args.input)[0:5] == 'THU_L':
		latitude[0] = 76.3998
		longitude[0] = 68.2665
	elif os.path.basename(args.input)[0:5] == 'THU_U':
		latitude[0] =  76.4197
		longitude[0] = 68.1463
	elif os.path.basename(args.input)[0:5] == 'UPE_L':
		latitude[0] = 72.8932
		longitude[0] =  54.2955
	elif os.path.basename(args.input)[0:5] == 'UPE_U':
		latitude[0] = 72.8878
		longitude[0] = 53.5783
	elif os.path.basename(args.input)[0:5] == 'CEN_h':
		latitude[0] = 0
		longitude[0] = 0
	

	f = open(args.input)
	count = 0
	for line in f:
		if line[0] == 'Y':
			continue
		elif len(line.strip()) == 0:
			continue
		else:
			count += 1
	f.close()

	print "calculating time variable..."
	k = 0
	while k < count:
		if hour[k] == 0:
			time[k] = ((date(year[k],month[k],day[k])-date(2007, 1, 1)).days)*86400
			k += 1
		elif hour[k] == 1:
			time[k] = ((date(year[k],month[k],day[k])-date(2007, 1, 1)).days)*86400 + (3600*1)
			k += 1
		elif hour[k] == 2:
			time[k] = ((date(year[k],month[k],day[k])-date(2007, 1, 1)).days)*86400 + (3600*2)
			k += 1
		elif hour[k] == 3:
			time[k] = ((date(year[k],month[k],day[k])-date(2007, 1, 1)).days)*86400 + (3600*3)
			k += 1
		elif hour[k] == 4:
			time[k] = ((date(year[k],month[k],day[k])-date(2007, 1, 1)).days)*86400 + (3600*4)
			k += 1
		elif hour[k] == 5:
			time[k] = ((date(year[k],month[k],day[k])-date(2007, 1, 1)).days)*86400 + (3600*5)
			k += 1
		elif hour[k] == 6:
			time[k] = ((date(year[k],month[k],day[k])-date(2007, 1, 1)).days)*86400 + (3600*6)
			k += 1
		elif hour[k] == 7:
			time[k] = ((date(year[k],month[k],day[k])-date(2007, 1, 1)).days)*86400 + (3600*7)
			k += 1
		elif hour[k] == 8:
			time[k] = ((date(year[k],month[k],day[k])-date(2007, 1, 1)).days)*86400 + (3600*8)
			k += 1
		elif hour[k] == 9:
			time[k] = ((date(year[k],month[k],day[k])-date(2007, 1, 1)).days)*86400 + (3600*9)
			k += 1
		elif hour[k] == 10:
			time[k] = ((date(year[k],month[k],day[k])-date(2007, 1, 1)).days)*86400 + (3600*10)
			k += 1
		elif hour[k] == 11:
			time[k] = ((date(year[k],month[k],day[k])-date(2007, 1, 1)).days)*86400 + (3600*11)
			k += 1
		elif hour[k] == 12:
			time[k] = ((date(year[k],month[k],day[k])-date(2007, 1, 1)).days)*86400 + (3600*12)
			k += 1
		elif hour[k] == 13:
			time[k] = ((date(year[k],month[k],day[k])-date(2007, 1, 1)).days)*86400 + (3600*13)
			k += 1
		elif hour[k] == 14:
			time[k] = ((date(year[k],month[k],day[k])-date(2007, 1, 1)).days)*86400 + (3600*14)
			k += 1
		elif hour[k] == 15:
			time[k] = ((date(year[k],month[k],day[k])-date(2007, 1, 1)).days)*86400 + (3600*15)
			k += 1
		elif hour[k] == 16:
			time[k] = ((date(year[k],month[k],day[k])-date(2007, 1, 1)).days)*86400 + (3600*16)
			k += 1
		elif hour[k] == 17:
			time[k] = ((date(year[k],month[k],day[k])-date(2007, 1, 1)).days)*86400 + (3600*17)
			k += 1
		elif hour[k] == 18:
			time[k] = ((date(year[k],month[k],day[k])-date(2007, 1, 1)).days)*86400 + (3600*18)
			k += 1
		elif hour[k] == 19:
			time[k] = ((date(year[k],month[k],day[k])-date(2007, 1, 1)).days)*86400 + (3600*19)
			k += 1
		elif hour[k] == 20:
			time[k] = ((date(year[k],month[k],day[k])-date(2007, 1, 1)).days)*86400 + (3600*20)
			k += 1
		elif hour[k] == 21:
			time[k] = ((date(year[k],month[k],day[k])-date(2007, 1, 1)).days)*86400 + (3600*21)
			k += 1
		elif hour[k] == 22:
			time[k] = ((date(year[k],month[k],day[k])-date(2007, 1, 1)).days)*86400 + (3600*22)
			k += 1
		elif hour[k] == 23:
			time[k] = ((date(year[k],month[k],day[k])-date(2007, 1, 1)).days)*86400 + (3600*23)
			k += 1
		
	l = 0
	while l < count:
		time_bounds[l] = (time[l], time[l]+3600)
		l += 1

	root_grp.close()
