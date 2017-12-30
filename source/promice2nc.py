from netCDF4 import Dataset
from datetime import date
from astropy.io import ascii

def promice2nc(args):

	data = ascii.read(args.input)

	# NC file setup
	op_file = str((args.input).split('.')[0])+'.nc'
	if args.output:
		op_file = str(args.output)
	root_grp = Dataset(op_file, 'w', format='NETCDF4')
	root_grp.TITLE = 'Weather Station Data'
	root_grp.SOURCE = 'Surface Observations'
	root_grp.INSTITUTION = 'Programme for Monitoring of the Greenland Ice Sheet'
	root_grp.REFERENCE = 'http://www.promice.dk/home.html'
	#root_grp.History = 'Created on '
	#root_grp.CREATED_BY = 'Created by'
	root_grp.Conventions = 'CF-v46'

	# dimension
	root_grp.createDimension('time', args.row_count)

	# variables
	year = root_grp.createVariable('year', 'i4', ('time',))
	month = root_grp.createVariable('month', 'i4', ('time',))
	day = root_grp.createVariable('day', 'i4', ('time',))
	hour = root_grp.createVariable('hour', 'i4', ('time',))
	day_of_year = root_grp.createVariable('day_of_year', 'i4', ('time',))
	day_of_century = root_grp.createVariable('day_of_century', 'i4', ('time',))
	pressure = root_grp.createVariable('pressure', 'f8', ('time',))
	air_temperature = root_grp.createVariable('air_temperature', 'f8', ('time',))
	air_temperature_hygroclip = root_grp.createVariable('air_temperature_hygroclip', 'f8', ('time',))
	relative_humidity_wrtwater = root_grp.createVariable('relative_humidity_wrtwater', 'f8', ('time',))
	relative_humidity = root_grp.createVariable('relative_humidity', 'f8', ('time',))
	wind_speed = root_grp.createVariable('wind_speed', 'f8', ('time',))
	wind_direction = root_grp.createVariable('wind_direction', 'f8', ('time',))
	shortwave_radiation_down = root_grp.createVariable('shortwave_radiation_down', 'f8', ('time',))
	shortwave_radiation_down_cor = root_grp.createVariable('shortwave_radiation_down_cor', 'f8', ('time',))
	shortwave_radiation_up = root_grp.createVariable('shortwave_radiation_up', 'f8', ('time',))
	shortwave_radiation_up_cor = root_grp.createVariable('shortwave_radiation_up_cor', 'f8', ('time',))
	albedo_theta = root_grp.createVariable('albedo_theta', 'f8', ('time',))
	longwave_radiation_down = root_grp.createVariable('longwave_radiation_down', 'f8', ('time',))
	longwave_radiation_up = root_grp.createVariable('longwave_radiation_up', 'f8', ('time',))
	cloudcover = root_grp.createVariable('cloudcover', 'f8', ('time',))
	surface_temp = root_grp.createVariable('surface_temp', 'f8', ('time',))
	height_sensor_boom = root_grp.createVariable('height_sensor_boom', 'f8', ('time',))
	height_stakes = root_grp.createVariable('height_stakes', 'f8', ('time',))
	depth_pressure_transducer = root_grp.createVariable('depth_pressure_transducer', 'f8', ('time',))
	depth_pressure_transducer_cor = root_grp.createVariable('depth_pressure_transducer_cor', 'f8', ('time',))
	ice_temp_01 = root_grp.createVariable('ice_temp_01', 'f8', ('time',))
	ice_temp_02 = root_grp.createVariable('ice_temp_02', 'f8', ('time',))
	ice_temp_03 = root_grp.createVariable('ice_temp_03', 'f8', ('time',))
	ice_temp_04 = root_grp.createVariable('ice_temp_04', 'f8', ('time',))
	ice_temp_05 = root_grp.createVariable('ice_temp_05', 'f8', ('time',))
	ice_temp_06 = root_grp.createVariable('ice_temp_06', 'f8', ('time',))
	ice_temp_07 = root_grp.createVariable('ice_temp_07', 'f8', ('time',))
	ice_temp_08 = root_grp.createVariable('ice_temp_08', 'f8', ('time',))
	tilt_east = root_grp.createVariable('tilt_east', 'f8', ('time',))
	tilt_north = root_grp.createVariable('tilt_north', 'f8', ('time',))
	time_gps = root_grp.createVariable('time_gps', 'i4', ('time',))
	latitude = root_grp.createVariable('latitude', 'f8', ('time',))
	longitude = root_grp.createVariable('longitude', 'f8', ('time',))
	elevation = root_grp.createVariable('elevation', 'f8', ('time',))
	hor_dil_prec = root_grp.createVariable('hor_dil_prec', 'f8', ('time',))
	logger_temp = root_grp.createVariable('logger_temp', 'f8', ('time',))
	fan_current = root_grp.createVariable('fan_current', 'f8', ('time',))
	battery_voltage = root_grp.createVariable('battery_voltage', 'f8', ('time',))

	
	time = root_grp.createVariable('time', 'f4', ('time',))


	year.units = '1'
	year.original_var_name = 'Year'

	month.units = '1'
	month.original_var_name = 'MonthOfYear'
	
	day.units = '1'
	day.original_var_name = 'DayOfMonth'
	
	hour.units = '1'
	hour.original_var_name = 'HourOfDay(UTC)'
	
	day_of_year.units = '1'
	day_of_year.original_var_name = 'DayOfYear'
	
	day_of_century.units = '1'
	day_of_century.original_var_name = 'DayOfCentury'
	
	pressure.units = 'hPa'
	pressure.original_var_name = 'AirPressure'
	pressure.standard_name = 'air_pressure'

	air_temperature.units = 'degC'
	air_temperature.original_var_name = 'AirTemperature'
	air_temperature.standard_name = 'air_temperature'
	
	air_temperature_hygroclip.units = 'degC'
	air_temperature_hygroclip.original_var_name = 'AirTemperatureHygroClip'
	air_temperature_hygroclip.standard_name = 'air_temperature'

	relative_humidity_wrtwater.units = '%'
	relative_humidity_wrtwater.original_var_name = 'RelativeHumidity_wrtWater'
	relative_humidity_wrtwater.standard_name = 'relative_humidity'

	relative_humidity.units = '%'
	relative_humidity.original_var_name = 'RelativeHumidity'
	relative_humidity.standard_name = 'relative_humidity'

	wind_speed.units = 'm/s'
	wind_speed.original_var_name = 'WindSpeed'
	wind_speed.standard_name = 'wind_speed'

	wind_direction.units = 'deg'
	wind_direction.original_var_name = 'WindDirection'
	wind_direction.standard_name = 'wind_from_direction'

	shortwave_radiation_down.units = 'W m-2'
	shortwave_radiation_down.original_var_name = 'ShortwaveRadiationDown'
	shortwave_radiation_down.standard_name = 'downwelling_shortwave_flux_in_air'

	shortwave_radiation_down_cor.units = 'W m-2'
	shortwave_radiation_down_cor.original_var_name = 'ShortwaveRadiationDown_Cor'
	shortwave_radiation_down_cor.standard_name = 'downwelling_shortwave_flux_in_air'

	shortwave_radiation_up.units = 'W m-2'
	shortwave_radiation_up.original_var_name = 'ShortwaveRadiationUp'
	shortwave_radiation_up.standard_name = 'upwelling_shortwave_flux_in_air'

	shortwave_radiation_up_cor.units = 'W m-2'
	shortwave_radiation_up_cor.original_var_name = 'ShortwaveRadiationUp_Cor'
	shortwave_radiation_up_cor.standard_name = 'upwelling_shortwave_flux_in_air'

	albedo_theta.units = '1'
	albedo_theta.original_var_name = 'Albedo_theta<70d'
	albedo_theta.standard_name = 'surface_albedo'

	longwave_radiation_down.units = 'W m-2'
	longwave_radiation_down.original_var_name = 'LongwaveRadiationDown'
	longwave_radiation_down.standard_name = 'downwelling_longwave_flux_in_air'

	longwave_radiation_up.units = 'W m-2'
	longwave_radiation_up.original_var_name = 'LongwaveRadiationUp'
	longwave_radiation_up.standard_name = 'upwelling_longwave_flux_in_air'

	cloudcover.units = '1'
	cloudcover.original_var_name = 'CloudCover'
	#cloudcover.standard_name = ''

	surface_temp.units = 'degC'
	surface_temp.original_var_name = 'surface_temperature'
	surface_temp.standard_name = 'surface_temperature'

	height_sensor_boom.units = 'm'
	height_sensor_boom.original_var_name = 'HeightSensorBoom'
	#height_sensor_boom.standard_name = ''

	height_stakes.units = 'm'
	height_stakes.original_var_name = 'HeightStakes'
	#height_stakes.standard_name = ''

	depth_pressure_transducer.units = 'm'
	depth_pressure_transducer.original_var_name = 'DepthPressureTransducer'
	#depth_pressure_transducer.standard_name = ''

	depth_pressure_transducer_cor.units = 'm'
	depth_pressure_transducer_cor.original_var_name = 'DepthPressureTransducer_Cor'
	#depth_pressure_transducer_cor.standard_name = ''

	ice_temp_01.units = 'degC'
	ice_temp_01.original_var_name = 'IceTemperature1'
	ice_temp_01.standard_name = 'land_ice_temperature'

	ice_temp_02.units = 'degC'
	ice_temp_02.original_var_name = 'IceTemperature2'
	ice_temp_02.standard_name = 'land_ice_temperature'
	
	ice_temp_03.units = 'degC'
	ice_temp_03.original_var_name = 'IceTemperature3'
	ice_temp_03.standard_name = 'land_ice_temperature'
	
	ice_temp_04.units = 'degC'
	ice_temp_04.original_var_name = 'IceTemperature4'
	ice_temp_04.standard_name = 'land_ice_temperature'

	ice_temp_05.units = 'degC'
	ice_temp_05.original_var_name = 'IceTemperature5'
	ice_temp_05.standard_name = 'land_ice_temperature'

	ice_temp_06.units = 'degC'
	ice_temp_06.original_var_name = 'IceTemperature6'
	ice_temp_06.standard_name = 'land_ice_temperature'

	ice_temp_07.units = 'degC'
	ice_temp_07.original_var_name = 'IceTemperature7'
	ice_temp_07.standard_name = 'land_ice_temperature'

	ice_temp_08.units = 'degC'
	ice_temp_08.original_var_name = 'IceTemperature8'
	ice_temp_08.standard_name = 'land_ice_temperature'

	tilt_east.units = 'deg'
	tilt_east.original_var_name = 'TiltToEast'
	#tilt_east.standard_name = ''

	tilt_north.units = 'deg'
	tilt_north.original_var_name = 'TiltToNorth'
	#tilt_north.standard_name = ''

	time_gps.units = 'UTC'
	time_gps.original_var_name = 'TimeGPS(hhmmssUTC)'
	time_gps.standard_name = 'time'

	latitude.units = 'ddmm'
	latitude.original_var_name = 'LatitudeGPS'
	latitude.standard_name = 'latitude'

	longitude.units = 'ddmm'
	longitude.original_var_name = 'LongitudeGPS'
	longitude.standard_name = 'longitude'

	elevation.units = 'm'
	elevation.original_var_name = 'ElevationGPS'
	#elevation.standard_name = ''

	hor_dil_prec.units = '1'
	hor_dil_prec.original_var_name = 'HorDilOfPrecGPS'
	#hor_dil_prec.standard_name = ''

	logger_temp.units = 'degC'
	logger_temp.original_var_name = 'LoggerTemperature'
	#logger_temp.standard_name = ''

	fan_current.units = 'mA'
	fan_current.original_var_name = 'FanCurrent'
	#fan_current.standard_name = ''

	battery_voltage.units = 'V'
	battery_voltage.original_var_name = 'BatteryVoltage'
	#battery_voltage.standard_name = ''

	time.units = 'days since 2007-01-01 00:00:00'
	time.long_name = 'time'
	time.calendar = 'noleap'
	time.bounds = 'time_bnds'
	time.note = 'Created new derived variable'

	for i in data:
	    year[:] = data['Year'] 
	    month[:] = data['MonthOfYear']
	    day[:] = data['DayOfMonth']
	    hour[:] = data['HourOfDay(UTC)']
	    day_of_year[:] = data['DayOfYear']
	    day_of_century[:] = data['DayOfCentury']
	    pressure[:] = data['AirPressure(hPa)']
	    air_temperature[:] = data['AirTemperature(C)']
	    air_temperature_hygroclip[:] = data['AirTemperatureHygroClip(C)']
	    relative_humidity_wrtwater[:] = data['RelativeHumidity_wrtWater(%)']
	    relative_humidity[:] = data['RelativeHumidity(%)']
	    wind_speed[:] = data['WindSpeed(m/s)']
	    wind_direction[:] = data['WindDirection(d)']
	    shortwave_radiation_down[:] = data['ShortwaveRadiationDown(W/m2)']
	    shortwave_radiation_down_cor[:] = data['ShortwaveRadiationDown_Cor(W/m2)']
	    shortwave_radiation_up[:] = data['ShortwaveRadiationUp(W/m2)']
	    shortwave_radiation_up_cor[:] = data['ShortwaveRadiationUp_Cor(W/m2)']
	    albedo_theta[:] = data['Albedo_theta<70d']
	    longwave_radiation_down[:] = data['LongwaveRadiationDown(W/m2)']
	    longwave_radiation_up[:] = data['LongwaveRadiationUp(W/m2)']
	    cloudcover[:] = data['CloudCover']
	    surface_temp[:] = data['SurfaceTemperature(C)']
	    height_sensor_boom[:] = data['HeightSensorBoom(m)'] 
	    height_stakes[:] = data['HeightStakes(m)'] 
	    depth_pressure_transducer[:] = data['DepthPressureTransducer(m)'] 
	    depth_pressure_transducer_cor[:] = data['DepthPressureTransducer_Cor(m)'] 
	    ice_temp_01[:] = data['IceTemperature1(C)'] 
	    ice_temp_02[:] = data['IceTemperature2(C)'] 
	    ice_temp_03[:] = data['IceTemperature3(C)'] 
	    ice_temp_04[:] = data['IceTemperature4(C)'] 
	    ice_temp_05[:] = data['IceTemperature5(C)'] 
	    ice_temp_06[:] = data['IceTemperature6(C)'] 
	    ice_temp_07[:] = data['IceTemperature7(C)'] 
	    ice_temp_08[:] = data['IceTemperature8(C)'] 
	    tilt_east[:] = data['TiltToEast(d)'] 
	    tilt_north[:] = data['TiltToNorth(d)'] 
	    time_gps[:] = data['TimeGPS(hhmmssUTC)'] 
	    latitude[:] = data['LatitudeGPS(ddmm)'] 
	    longitude[:] = data['LongitudeGPS(ddmm)'] 
	    elevation[:] = data['ElevationGPS(m)'] 
	    hor_dil_prec[:] = data['HorDilOfPrecGPS'] 
	    logger_temp[:] = data['LoggerTemperature(C)'] 
	    fan_current[:] = data['FanCurrent(mA)'] 
	    battery_voltage[:] = data['BatteryVoltage(V)']

	j = 0

	while j < args.row_count:
	   	time[j] = (date(year[j],month[j],day[j])-date(2007, 1, 1)).days
	   	j += 1


	root_grp.close()
