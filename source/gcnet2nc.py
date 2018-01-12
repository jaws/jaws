from netCDF4 import Dataset
from datetime import date
import os

def gcnet2nc(args):

	'''f = open(args.input)
	count, a = 0, 0
	while a < 54:
		f.readline()
		a += 1
	for line in f:
		count += 1
	f.close()'''

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
	
	root_grp.title = 'Surface Radiation Data from Greenland Climate Network'
	root_grp.source = 'Surface Observations'
	root_grp.institution = 'Cooperative Institute for Research in Enviornmental Sciences'
	root_grp.reference = 'http://cires.colorado.edu/science/groups/steffen/gcnet/'
	root_grp.URL = 'http://cires.colorado.edu/science/groups/steffen/gcnet/'
	root_grp.Conventions = 'CF-1.6'

	# dimension
	root_grp.createDimension('latitude', 1)
	root_grp.createDimension('longitude', 1)
	root_grp.createDimension('time', None)
	root_grp.createDimension('nbnd', 2)
	root_grp.createDimension('station', 1)

	# variables
	latitude = root_grp.createVariable('latitude', 'f4', ('latitude',))
	longitude = root_grp.createVariable('longitude', 'f4', ('longitude',))
	time = root_grp.createVariable('time', 'i4', ('time',))
	time_bounds = root_grp.createVariable('time_bounds', 'i4', ('time','nbnd'))
	station_number = root_grp.createVariable('station_number', 'i1', ('station',))
	year = root_grp.createVariable('year', 'i4', ('time',))
	julian_decimal_time = root_grp.createVariable('julian_decimal_time', 'f4', ('time',))
	sw_down = root_grp.createVariable('sw_down', 'f4', ('time',))
	sw_up = root_grp.createVariable('sw_up', 'f4', ('time',))
	net_radiation = root_grp.createVariable('net_radiation', 'f4', ('time',))
	temperature_tc_1 = root_grp.createVariable('temperature_tc_1', 'f4', ('time',))
	temperature_tc_2 = root_grp.createVariable('temperature_tc_2', 'f4', ('time',))
	temperature_cs500_1 = root_grp.createVariable('temperature_cs500_1', 'f4', ('time',))
	temperature_cs500_2 = root_grp.createVariable('temperature_cs500_2', 'f4', ('time',))
	relative_humidity_1 = root_grp.createVariable('relative_humidity_1', 'f4', ('time',))
	relative_humidity_2 = root_grp.createVariable('relative_humidity_2', 'f4', ('time',))
	u1_wind_speed = root_grp.createVariable('u1_wind_speed', 'f4', ('time',))
	u2_wind_speed = root_grp.createVariable('u2_wind_speed', 'f4', ('time',))
	u_direction_1 = root_grp.createVariable('u_direction_1', 'f4', ('time',))
	u_direction_2 = root_grp.createVariable('u_direction_2', 'f4', ('time',))
	atmos_pressure = root_grp.createVariable('atmos_pressure', 'f4', ('time',))
	snow_height_1 = root_grp.createVariable('snow_height_1', 'f4', ('time',))
	snow_height_2 = root_grp.createVariable('snow_height_2', 'f4', ('time',))
	t_snow_01 = root_grp.createVariable('t_snow_01', 'f4', ('time',))
	t_snow_02 = root_grp.createVariable('t_snow_02', 'f4', ('time',))
	t_snow_03 = root_grp.createVariable('t_snow_03', 'f4', ('time',))
	t_snow_04 = root_grp.createVariable('t_snow_04', 'f4', ('time',))
	t_snow_05 = root_grp.createVariable('t_snow_05', 'f4', ('time',))
	t_snow_06 = root_grp.createVariable('t_snow_06', 'f4', ('time',))
	t_snow_07 = root_grp.createVariable('t_snow_07', 'f4', ('time',))
	t_snow_08 = root_grp.createVariable('t_snow_08', 'f4', ('time',))
	t_snow_09 = root_grp.createVariable('t_snow_09', 'f4', ('time',))
	t_snow_10 = root_grp.createVariable('t_snow_10', 'f4', ('time',))
	battery_voltage = root_grp.createVariable('battery_voltage', 'f4', ('time',))
	sw_down_max = root_grp.createVariable('sw_down_max', 'f4', ('time',))
	sw_up_max = root_grp.createVariable('sw_up_max', 'f4', ('time',))
	net_radiation_max = root_grp.createVariable('net_radiation_max', 'f4', ('time',))
	max_air_temperature_1 = root_grp.createVariable('max_air_temperature_1', 'f4', ('time',))
	max_air_temperature_2 = root_grp.createVariable('max_air_temperature_2', 'f4', ('time',))
	min_air_temperature_1 = root_grp.createVariable('min_air_temperature_1', 'f4', ('time',))
	min_air_temperature_2 = root_grp.createVariable('min_air_temperature_2', 'f4', ('time',))
	max_windspeed_u1 = root_grp.createVariable('max_windspeed_u1', 'f4', ('time',))
	max_windspeed_u2 = root_grp.createVariable('max_windspeed_u2', 'f4', ('time',))
	stdev_windspeed_u1 = root_grp.createVariable('stdev_windspeed_u1', 'f4', ('time',))
	stdev_windspeed_u2 = root_grp.createVariable('stdev_windspeed_u2', 'f4', ('time',))
	ref_temperature = root_grp.createVariable('ref_temperature', 'f4', ('time',))
	windspeed_2m = root_grp.createVariable('windspeed_2m', 'f4', ('time',))
	windspeed_10m = root_grp.createVariable('windspeed_10m', 'f4', ('time',))
	wind_sensor_height_1 = root_grp.createVariable('wind_sensor_height_1', 'f4', ('time',))
	wind_sensor_height_2 = root_grp.createVariable('wind_sensor_height_2', 'f4', ('time',))
	albedo = root_grp.createVariable('albedo', 'f4', ('time',))
	zenith_angle = root_grp.createVariable('zenith_angle', 'f4', ('time',))
	qc1 = root_grp.createVariable('qc1', 'i4', ('time',))
	qc9 = root_grp.createVariable('qc9', 'i4', ('time',))
	qc17 = root_grp.createVariable('qc17', 'i4', ('time',))
	qc25 = root_grp.createVariable('qc25', 'i4', ('time',))
	
	qc_swdn = root_grp.createVariable('qc_swdn', 'i1', ('time',))
	qc_swup = root_grp.createVariable('qc_swup', 'i1', ('time',))
	qc_netradiation = root_grp.createVariable('qc_netradiation', 'i1', ('time',))
	qc_ttc1 = root_grp.createVariable('qc_ttc1', 'i1', ('time',))
	qc_ttc2 = root_grp.createVariable('qc_ttc2', 'i1', ('time',))
	qc_tcs1 = root_grp.createVariable('qc_tcs1', 'i1', ('time',))
	qc_tcs2 = root_grp.createVariable('qc_tcs2', 'i1', ('time',))
	qc_rh1 = root_grp.createVariable('qc_rh1', 'i1', ('time',))
	qc_rh2 = root_grp.createVariable('qc_rh2', 'i1', ('time',))
	qc_u1 = root_grp.createVariable('qc_u1', 'i1', ('time',))
	qc_u2 = root_grp.createVariable('qc_u2', 'i1', ('time',))
	qc_ud1 = root_grp.createVariable('qc_ud1', 'i1', ('time',))
	qc_ud2 = root_grp.createVariable('qc_ud2', 'i1', ('time',))
	qc_pressure = root_grp.createVariable('qc_pressure', 'i1', ('time',))
	qc_snowheight1 = root_grp.createVariable('qc_snowheight1', 'i1', ('time',))
	qc_snowheight2 = root_grp.createVariable('qc_snowheight2', 'i1', ('time',))
	qc_tsnow1 = root_grp.createVariable('qc_tsnow1', 'i1', ('time',))
	qc_tsnow2 = root_grp.createVariable('qc_tsnow2', 'i1', ('time',))
	qc_tsnow3 = root_grp.createVariable('qc_tsnow3', 'i1', ('time',))
	qc_tsnow4 = root_grp.createVariable('qc_tsnow4', 'i1', ('time',))
	qc_tsnow5 = root_grp.createVariable('qc_tsnow5', 'i1', ('time',))
	qc_tsnow6 = root_grp.createVariable('qc_tsnow6', 'i1', ('time',))
	qc_tsnow7 = root_grp.createVariable('qc_tsnow7', 'i1', ('time',))
	qc_tsnow8 = root_grp.createVariable('qc_tsnow8', 'i1', ('time',))
	qc_tsnow9 = root_grp.createVariable('qc_tsnow9', 'i1', ('time',))
	qc_tsnow10 = root_grp.createVariable('qc_tsnow10', 'i1', ('time',))
	qc_battery = root_grp.createVariable('qc_battery', 'i1', ('time',))
	
	#date_derived = root_grp.createVariable('date_derived', 'S10', ('time',))
	month = root_grp.createVariable('month', 'i1', ('time',))
	day = root_grp.createVariable('day', 'i1', ('time',))
	hour = root_grp.createVariable('hour', 'i1', ('time',))
	

	latitude.units = 'degree_north'
	latitude.standard_name = 'latitude'

	longitude.units = 'degree_east'
	longitude.standard_name = 'longitude'

	time.units = 'seconds since 1995-01-01 00:00:00'
	time.long_name = 'time of measurement'
	time.standard_name = 'time'
	time.bounds = 'time_bounds'
	time.calendar = 'noleap'
	
	station_number.units = '1'
	station_number.long_name = 'Station Number'

	year.units = '1'
	year.long_name = 'Year'

	julian_decimal_time.units = 'decimal time'
	julian_decimal_time.long_name = 'Julian Decimal Time'
	julian_decimal_time.note = 'Not really a standard Julian time. For each year, time starts at 1.0000 and ends at 365.9999.'

	sw_down.units = 'watt meter-2'
	sw_down.long_name = 'Shortwave Flux down'
	sw_down.standard_name = 'downwelling_shortwave_flux_in_air'

	sw_up.units = 'watt meter-2'
	sw_up.long_name = 'Shortwave Flux up'
	sw_up.standard_name = 'upwelling_shortwave_flux_in_air'

	net_radiation.units = 'watt meter-2'
	net_radiation.long_name = 'Net Radiation'
	net_radiation.standard_name = 'surface_net_downward_radiative_flux'

	temperature_tc_1.units = 'kelvin'
	temperature_tc_1.long_name = 'TC-1 Air Temperature'
	temperature_tc_1.standard_name = 'air_temperature'
	temperature_tc_1.note = 'air temperature from TC sensor'

	temperature_tc_2.units = 'kelvin'
	temperature_tc_2.long_name = 'TC-2 Air Temperature'
	temperature_tc_2.standard_name = 'air_temperature'

	temperature_cs500_1.units = 'kelvin'
	temperature_cs500_1.long_name = 'CS500-1 Air Temperature'
	temperature_cs500_1.standard_name = 'air_temperature'
	temperature_cs500_1.note = 'air temperature from CS500 sensor'

	temperature_cs500_2.units = 'kelvin'
	temperature_cs500_2.long_name = 'CS500-2 Air Temperature'
	temperature_cs500_2.standard_name = 'air_temperature'

	relative_humidity_1.units = '1'
	relative_humidity_1.long_name = 'Relative Humidity 1'
	relative_humidity_1.standard_name = 'realtive_humidity'

	relative_humidity_2.units = '1'
	relative_humidity_2.long_name = 'Relative Humidity 2'
	relative_humidity_2.standard_name = 'realtive_humidity'

	u1_wind_speed.units = 'meter second-1'
	u1_wind_speed.long_name = 'U1 Wind Speed'
	u1_wind_speed.standard_name = 'wind_speed'

	u2_wind_speed.units = 'meter second-1'
	u2_wind_speed.long_name = 'U2 Wind Speed'
	u2_wind_speed.standard_name = 'wind_speed'

	u_direction_1.units = 'degree'
	u_direction_1.long_name = 'U Direction 1'
	u_direction_1.standard_name = 'wind_from_direction'

	u_direction_2.units = 'degree'
	u_direction_2.long_name = 'U Direction 2'
	u_direction_2.standard_name = 'wind_from_direction'

	atmos_pressure.units = 'pascal'
	atmos_pressure.long_name = 'Atmospheric Pressure'
	atmos_pressure.standard_name = 'surface_air_pressure'

	snow_height_1.units = 'meter'
	snow_height_1.long_name = 'Snow Height 1'
	snow_height_1.standard_name = 'snow_height'

	snow_height_2.units = 'meter'
	snow_height_2.long_name = 'Snow Height 2'
	snow_height_2.standard_name = 'snow_height'

	t_snow_01.units = 'kelvin'
	t_snow_01.long_name = 'T Snow 1'
	#t_snow_01.standard_name = 'temperature_in_surface_snow'

	t_snow_02.units = 'kelvin'
	t_snow_02.long_name = 'T Snow 2'
	#t_snow_02.standard_name = 'temperature_in_surface_snow'

	t_snow_03.units = 'kelvin'
	t_snow_03.long_name = 'T Snow 3'
	#t_snow_03.standard_name = 'temperature_in_surface_snow'

	t_snow_04.units = 'kelvin'
	t_snow_04.long_name = 'T Snow 4'
	#t_snow_04.standard_name = 'temperature_in_surface_snow'

	t_snow_05.units = 'kelvin'
	t_snow_05.long_name = 'T Snow 5'
	#t_snow_05.standard_name = 'temperature_in_surface_snow'

	t_snow_06.units = 'kelvin'
	t_snow_06.long_name = 'T Snow 6'
	#t_snow_06.standard_name = 'temperature_in_surface_snow'

	t_snow_07.units = 'kelvin'
	t_snow_07.long_name = 'T Snow 7'
	#t_snow_07.standard_name = 'temperature_in_surface_snow'

	t_snow_08.units = 'kelvin'
	t_snow_08.long_name = 'T Snow 8'
	#t_snow_08.standard_name = 'temperature_in_surface_snow'

	t_snow_09.units = 'kelvin'
	t_snow_09.long_name = 'T Snow 9'
	#t_snow_09.standard_name = 'temperature_in_surface_snow'

	t_snow_10.units = 'kelvin'
	t_snow_10.long_name = 'T Snow 10'
	#t_snow_10.standard_name = 'temperature_in_surface_snow'

	battery_voltage.units = 'volts'
	battery_voltage.long_name = 'Battery Voltage'
	battery_voltage.standard_name = 'battery_voltage'

	sw_down_max.units = 'watt meter-2'
	sw_down_max.long_name = 'Shortwave Flux down max'
	sw_down_max.standard_name = 'maximum_downwelling_shortwave_flux_in_air'
	
	sw_up_max.units = 'watt meter-2'
	sw_up_max.long_name = 'Shortwave Flux up max'
	sw_up_max.standard_name = 'maximum_upwelling_shortwave_flux_in_air'
	
	net_radiation_max.units = 'watt meter-2'
	net_radiation_max.long_name = 'Net Radiation max'
	net_radiation_max.standard_name = 'maximum_net_radiation'

	max_air_temperature_1.units = 'kelvin'
	max_air_temperature_1.long_name = 'Max Air Temperture 1'
	max_air_temperature_1.standard_name = 'air_temperature'

	max_air_temperature_2.units = 'kelvin'
	max_air_temperature_2.long_name = 'Max Air Temperture 2'
	max_air_temperature_2.standard_name = 'air_temperature'

	min_air_temperature_1.units = 'kelvin'
	min_air_temperature_1.long_name = 'Min Air Temperture 1'
	min_air_temperature_1.standard_name = 'air_temperature'

	min_air_temperature_2.units = 'kelvin'
	min_air_temperature_2.long_name = 'Min Air Temperture 2'
	min_air_temperature_2.standard_name = 'air_temperature'

	max_windspeed_u1.units = 'meter second-1'
	max_windspeed_u1.long_name = 'Max Windspeed-U1'
	max_windspeed_u1.standard_name = 'wind_speed'

	max_windspeed_u2.units = 'meter second-1'
	max_windspeed_u2.long_name = 'Max Windspeed-U2'
	max_windspeed_u2.standard_name = 'wind_speed'

	stdev_windspeed_u1.units = 'meter second-1'
	stdev_windspeed_u1.long_name = 'StdDev Windspeed-U1'
	stdev_windspeed_u1.standard_name = 'wind_speed'

	stdev_windspeed_u2.units = 'meter second-1'
	stdev_windspeed_u2.long_name = 'StdDev Windspeed-U2'
	stdev_windspeed_u2.standard_name = 'wind_speed'

	ref_temperature.units = 'kelvin'
	ref_temperature.long_name = 'Reference Temperature'
	ref_temperature.note = 'Need to ask network manager about long name'

	windspeed_2m.units = 'meter second-1'
	windspeed_2m.long_name = 'Windspeed@2m'
	windspeed_2m.standard_name = 'wind_speed'

	windspeed_10m.units = 'meter second-1'
	windspeed_10m.long_name = 'Windspeed@10m'
	windspeed_10m.standard_name = '10-m_wind_speed'

	wind_sensor_height_1.units = 'meter'
	wind_sensor_height_1.long_name = 'Wind Sensor Height 1'
	wind_sensor_height_1.standard_name = 'n/a'

	wind_sensor_height_2.units = 'meter'
	wind_sensor_height_2.long_name = 'Wind Sensor Height 2'
	wind_sensor_height_2.standard_name = 'n/a'

	albedo.units = '1'
	albedo.long_name = 'Albedo'
	albedo.standard_name = 'surface_albedo'

	zenith_angle.units = 'degree'
	zenith_angle.long_name = 'Zenith Angle'
	zenith_angle.standard_name = 'solar_zenith_angle'

	qc1.units = '1'
	qc1.long_name = 'Quality Control variables 01-08'

	qc9.units = '1'
	qc9.long_name = 'Quality Control variables 09-16'

	qc17.units = '1'
	qc17.long_name = 'Quality Control variables 17-24'

	qc25.units = '1'
	qc25.long_name = 'Quality Control variables 25-27'

	#date_derived.note = 'Created date from year and julian decimal time.'
	
	print "converting data..."
	i,j = 0,0
	ip_file = open(str(args.input), 'r')

	while i < 54:
	    ip_file.readline()
	    i += 1

	for line in ip_file:
	    
		line = line.strip()
		columns = line.split()
		
		station_number[0] = columns[0]
		year[j] = columns[1]
		julian_decimal_time[j] = columns[2]
		sw_down[j] = columns[3]
		sw_up[j] = columns[4]
		net_radiation[j] = columns[5]
		
		if columns[6] == '999.0':
			temperature_tc_1[j] = columns[6]
		else:
			temperature_tc_1[j] = float(columns[6]) + 273.15

		if columns[7] == '999.0':
			temperature_tc_2[j] = columns[7]
		else:
			temperature_tc_2[j] = float(columns[7]) + 273.15

		if columns[8] == '999.0':
			temperature_cs500_1[j] = columns[8]
		else:
			temperature_cs500_1[j] = float(columns[8]) + 273.15

		if columns[9] == '999.0':
			temperature_cs500_2[j] = columns[9]
		else:
			temperature_cs500_2[j] = float(columns[9]) + 273.15

		relative_humidity_1[j] = columns[10]
		relative_humidity_2[j] = columns[11]
		u1_wind_speed[j] = columns[12]
		u2_wind_speed[j] = columns[13]
		u_direction_1[j] = columns[14]
		u_direction_2[j] = columns[15]
		
		if columns[16] == '999.0':
			atmos_pressure[j] = columns[16]
		else:
			atmos_pressure[j] = float(columns[16]) * 100
		
		snow_height_1[j] = columns[17]
		snow_height_2[j] = columns[18]
		
		if columns[19] == '999.0':
			t_snow_01[j] = columns[19]
		else:
			t_snow_01[j] = float(columns[19]) + 273.15

		if columns[20] == '999.0':
			t_snow_02[j] = columns[20]
		else:
			t_snow_02[j] = float(columns[20]) + 273.15

		if columns[21] == '999.0':
			t_snow_03[j] = columns[21]
		else:
			t_snow_03[j] = float(columns[2]) + 273.15
		
		if columns[22] == '999.0':
			t_snow_04[j] = columns[22]
		else:
			t_snow_04[j] = float(columns[22]) + 273.15
		
		if columns[23] == '999.0':
			t_snow_05[j] = columns[23]
		else:
			t_snow_05[j] = float(columns[23]) + 273.15
		
		if columns[24] == '999.0':
			t_snow_06[j] = columns[24]
		else:
			t_snow_06[j] = float(columns[24]) + 273.15
		
		if columns[25] == '999.0':
			t_snow_07[j] = columns[25]
		else:
			t_snow_07[j] = float(columns[25]) + 273.15
		
		if columns[26] == '999.0':
			t_snow_08[j] = columns[26]
		else:
			t_snow_08[j] = float(columns[26]) + 273.15
		
		if columns[27] == '999.0':
			t_snow_09[j] = columns[27]
		else:
			t_snow_09[j] = float(columns[27]) + 273.15
		
		if columns[28] == '999.0':
			t_snow_10[j] = columns[28]
		else:
			t_snow_10[j] = float(columns[28]) + 273.15
		
		battery_voltage[j] = columns[29]
		sw_down_max[j] = columns[30]
		sw_up_max[j] = columns[31]
		net_radiation_max[j] = columns[32]
		
		if columns[33] == '999.0':
			max_air_temperature_1[j] = columns[33]
		else:
			max_air_temperature_1[j] = float(columns[33]) + 273.15
		
		if columns[34] == '999.0':
			max_air_temperature_2[j] = columns[34]
		else:
			max_air_temperature_2[j] = float(columns[34]) + 273.15
		
		if columns[35] == '999.0':
			min_air_temperature_1[j] = columns[35]
		else:
			min_air_temperature_1[j] = float(columns[35]) + 273.15
		
		if columns[36] == '999.0':
			min_air_temperature_2[j] = columns[36]
		else:
			min_air_temperature_2[j] = float(columns[36]) + 273.15
		
		max_windspeed_u1[j] = columns[37]
		max_windspeed_u2[j] = columns[38]
		stdev_windspeed_u1[j] = columns[39]
		stdev_windspeed_u2[j] = columns[40]
		
		if columns[41] == '999.0':
			ref_temperature[j] = columns[41]
		else:
			ref_temperature[j] = float(columns[41]) + 273.15
		
		windspeed_2m[j] = columns[42]
		windspeed_10m[j] = columns[43]
		wind_sensor_height_1[j] = columns[44]
		wind_sensor_height_2[j] = columns[45]
		albedo[j] = columns[46]
		zenith_angle[j] = columns[47]
		qc1[j] = columns[48]
		qc9[j] = columns[49]
		qc17[j] = columns[50]
		qc25[j] = columns[51]

		columns[2] = float(columns[2])
		if str(columns[2]-int(columns[2]))[1:] == '.0':
			hour[j] = 0
		elif str(columns[2]-int(columns[2]))[1:] == '.0417':
			hour[j] = 1
		elif str(columns[2]-int(columns[2]))[1:] == '.0833':
			hour[j] = 2
		elif str(columns[2]-int(columns[2]))[1:] == '.125':
			hour[j] = 3
		elif str(columns[2]-int(columns[2]))[1:] == '.1667':
			hour[j] = 4
		elif str(columns[2]-int(columns[2]))[1:] == '.2083':
			hour[j] = 5
		elif str(columns[2]-int(columns[2]))[1:] == '.25':
			hour[j] = 6
		elif str(columns[2]-int(columns[2]))[1:] == '.2917':
			hour[j] = 7
		elif str(columns[2]-int(columns[2]))[1:] == '.3333':
			hour[j] = 8
		elif str(columns[2]-int(columns[2]))[1:] == '.375':
			hour[j] = 9
		elif str(columns[2]-int(columns[2]))[1:] == '.4167':
			hour[j] = 10
		elif str(columns[2]-int(columns[2]))[1:] == '.4583':
			hour[j] = 11
		elif str(columns[2]-int(columns[2]))[1:] == '.5':
			hour[j] = 12
		elif str(columns[2]-int(columns[2]))[1:] == '.5417':
			hour[j] = 13
		elif str(columns[2]-int(columns[2]))[1:] == '.5833':
			hour[j] = 14
		elif str(columns[2]-int(columns[2]))[1:] == '.625':
			hour[j] = 15
		elif str(columns[2]-int(columns[2]))[1:] == '.6667':
			hour[j] = 16
		elif str(columns[2]-int(columns[2]))[1:] == '.7083':
			hour[j] = 17
		elif str(columns[2]-int(columns[2]))[1:] == '.75':
			hour[j] = 18
		elif str(columns[2]-int(columns[2]))[1:] == '.7917':
			hour[j] = 19
		elif str(columns[2]-int(columns[2]))[1:] == '.8333':
			hour[j] = 20
		elif str(columns[2]-int(columns[2]))[1:] == '.875':
			hour[j] = 21
		elif str(columns[2]-int(columns[2]))[1:] == '.9167':
			hour[j] = 22
		elif str(columns[2]-int(columns[2]))[1:] == '.9583':
			hour[j] = 23
		
		j += 1

	if station_number[0] == 1:
		latitude[0] = 69.56833
		longitude[0] = -49.31582
	elif station_number[0] == 2:
		latitude[0] = 69.87975
		longitude[0] = -46.98667
	elif station_number[0] == 3:
		latitude[0] = 73.84189
		longitude[0] = -49.49831
	elif station_number[0] == 4:
		latitude[0] = 77.13781
		longitude[0] = -61.04113
	elif station_number[0] == 5:
		latitude[0] = 78.5266
		longitude[0] = -56.8305
	elif station_number[0] == 6:
		latitude[0] = 72.57972
		longitude[0] = -38.50454
	elif station_number[0] == 7:
		latitude[0] = 78.01677
		longitude[0] = -33.99387
	elif station_number[0] == 8:
		latitude[0] = 66.48001
		longitude[0] = -46.27889
	elif station_number[0] == 9:
		latitude[0] = 69.498358
		longitude[0] = -49.68156
	elif station_number[0] == 10:
		latitude[0] = 65.99947
		longitude[0] = -44.50016
	elif station_number[0] == 11:
		latitude[0] = 63.14889
		longitude[0] = -44.81717
	elif station_number[0] == 12:
		latitude[0] = 75.00000
		longitude[0] = -29.99972
	elif station_number[0] == 13:
		latitude[0] = 69.87968
		longitude[0] = -46.98692
	elif station_number[0] == 14:
		latitude[0] = 75.09975
		longitude[0] = -42.33256
	elif station_number[0] == 15:
		latitude[0] = 66.4797
		longitude[0] = -42.5002 
	elif station_number[0] == 16:
		latitude[0] = 69.69942
		longitude[0] = -33.00058
	elif station_number[0] == 17:
		latitude[0] = 69.42000
		longitude[0] = -50.05750
	elif station_number[0] == 18:
		latitude[0] = 65.75845
		longitude[0] = -39.60177
	


	print "extracting quality control variables..."

	qc1_str = [str(e) for e in qc1]
	qc9_str = [str(e) for e in qc9]
	qc17_str = [str(e) for e in qc17]
	qc25_str = [str(e) for e in qc25]
	
	k,l = 0,0

	for item in qc1_str:
		qc_swdn[k] = int(qc1_str[k][l])
		qc_swup[k] = int(qc1_str[k][l+1])
		qc_netradiation[k] = int(qc1_str[k][l+2])
		qc_ttc1[k] = int(qc1_str[k][l+3])
		qc_ttc2[k] = int(qc1_str[k][l+4])
		qc_tcs1[k] = int(qc1_str[k][l+5])
		qc_tcs2[k] = int(qc1_str[k][l+6])
		qc_rh1[k] = int(qc1_str[k][l+7])

		k += 1
		
	k,l = 0,0

	for item in qc9_str:
		qc_rh2[k] = int(qc9_str[k][l])
		qc_u1[k] = int(qc9_str[k][l+1])
		qc_u2[k] = int(qc9_str[k][l+2])
		qc_ud1[k] = int(qc9_str[k][l+3])
		qc_ud2[k] = int(qc9_str[k][l+4])
		qc_pressure[k] = int(qc9_str[k][l+5])
		qc_snowheight1[k] = int(qc9_str[k][l+6])
		qc_snowheight2[k] = int(qc9_str[k][l+7])

		k += 1
		
	k,l = 0,0

	for item in qc17_str:
		qc_tsnow1[k] = int(qc17_str[k][l])
		qc_tsnow2[k] = int(qc17_str[k][l+1])
		qc_tsnow3[k] = int(qc17_str[k][l+2])
		qc_tsnow4[k] = int(qc17_str[k][l+3])
		qc_tsnow5[k] = int(qc17_str[k][l+4])
		qc_tsnow6[k] = int(qc17_str[k][l+5])
		qc_tsnow7[k] = int(qc17_str[k][l+6])
		qc_tsnow8[k] = int(qc17_str[k][l+7])

		k += 1
		
	k,l = 0,0

	for item in qc25_str:
		qc_tsnow9[k] = int(qc25_str[k][l])
		qc_tsnow10[k] = int(qc25_str[k][l+1])
		qc_battery[k] = int(qc25_str[k][l+2])

		k += 1
	
#############################################################################################################################################################
	'''
	qc1_str = ''.join(str(e) for e in qc1)
	qc9_str = ''.join(str(e) for e in qc9)
	qc17_str = ''.join(str(e) for e in qc17)
	qc25_str = ''.join(str(e) for e in qc25)


	a,b = 0,0
	while a < 12183:
		qc_swdn[a] = qc1_str[b]
		qc_swup[a] = qc1_str[b+1]
		qc_netradiation[a] = qc1_str[b+2]
		qc_ttc1[a] = qc1_str[b+3]
		qc_ttc2[a] = qc1_str[b+4]
		qc_tcs1[a] = qc1_str[b+5]
		qc_tcs2[a] = qc1_str[b+6]
		qc_rh1[a] = qc1_str[b+7]

		a += 1
		b += 8

	a,b = 0,0
	while a < 12183:
		qc_rh2[a] = qc9_str[b]
		qc_u1[a] = qc9_str[b+1]
		qc_u2[a] = qc9_str[b+2]
		qc_ud1[a] = qc9_str[b+3]
		qc_ud2[a] = qc9_str[b+4]
		qc_pressure[a] = qc9_str[b+5]
		qc_snowheight1[a] = qc9_str[b+6]
		qc_snowheight2[a] = qc9_str[b+7]

		a += 1
		b += 8


	a,b = 0,0
	while a < 12183:
		qc_tsnow1[a] = qc17_str[b]
		qc_tsnow2[a] = qc17_str[b+1]
		qc_tsnow3[a] = qc17_str[b+2]
		qc_tsnow4[a] = qc17_str[b+3]
		qc_tsnow5[a] = qc17_str[b+4]
		qc_tsnow6[a] = qc17_str[b+5]
		qc_tsnow7[a] = qc17_str[b+6]
		qc_tsnow8[a] = qc17_str[b+7]

		a += 1
		b += 8


	a,b = 0,0
	while a < 12183:
		qc_tsnow9[a] = qc25_str[b]
		qc_tsnow10[a] = qc25_str[b+1]
		qc_battery[a] = qc25_str[b+2]
		
		a += 1
		b += 3
	'''
##################################################################################################################################################################
	print "calculating time..."
	m = 0
	for item in julian_decimal_time:
		if hour[m] == 0:
			time[m] = ((date(year[m], 1, 1) - date(1995, 1, 1)).days + int(julian_decimal_time[m]))*86400
			m += 1
		elif hour[m] == 1:
			time[m] = ((date(year[m], 1, 1) - date(1995, 1, 1)).days + int(julian_decimal_time[m]))*86400 + (3600*1)
			m += 1
		elif hour[m] == 2:
			time[m] = ((date(year[m], 1, 1) - date(1995, 1, 1)).days + int(julian_decimal_time[m]))*86400 + (3600*2)
			m += 1
		elif hour[m] == 3:
			time[m] = ((date(year[m], 1, 1) - date(1995, 1, 1)).days + int(julian_decimal_time[m]))*86400 + (3600*3)
			m += 1
		elif hour[m] == 4:
			time[m] = ((date(year[m], 1, 1) - date(1995, 1, 1)).days + int(julian_decimal_time[m]))*86400 + (3600*4)
			m += 1
		elif hour[m] == 5:
			time[m] = ((date(year[m], 1, 1) - date(1995, 1, 1)).days + int(julian_decimal_time[m]))*86400 + (3600*5)
			m += 1
		elif hour[m] == 6:
			time[m] = ((date(year[m], 1, 1) - date(1995, 1, 1)).days + int(julian_decimal_time[m]))*86400 + (3600*6)
			m += 1
		elif hour[m] == 7:
			time[m] = ((date(year[m], 1, 1) - date(1995, 1, 1)).days + int(julian_decimal_time[m]))*86400 + (3600*7)
			m += 1
		elif hour[m] == 8:
			time[m] = ((date(year[m], 1, 1) - date(1995, 1, 1)).days + int(julian_decimal_time[m]))*86400 + (3600*8)
			m += 1
		elif hour[m] == 9:
			time[m] = ((date(year[m], 1, 1) - date(1995, 1, 1)).days + int(julian_decimal_time[m]))*86400 + (3600*9)
			m += 1
		elif hour[m] == 10:
			time[m] = ((date(year[m], 1, 1) - date(1995, 1, 1)).days + int(julian_decimal_time[m]))*86400 + (3600*10)
			m += 1
		elif hour[m] == 11:
			time[m] = ((date(year[m], 1, 1) - date(1995, 1, 1)).days + int(julian_decimal_time[m]))*86400 + (3600*11)
			m += 1
		elif hour[m] == 12:
			time[m] = ((date(year[m], 1, 1) - date(1995, 1, 1)).days + int(julian_decimal_time[m]))*86400 + (3600*12)
			m += 1
		elif hour[m] == 13:
			time[m] = ((date(year[m], 1, 1) - date(1995, 1, 1)).days + int(julian_decimal_time[m]))*86400 + (3600*13)
			m += 1
		elif hour[m] == 14:
			time[m] = ((date(year[m], 1, 1) - date(1995, 1, 1)).days + int(julian_decimal_time[m]))*86400 + (3600*14)
			m += 1
		elif hour[m] == 15:
			time[m] = ((date(year[m], 1, 1) - date(1995, 1, 1)).days + int(julian_decimal_time[m]))*86400 + (3600*15)
			m += 1
		elif hour[m] == 16:
			time[m] = ((date(year[m], 1, 1) - date(1995, 1, 1)).days + int(julian_decimal_time[m]))*86400 + (3600*16)
			m += 1
		elif hour[m] == 17:
			time[m] = ((date(year[m], 1, 1) - date(1995, 1, 1)).days + int(julian_decimal_time[m]))*86400 + (3600*17)
			m += 1
		elif hour[m] == 18:
			time[m] = ((date(year[m], 1, 1) - date(1995, 1, 1)).days + int(julian_decimal_time[m]))*86400 + (3600*18)
			m += 1
		elif hour[m] == 19:
			time[m] = ((date(year[m], 1, 1) - date(1995, 1, 1)).days + int(julian_decimal_time[m]))*86400 + (3600*19)
			m += 1
		elif hour[m] == 20:
			time[m] = ((date(year[m], 1, 1) - date(1995, 1, 1)).days + int(julian_decimal_time[m]))*86400 + (3600*20)
			m += 1
		elif hour[m] == 21:
			time[m] = ((date(year[m], 1, 1) - date(1995, 1, 1)).days + int(julian_decimal_time[m]))*86400 + (3600*21)
			m += 1
		elif hour[m] == 22:
			time[m] = ((date(year[m], 1, 1) - date(1995, 1, 1)).days + int(julian_decimal_time[m]))*86400 + (3600*22)
			m += 1
		elif hour[m] == 23:
			time[m] = ((date(year[m], 1, 1) - date(1995, 1, 1)).days + int(julian_decimal_time[m]))*86400 + (3600*23)
			m += 1
		
	x = 0
	while x < len(time):
		time_bounds[x] = (time[x]-3600, time[x])
		x += 1	
		

	print "calculating day and month..."
	n = 0
	for item in julian_decimal_time:
		if int(julian_decimal_time[n]) == 1:
			#date_derived[n] = str(year[n])+'-01-01'
			day[n] = 1
			month[n] = 01
			n += 1
		elif int(julian_decimal_time[n]) == 2:
			#date_derived[n] = str(year[n])+'-01-02'
			day[n] = 2
			month[n] = 01
			n += 1
		elif int(julian_decimal_time[n]) == 3:
			#date_derived[n] = str(year[n])+'-01-03'
			day[n] = 3
			month[n] = 01
			n += 1
		elif int(julian_decimal_time[n]) == 4:
			#date_derived[n] = str(year[n])+'-01-04'
			day[n] = 4
			month[n] = 01
			n += 1
		elif int(julian_decimal_time[n]) == 5:
			#date_derived[n] = str(year[n])+'-01-05'
			day[n] = 5
			month[n] = 01
			n += 1
		elif int(julian_decimal_time[n]) == 6:
			#date_derived[n] = str(year[n])+'-01-06'
			day[n] = 6
			month[n] = 01
			n += 1
		elif int(julian_decimal_time[n]) == 7:
			#date_derived[n] = str(year[n])+'-01-07'
			day[n] = 7
			month[n] = 01
			n += 1
		elif int(julian_decimal_time[n]) == 8:
			#date_derived[n] = str(year[n])+'-01-08'
			day[n] = 8
			month[n] = 01
			n += 1
		elif int(julian_decimal_time[n]) == 9:
			#date_derived[n] = str(year[n])+'-01-09'
			day[n] = 9
			month[n] = 01
			n += 1
		elif int(julian_decimal_time[n]) == 10:
			#date_derived[n] = str(year[n])+'-01-10'
			day[n] = 10
			month[n] = 01
			n += 1
		elif int(julian_decimal_time[n]) == 11:
			#date_derived[n] = str(year[n])+'-01-11'
			day[n] = 11
			month[n] = 01
			n += 1
		elif int(julian_decimal_time[n]) == 12:
			#date_derived[n] = str(year[n])+'-01-12'
			day[n] = 12
			month[n] = 01
			n += 1
		elif int(julian_decimal_time[n]) == 13:
			#date_derived[n] = str(year[n])+'-01-13'
			day[n] = 13
			month[n] = 01
			n += 1
		elif int(julian_decimal_time[n]) == 14:
			#date_derived[n] = str(year[n])+'-01-14'
			day[n] = 14
			month[n] = 01
			n += 1
		elif int(julian_decimal_time[n]) == 15:
			#date_derived[n] = str(year[n])+'-01-15'
			day[n] = 15
			month[n] = 01
			n += 1
		elif int(julian_decimal_time[n]) == 16:
			#date_derived[n] = str(year[n])+'-01-16'
			day[n] = 16
			month[n] = 01
			n += 1
		elif int(julian_decimal_time[n]) == 17:
			#date_derived[n] = str(year[n])+'-01-17'
			day[n] = 17
			month[n] = 01
			n += 1
		elif int(julian_decimal_time[n]) == 18:
			#date_derived[n] = str(year[n])+'-01-18'
			day[n] = 18
			month[n] = 01
			n += 1
		elif int(julian_decimal_time[n]) == 19:
			#date_derived[n] = str(year[n])+'-01-19'
			day[n] = 19
			month[n] = 01
			n += 1
		elif int(julian_decimal_time[n]) == 20:
			#date_derived[n] = str(year[n])+'-01-20'
			day[n] = 20
			month[n] = 01
			n += 1
		elif int(julian_decimal_time[n]) == 21:
			#date_derived[n] = str(year[n])+'-01-21'
			day[n] = 21
			month[n] = 01
			n += 1
		elif int(julian_decimal_time[n]) == 22:
			#date_derived[n] = str(year[n])+'-01-22'
			day[n] = 22
			month[n] = 01
			n += 1
		elif int(julian_decimal_time[n]) == 23:
			#date_derived[n] = str(year[n])+'-01-23'
			day[n] = 23
			month[n] = 01
			n += 1
		elif int(julian_decimal_time[n]) == 24:
			#date_derived[n] = str(year[n])+'-01-24'
			day[n] = 24
			month[n] = 01
			n += 1
		elif int(julian_decimal_time[n]) == 25:
			#date_derived[n] = str(year[n])+'-01-25'
			day[n] = 25
			month[n] = 01
			n += 1
		elif int(julian_decimal_time[n]) == 26:
			#date_derived[n] = str(year[n])+'-01-26'
			day[n] = 26
			month[n] = 01
			n += 1
		elif int(julian_decimal_time[n]) == 27:
			#date_derived[n] = str(year[n])+'-01-27'
			day[n] = 27
			month[n] = 01
			n += 1
		elif int(julian_decimal_time[n]) == 28:
			#date_derived[n] = str(year[n])+'-01-28'
			day[n] = 28
			month[n] = 01
			n += 1
		elif int(julian_decimal_time[n]) == 29:
			#date_derived[n] = str(year[n])+'-01-29'
			day[n] = 29
			month[n] = 01
			n += 1
		elif int(julian_decimal_time[n]) == 30:
			#date_derived[n] = str(year[n])+'-01-30'
			day[n] = 30
			month[n] = 01
			n += 1
		elif int(julian_decimal_time[n]) == 31:
			#date_derived[n] = str(year[n])+'-01-31'
			day[n] = 31
			month[n] = 01
			n += 1
		elif int(julian_decimal_time[n]) == 32:
			#date_derived[n] = str(year[n])+'-02-01'
			day[n] = 1
			month[n] = 02
			n += 1
		elif int(julian_decimal_time[n]) == 33:
			#date_derived[n] = str(year[n])+'-02-02'
			day[n] = 2
			month[n] = 02
			n += 1
		elif int(julian_decimal_time[n]) == 34:
			#date_derived[n] = str(year[n])+'-02-03'
			day[n] = 3
			month[n] = 02
			n += 1
		elif int(julian_decimal_time[n]) == 35:
			#date_derived[n] = str(year[n])+'-02-04'
			day[n] = 4
			month[n] = 02
			n += 1
		elif int(julian_decimal_time[n]) == 36:
			#date_derived[n] = str(year[n])+'-02-05'
			day[n] = 5
			month[n] = 02
			n += 1
		elif int(julian_decimal_time[n]) == 37:
			#date_derived[n] = str(year[n])+'-02-06'
			day[n] = 6
			month[n] = 02
			n += 1
		elif int(julian_decimal_time[n]) == 38:
			#date_derived[n] = str(year[n])+'-02-07'
			day[n] = 7
			month[n] = 02
			n += 1
		elif int(julian_decimal_time[n]) == 39:
			#date_derived[n] = str(year[n])+'-02-08'
			day[n] = 8
			month[n] = 02
			n += 1
		elif int(julian_decimal_time[n]) == 40:
			#date_derived[n] = str(year[n])+'-02-09'
			day[n] = 9
			month[n] = 02
			n += 1
		elif int(julian_decimal_time[n]) == 41:
			#date_derived[n] = str(year[n])+'-02-10'
			day[n] = 10
			month[n] = 02
			n += 1
		elif int(julian_decimal_time[n]) == 42:
			#date_derived[n] = str(year[n])+'-02-11'
			day[n] = 11
			month[n] = 02
			n += 1
		elif int(julian_decimal_time[n]) == 43:
			#date_derived[n] = str(year[n])+'-02-12'
			day[n] = 12
			month[n] = 02
			n += 1
		elif int(julian_decimal_time[n]) == 44:
			#date_derived[n] = str(year[n])+'-02-13'
			day[n] = 13
			month[n] = 02
			n += 1
		elif int(julian_decimal_time[n]) == 45:
			#date_derived[n] = str(year[n])+'-02-14'
			day[n] = 14
			month[n] = 02
			n += 1
		elif int(julian_decimal_time[n]) == 46:
			#date_derived[n] = str(year[n])+'-02-15'
			day[n] = 15
			month[n] = 02
			n += 1
		elif int(julian_decimal_time[n]) == 47:
			#date_derived[n] = str(year[n])+'-02-16'
			day[n] = 16
			month[n] = 02
			n += 1
		elif int(julian_decimal_time[n]) == 48:
			#date_derived[n] = str(year[n])+'-02-17'
			day[n] = 17
			month[n] = 02
			n += 1
		elif int(julian_decimal_time[n]) == 49:
			#date_derived[n] = str(year[n])+'-02-18'
			day[n] = 18
			month[n] = 02
			n += 1
		elif int(julian_decimal_time[n]) == 50:
			#date_derived[n] = str(year[n])+'-02-19'
			day[n] = 19
			month[n] = 02
			n += 1
		elif int(julian_decimal_time[n]) == 51:
			#date_derived[n] = str(year[n])+'-02-20'
			day[n] = 20
			month[n] = 02
			n += 1
		elif int(julian_decimal_time[n]) == 52:
			#date_derived[n] = str(year[n])+'-02-21'
			day[n] = 21
			month[n] = 02
			n += 1
		elif int(julian_decimal_time[n]) == 53:
			#date_derived[n] = str(year[n])+'-02-22'
			day[n] = 22
			month[n] = 02
			n += 1
		elif int(julian_decimal_time[n]) == 54:
			#date_derived[n] = str(year[n])+'-02-23'
			day[n] = 23
			month[n] = 02
			n += 1
		elif int(julian_decimal_time[n]) == 55:
			#date_derived[n] = str(year[n])+'-02-24'
			day[n] = 24
			month[n] = 02
			n += 1
		elif int(julian_decimal_time[n]) == 56:
			#date_derived[n] = str(year[n])+'-02-25'
			day[n] = 25
			month[n] = 02
			n += 1
		elif int(julian_decimal_time[n]) == 57:
			#date_derived[n] = str(year[n])+'-02-26'
			day[n] = 26
			month[n] = 02
			n += 1
		elif int(julian_decimal_time[n]) == 58:
			#date_derived[n] = str(year[n])+'-02-27'
			day[n] = 27
			month[n] = 02
			n += 1
		elif int(julian_decimal_time[n]) == 59:
			#date_derived[n] = str(year[n])+'-02-28'
			day[n] = 28
			month[n] = 02
			n += 1
		elif int(julian_decimal_time[n]) == 60:
			#date_derived[n] = str(year[n])+'-03-01'
			day[n] = 1
			month[n] = 03
			n += 1
		elif int(julian_decimal_time[n]) == 61:
			#date_derived[n] = str(year[n])+'-03-02'
			day[n] = 2
			month[n] = 03
			n += 1
		elif int(julian_decimal_time[n]) == 62:
			#date_derived[n] = str(year[n])+'-03-03'
			day[n] = 3
			month[n] = 03
			n += 1
		elif int(julian_decimal_time[n]) == 63:
			#date_derived[n] = str(year[n])+'-03-04'
			day[n] = 4
			month[n] = 03
			n += 1
		elif int(julian_decimal_time[n]) == 64:
			#date_derived[n] = str(year[n])+'-03-05'
			day[n] = 5
			month[n] = 03
			n += 1
		elif int(julian_decimal_time[n]) == 65:
			#date_derived[n] = str(year[n])+'-03-06'
			day[n] = 6
			month[n] = 03
			n += 1
		elif int(julian_decimal_time[n]) == 66:
			#date_derived[n] = str(year[n])+'-03-07'
			day[n] = 7
			month[n] = 03
			n += 1
		elif int(julian_decimal_time[n]) == 67:
			#date_derived[n] = str(year[n])+'-03-08'
			day[n] = 8
			month[n] = 03
			n += 1
		elif int(julian_decimal_time[n]) == 68:
			#date_derived[n] = str(year[n])+'-03-09'
			day[n] = 9
			month[n] = 03
			n += 1
		elif int(julian_decimal_time[n]) == 69:
			#date_derived[n] = str(year[n])+'-03-10'
			day[n] = 10
			month[n] = 03
			n += 1
		elif int(julian_decimal_time[n]) == 70:
			#date_derived[n] = str(year[n])+'-03-11'
			day[n] = 11
			month[n] = 03
			n += 1
		elif int(julian_decimal_time[n]) == 71:
			#date_derived[n] = str(year[n])+'-03-12'
			day[n] = 12
			month[n] = 03
			n += 1
		elif int(julian_decimal_time[n]) == 72:
			#date_derived[n] = str(year[n])+'-03-13'
			day[n] = 13
			month[n] = 03
			n += 1
		elif int(julian_decimal_time[n]) == 73:
			#date_derived[n] = str(year[n])+'-03-14'
			day[n] = 14
			month[n] = 03
			n += 1
		elif int(julian_decimal_time[n]) == 74:
			#date_derived[n] = str(year[n])+'-03-15'
			day[n] = 15
			month[n] = 03
			n += 1
		elif int(julian_decimal_time[n]) == 75:
			#date_derived[n] = str(year[n])+'-03-16'
			day[n] = 16
			month[n] = 03
			n += 1
		elif int(julian_decimal_time[n]) == 76:
			#date_derived[n] = str(year[n])+'-03-17'
			day[n] = 17
			month[n] = 03
			n += 1
		elif int(julian_decimal_time[n]) == 77:
			#date_derived[n] = str(year[n])+'-03-18'
			day[n] = 18
			month[n] = 03
			n += 1
		elif int(julian_decimal_time[n]) == 78:
			#date_derived[n] = str(year[n])+'-03-19'
			day[n] = 19
			month[n] = 03
			n += 1
		elif int(julian_decimal_time[n]) == 79:
			#date_derived[n] = str(year[n])+'-03-20'
			day[n] = 20
			month[n] = 03
			n += 1
		elif int(julian_decimal_time[n]) == 80:
			#date_derived[n] = str(year[n])+'-03-21'
			day[n] = 21
			month[n] = 03
			n += 1
		elif int(julian_decimal_time[n]) == 81:
			#date_derived[n] = str(year[n])+'-03-22'
			day[n] = 22
			month[n] = 03
			n += 1
		elif int(julian_decimal_time[n]) == 82:
			#date_derived[n] = str(year[n])+'-03-23'
			day[n] = 23
			month[n] = 03
			n += 1
		elif int(julian_decimal_time[n]) == 83:
			#date_derived[n] = str(year[n])+'-03-24'
			day[n] = 24
			month[n] = 03
			n += 1
		elif int(julian_decimal_time[n]) == 84:
			#date_derived[n] = str(year[n])+'-03-25'
			day[n] = 25
			month[n] = 03
			n += 1
		elif int(julian_decimal_time[n]) == 85:
			#date_derived[n] = str(year[n])+'-03-26'
			day[n] = 26
			month[n] = 03
			n += 1
		elif int(julian_decimal_time[n]) == 86:
			#date_derived[n] = str(year[n])+'-03-27'
			day[n] = 27
			month[n] = 03
			n += 1
		elif int(julian_decimal_time[n]) == 87:
			#date_derived[n] = str(year[n])+'-03-28'
			day[n] = 28
			month[n] = 03
			n += 1
		elif int(julian_decimal_time[n]) == 88:
			#date_derived[n] = str(year[n])+'-03-29'
			day[n] = 29
			month[n] = 03
			n += 1
		elif int(julian_decimal_time[n]) == 89:
			#date_derived[n] = str(year[n])+'-03-30'
			day[n] = 30
			month[n] = 03
			n += 1
		elif int(julian_decimal_time[n]) == 90:
			#date_derived[n] = str(year[n])+'-03-31'
			day[n] = 31
			month[n] = 03
			n += 1
		elif int(julian_decimal_time[n]) == 91:
			#date_derived[n] = str(year[n])+'-04-01'
			day[n] = 1
			month[n] = 04
			n += 1
		elif int(julian_decimal_time[n]) == 92:
			#date_derived[n] = str(year[n])+'-04-02'
			day[n] = 2
			month[n] = 04
			n += 1
		elif int(julian_decimal_time[n]) == 93:
			#date_derived[n] = str(year[n])+'-04-03'
			day[n] = 3
			month[n] = 04
			n += 1
		elif int(julian_decimal_time[n]) == 94:
			#date_derived[n] = str(year[n])+'-04-04'
			day[n] = 4
			month[n] = 04
			n += 1
		elif int(julian_decimal_time[n]) == 95:
			#date_derived[n] = str(year[n])+'-04-05'
			day[n] = 5
			month[n] = 04
			n += 1
		elif int(julian_decimal_time[n]) == 96:
			#date_derived[n] = str(year[n])+'-04-06'
			day[n] = 6
			month[n] = 04
			n += 1
		elif int(julian_decimal_time[n]) == 97:
			#date_derived[n] = str(year[n])+'-04-07'
			day[n] = 7
			month[n] = 04
			n += 1
		elif int(julian_decimal_time[n]) == 98:
			#date_derived[n] = str(year[n])+'-04-08'
			day[n] = 8
			month[n] = 04
			n += 1
		elif int(julian_decimal_time[n]) == 99:
			#date_derived[n] = str(year[n])+'-04-09'
			day[n] = 9
			month[n] = 04
			n += 1
		elif int(julian_decimal_time[n]) == 100:
			#date_derived[n] = str(year[n])+'-04-10'
			day[n] = 10
			month[n] = 04
			n += 1
		elif int(julian_decimal_time[n]) == 101:
			#date_derived[n] = str(year[n])+'-04-11'
			day[n] = 11
			month[n] = 04
			n += 1
		elif int(julian_decimal_time[n]) == 102:
			#date_derived[n] = str(year[n])+'-04-12'
			day[n] = 12
			month[n] = 04
			n += 1
		elif int(julian_decimal_time[n]) == 103:
			#date_derived[n] = str(year[n])+'-04-13'
			day[n] = 13
			month[n] = 04
			n += 1
		elif int(julian_decimal_time[n]) == 104:
			#date_derived[n] = str(year[n])+'-04-14'
			day[n] = 14
			month[n] = 04
			n += 1
		elif int(julian_decimal_time[n]) == 105:
			#date_derived[n] = str(year[n])+'-04-15'
			day[n] = 15
			month[n] = 04
			n += 1
		elif int(julian_decimal_time[n]) == 106:
			#date_derived[n] = str(year[n])+'-04-16'
			day[n] = 16
			month[n] = 04
			n += 1
		elif int(julian_decimal_time[n]) == 107:
			#date_derived[n] = str(year[n])+'-04-17'
			day[n] = 17
			month[n] = 04
			n += 1
		elif int(julian_decimal_time[n]) == 108:
			#date_derived[n] = str(year[n])+'-04-18'
			day[n] = 18
			month[n] = 04
			n += 1
		elif int(julian_decimal_time[n]) == 109:
			#date_derived[n] = str(year[n])+'-04-19'
			day[n] = 19
			month[n] = 04
			n += 1
		elif int(julian_decimal_time[n]) == 110:
			#date_derived[n] = str(year[n])+'-04-20'
			day[n] = 20
			month[n] = 04
			n += 1
		elif int(julian_decimal_time[n]) == 111:
			#date_derived[n] = str(year[n])+'-04-21'
			day[n] = 21
			month[n] = 04
			n += 1
		elif int(julian_decimal_time[n]) == 112:
			#date_derived[n] = str(year[n])+'-04-22'
			day[n] = 22
			month[n] = 04
			n += 1
		elif int(julian_decimal_time[n]) == 113:
			#date_derived[n] = str(year[n])+'-04-23'
			day[n] = 23
			month[n] = 04
			n += 1
		elif int(julian_decimal_time[n]) == 114:
			#date_derived[n] = str(year[n])+'-04-24'
			day[n] = 24
			month[n] = 04
			n += 1
		elif int(julian_decimal_time[n]) == 115:
			#date_derived[n] = str(year[n])+'-04-25'
			day[n] = 25
			month[n] = 04
			n += 1
		elif int(julian_decimal_time[n]) == 116:
			#date_derived[n] = str(year[n])+'-04-26'
			day[n] = 26
			month[n] = 04
			n += 1
		elif int(julian_decimal_time[n]) == 117:
			#date_derived[n] = str(year[n])+'-04-27'
			day[n] = 27
			month[n] = 04
			n += 1
		elif int(julian_decimal_time[n]) == 118:
			#date_derived[n] = str(year[n])+'-04-28'
			day[n] = 28
			month[n] = 04
			n += 1
		elif int(julian_decimal_time[n]) == 119:
			#date_derived[n] = str(year[n])+'-04-29'
			day[n] = 29
			month[n] = 04
			n += 1
		elif int(julian_decimal_time[n]) == 120:
			#date_derived[n] = str(year[n])+'-04-30'
			day[n] = 30
			month[n] = 04
			n += 1
		elif int(julian_decimal_time[n]) == 121:
			#date_derived[n] = str(year[n])+'-05-01'
			day[n] = 1
			month[n] = 05
			n += 1
		elif int(julian_decimal_time[n]) == 122:
			#date_derived[n] = str(year[n])+'-05-02'
			day[n] = 2
			month[n] = 05
			n += 1
		elif int(julian_decimal_time[n]) == 123:
			#date_derived[n] = str(year[n])+'-05-03'
			day[n] = 3
			month[n] = 05
			n += 1
		elif int(julian_decimal_time[n]) == 124:
			#date_derived[n] = str(year[n])+'-05-04'
			day[n] = 4
			month[n] = 05
			n += 1
		elif int(julian_decimal_time[n]) == 125:
			#date_derived[n] = str(year[n])+'-05-05'
			day[n] = 5
			month[n] = 05
			n += 1
		elif int(julian_decimal_time[n]) == 126:
			#date_derived[n] = str(year[n])+'-05-06'
			day[n] = 6
			month[n] = 05
			n += 1
		elif int(julian_decimal_time[n]) == 127:
			#date_derived[n] = str(year[n])+'-05-07'
			day[n] = 7
			month[n] = 05
			n += 1
		elif int(julian_decimal_time[n]) == 128:
			#date_derived[n] = str(year[n])+'-05-08'
			day[n] = 8
			month[n] = 05
			n += 1
		elif int(julian_decimal_time[n]) == 129:
			#date_derived[n] = str(year[n])+'-05-09'
			day[n] = 9
			month[n] = 05
			n += 1
		elif int(julian_decimal_time[n]) == 130:
			#date_derived[n] = str(year[n])+'-05-10'
			day[n] = 10
			month[n] = 05
			n += 1
		elif int(julian_decimal_time[n]) == 131:
			#date_derived[n] = str(year[n])+'-05-11'
			day[n] = 11
			month[n] = 05
			n += 1
		elif int(julian_decimal_time[n]) == 132:
			#date_derived[n] = str(year[n])+'-05-12'
			day[n] = 12
			month[n] = 05
			n += 1
		elif int(julian_decimal_time[n]) == 133:
			#date_derived[n] = str(year[n])+'-05-13'
			day[n] = 13
			month[n] = 05
			n += 1
		elif int(julian_decimal_time[n]) == 134:
			#date_derived[n] = str(year[n])+'-05-14'
			day[n] = 14
			month[n] = 05
			n += 1
		elif int(julian_decimal_time[n]) == 135:
			#date_derived[n] = str(year[n])+'-05-15'
			day[n] = 15
			month[n] = 05
			n += 1
		elif int(julian_decimal_time[n]) == 136:
			#date_derived[n] = str(year[n])+'-05-16'
			day[n] = 16
			month[n] = 05
			n += 1
		elif int(julian_decimal_time[n]) == 137:
			#date_derived[n] = str(year[n])+'-05-17'
			day[n] = 17
			month[n] = 05
			n += 1
		elif int(julian_decimal_time[n]) == 138:
			#date_derived[n] = str(year[n])+'-05-18'
			day[n] = 18
			month[n] = 05
			n += 1
		elif int(julian_decimal_time[n]) == 139:
			#date_derived[n] = str(year[n])+'-05-19'
			day[n] = 19
			month[n] = 05
			n += 1
		elif int(julian_decimal_time[n]) == 140:
			#date_derived[n] = str(year[n])+'-05-20'
			day[n] = 20
			month[n] = 05
			n += 1
		elif int(julian_decimal_time[n]) == 141:
			#date_derived[n] = str(year[n])+'-05-21'
			day[n] = 21
			month[n] = 05
			n += 1
		elif int(julian_decimal_time[n]) == 142:
			#date_derived[n] = str(year[n])+'-05-22'
			day[n] = 22
			month[n] = 05
			n += 1
		elif int(julian_decimal_time[n]) == 143:
			#date_derived[n] = str(year[n])+'-05-23'
			day[n] = 23
			month[n] = 05
			n += 1
		elif int(julian_decimal_time[n]) == 144:
			#date_derived[n] = str(year[n])+'-05-24'
			day[n] = 24
			month[n] = 05
			n += 1
		elif int(julian_decimal_time[n]) == 145:
			#date_derived[n] = str(year[n])+'-05-25'
			day[n] = 25
			month[n] = 05
			n += 1
		elif int(julian_decimal_time[n]) == 146:
			#date_derived[n] = str(year[n])+'-05-26'
			day[n] = 26
			month[n] = 05
			n += 1
		elif int(julian_decimal_time[n]) == 147:
			#date_derived[n] = str(year[n])+'-05-27'
			day[n] = 27
			month[n] = 05
			n += 1
		elif int(julian_decimal_time[n]) == 148:
			#date_derived[n] = str(year[n])+'-05-28'
			day[n] = 28
			month[n] = 05
			n += 1
		elif int(julian_decimal_time[n]) == 149:
			#date_derived[n] = str(year[n])+'-05-29'
			day[n] = 29
			month[n] = 05
			n += 1
		elif int(julian_decimal_time[n]) == 150:
			#date_derived[n] = str(year[n])+'-05-30'
			day[n] = 30
			month[n] = 05
			n += 1
		elif int(julian_decimal_time[n]) == 151:
			#date_derived[n] = str(year[n])+'-05-31'
			day[n] = 31
			month[n] = 05
			n += 1
		elif int(julian_decimal_time[n]) == 152:
			#date_derived[n] = str(year[n])+'-06-01'
			day[n] = 1
			month[n] = 06
			n += 1
		elif int(julian_decimal_time[n]) == 153:
			#date_derived[n] = str(year[n])+'-06-02'
			day[n] = 2
			month[n] = 06
			n += 1
		elif int(julian_decimal_time[n]) == 154:
			#date_derived[n] = str(year[n])+'-06-03'
			day[n] = 3
			month[n] = 06
			n += 1
		elif int(julian_decimal_time[n]) == 155:
			#date_derived[n] = str(year[n])+'-06-04'
			day[n] = 4
			month[n] = 06
			n += 1
		elif int(julian_decimal_time[n]) == 156:
			#date_derived[n] = str(year[n])+'-06-05'
			day[n] = 5
			month[n] = 06
			n += 1
		elif int(julian_decimal_time[n]) == 157:
			#date_derived[n] = str(year[n])+'-06-06'
			day[n] = 6
			month[n] = 06
			n += 1
		elif int(julian_decimal_time[n]) == 158:
			#date_derived[n] = str(year[n])+'-06-07'
			day[n] = 7
			month[n] = 06
			n += 1
		elif int(julian_decimal_time[n]) == 159:
			#date_derived[n] = str(year[n])+'-06-08'
			day[n] = 8
			month[n] = 06
			n += 1
		elif int(julian_decimal_time[n]) == 160:
			#date_derived[n] = str(year[n])+'-06-09'
			day[n] = 9
			month[n] = 06
			n += 1
		elif int(julian_decimal_time[n]) == 161:
			#date_derived[n] = str(year[n])+'-06-10'
			day[n] = 10
			month[n] = 06
			n += 1
		elif int(julian_decimal_time[n]) == 162:
			#date_derived[n] = str(year[n])+'-06-11'
			day[n] = 11
			month[n] = 06
			n += 1
		elif int(julian_decimal_time[n]) == 163:
			#date_derived[n] = str(year[n])+'-06-12'
			day[n] = 12
			month[n] = 06
			n += 1
		elif int(julian_decimal_time[n]) == 164:
			#date_derived[n] = str(year[n])+'-06-13'
			day[n] = 13
			month[n] = 06
			n += 1
		elif int(julian_decimal_time[n]) == 165:
			#date_derived[n] = str(year[n])+'-06-14'
			day[n] = 14
			month[n] = 06
			n += 1
		elif int(julian_decimal_time[n]) == 166:
			#date_derived[n] = str(year[n])+'-06-15'
			day[n] = 15
			month[n] = 06
			n += 1
		elif int(julian_decimal_time[n]) == 167:
			#date_derived[n] = str(year[n])+'-06-16'
			day[n] = 16
			month[n] = 06
			n += 1
		elif int(julian_decimal_time[n]) == 168:
			#date_derived[n] = str(year[n])+'-06-17'
			day[n] = 17
			month[n] = 06
			n += 1
		elif int(julian_decimal_time[n]) == 169:
			#date_derived[n] = str(year[n])+'-06-18'
			day[n] = 18
			month[n] = 06
			n += 1
		elif int(julian_decimal_time[n]) == 170:
			#date_derived[n] = str(year[n])+'-06-19'
			day[n] = 19
			month[n] = 06
			n += 1
		elif int(julian_decimal_time[n]) == 171:
			#date_derived[n] = str(year[n])+'-06-20'
			day[n] = 20
			month[n] = 06
			n += 1
		elif int(julian_decimal_time[n]) == 172:
			#date_derived[n] = str(year[n])+'-06-21'
			day[n] = 21
			month[n] = 06
			n += 1
		elif int(julian_decimal_time[n]) == 173:
			#date_derived[n] = str(year[n])+'-06-22'
			day[n] = 22
			month[n] = 06
			n += 1
		elif int(julian_decimal_time[n]) == 174:
			#date_derived[n] = str(year[n])+'-06-23'
			day[n] = 23
			month[n] = 06
			n += 1
		elif int(julian_decimal_time[n]) == 175:
			#date_derived[n] = str(year[n])+'-06-24'
			day[n] = 24
			month[n] = 06
			n += 1
		elif int(julian_decimal_time[n]) == 176:
			#date_derived[n] = str(year[n])+'-06-25'
			day[n] = 25
			month[n] = 06
			n += 1
		elif int(julian_decimal_time[n]) == 177:
			#date_derived[n] = str(year[n])+'-06-26'
			day[n] = 26
			month[n] = 06
			n += 1
		elif int(julian_decimal_time[n]) == 178:
			#date_derived[n] = str(year[n])+'-06-27'
			day[n] = 27
			month[n] = 06
			n += 1
		elif int(julian_decimal_time[n]) == 179:
			#date_derived[n] = str(year[n])+'-06-28'
			day[n] = 28
			month[n] = 06
			n += 1
		elif int(julian_decimal_time[n]) == 180:
			#date_derived[n] = str(year[n])+'-06-29'
			day[n] = 29
			month[n] = 06
			n += 1
		elif int(julian_decimal_time[n]) == 181:
			#date_derived[n] = str(year[n])+'-06-30'
			day[n] = 30
			month[n] = 06
			n += 1
		elif int(julian_decimal_time[n]) == 182:
			#date_derived[n] = str(year[n])+'-07-01'
			day[n] = 1
			month[n] = 07
			n += 1
		elif int(julian_decimal_time[n]) == 183:
			#date_derived[n] = str(year[n])+'-07-02'
			day[n] = 2
			month[n] = 07
			n += 1
		elif int(julian_decimal_time[n]) == 184:
			#date_derived[n] = str(year[n])+'-07-03'
			day[n] = 3
			month[n] = 07
			n += 1
		elif int(julian_decimal_time[n]) == 185:
			#date_derived[n] = str(year[n])+'-07-04'
			day[n] = 4
			month[n] = 07
			n += 1
		elif int(julian_decimal_time[n]) == 186:
			#date_derived[n] = str(year[n])+'-07-05'
			day[n] = 5
			month[n] = 07
			n += 1
		elif int(julian_decimal_time[n]) == 187:
			#date_derived[n] = str(year[n])+'-07-06'
			day[n] = 6
			month[n] = 07
			n += 1
		elif int(julian_decimal_time[n]) == 188:
			#date_derived[n] = str(year[n])+'-07-07'
			day[n] = 7
			month[n] = 07
			n += 1
		elif int(julian_decimal_time[n]) == 189:
			#date_derived[n] = str(year[n])+'-07-08'
			day[n] = 8
			month[n] = 07
			n += 1
		elif int(julian_decimal_time[n]) == 190:
			#date_derived[n] = str(year[n])+'-07-09'
			day[n] = 9
			month[n] = 07
			n += 1
		elif int(julian_decimal_time[n]) == 191:
			#date_derived[n] = str(year[n])+'-07-10'
			day[n] = 10
			month[n] = 07
			n += 1
		elif int(julian_decimal_time[n]) == 192:
			#date_derived[n] = str(year[n])+'-07-11'
			day[n] = 11
			month[n] = 07
			n += 1
		elif int(julian_decimal_time[n]) == 193:
			#date_derived[n] = str(year[n])+'-07-12'
			day[n] = 12
			month[n] = 07
			n += 1
		elif int(julian_decimal_time[n]) == 194:
			#date_derived[n] = str(year[n])+'-07-13'
			day[n] = 13
			month[n] = 07
			n += 1
		elif int(julian_decimal_time[n]) == 195:
			#date_derived[n] = str(year[n])+'-07-14'
			day[n] = 14
			month[n] = 07
			n += 1
		elif int(julian_decimal_time[n]) == 196:
			#date_derived[n] = str(year[n])+'-07-15'
			day[n] = 15
			month[n] = 07
			n += 1
		elif int(julian_decimal_time[n]) == 197:
			#date_derived[n] = str(year[n])+'-07-16'
			day[n] = 16
			month[n] = 07
			n += 1
		elif int(julian_decimal_time[n]) == 198:
			#date_derived[n] = str(year[n])+'-07-17'
			day[n] = 17
			month[n] = 07
			n += 1
		elif int(julian_decimal_time[n]) == 199:
			#date_derived[n] = str(year[n])+'-07-18'
			day[n] = 18
			month[n] = 07
			n += 1
		elif int(julian_decimal_time[n]) == 200:
			#date_derived[n] = str(year[n])+'-07-19'
			day[n] = 19
			month[n] = 07
			n += 1
		elif int(julian_decimal_time[n]) == 201:
			#date_derived[n] = str(year[n])+'-07-20'
			day[n] = 20
			month[n] = 07
			n += 1
		elif int(julian_decimal_time[n]) == 202:
			#date_derived[n] = str(year[n])+'-07-21'
			day[n] = 21
			month[n] = 07
			n += 1
		elif int(julian_decimal_time[n]) == 203:
			#date_derived[n] = str(year[n])+'-07-22'
			day[n] = 22
			month[n] = 07
			n += 1
		elif int(julian_decimal_time[n]) == 204:
			#date_derived[n] = str(year[n])+'-07-23'
			day[n] = 23
			month[n] = 07
			n += 1
		elif int(julian_decimal_time[n]) == 205:
			#date_derived[n] = str(year[n])+'-07-24'
			day[n] = 24
			month[n] = 07
			n += 1
		elif int(julian_decimal_time[n]) == 206:
			#date_derived[n] = str(year[n])+'-07-25'
			day[n] = 25
			month[n] = 07
			n += 1
		elif int(julian_decimal_time[n]) == 207:
			#date_derived[n] = str(year[n])+'-07-26'
			day[n] = 26
			month[n] = 07
			n += 1
		elif int(julian_decimal_time[n]) == 208:
			#date_derived[n] = str(year[n])+'-07-27'
			day[n] = 27
			month[n] = 07
			n += 1
		elif int(julian_decimal_time[n]) == 209:
			#date_derived[n] = str(year[n])+'-07-28'
			day[n] = 28
			month[n] = 07
			n += 1
		elif int(julian_decimal_time[n]) == 210:
			#date_derived[n] = str(year[n])+'-07-29'
			day[n] = 29
			month[n] = 07
			n += 1
		elif int(julian_decimal_time[n]) == 211:
			#date_derived[n] = str(year[n])+'-07-30'
			day[n] = 30
			month[n] = 07
			n += 1
		elif int(julian_decimal_time[n]) == 212:
			#date_derived[n] = str(year[n])+'-07-31'
			day[n] = 31
			month[n] = 07
			n += 1
		elif int(julian_decimal_time[n]) == 213:
			#date_derived[n] = str(year[n])+'-08-01'
			day[n] = 1
			month[n] = 8
			n += 1
		elif int(julian_decimal_time[n]) == 214:
			#date_derived[n] = str(year[n])+'-08-02'
			day[n] = 2
			month[n] = 8
			n += 1
		elif int(julian_decimal_time[n]) == 215:
			#date_derived[n] = str(year[n])+'-08-03'
			day[n] = 3
			month[n] = 8
			n += 1
		elif int(julian_decimal_time[n]) == 216:
			#date_derived[n] = str(year[n])+'-08-04'
			day[n] = 4
			month[n] = 8
			n += 1
		elif int(julian_decimal_time[n]) == 217:
			#date_derived[n] = str(year[n])+'-08-05'
			day[n] = 5
			month[n] = 8
			n += 1
		elif int(julian_decimal_time[n]) == 218:
			#date_derived[n] = str(year[n])+'-08-06'
			day[n] = 6
			month[n] = 8
			n += 1
		elif int(julian_decimal_time[n]) == 219:
			#date_derived[n] = str(year[n])+'-08-07'
			day[n] = 7
			month[n] = 8
			n += 1
		elif int(julian_decimal_time[n]) == 220:
			#date_derived[n] = str(year[n])+'-08-08'
			day[n] = 8
			month[n] = 8
			n += 1
		elif int(julian_decimal_time[n]) == 221:
			#date_derived[n] = str(year[n])+'-08-09'
			day[n] = 9
			month[n] = 8
			n += 1
		elif int(julian_decimal_time[n]) == 222:
			#date_derived[n] = str(year[n])+'-08-10'
			day[n] = 10
			month[n] = 8
			n += 1
		elif int(julian_decimal_time[n]) == 223:
			#date_derived[n] = str(year[n])+'-08-11'
			day[n] = 11
			month[n] = 8
			n += 1
		elif int(julian_decimal_time[n]) == 224:
			#date_derived[n] = str(year[n])+'-08-12'
			day[n] = 12
			month[n] = 8
			n += 1
		elif int(julian_decimal_time[n]) == 225:
			#date_derived[n] = str(year[n])+'-08-13'
			day[n] = 13
			month[n] = 8
			n += 1
		elif int(julian_decimal_time[n]) == 226:
			#date_derived[n] = str(year[n])+'-08-14'
			day[n] = 14
			month[n] = 8
			n += 1
		elif int(julian_decimal_time[n]) == 227:
			#date_derived[n] = str(year[n])+'-08-15'
			day[n] = 15
			month[n] = 8
			n += 1
		elif int(julian_decimal_time[n]) == 228:
			#date_derived[n] = str(year[n])+'-08-16'
			day[n] = 16
			month[n] = 8
			n += 1
		elif int(julian_decimal_time[n]) == 229:
			#date_derived[n] = str(year[n])+'-08-17'
			day[n] = 17
			month[n] = 8
			n += 1
		elif int(julian_decimal_time[n]) == 230:
			#date_derived[n] = str(year[n])+'-08-18'
			day[n] = 18
			month[n] = 8
			n += 1
		elif int(julian_decimal_time[n]) == 231:
			#date_derived[n] = str(year[n])+'-08-19'
			day[n] = 19
			month[n] = 8
			n += 1
		elif int(julian_decimal_time[n]) == 232:
			#date_derived[n] = str(year[n])+'-08-20'
			day[n] = 20
			month[n] = 8
			n += 1
		elif int(julian_decimal_time[n]) == 233:
			#date_derived[n] = str(year[n])+'-08-21'
			day[n] = 21
			month[n] = 8
			n += 1
		elif int(julian_decimal_time[n]) == 234:
			#date_derived[n] = str(year[n])+'-08-22'
			day[n] = 22
			month[n] = 8
			n += 1
		elif int(julian_decimal_time[n]) == 235:
			#date_derived[n] = str(year[n])+'-08-23'
			day[n] = 23
			month[n] = 8
			n += 1
		elif int(julian_decimal_time[n]) == 236:
			#date_derived[n] = str(year[n])+'-08-24'
			day[n] = 24
			month[n] = 8
			n += 1
		elif int(julian_decimal_time[n]) == 237:
			#date_derived[n] = str(year[n])+'-08-25'
			day[n] = 25
			month[n] = 8
			n += 1
		elif int(julian_decimal_time[n]) == 238:
			#date_derived[n] = str(year[n])+'-08-26'
			day[n] = 26
			month[n] = 8
			n += 1
		elif int(julian_decimal_time[n]) == 239:
			#date_derived[n] = str(year[n])+'-08-27'
			day[n] = 27
			month[n] = 8
			n += 1
		elif int(julian_decimal_time[n]) == 240:
			#date_derived[n] = str(year[n])+'-08-28'
			day[n] = 28
			month[n] = 8
			n += 1
		elif int(julian_decimal_time[n]) == 241:
			#date_derived[n] = str(year[n])+'-08-29'
			day[n] = 29
			month[n] = 8
			n += 1
		elif int(julian_decimal_time[n]) == 242:
			#date_derived[n] = str(year[n])+'-08-30'
			day[n] = 30
			month[n] = 8
			n += 1
		elif int(julian_decimal_time[n]) == 243:
			#date_derived[n] = str(year[n])+'-08-31'
			day[n] = 31
			month[n] = 8
			n += 1
		elif int(julian_decimal_time[n]) == 244:
			#date_derived[n] = str(year[n])+'-09-01'
			day[n] = 1
			month[n] = 9
			n += 1
		elif int(julian_decimal_time[n]) == 245:
			#date_derived[n] = str(year[n])+'-09-02'
			day[n] = 2
			month[n] = 9
			n += 1
		elif int(julian_decimal_time[n]) == 246:
			#date_derived[n] = str(year[n])+'-09-03'
			day[n] = 3
			month[n] = 9
			n += 1
		elif int(julian_decimal_time[n]) == 247:
			#date_derived[n] = str(year[n])+'-09-04'
			day[n] = 4
			month[n] = 9
			n += 1
		elif int(julian_decimal_time[n]) == 248:
			#date_derived[n] = str(year[n])+'-09-05'
			day[n] = 5
			month[n] = 9
			n += 1
		elif int(julian_decimal_time[n]) == 249:
			#date_derived[n] = str(year[n])+'-09-06'
			day[n] = 6
			month[n] = 9
			n += 1
		elif int(julian_decimal_time[n]) == 250:
			#date_derived[n] = str(year[n])+'-09-07'
			day[n] = 7
			month[n] = 9
			n += 1
		elif int(julian_decimal_time[n]) == 251:
			#date_derived[n] = str(year[n])+'-09-08'
			day[n] = 8
			month[n] = 9
			n += 1
		elif int(julian_decimal_time[n]) == 252:
			#date_derived[n] = str(year[n])+'-09-09'
			day[n] = 9
			month[n] = 9
			n += 1
		elif int(julian_decimal_time[n]) == 253:
			#date_derived[n] = str(year[n])+'-09-10'
			day[n] = 10
			month[n] = 9
			n += 1
		elif int(julian_decimal_time[n]) == 254:
			#date_derived[n] = str(year[n])+'-09-11'
			day[n] = 11
			month[n] = 9
			n += 1
		elif int(julian_decimal_time[n]) == 255:
			#date_derived[n] = str(year[n])+'-09-12'
			day[n] = 12
			month[n] = 9
			n += 1
		elif int(julian_decimal_time[n]) == 256:
			#date_derived[n] = str(year[n])+'-09-13'
			day[n] = 13
			month[n] = 9
			n += 1
		elif int(julian_decimal_time[n]) == 257:
			#date_derived[n] = str(year[n])+'-09-14'
			day[n] = 14
			month[n] = 9
			n += 1
		elif int(julian_decimal_time[n]) == 258:
			#date_derived[n] = str(year[n])+'-09-15'
			day[n] = 15
			month[n] = 9
			n += 1
		elif int(julian_decimal_time[n]) == 259:
			#date_derived[n] = str(year[n])+'-09-16'
			day[n] = 16
			month[n] = 9
			n += 1
		elif int(julian_decimal_time[n]) == 260:
			#date_derived[n] = str(year[n])+'-09-17'
			day[n] = 17
			month[n] = 9
			n += 1
		elif int(julian_decimal_time[n]) == 261:
			#date_derived[n] = str(year[n])+'-09-18'
			day[n] = 18
			month[n] = 9
			n += 1
		elif int(julian_decimal_time[n]) == 262:
			#date_derived[n] = str(year[n])+'-09-19'
			day[n] = 19
			month[n] = 9
			n += 1
		elif int(julian_decimal_time[n]) == 263:
			#date_derived[n] = str(year[n])+'-09-20'
			day[n] = 20
			month[n] = 9
			n += 1
		elif int(julian_decimal_time[n]) == 264:
			#date_derived[n] = str(year[n])+'-09-21'
			day[n] = 21
			month[n] = 9
			n += 1
		elif int(julian_decimal_time[n]) == 265:
			#date_derived[n] = str(year[n])+'-09-22'
			day[n] = 22
			month[n] = 9
			n += 1
		elif int(julian_decimal_time[n]) == 266:
			#date_derived[n] = str(year[n])+'-09-23'
			day[n] = 23
			month[n] = 9
			n += 1
		elif int(julian_decimal_time[n]) == 267:
			#date_derived[n] = str(year[n])+'-09-24'
			day[n] = 24
			month[n] = 9
			n += 1
		elif int(julian_decimal_time[n]) == 268:
			#date_derived[n] = str(year[n])+'-09-25'
			day[n] = 25
			month[n] = 9
			n += 1
		elif int(julian_decimal_time[n]) == 269:
			#date_derived[n] = str(year[n])+'-09-26'
			day[n] = 26
			month[n] = 9
			n += 1
		elif int(julian_decimal_time[n]) == 270:
			#date_derived[n] = str(year[n])+'-09-27'
			day[n] = 27
			month[n] = 9
			n += 1
		elif int(julian_decimal_time[n]) == 271:
			#date_derived[n] = str(year[n])+'-09-28'
			day[n] = 28
			month[n] = 9
			n += 1
		elif int(julian_decimal_time[n]) == 272:
			#date_derived[n] = str(year[n])+'-09-29'
			day[n] = 29
			month[n] = 9
			n += 1
		elif int(julian_decimal_time[n]) == 273:
			#date_derived[n] = str(year[n])+'-09-30'
			day[n] = 30
			month[n] = 9
			n += 1
		elif int(julian_decimal_time[n]) == 274:
			#date_derived[n] = str(year[n])+'-10-01'
			day[n] = 1
			month[n] = 10
			n += 1
		elif int(julian_decimal_time[n]) == 275:
			#date_derived[n] = str(year[n])+'-10-02'
			day[n] = 2
			month[n] = 10
			n += 1
		elif int(julian_decimal_time[n]) == 276:
			#date_derived[n] = str(year[n])+'-10-03'
			day[n] = 3
			month[n] = 10
			n += 1
		elif int(julian_decimal_time[n]) == 277:
			#date_derived[n] = str(year[n])+'-10-04'
			day[n] = 4
			month[n] = 10
			n += 1
		elif int(julian_decimal_time[n]) == 278:
			#date_derived[n] = str(year[n])+'-10-05'
			day[n] = 5
			month[n] = 10
			n += 1
		elif int(julian_decimal_time[n]) == 279:
			#date_derived[n] = str(year[n])+'-10-06'
			day[n] = 6
			month[n] = 10
			n += 1
		elif int(julian_decimal_time[n]) == 280:
			#date_derived[n] = str(year[n])+'-10-07'
			day[n] = 7
			month[n] = 10
			n += 1
		elif int(julian_decimal_time[n]) == 281:
			#date_derived[n] = str(year[n])+'-10-08'
			day[n] = 8
			month[n] = 10
			n += 1
		elif int(julian_decimal_time[n]) == 282:
			#date_derived[n] = str(year[n])+'-10-09'
			day[n] = 9
			month[n] = 10
			n += 1
		elif int(julian_decimal_time[n]) == 283:
			#date_derived[n] = str(year[n])+'-10-10'
			day[n] = 10
			month[n] = 10
			n += 1
		elif int(julian_decimal_time[n]) == 284:
			#date_derived[n] = str(year[n])+'-10-11'
			day[n] = 11
			month[n] = 10
			n += 1
		elif int(julian_decimal_time[n]) == 285:
			#date_derived[n] = str(year[n])+'-10-12'
			day[n] = 12
			month[n] = 10
			n += 1
		elif int(julian_decimal_time[n]) == 286:
			#date_derived[n] = str(year[n])+'-10-13'
			day[n] = 13
			month[n] = 10
			n += 1
		elif int(julian_decimal_time[n]) == 287:
			#date_derived[n] = str(year[n])+'-10-14'
			day[n] = 14
			month[n] = 10
			n += 1
		elif int(julian_decimal_time[n]) == 288:
			#date_derived[n] = str(year[n])+'-10-15'
			day[n] = 15
			month[n] = 10
			n += 1
		elif int(julian_decimal_time[n]) == 289:
			#date_derived[n] = str(year[n])+'-10-16'
			day[n] = 16
			month[n] = 10
			n += 1
		elif int(julian_decimal_time[n]) == 290:
			#date_derived[n] = str(year[n])+'-10-17'
			day[n] = 17
			month[n] = 10
			n += 1
		elif int(julian_decimal_time[n]) == 291:
			#date_derived[n] = str(year[n])+'-10-18'
			day[n] = 18
			month[n] = 10
			n += 1
		elif int(julian_decimal_time[n]) == 292:
			#date_derived[n] = str(year[n])+'-10-19'
			day[n] = 19
			month[n] = 10
			n += 1
		elif int(julian_decimal_time[n]) == 293:
			#date_derived[n] = str(year[n])+'-10-20'
			day[n] = 20
			month[n] = 10
			n += 1
		elif int(julian_decimal_time[n]) == 294:
			#date_derived[n] = str(year[n])+'-10-21'
			day[n] = 21
			month[n] = 10
			n += 1
		elif int(julian_decimal_time[n]) == 295:
			#date_derived[n] = str(year[n])+'-10-22'
			day[n] = 22
			month[n] = 10
			n += 1
		elif int(julian_decimal_time[n]) == 296:
			#date_derived[n] = str(year[n])+'-10-23'
			day[n] = 23
			month[n] = 10
			n += 1
		elif int(julian_decimal_time[n]) == 297:
			#date_derived[n] = str(year[n])+'-10-24'
			day[n] = 24
			month[n] = 10
			n += 1
		elif int(julian_decimal_time[n]) == 298:
			#date_derived[n] = str(year[n])+'-10-25'
			day[n] = 25
			month[n] = 10
			n += 1
		elif int(julian_decimal_time[n]) == 299:
			#date_derived[n] = str(year[n])+'-10-26'
			day[n] = 26
			month[n] = 10
			n += 1
		elif int(julian_decimal_time[n]) == 300:
			#date_derived[n] = str(year[n])+'-10-27'
			day[n] = 27
			month[n] = 10
			n += 1
		elif int(julian_decimal_time[n]) == 301:
			#date_derived[n] = str(year[n])+'-10-28'
			day[n] = 28
			month[n] = 10
			n += 1
		elif int(julian_decimal_time[n]) == 302:
			#date_derived[n] = str(year[n])+'-10-29'
			day[n] = 29
			month[n] = 10
			n += 1
		elif int(julian_decimal_time[n]) == 303:
			#date_derived[n] = str(year[n])+'-10-30'
			day[n] = 30
			month[n] = 10
			n += 1
		elif int(julian_decimal_time[n]) == 304:
			#date_derived[n] = str(year[n])+'-10-31'
			day[n] = 31
			month[n] = 10
			n += 1
		elif int(julian_decimal_time[n]) == 305:
			#date_derived[n] = str(year[n])+'-11-01'
			day[n] = 1
			month[n] = 11
			n += 1
		elif int(julian_decimal_time[n]) == 306:
			#date_derived[n] = str(year[n])+'-11-02'
			day[n] = 2
			month[n] = 11
			n += 1
		elif int(julian_decimal_time[n]) == 307:
			#date_derived[n] = str(year[n])+'-11-03'
			day[n] = 3
			month[n] = 11
			n += 1
		elif int(julian_decimal_time[n]) == 308:
			#date_derived[n] = str(year[n])+'-11-04'
			day[n] = 4
			month[n] = 11
			n += 1
		elif int(julian_decimal_time[n]) == 309:
			#date_derived[n] = str(year[n])+'-11-05'
			day[n] = 5
			month[n] = 11
			n += 1
		elif int(julian_decimal_time[n]) == 310:
			#date_derived[n] = str(year[n])+'-11-06'
			day[n] = 6
			month[n] = 11
			n += 1
		elif int(julian_decimal_time[n]) == 311:
			#date_derived[n] = str(year[n])+'-11-07'
			day[n] = 7
			month[n] = 11
			n += 1
		elif int(julian_decimal_time[n]) == 312:
			#date_derived[n] = str(year[n])+'-11-08'
			day[n] = 8
			month[n] = 11
			n += 1
		elif int(julian_decimal_time[n]) == 313:
			#date_derived[n] = str(year[n])+'-11-09'
			day[n] = 9
			month[n] = 11
			n += 1
		elif int(julian_decimal_time[n]) == 314:
			#date_derived[n] = str(year[n])+'-11-10'
			day[n] = 10
			month[n] = 11
			n += 1
		elif int(julian_decimal_time[n]) == 315:
			#date_derived[n] = str(year[n])+'-11-11'
			day[n] = 11
			month[n] = 11
			n += 1
		elif int(julian_decimal_time[n]) == 316:
			#date_derived[n] = str(year[n])+'-11-12'
			day[n] = 12
			month[n] = 11
			n += 1
		elif int(julian_decimal_time[n]) == 317:
			#date_derived[n] = str(year[n])+'-11-13'
			day[n] = 13
			month[n] = 11
			n += 1
		elif int(julian_decimal_time[n]) == 318:
			#date_derived[n] = str(year[n])+'-11-14'
			day[n] = 14
			month[n] = 11
			n += 1
		elif int(julian_decimal_time[n]) == 319:
			#date_derived[n] = str(year[n])+'-11-15'
			day[n] = 15
			month[n] = 11
			n += 1
		elif int(julian_decimal_time[n]) == 320:
			#date_derived[n] = str(year[n])+'-11-16'
			day[n] = 16
			month[n] = 11
			n += 1
		elif int(julian_decimal_time[n]) == 321:
			#date_derived[n] = str(year[n])+'-11-17'
			day[n] = 17
			month[n] = 11
			n += 1
		elif int(julian_decimal_time[n]) == 322:
			#date_derived[n] = str(year[n])+'-11-18'
			day[n] = 18
			month[n] = 11
			n += 1
		elif int(julian_decimal_time[n]) == 323:
			#date_derived[n] = str(year[n])+'-11-19'
			day[n] = 19
			month[n] = 11
			n += 1
		elif int(julian_decimal_time[n]) == 324:
			#date_derived[n] = str(year[n])+'-11-20'
			day[n] = 20
			month[n] = 11
			n += 1
		elif int(julian_decimal_time[n]) == 325:
			#date_derived[n] = str(year[n])+'-11-21'
			day[n] = 21
			month[n] = 11
			n += 1
		elif int(julian_decimal_time[n]) == 326:
			#date_derived[n] = str(year[n])+'-11-22'
			day[n] = 22
			month[n] = 11
			n += 1
		elif int(julian_decimal_time[n]) == 327:
			#date_derived[n] = str(year[n])+'-11-23'
			day[n] = 23
			month[n] = 11
			n += 1
		elif int(julian_decimal_time[n]) == 328:
			#date_derived[n] = str(year[n])+'-11-24'
			day[n] = 24
			month[n] = 11
			n += 1
		elif int(julian_decimal_time[n]) == 329:
			#date_derived[n] = str(year[n])+'-11-25'
			day[n] = 25
			month[n] = 11
			n += 1
		elif int(julian_decimal_time[n]) == 330:
			#date_derived[n] = str(year[n])+'-11-26'
			day[n] = 26
			month[n] = 11
			n += 1
		elif int(julian_decimal_time[n]) == 331:
			#date_derived[n] = str(year[n])+'-11-27'
			day[n] = 27
			month[n] = 11
			n += 1
		elif int(julian_decimal_time[n]) == 332:
			#date_derived[n] = str(year[n])+'-11-28'
			day[n] = 28
			month[n] = 11
			n += 1
		elif int(julian_decimal_time[n]) == 333:
			#date_derived[n] = str(year[n])+'-11-29'
			day[n] = 29
			month[n] = 11
			n += 1
		elif int(julian_decimal_time[n]) == 334:
			#date_derived[n] = str(year[n])+'-11-30'
			day[n] = 30
			month[n] = 11
			n += 1
		elif int(julian_decimal_time[n]) == 335:
			#date_derived[n] = str(year[n])+'-12-01'
			day[n] = 1
			month[n] = 12
			n += 1
		elif int(julian_decimal_time[n]) == 336:
			#date_derived[n] = str(year[n])+'-12-02'
			day[n] = 2
			month[n] = 12
			n += 1
		elif int(julian_decimal_time[n]) == 337:
			#date_derived[n] = str(year[n])+'-12-03'
			day[n] = 3
			month[n] = 12
			n += 1
		elif int(julian_decimal_time[n]) == 338:
			#date_derived[n] = str(year[n])+'-12-04'
			day[n] = 4
			month[n] = 12
			n += 1
		elif int(julian_decimal_time[n]) == 339:
			#date_derived[n] = str(year[n])+'-12-05'
			day[n] = 5
			month[n] = 12
			n += 1
		elif int(julian_decimal_time[n]) == 340:
			#date_derived[n] = str(year[n])+'-12-06'
			day[n] = 6
			month[n] = 12
			n += 1
		elif int(julian_decimal_time[n]) == 341:
			#date_derived[n] = str(year[n])+'-12-07'
			day[n] = 7
			month[n] = 12
			n += 1
		elif int(julian_decimal_time[n]) == 342:
			#date_derived[n] = str(year[n])+'-12-08'
			day[n] = 8
			month[n] = 12
			n += 1
		elif int(julian_decimal_time[n]) == 343:
			#date_derived[n] = str(year[n])+'-12-09'
			day[n] = 9
			month[n] = 12
			n += 1
		elif int(julian_decimal_time[n]) == 344:
			#date_derived[n] = str(year[n])+'-12-10'
			day[n] = 10
			month[n] = 12
			n += 1
		elif int(julian_decimal_time[n]) == 345:
			#date_derived[n] = str(year[n])+'-12-11'
			day[n] = 11
			month[n] = 12
			n += 1
		elif int(julian_decimal_time[n]) == 346:
			#date_derived[n] = str(year[n])+'-12-12'
			day[n] = 12
			month[n] = 12
			n += 1
		elif int(julian_decimal_time[n]) == 347:
			#date_derived[n] = str(year[n])+'-12-13'
			day[n] = 13
			month[n] = 12
			n += 1
		elif int(julian_decimal_time[n]) == 348:
			#date_derived[n] = str(year[n])+'-12-14'
			day[n] = 14
			month[n] = 12
			n += 1
		elif int(julian_decimal_time[n]) == 349:
			#date_derived[n] = str(year[n])+'-12-15'
			day[n] = 15
			month[n] = 12
			n += 1
		elif int(julian_decimal_time[n]) == 350:
			#date_derived[n] = str(year[n])+'-12-16'
			day[n] = 16
			month[n] = 12
			n += 1
		elif int(julian_decimal_time[n]) == 351:
			#date_derived[n] = str(year[n])+'-12-17'
			day[n] = 17
			month[n] = 12
			n += 1
		elif int(julian_decimal_time[n]) == 352:
			#date_derived[n] = str(year[n])+'-12-18'
			day[n] = 18
			month[n] = 12
			n += 1
		elif int(julian_decimal_time[n]) == 353:
			#date_derived[n] = str(year[n])+'-12-19'
			day[n] = 19
			month[n] = 12
			n += 1
		elif int(julian_decimal_time[n]) == 354:
			#date_derived[n] = str(year[n])+'-12-20'
			day[n] = 20
			month[n] = 12
			n += 1
		elif int(julian_decimal_time[n]) == 355:
			#date_derived[n] = str(year[n])+'-12-21'
			day[n] = 21
			month[n] = 12
			n += 1
		elif int(julian_decimal_time[n]) == 356:
			#date_derived[n] = str(year[n])+'-12-22'
			day[n] = 22
			month[n] = 12
			n += 1
		elif int(julian_decimal_time[n]) == 357:
			#date_derived[n] = str(year[n])+'-12-23'
			day[n] = 23
			month[n] = 12
			n += 1
		elif int(julian_decimal_time[n]) == 358:
			#date_derived[n] = str(year[n])+'-12-24'
			day[n] = 24
			month[n] = 12
			n += 1
		elif int(julian_decimal_time[n]) == 359:
			#date_derived[n] = str(year[n])+'-12-25'
			day[n] = 25
			month[n] = 12
			n += 1
		elif int(julian_decimal_time[n]) == 360:
			#date_derived[n] = str(year[n])+'-12-26'
			day[n] = 26
			month[n] = 12
			n += 1
		elif int(julian_decimal_time[n]) == 361:
			#date_derived[n] = str(year[n])+'-12-27'
			day[n] = 27
			month[n] = 12
			n += 1
		elif int(julian_decimal_time[n]) == 362:
			#date_derived[n] = str(year[n])+'-12-28'
			day[n] = 28
			month[n] = 12
			n += 1
		elif int(julian_decimal_time[n]) == 363:
			#date_derived[n] = str(year[n])+'-12-29'
			day[n] = 29
			month[n] = 12
			n += 1
		elif int(julian_decimal_time[n]) == 364:
			#date_derived[n] = str(year[n])+'-12-30'
			day[n] = 30
			month[n] = 12
			n += 1
		else:
			#date_derived[n] = str(year[n])+'-12-31'
			day[n] = 31
			month[n] = 12
			n += 1
		

	root_grp.close()