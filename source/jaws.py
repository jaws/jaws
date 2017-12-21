import argparse
from netCDF4 import Dataset
from datetime import date
from astropy.io import ascii


def gcnet2nc(f):

	# NC file setup
	global op_file
	op_file = 'converted-gcnet.nc'
	if args.output:
		op_file = str(args.output)
	root_grp = Dataset(op_file, 'w', format='NETCDF4')
	root_grp.TITLE = 'Surface Radiation Data from Greenland Climate Network'
	root_grp.SOURCE = 'Surface Observations'
	root_grp.INSTITUTION = 'Cooperative Institute for Research in Enviornmental Sciences'
	root_grp.REFERENCE = 'http://cires.colorado.edu/science/groups/steffen/gcnet/'
	root_grp.URL = 'http://cires.colorado.edu/science/groups/steffen/gcnet/'
	#root_grp.History = 'Created on '
	#root_grp.CREATED_BY = 'Created by'
	root_grp.Conventions = 'CF-v46'

	# dimension
	root_grp.createDimension('time', args.row_count)

	# variables
	station_number = root_grp.createVariable('station_number', 'u1', ('time',))
	year = root_grp.createVariable('year', 'i8', ('time',))
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
	pressure = root_grp.createVariable('pressure', 'f4', ('time',))
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
	qc1 = root_grp.createVariable('qc1', 'i8', ('time',))
	qc9 = root_grp.createVariable('qc9', 'i8', ('time',))
	qc17 = root_grp.createVariable('qc17', 'i8', ('time',))
	qc25 = root_grp.createVariable('qc25', 'i8', ('time',))

	qc_swdn = root_grp.createVariable('qc_swdn', 'S1', ('time',))
	qc_swup = root_grp.createVariable('qc_swup', 'S1', ('time',))
	qc_netradiation = root_grp.createVariable('qc_netradiation', 'S1', ('time',))
	qc_ttc1 = root_grp.createVariable('qc_ttc1', 'S1', ('time',))
	qc_ttc2 = root_grp.createVariable('qc_ttc2', 'S1', ('time',))
	qc_tcs1 = root_grp.createVariable('qc_tcs1', 'S1', ('time',))
	qc_tcs2 = root_grp.createVariable('qc_tcs2', 'S1', ('time',))
	qc_rh1 = root_grp.createVariable('qc_rh1', 'S1', ('time',))
	qc_rh2 = root_grp.createVariable('qc_rh2', 'S1', ('time',))
	qc_u1 = root_grp.createVariable('qc_u1', 'S1', ('time',))
	qc_u2 = root_grp.createVariable('qc_u2', 'S1', ('time',))
	qc_ud1 = root_grp.createVariable('qc_ud1', 'S1', ('time',))
	qc_ud2 = root_grp.createVariable('qc_ud2', 'S1', ('time',))
	qc_pressure = root_grp.createVariable('qc_pressure', 'S1', ('time',))
	qc_snowheight1 = root_grp.createVariable('qc_snowheight1', 'S1', ('time',))
	qc_snowheight2 = root_grp.createVariable('qc_snowheight2', 'S1', ('time',))
	qc_tsnow1 = root_grp.createVariable('qc_tsnow1', 'S1', ('time',))
	qc_tsnow2 = root_grp.createVariable('qc_tsnow2', 'S1', ('time',))
	qc_tsnow3 = root_grp.createVariable('qc_tsnow3', 'S1', ('time',))
	qc_tsnow4 = root_grp.createVariable('qc_tsnow4', 'S1', ('time',))
	qc_tsnow5 = root_grp.createVariable('qc_tsnow5', 'S1', ('time',))
	qc_tsnow6 = root_grp.createVariable('qc_tsnow6', 'S1', ('time',))
	qc_tsnow7 = root_grp.createVariable('qc_tsnow7', 'S1', ('time',))
	qc_tsnow8 = root_grp.createVariable('qc_tsnow8', 'S1', ('time',))
	qc_tsnow9 = root_grp.createVariable('qc_tsnow9', 'S1', ('time',))
	qc_tsnow10 = root_grp.createVariable('qc_tsnow10', 'S1', ('time',))
	qc_battery = root_grp.createVariable('qc_battery', 'S1', ('time',))
	
	time = root_grp.createVariable('time', 'f4', ('time',))


	station_number.units = '1'
	station_number.original_var_name = 'Station Number'

	year.units = '1'
	year.original_var_name = 'Year'

	julian_decimal_time.units = 'decimal time'
	julian_decimal_time.original_var_name = 'Julian Decimal Time'
	julian_decimal_time.note = 'Not really a standard Julian time. For each year, time starts at 1.0000 and ends at 365.9999.'

	sw_down.units = 'W m-2'
	sw_down.original_var_name = 'SW_down'
	sw_down.long_name = 'downwelling_shortwave_flux_in_air'

	sw_up.units = 'W m-2'
	sw_up.original_var_name = 'SW_up'
	sw_up.long_name = 'upwelling_shortwave_flux_in_air'

	net_radiation.units = 'W m-2'
	net_radiation.original_var_name = 'Net Radiation'
	net_radiation.long_name = 'surface_net_downward_radiative_flux'

	temperature_tc_1.units = 'degC'
	temperature_tc_1.original_var_name = 'TC Air 1 Air Temperature'
	temperature_tc_1.long_name = 'air_temperature'
	temperature_tc_1.note = 'air temperature from TC sensor'

	temperature_tc_2.units = 'degC'
	temperature_tc_2.original_var_name = 'TC Air 2 Air Temperature'
	temperature_tc_2.long_name = 'air_temperature'

	temperature_cs500_1.units = 'degC'
	temperature_cs500_1.original_var_name = 'CS500 T Air 1 Air Temperature'
	temperature_cs500_1.long_name = 'air_temperature'
	temperature_cs500_1.note = 'air temperature from CS500 sensor'

	temperature_cs500_2.units = 'degC'
	temperature_cs500_2.original_var_name = 'CS500 T Air 2 Air Temperature'
	temperature_cs500_2.long_name = 'air_temperature'

	relative_humidity_1.units = '%'
	relative_humidity_1.original_var_name = 'RH 1 Relative Humidity'
	relative_humidity_1.long_name = 'realtive_humidity'

	relative_humidity_2.units = '%'
	relative_humidity_2.original_var_name = 'RH 2 Relative Humidity'
	relative_humidity_2.long_name = 'realtive_humidity'

	u1_wind_speed.units = 'm/s'
	u1_wind_speed.original_var_name = 'U1 Wind Speed'
	u1_wind_speed.long_name = 'wind_speed'

	u2_wind_speed.units = 'm/s'
	u2_wind_speed.original_var_name = 'U2 Wind Speed'
	u2_wind_speed.long_name = 'wind_speed'

	u_direction_1.units = 'deg'
	u_direction_1.original_var_name = 'U Dir 1'
	u_direction_1.long_name = 'wind_from_direction'

	u_direction_2.units = 'deg'
	u_direction_2.original_var_name = 'U Dir 2'
	u_direction_2.long_name = 'wind_from_direction'

	pressure.units = 'mbar'
	pressure.original_var_name = 'Atmos Pressure'
	pressure.long_name = 'surface_air_pressure'

	snow_height_1.units = 'm'
	snow_height_1.original_var_name = 'Snow Height 1'
	snow_height_1.long_name = 'snow_height'

	snow_height_2.units = 'm'
	snow_height_2.original_var_name = 'Snow Height 2'
	snow_height_2.long_name = 'snow_height'

	t_snow_01.units = 'degC'
	t_snow_01.original_var_name = 'T Snow 1'
	#t_snow_01.long_name = 'temperature_in_surface_snow'

	t_snow_02.units = 'degC'
	t_snow_02.original_var_name = 'T Snow 2'
	#t_snow_02.long_name = 'temperature_in_surface_snow'

	t_snow_03.units = 'degC'
	t_snow_03.original_var_name = 'T Snow 3'
	#t_snow_03.long_name = 'temperature_in_surface_snow'

	t_snow_04.units = 'degC'
	t_snow_04.original_var_name = 'T Snow 4'
	#t_snow_04.long_name = 'temperature_in_surface_snow'

	t_snow_05.units = 'degC'
	t_snow_05.original_var_name = 'T Snow 5'
	#t_snow_05.long_name = 'temperature_in_surface_snow'

	t_snow_06.units = 'degC'
	t_snow_06.original_var_name = 'T Snow 6'
	#t_snow_06.long_name = 'temperature_in_surface_snow'

	t_snow_07.units = 'degC'
	t_snow_07.original_var_name = 'T Snow 7'
	#t_snow_07.long_name = 'temperature_in_surface_snow'

	t_snow_08.units = 'degC'
	t_snow_08.original_var_name = 'T Snow 8'
	#t_snow_08.long_name = 'temperature_in_surface_snow'

	t_snow_09.units = 'degC'
	t_snow_09.original_var_name = 'T Snow 9'
	#t_snow_09.long_name = 'temperature_in_surface_snow'

	t_snow_10.units = 'degC'
	t_snow_10.original_var_name = 'T Snow 10'
	#t_snow_10.long_name = 'temperature_in_surface_snow'

	battery_voltage.units = 'V'
	battery_voltage.original_var_name = 'Battery Voltage'
	battery_voltage.long_name = 'battery_voltage'

	sw_down_max.units = 'W m-2'
	sw_down_max.original_var_name = 'SWinMax'
	sw_down_max.long_name = 'maximum_downwelling_shortwave_flux_in_air'
	
	sw_up_max.units = 'W m-2'
	sw_up_max.original_var_name = 'SWoutMax'
	sw_up_max.long_name = 'maximum_upwelling_shortwave_flux_in_air'
	
	net_radiation_max.units = 'W m-2'
	net_radiation_max.original_var_name = 'NetRadMax'
	net_radiation_max.long_name = 'maximum_net_radiation'

	max_air_temperature_1.units = 'degC'
	max_air_temperature_1.original_var_name = 'Max Air Temperture 1'
	max_air_temperature_1.long_name = 'air_temperature'

	max_air_temperature_2.units = 'degC'
	max_air_temperature_2.original_var_name = 'Max Air Temperture 2'
	max_air_temperature_2.long_name = 'air_temperature'

	min_air_temperature_1.units = 'degC'
	min_air_temperature_1.original_var_name = 'Min Air Temperture 1'
	min_air_temperature_1.long_name = 'air_temperature'

	min_air_temperature_2.units = 'degC'
	min_air_temperature_2.original_var_name = 'Min Air Temperture 2'
	min_air_temperature_2.long_name = 'air_temperature'

	max_windspeed_u1.units = 'm/s'
	max_windspeed_u1.original_var_name = 'Max Windspeed-U1'
	max_windspeed_u1.long_name = 'wind_speed'

	max_windspeed_u2.units = 'm/s'
	max_windspeed_u2.original_var_name = 'Max Windspeed-U2'
	max_windspeed_u2.long_name = 'wind_speed'

	stdev_windspeed_u1.units = 'm/s'
	stdev_windspeed_u1.original_var_name = 'StdDev Windspeed-U1'
	stdev_windspeed_u1.long_name = 'wind_speed'

	stdev_windspeed_u2.units = 'm/s'
	stdev_windspeed_u2.original_var_name = 'StdDev Windspeed-U2'
	stdev_windspeed_u2.long_name = 'wind_speed'

	ref_temperature.units = 'degC'
	ref_temperature.original_var_name = 'Ref Temperature'
	ref_temperature.note = 'Need to ask network manager about long name'

	windspeed_2m.units = 'm/s'
	windspeed_2m.original_var_name = 'Windspeed@2m'
	windspeed_2m.long_name = 'wind_speed'

	windspeed_10m.units = 'm/s'
	windspeed_10m.original_var_name = 'Windspeed@10m'
	windspeed_10m.long_name = '10-m_wind_speed'

	wind_sensor_height_1.units = 'm'
	wind_sensor_height_1.original_var_name = 'WindSensorHeight1'
	wind_sensor_height_1.long_name = 'n/a'

	wind_sensor_height_2.units = 'm'
	wind_sensor_height_2.original_var_name = 'WindSensorHeight2'
	wind_sensor_height_2.long_name = 'n/a'

	albedo.units = '1'
	albedo.original_var_name = 'Albedo'
	albedo.long_name = 'surface_albedo'

	zenith_angle.units = 'deg'
	zenith_angle.original_var_name = 'Zenith Angle'
	zenith_angle.long_name = 'solar_zenith_angle'

	qc1.units = '1'
	qc1.original_var_name = 'QCl01-08'

	qc9.units = '1'
	qc9.original_var_name = 'QCl09-16'

	qc17.units = '1'
	qc17.original_var_name = 'QCl17-24'

	qc25.units = '1'
	qc25.original_var_name = 'QCl25-27'

	time.units = 'days since 1995-01-01 00:00:00'
	time.long_name = 'time'
	time.calendar = 'noleap'
	time.bounds = 'time_bnds'
	time.note = 'Created new derived variable'


	i,j = 0,0
	ip_file = open(str(args.input), 'r')

	while i < 54:
	    ip_file.readline()
	    i += 1

	for line in ip_file:
	    
	    line = line.strip()
	    columns = line.split()
	    
	    station_number[j] = columns[0]
	    year[j] = columns[1]
	    julian_decimal_time[j] = columns[2]
	    sw_down[j] = columns[3]
	    sw_up[j] = columns[4]
	    net_radiation[j] = columns[5]
	    temperature_tc_1[j] = columns[6]
	    temperature_tc_2[j] = columns[7]
	    temperature_cs500_1[j] = columns[8]
	    temperature_cs500_2[j] = columns[9]
	    relative_humidity_1[j] = columns[10]
	    relative_humidity_2[j] = columns[11]
	    u1_wind_speed[j] = columns[12]
	    u2_wind_speed[j] = columns[13]
	    u_direction_1[j] = columns[14]
	    u_direction_2[j] = columns[15]
	    pressure[j] = columns[16]
	    snow_height_1[j] = columns[17]
	    snow_height_2[j] = columns[18]
	    t_snow_01[j] = columns[19]
	    t_snow_02[j] = columns[20]
	    t_snow_03[j] = columns[21]
	    t_snow_04[j] = columns[22]
	    t_snow_05[j] = columns[23]
	    t_snow_06[j] = columns[24]
	    t_snow_07[j] = columns[25]
	    t_snow_08[j] = columns[26]
	    t_snow_09[j] = columns[27]
	    t_snow_10[j] = columns[28]
	    battery_voltage[j] = columns[29]
	    sw_down_max[j] = columns[30]
	    sw_up_max[j] = columns[31]
	    net_radiation_max[j] = columns[32]
	    max_air_temperature_1[j] = columns[33]
	    max_air_temperature_2[j] = columns[34]
	    min_air_temperature_1[j] = columns[35]
	    min_air_temperature_2[j] = columns[36]
	    max_windspeed_u1[j] = columns[37]
	    max_windspeed_u2[j] = columns[38]
	    stdev_windspeed_u1[j] = columns[39]
	    stdev_windspeed_u2[j] = columns[40]
	    ref_temperature[j] = columns[41]
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
	    j += 1


	qc1_str = [str(e) for e in qc1]
	qc9_str = [str(e) for e in qc9]
	qc17_str = [str(e) for e in qc17]
	qc25_str = [str(e) for e in qc25]
	
	k,l = 0,0

	for item in qc1_str:
		qc_swdn[k] = qc1_str[k][l]
		qc_swup[k] = qc1_str[k][l+1]
		qc_netradiation[k] = qc1_str[k][l+2]
		qc_ttc1[k] = qc1_str[k][l+3]
		qc_ttc2[k] = qc1_str[k][l+4]
		qc_tcs1[k] = qc1_str[k][l+5]
		qc_tcs2[k] = qc1_str[k][l+6]
		qc_rh1[k] = qc1_str[k][l+7]

		k += 1
		
	k,l = 0,0

	for item in qc9_str:
		qc_rh2[k] = qc9_str[k][l]
		qc_u1[k] = qc9_str[k][l+1]
		qc_u2[k] = qc9_str[k][l+2]
		qc_ud1[k] = qc9_str[k][l+3]
		qc_ud2[k] = qc9_str[k][l+4]
		qc_pressure[k] = qc9_str[k][l+5]
		qc_snowheight1[k] = qc9_str[k][l+6]
		qc_snowheight2[k] = qc9_str[k][l+7]

		k += 1
		
	k,l = 0,0

	for item in qc17_str:
		qc_tsnow1[k] = qc17_str[k][l]
		qc_tsnow2[k] = qc17_str[k][l+1]
		qc_tsnow3[k] = qc17_str[k][l+2]
		qc_tsnow4[k] = qc17_str[k][l+3]
		qc_tsnow5[k] = qc17_str[k][l+4]
		qc_tsnow6[k] = qc17_str[k][l+5]
		qc_tsnow7[k] = qc17_str[k][l+6]
		qc_tsnow8[k] = qc17_str[k][l+7]

		k += 1
		
	k,l = 0,0

	for item in qc25_str:
		qc_tsnow9[k] = qc25_str[k][l]
		qc_tsnow10[k] = qc25_str[k][l+1]
		qc_battery[k] = qc25_str[k][l+2]

		k += 1
		
#############################################################################################################################################################

	#qc1_str = ''.join(str(e) for e in qc1)
	#qc9_str = ''.join(str(e) for e in qc9)
	#qc17_str = ''.join(str(e) for e in qc17)
	#qc25_str = ''.join(str(e) for e in qc25)


	#a,b = 0,0
	#while a < 12183:
	#	qc_swdn[a] = qc1_str[b]
	#	qc_swup[a] = qc1_str[b+1]
	#	qc_netradiation[a] = qc1_str[b+2]
	#	qc_ttc1[a] = qc1_str[b+3]
	#	qc_ttc2[a] = qc1_str[b+4]
	#	qc_tcs1[a] = qc1_str[b+5]
	#	qc_tcs2[a] = qc1_str[b+6]
	#	qc_rh1[a] = qc1_str[b+7]

	#	a += 1
	#	b += 8

	#a,b = 0,0
	#while a < 12183:
	#	qc_rh2[a] = qc9_str[b]
	#	qc_u1[a] = qc9_str[b+1]
	#	qc_u2[a] = qc9_str[b+2]
	#	qc_ud1[a] = qc9_str[b+3]
	#	qc_ud2[a] = qc9_str[b+4]
	#	qc_pressure[a] = qc9_str[b+5]
	#	qc_snowheight1[a] = qc9_str[b+6]
	#	qc_snowheight2[a] = qc9_str[b+7]

	#	a += 1
	#	b += 8


	#a,b = 0,0
	#while a < 12183:
	#	qc_tsnow1[a] = qc17_str[b]
	#	qc_tsnow2[a] = qc17_str[b+1]
	#	qc_tsnow3[a] = qc17_str[b+2]
	#	qc_tsnow4[a] = qc17_str[b+3]
	#	qc_tsnow5[a] = qc17_str[b+4]
	#	qc_tsnow6[a] = qc17_str[b+5]
	#	qc_tsnow7[a] = qc17_str[b+6]
	#	qc_tsnow8[a] = qc17_str[b+7]

	#	a += 1
	#	b += 8


	#a,b = 0,0
	#while a < 12183:
	#	qc_tsnow9[a] = qc25_str[b]
	#	qc_tsnow10[a] = qc25_str[b+1]
	#	qc_battery[a] = qc25_str[b+2]
		
	#	a += 1
	#	b += 3

##################################################################################################################################################################

	m = 0
	d0 = date(1995, 1, 1)
	d1 = date(2012, 12, 31)
	offset = (d1 - d0).days

	for item in julian_decimal_time:
	    time[m] = offset + int(julian_decimal_time[m])
	    m += 1

	root_grp.close()








#################################################################################################################

#							PROMICE																				#

#################################################################################################################

def promice2nc(f):

	data = ascii.read(args.input)

	# NC file setup
	global op_file
	op_file = 'converted-promice.nc'
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



def Main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="The PROMICE file you wish to convert to netCDF.", type=str)
    parser.add_argument("row_count", help="Total number of rows in your dataset", type=int)
    parser.add_argument("-o", "--output", help="Path where you want to store the output file", type=str)

    global args
    
    args = parser.parse_args()

    #global ip_file

    #ip_file = open(str(args.input), 'r')
    with open(str(args.input),'r') as f:
    	line = f.readline()


    if line[0] == 'D': 
    	gcnet2nc(args.input)

    elif line[0] == 'Y':
    	promice2nc(args.input)
    
    print "The file " + str(args.input) + " is converted into netCDF format and is saved at " + op_file


if __name__ == '__main__':
    Main()


