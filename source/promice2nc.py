from netCDF4 import Dataset
from datetime import date

def promice2nc(args):

	# NC file setup
	#op_file = str((args.input).split('.')[0])+'.nc'
	op_file = 'promice.nc'
	if args.output:
		op_file = str(args.output)

	if args.format == 3:
		root_grp = Dataset(op_file, 'w', format='NETCDF3_CLASSIC')
	elif args.format == 4:
		root_grp = Dataset(op_file, 'w', format='NETCDF4')
	elif args.format == 5:
		root_grp = Dataset(op_file, 'w', format='NETCDF3_64BIT_DATA')
	elif args.format == 6:
		root_grp = Dataset(op_file, 'w', format='NETCDF3_64BIT_OFFSET')
	elif args.format == 7:
		root_grp = Dataset(op_file, 'w', format='NETCDF4_CLASSIC')
	else:
		root_grp = Dataset(op_file, 'w', format='NETCDF4')
	
	root_grp.title = 'Weather Station Data'
	root_grp.source = 'Surface Observations'
	root_grp.institution = 'Programme for Monitoring of the Greenland Ice Sheet'
	root_grp.reference = 'http://www.promice.dk/home.html'
	root_grp.Conventions = 'CF-1.6'

	# dimension
	root_grp.createDimension('station', 1)
	root_grp.createDimension('time', None)

	# variables
	station_name = root_grp.createVariable('station_name', 'S20', ('station',))
	time = root_grp.createVariable('time', 'i4', ('time',))
	year = root_grp.createVariable('year', 'i4', ('time',))
	month = root_grp.createVariable('month', 'i4', ('time',))
	day = root_grp.createVariable('day', 'i4', ('time',))
	hour = root_grp.createVariable('hour', 'i4', ('time',))
	day_of_year = root_grp.createVariable('day_of_year', 'i4', ('time',))
	day_of_century = root_grp.createVariable('day_of_century', 'i4', ('time',))
	air_pressure = root_grp.createVariable('air_pressure', 'f4', ('time',))
	air_temperature = root_grp.createVariable('air_temperature', 'f4', ('time',))
	air_temperature_hygroclip = root_grp.createVariable('air_temperature_hygroclip', 'f4', ('time',))
	relative_humidity_wrtwater = root_grp.createVariable('relative_humidity_wrtwater', 'f4', ('time',))
	relative_humidity = root_grp.createVariable('relative_humidity', 'f4', ('time',))
	wind_speed = root_grp.createVariable('wind_speed', 'f4', ('time',))
	wind_direction = root_grp.createVariable('wind_direction', 'f4', ('time',))
	shortwave_radiation_down = root_grp.createVariable('shortwave_radiation_down', 'f4', ('time',))
	shortwave_radiation_down_cor = root_grp.createVariable('shortwave_radiation_down_cor', 'f4', ('time',))
	shortwave_radiation_up = root_grp.createVariable('shortwave_radiation_up', 'f4', ('time',))
	shortwave_radiation_up_cor = root_grp.createVariable('shortwave_radiation_up_cor', 'f4', ('time',))
	albedo_theta = root_grp.createVariable('albedo_theta', 'f4', ('time',))
	longwave_radiation_down = root_grp.createVariable('longwave_radiation_down', 'f4', ('time',))
	longwave_radiation_up = root_grp.createVariable('longwave_radiation_up', 'f4', ('time',))
	cloudcover = root_grp.createVariable('cloudcover', 'f4', ('time',))
	surface_temp = root_grp.createVariable('surface_temp', 'f4', ('time',))
	height_sensor_boom = root_grp.createVariable('height_sensor_boom', 'f4', ('time',))
	height_stakes = root_grp.createVariable('height_stakes', 'f4', ('time',))
	depth_pressure_transducer = root_grp.createVariable('depth_pressure_transducer', 'f4', ('time',))
	depth_pressure_transducer_cor = root_grp.createVariable('depth_pressure_transducer_cor', 'f4', ('time',))
	ice_temp_01 = root_grp.createVariable('ice_temp_01', 'f4', ('time',))
	ice_temp_02 = root_grp.createVariable('ice_temp_02', 'f4', ('time',))
	ice_temp_03 = root_grp.createVariable('ice_temp_03', 'f4', ('time',))
	ice_temp_04 = root_grp.createVariable('ice_temp_04', 'f4', ('time',))
	ice_temp_05 = root_grp.createVariable('ice_temp_05', 'f4', ('time',))
	ice_temp_06 = root_grp.createVariable('ice_temp_06', 'f4', ('time',))
	ice_temp_07 = root_grp.createVariable('ice_temp_07', 'f4', ('time',))
	ice_temp_08 = root_grp.createVariable('ice_temp_08', 'f4', ('time',))
	tilt_east = root_grp.createVariable('tilt_east', 'f4', ('time',))
	tilt_north = root_grp.createVariable('tilt_north', 'f4', ('time',))
	time_gps = root_grp.createVariable('time_gps', 'i4', ('time',))
	latitude = root_grp.createVariable('latitude', 'f4', ('time',))
	longitude = root_grp.createVariable('longitude', 'f4', ('time',))
	elevation = root_grp.createVariable('elevation', 'f4', ('time',))
	hor_dil_prec = root_grp.createVariable('hor_dil_prec', 'f4', ('time',))
	logger_temp = root_grp.createVariable('logger_temp', 'f4', ('time',))
	fan_current = root_grp.createVariable('fan_current', 'f4', ('time',))
	battery_voltage = root_grp.createVariable('battery_voltage', 'f4', ('time',))

	station_name.long_name = 'name of station'
	station_name.cf_role = 'timeseries_id'

	time.units = 'seconds since 2007-01-01 00:00:00'
	time.long_name = 'time of measurement'
	time.standard_name = 'time'
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

	time_gps.units = 'UTC'
	time_gps.long_name = 'Time GPS(hhmmssUTC)'
	time_gps.standard_name = 'time'

	latitude.units = 'ddmm'
	latitude.long_name = 'Latitude GPS'
	latitude.standard_name = 'latitude'

	longitude.units = 'ddmm'
	longitude.long_name = 'Longitude GPS'
	longitude.standard_name = 'longitude'

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

	j = 0

	for line in ip_file:
	    
	    line = line.strip()
	    columns = line.split()
	    
	    year[j] = columns[0]
	    month[j] = columns[1]
	    day[j] = columns[2]
	    hour[j] = columns[3]
	    day_of_year[j] = columns[4]
	    day_of_century[j] = columns[5]
	    air_pressure[j] = float(columns[6]) * 100
	    air_temperature[j] = float(columns[7]) + 273.15
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
	    surface_temp[j] = float(columns[21]) + 273.15
	    height_sensor_boom[j] = columns[22]
	    height_stakes[j] = columns[23]
	    depth_pressure_transducer[j] = columns[24]
	    depth_pressure_transducer_cor[j] = columns[25]
	    ice_temp_01[j] = float(columns[26]) + 273.15
	    ice_temp_02[j] = float(columns[27]) + 273.15
	    ice_temp_03[j] = float(columns[28]) + 273.15
	    ice_temp_04[j] = float(columns[29]) + 273.15
	    ice_temp_05[j] = float(columns[30]) + 273.15
	    ice_temp_06[j] = float(columns[31]) + 273.15
	    ice_temp_07[j] = float(columns[32]) + 273.15
	    ice_temp_08[j] = float(columns[33]) + 273.15
	    tilt_east[j] = columns[34]
	    tilt_north[j] = columns[35]
	    time_gps[j] = columns[36]
	    latitude[j] = columns[37]
	    longitude[j] = columns[38]
	    elevation[j] = columns[39]
	    hor_dil_prec[j] = columns[40]
	    logger_temp[j] = float(columns[41]) + 273.15
	    fan_current[j] = float(columns[42] ) / 1000
	    battery_voltage[j] = columns[43]
	    j += 1


	station_name = args.input[0:5]

	f = open(args.input)
	count = 0
	for line in f:
		if line[0] == 'Y':
			continue
		else:
			count += 1
	f.close()

	
	k = 0
	while k < count:
	   	time[k] = ((date(year[k],month[k],day[k])-date(2007, 1, 1)).days)*86400
	   	k += 1


	root_grp.close()
