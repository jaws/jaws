import argparse
from netCDF4 import Dataset
from datetime import date
from astropy.io import ascii

def imau2nc(args):

	data = ascii.read(args.input)

	# NC file setup
	op_file = str((args.input).split('.')[0])+'.nc'
	if args.output:
		op_file = str(args.output)
	root_grp = Dataset(op_file, 'w', format='NETCDF4')
	root_grp.TITLE = 'Weather Station Data'
	root_grp.SOURCE = 'Surface Observations'
	root_grp.INSTITUTION = 'Institute for Marine and Atmospheric Research'
	root_grp.REFERENCE = 'https://www.uu.nl/en/research/imau'
	#root_grp.History = 'Created on '
	#root_grp.CREATED_BY = 'Created by'
	root_grp.Conventions = 'CF-v46'

	# dimension
	root_grp.createDimension('time', args.row_count)

	# variables
	wind_direction = root_grp.createVariable('wind_direction', 'f8', ('time',))
	wind_speed = root_grp.createVariable('wind_speed', 'f8', ('time',))
	wind_speed_max = root_grp.createVariable('wind_speed_max', 'f8', ('time',))
	shortwave_in = root_grp.createVariable('shortwave_in', 'f8', ('time',))
	shortwave_ref = root_grp.createVariable('shortwave_ref', 'f8', ('time',))
	longwave_in = root_grp.createVariable('longwave_in', 'f8', ('time',))
	longwave_out = root_grp.createVariable('longwave_out', 'f8', ('time',))
	temp_cnr1 = root_grp.createVariable('temp_cnr1', 'f8', ('time',))
	air_temperature = root_grp.createVariable('air_temperature', 'f8', ('time',))
	relative_humidity = root_grp.createVariable('relative_humidity', 'f8', ('time',))
	air_pressure = root_grp.createVariable('air_pressure', 'f8', ('time',))
	sonic_alt = root_grp.createVariable('sonic_alt', 'f8', ('time',))
	melt_wire = root_grp.createVariable('melt_wire', 'f8', ('time',))
	snow_temp_01 = root_grp.createVariable('snow_temp_01', 'f8', ('time',))
	snow_temp_02 = root_grp.createVariable('snow_temp_02', 'f8', ('time',))
	snow_temp_03 = root_grp.createVariable('snow_temp_03', 'f8', ('time',))
	snow_temp_04 = root_grp.createVariable('snow_temp_04', 'f8', ('time',))
	snow_temp_05 = root_grp.createVariable('snow_temp_05', 'f8', ('time',))
	snow_temp_06 = root_grp.createVariable('snow_temp_06', 'f8', ('time',))
	snow_temp_07 = root_grp.createVariable('snow_temp_07', 'f8', ('time',))
	snow_temp_08 = root_grp.createVariable('snow_temp_08', 'f8', ('time',))
	temp_tc1 = root_grp.createVariable('temp_tc1', 'f8', ('time',))
	temp_tc2 = root_grp.createVariable('temp_tc2', 'f8', ('time',))
	tilt_pitch = root_grp.createVariable('tilt_pitch', 'f8', ('time',))
	tilt_roll = root_grp.createVariable('tilt_roll', 'f8', ('time',))
	compass_heading = root_grp.createVariable('compass_heading', 'f8', ('time',))
	battery_usage = root_grp.createVariable('battery_usage', 'i4', ('time',))
	memory_usage = root_grp.createVariable('memory_usage', 'f8', ('time',))
	battery_voltage = root_grp.createVariable('battery_voltage', 'f8', ('time',))
	status = root_grp.createVariable('status', 'f8', ('time',))
	gps_height = root_grp.createVariable('gps_height', 'f8', ('time',))
	
	
	time = root_grp.createVariable('time', 'f4', ('time',))


	wind_direction.units = 'deg'
	wind_direction.original_var_name = 'wind direction'
	wind_direction.standard_name = 'wind_from_direction'

	wind_speed.units = 'ms-1'
	wind_speed.original_var_name = 'wind speed'
	wind_speed.standard_name = 'wind_speed'
	
	wind_speed_max.units = 'ms-1'
	wind_speed_max.original_var_name = 'wind speed maximum'
	wind_speed_max.standard_name = 'wind_speed'
	
	shortwave_in.units = 'Wm-2'
	shortwave_in.original_var_name = 'shortwave in'
	shortwave_in.standard_name = ''
	
	shortwave_ref.units = 'Wm-2'
	shortwave_ref.original_var_name = 'shortwave ref'
	shortwave_ref.standard_name = ''
	
	longwave_in.units = 'Wm-2'
	longwave_in.original_var_name = 'longwave in'
	longwave_in.standard_name = ''

	longwave_out.units = 'Wm-2'
	longwave_out.original_var_name = 'longwave out'
	longwave_out.standard_name = ''
	
	temp_cnr1.units = 'degC'
	temp_cnr1.original_var_name = 'temp CNR1'
	temp_cnr1.standard_name = ''

	air_temperature.units = 'degC'
	air_temperature.original_var_name = 'AirTemperature'
	air_temperature.standard_name = 'air_temperature'
	
	relative_humidity.units = '%'
	relative_humidity.original_var_name = 'RelativeHumidity'
	relative_humidity.standard_name = 'relative_humidity'

	air_pressure.units = 'hPa'
	air_pressure.original_var_name = 'AirPressure'
	air_pressure.standard_name = 'air_pressure'

	sonic_alt.units = 'm'
	sonic_alt.original_var_name = 'sonic alt'
	sonic_alt.standard_name = ''

	melt_wire.units = 'm'
	melt_wire.original_var_name = 'melt wire'
	melt_wire.standard_name = 'wind_speed'

	snow_temp_01.units = 'degC'
	snow_temp_01.original_var_name = 'snowTemperature1'
	snow_temp_01.standard_name = 'land_snow_temperature'

	snow_temp_02.units = 'degC'
	snow_temp_02.original_var_name = 'snowTemperature2'
	snow_temp_02.standard_name = 'land_snow_temperature'
	
	snow_temp_03.units = 'degC'
	snow_temp_03.original_var_name = 'snowTemperature3'
	snow_temp_03.standard_name = 'land_snow_temperature'
	
	snow_temp_04.units = 'degC'
	snow_temp_04.original_var_name = 'snowTemperature4'
	snow_temp_04.standard_name = 'land_snow_temperature'

	snow_temp_05.units = 'degC'
	snow_temp_05.original_var_name = 'snowTemperature5'
	snow_temp_05.standard_name = 'land_snow_temperature'

	snow_temp_06.units = 'degC'
	snow_temp_06.original_var_name = 'snowTemperature6'
	snow_temp_06.standard_name = 'land_snow_temperature'

	snow_temp_07.units = 'degC'
	snow_temp_07.original_var_name = 'snowTemperature7'
	snow_temp_07.standard_name = 'land_snow_temperature'

	snow_temp_08.units = 'degC'
	snow_temp_08.original_var_name = 'snowTemperature8'
	snow_temp_08.standard_name = 'land_snow_temperature'

	temp_tc1.units = 'degC'
	temp_tc1.original_var_name = 'temp TC1'
	temp_tc1.standard_name = 'air_temperature'

	temp_tc2.units = 'degC'
	temp_tc2.original_var_name = 'temp TC2'
	temp_tc2.standard_name = 'air_temperature'

	tilt_pitch.units = 'deg'
	tilt_pitch.original_var_name = 'tilt pitch'
	tilt_pitch.standard_name = ''

	tilt_roll.units = 'deg'
	tilt_roll.original_var_name = 'tilt roll'
	tilt_roll.standard_name = ''

	compass_heading.units = 'deg'
	compass_heading.original_var_name = 'compass heading'
	compass_heading.standard_name = ''

	battery_usage.units = '1'
	battery_usage.original_var_name = 'battery usage'
	battery_usage.standard_name = ''

	memory_usage.units = '%'
	memory_usage.original_var_name = 'memory usage'
	memory_usage.standard_name = ''

	battery_voltage.units = 'V'
	battery_voltage.original_var_name = 'BatteryVoltage'
	battery_voltage.standard_name = 'battery_voltage'

	status.units = '1'
	status.original_var_name = 'status'
	status.standard_name = ''

	gps_height.units = 'masl'
	gps_height.original_var_name = 'GPS height'
	gps_height.standard_name = ''

	time.units = 'days since 1995-01-01 00:00:00'
	time.long_name = 'time'
	time.calendar = 'noleap'
	time.bounds = 'time_bnds'
	time.note = 'Created new derived variable'

	root_grp.close()
