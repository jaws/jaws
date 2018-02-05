import os
from datetime import datetime, timedelta
from common import time_calc, solar

def gcnet2nc(args, op_file, root_grp, station_name, latitude, longitude, time, time_bounds, sza, station_dict):

	#Global Attributes
	root_grp.title = 'Surface Radiation Data from Greenland Climate Network'
	root_grp.source = 'Surface Observations'
	root_grp.featureType = 'timeSeries'
	root_grp.institution = 'Cooperative Institute for Research in Enviornmental Sciences'
	root_grp.reference = 'http://cires.colorado.edu/science/groups/steffen/gcnet/'
	root_grp.Conventions = 'CF-1.7'
	root_grp.time_convention = "'time: point' variables match the time coordinate values exactly, whereas 'time: mean' variables are valid for the mean time within the time_bounds variable." + " e.g.: battery_voltage is measured once per hour at the time stored in the 'time' coordinate." + 	" On the other hand, temperature_tc_1 is continuously measured and then hourly-mean values are stored for each period contained in the time_bounds variable"

	# variables
	station_number = root_grp.createVariable('station_number', 'i1', ('station',))
	year = root_grp.createVariable('year', 'i4', ('time',))
	julian_decimal_time = root_grp.createVariable('julian_decimal_time', 'f4', ('time',))
	sw_down = root_grp.createVariable('sw_down', 'f4', ('time',), fill_value = 999)
	sw_up = root_grp.createVariable('sw_up', 'f4', ('time',), fill_value = 999)
	net_radiation = root_grp.createVariable('net_radiation', 'f4', ('time',), fill_value = 999)
	temperature_tc_1 = root_grp.createVariable('temperature_tc_1', 'f4', ('time',), fill_value = 999)
	temperature_tc_2 = root_grp.createVariable('temperature_tc_2', 'f4', ('time',), fill_value = 999)
	temperature_cs500_1 = root_grp.createVariable('temperature_cs500_1', 'f4', ('time',), fill_value = 999)
	temperature_cs500_2 = root_grp.createVariable('temperature_cs500_2', 'f4', ('time',), fill_value = 999)
	relative_humidity_1 = root_grp.createVariable('relative_humidity_1', 'f4', ('time',), fill_value = 999)
	relative_humidity_2 = root_grp.createVariable('relative_humidity_2', 'f4', ('time',), fill_value = 999)
	u1_wind_speed = root_grp.createVariable('u1_wind_speed', 'f4', ('time',), fill_value = 999)
	u2_wind_speed = root_grp.createVariable('u2_wind_speed', 'f4', ('time',), fill_value = 999)
	u_direction_1 = root_grp.createVariable('u_direction_1', 'f4', ('time',), fill_value = 999)
	u_direction_2 = root_grp.createVariable('u_direction_2', 'f4', ('time',), fill_value = 999)
	atmos_pressure = root_grp.createVariable('atmos_pressure', 'f4', ('time',), fill_value = 999)
	snow_height_1 = root_grp.createVariable('snow_height_1', 'f4', ('time',), fill_value = 999)
	snow_height_2 = root_grp.createVariable('snow_height_2', 'f4', ('time',), fill_value = 999)
	t_snow_01 = root_grp.createVariable('t_snow_01', 'f4', ('time',), fill_value = 999)
	t_snow_02 = root_grp.createVariable('t_snow_02', 'f4', ('time',), fill_value = 999)
	t_snow_03 = root_grp.createVariable('t_snow_03', 'f4', ('time',), fill_value = 999)
	t_snow_04 = root_grp.createVariable('t_snow_04', 'f4', ('time',), fill_value = 999)
	t_snow_05 = root_grp.createVariable('t_snow_05', 'f4', ('time',), fill_value = 999)
	t_snow_06 = root_grp.createVariable('t_snow_06', 'f4', ('time',), fill_value = 999)
	t_snow_07 = root_grp.createVariable('t_snow_07', 'f4', ('time',), fill_value = 999)
	t_snow_08 = root_grp.createVariable('t_snow_08', 'f4', ('time',), fill_value = 999)
	t_snow_09 = root_grp.createVariable('t_snow_09', 'f4', ('time',), fill_value = 999)
	t_snow_10 = root_grp.createVariable('t_snow_10', 'f4', ('time',), fill_value = 999)
	battery_voltage = root_grp.createVariable('battery_voltage', 'f4', ('time',), fill_value = 999)
	sw_down_max = root_grp.createVariable('sw_down_max', 'f4', ('time',), fill_value = 999)
	sw_up_max = root_grp.createVariable('sw_up_max', 'f4', ('time',), fill_value = 999)
	net_radiation_max = root_grp.createVariable('net_radiation_max', 'f4', ('time',), fill_value = 999)
	max_air_temperature_1 = root_grp.createVariable('max_air_temperature_1', 'f4', ('time',), fill_value = 999)
	max_air_temperature_2 = root_grp.createVariable('max_air_temperature_2', 'f4', ('time',), fill_value = 999)
	min_air_temperature_1 = root_grp.createVariable('min_air_temperature_1', 'f4', ('time',), fill_value = 999)
	min_air_temperature_2 = root_grp.createVariable('min_air_temperature_2', 'f4', ('time',), fill_value = 999)
	max_windspeed_u1 = root_grp.createVariable('max_windspeed_u1', 'f4', ('time',), fill_value = 999)
	max_windspeed_u2 = root_grp.createVariable('max_windspeed_u2', 'f4', ('time',), fill_value = 999)
	stdev_windspeed_u1 = root_grp.createVariable('stdev_windspeed_u1', 'f4', ('time',), fill_value = 999)
	stdev_windspeed_u2 = root_grp.createVariable('stdev_windspeed_u2', 'f4', ('time',), fill_value = 999)
	ref_temperature = root_grp.createVariable('ref_temperature', 'f4', ('time',), fill_value = 999)
	windspeed_2m = root_grp.createVariable('windspeed_2m', 'f4', ('time',), fill_value = 999)
	windspeed_10m = root_grp.createVariable('windspeed_10m', 'f4', ('time',), fill_value = 999)
	wind_sensor_height_1 = root_grp.createVariable('wind_sensor_height_1', 'f4', ('time',), fill_value = 999)
	wind_sensor_height_2 = root_grp.createVariable('wind_sensor_height_2', 'f4', ('time',), fill_value = 999)
	albedo = root_grp.createVariable('albedo', 'f4', ('time',), fill_value = 999)
	zenith_angle = root_grp.createVariable('zenith_angle', 'f4', ('time',), fill_value = 999)
	qc1 = root_grp.createVariable('qc1', 'i4', ('time',), fill_value = 999)
	qc9 = root_grp.createVariable('qc9', 'i4', ('time',), fill_value = 999)
	qc17 = root_grp.createVariable('qc17', 'i4', ('time',), fill_value = 999)
	qc25 = root_grp.createVariable('qc25', 'i4', ('time',), fill_value = 999)
	
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
	
	month = root_grp.createVariable('month', 'i1', ('time',))
	day = root_grp.createVariable('day', 'i1', ('time',))
	hour = root_grp.createVariable('hour', 'i1', ('time',))
	

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
	sw_down.coordinates = 'longitude latitude'
	sw_down.cell_methods = 'time: mean'

	sw_up.units = 'watt meter-2'
	sw_up.long_name = 'Shortwave Flux up'
	sw_up.standard_name = 'upwelling_shortwave_flux_in_air'
	sw_up.coordinates = 'longitude latitude'
	sw_up.cell_methods = 'time: mean'

	net_radiation.units = 'watt meter-2'
	net_radiation.long_name = 'Net Radiation'
	net_radiation.standard_name = 'surface_net_downward_radiative_flux'
	net_radiation.coordinates = 'longitude latitude'
	net_radiation.cell_methods = 'time: mean'

	temperature_tc_1.units = 'kelvin'
	temperature_tc_1.long_name = 'TC-1 Air Temperature'
	temperature_tc_1.standard_name = 'air_temperature'
	temperature_tc_1.note = 'air temperature from TC sensor'
	temperature_tc_1.coordinates = 'longitude latitude'
	temperature_tc_1.cell_methods = 'time: mean'

	temperature_tc_2.units = 'kelvin'
	temperature_tc_2.long_name = 'TC-2 Air Temperature'
	temperature_tc_2.standard_name = 'air_temperature'
	temperature_tc_2.coordinates = 'longitude latitude'
	temperature_tc_2.cell_methods = 'time: mean'

	temperature_cs500_1.units = 'kelvin'
	temperature_cs500_1.long_name = 'CS500-1 Air Temperature'
	temperature_cs500_1.standard_name = 'air_temperature'
	temperature_cs500_1.note = 'air temperature from CS500 sensor'
	temperature_cs500_1.coordinates = 'longitude latitude'
	temperature_cs500_1.cell_methods = 'time: mean'

	temperature_cs500_2.units = 'kelvin'
	temperature_cs500_2.long_name = 'CS500-2 Air Temperature'
	temperature_cs500_2.standard_name = 'air_temperature'
	temperature_cs500_2.coordinates = 'longitude latitude'
	temperature_cs500_2.cell_methods = 'time: mean'

	relative_humidity_1.units = '1'
	relative_humidity_1.long_name = 'Relative Humidity 1'
	relative_humidity_1.standard_name = 'realtive_humidity'
	relative_humidity_1.coordinates = 'longitude latitude'
	relative_humidity_1.cell_methods = 'time: mean'

	relative_humidity_2.units = '1'
	relative_humidity_2.long_name = 'Relative Humidity 2'
	relative_humidity_2.standard_name = 'realtive_humidity'
	relative_humidity_2.coordinates = 'longitude latitude'
	relative_humidity_2.cell_methods = 'time: mean'

	u1_wind_speed.units = 'meter second-1'
	u1_wind_speed.long_name = 'U1 Wind Speed'
	u1_wind_speed.standard_name = 'wind_speed'
	u1_wind_speed.coordinates = 'longitude latitude'
	u1_wind_speed.cell_methods = 'time: mean'

	u2_wind_speed.units = 'meter second-1'
	u2_wind_speed.long_name = 'U2 Wind Speed'
	u2_wind_speed.standard_name = 'wind_speed'
	u2_wind_speed.coordinates = 'longitude latitude'
	u2_wind_speed.cell_methods = 'time: mean'

	u_direction_1.units = 'degree'
	u_direction_1.long_name = 'U Direction 1'
	u_direction_1.standard_name = 'wind_from_direction'
	u_direction_1.coordinates = 'longitude latitude'
	u_direction_1.cell_methods = 'time: mean'

	u_direction_2.units = 'degree'
	u_direction_2.long_name = 'U Direction 2'
	u_direction_2.standard_name = 'wind_from_direction'
	u_direction_2.coordinates = 'longitude latitude'
	u_direction_2.cell_methods = 'time: mean'

	atmos_pressure.units = 'pascal'
	atmos_pressure.long_name = 'Atmospheric Pressure'
	atmos_pressure.standard_name = 'surface_air_pressure'
	atmos_pressure.coordinates = 'longitude latitude'
	atmos_pressure.cell_methods = 'time: mean'

	snow_height_1.units = 'meter'
	snow_height_1.long_name = 'Snow Height 1'
	snow_height_1.standard_name = 'snow_height'
	snow_height_1.coordinates = 'longitude latitude'
	snow_height_1.cell_methods = 'time: mean'

	snow_height_2.units = 'meter'
	snow_height_2.long_name = 'Snow Height 2'
	snow_height_2.standard_name = 'snow_height'
	snow_height_2.coordinates = 'longitude latitude'
	snow_height_2.cell_methods = 'time: mean'

	t_snow_01.units = 'kelvin'
	t_snow_01.long_name = 'T Snow 1'
	#t_snow_01.standard_name = 'temperature_in_surface_snow'
	t_snow_01.coordinates = 'longitude latitude'
	t_snow_01.cell_methods = 'time: mean'

	t_snow_02.units = 'kelvin'
	t_snow_02.long_name = 'T Snow 2'
	#t_snow_02.standard_name = 'temperature_in_surface_snow'
	t_snow_02.coordinates = 'longitude latitude'
	t_snow_02.cell_methods = 'time: mean'

	t_snow_03.units = 'kelvin'
	t_snow_03.long_name = 'T Snow 3'
	#t_snow_03.standard_name = 'temperature_in_surface_snow'
	t_snow_03.coordinates = 'longitude latitude'
	t_snow_03.cell_methods = 'time: mean'

	t_snow_04.units = 'kelvin'
	t_snow_04.long_name = 'T Snow 4'
	#t_snow_04.standard_name = 'temperature_in_surface_snow'
	t_snow_04.coordinates = 'longitude latitude'
	t_snow_04.cell_methods = 'time: mean'

	t_snow_05.units = 'kelvin'
	t_snow_05.long_name = 'T Snow 5'
	#t_snow_05.standard_name = 'temperature_in_surface_snow'
	t_snow_05.coordinates = 'longitude latitude'
	t_snow_05.cell_methods = 'time: mean'

	t_snow_06.units = 'kelvin'
	t_snow_06.long_name = 'T Snow 6'
	#t_snow_06.standard_name = 'temperature_in_surface_snow'
	t_snow_06.coordinates = 'longitude latitude'
	t_snow_06.cell_methods = 'time: mean'

	t_snow_07.units = 'kelvin'
	t_snow_07.long_name = 'T Snow 7'
	#t_snow_07.standard_name = 'temperature_in_surface_snow'
	t_snow_07.coordinates = 'longitude latitude'
	t_snow_07.cell_methods = 'time: mean'

	t_snow_08.units = 'kelvin'
	t_snow_08.long_name = 'T Snow 8'
	#t_snow_08.standard_name = 'temperature_in_surface_snow'
	t_snow_08.coordinates = 'longitude latitude'
	t_snow_08.cell_methods = 'time: mean'

	t_snow_09.units = 'kelvin'
	t_snow_09.long_name = 'T Snow 9'
	#t_snow_09.standard_name = 'temperature_in_surface_snow'
	t_snow_09.coordinates = 'longitude latitude'
	t_snow_09.cell_methods = 'time: mean'

	t_snow_10.units = 'kelvin'
	t_snow_10.long_name = 'T Snow 10'
	#t_snow_10.standard_name = 'temperature_in_surface_snow'
	t_snow_10.coordinates = 'longitude latitude'
	t_snow_10.cell_methods = 'time: mean'

	battery_voltage.units = 'volts'
	battery_voltage.long_name = 'Battery Voltage'
	battery_voltage.standard_name = 'battery_voltage'
	battery_voltage.coordinates = 'longitude latitude'
	battery_voltage.cell_methods = 'time: point'

	sw_down_max.units = 'watt meter-2'
	sw_down_max.long_name = 'Shortwave Flux down max'
	sw_down_max.standard_name = 'maximum_downwelling_shortwave_flux_in_air'
	sw_down_max.coordinates = 'longitude latitude'
	sw_down_max.cell_methods = 'time: mean'
	
	sw_up_max.units = 'watt meter-2'
	sw_up_max.long_name = 'Shortwave Flux up max'
	sw_up_max.standard_name = 'maximum_upwelling_shortwave_flux_in_air'
	sw_up_max.coordinates = 'longitude latitude'
	sw_up_max.cell_methods = 'time: mean'
	
	net_radiation_max.units = 'watt meter-2'
	net_radiation_max.long_name = 'Net Radiation max'
	net_radiation_max.standard_name = 'maximum_net_radiation'
	net_radiation_max.coordinates = 'longitude latitude'
	net_radiation_max.cell_methods = 'time: mean'

	max_air_temperature_1.units = 'kelvin'
	max_air_temperature_1.long_name = 'Max Air Temperture 1'
	max_air_temperature_1.standard_name = 'air_temperature'
	max_air_temperature_1.coordinates = 'longitude latitude'
	max_air_temperature_1.cell_methods = 'time: mean'

	max_air_temperature_2.units = 'kelvin'
	max_air_temperature_2.long_name = 'Max Air Temperture 2'
	max_air_temperature_2.standard_name = 'air_temperature'
	max_air_temperature_2.coordinates = 'longitude latitude'
	max_air_temperature_2.cell_methods = 'time: mean'

	min_air_temperature_1.units = 'kelvin'
	min_air_temperature_1.long_name = 'Min Air Temperture 1'
	min_air_temperature_1.standard_name = 'air_temperature'
	min_air_temperature_1.coordinates = 'longitude latitude'
	min_air_temperature_1.cell_methods = 'time: mean'

	min_air_temperature_2.units = 'kelvin'
	min_air_temperature_2.long_name = 'Min Air Temperture 2'
	min_air_temperature_2.standard_name = 'air_temperature'
	min_air_temperature_2.coordinates = 'longitude latitude'
	min_air_temperature_2.cell_methods = 'time: mean'

	max_windspeed_u1.units = 'meter second-1'
	max_windspeed_u1.long_name = 'Max Windspeed-U1'
	max_windspeed_u1.standard_name = 'wind_speed'
	max_windspeed_u1.coordinates = 'longitude latitude'
	max_windspeed_u1.cell_methods = 'time: mean'

	max_windspeed_u2.units = 'meter second-1'
	max_windspeed_u2.long_name = 'Max Windspeed-U2'
	max_windspeed_u2.standard_name = 'wind_speed'
	max_windspeed_u2.coordinates = 'longitude latitude'
	max_windspeed_u2.cell_methods = 'time: mean'

	stdev_windspeed_u1.units = 'meter second-1'
	stdev_windspeed_u1.long_name = 'StdDev Windspeed-U1'
	stdev_windspeed_u1.standard_name = 'wind_speed'
	stdev_windspeed_u1.coordinates = 'longitude latitude'
	stdev_windspeed_u1.cell_methods = 'time: mean'

	stdev_windspeed_u2.units = 'meter second-1'
	stdev_windspeed_u2.long_name = 'StdDev Windspeed-U2'
	stdev_windspeed_u2.standard_name = 'wind_speed'
	stdev_windspeed_u2.coordinates = 'longitude latitude'
	stdev_windspeed_u2.cell_methods = 'time: mean'

	ref_temperature.units = 'kelvin'
	ref_temperature.long_name = 'Reference Temperature'
	ref_temperature.note = 'Need to ask network manager about long name'
	ref_temperature.coordinates = 'longitude latitude'
	ref_temperature.cell_methods = 'time: mean'

	windspeed_2m.units = 'meter second-1'
	windspeed_2m.long_name = 'Windspeed@2m'
	windspeed_2m.standard_name = 'wind_speed'
	windspeed_2m.coordinates = 'longitude latitude'
	windspeed_2m.cell_methods = 'time: mean'

	windspeed_10m.units = 'meter second-1'
	windspeed_10m.long_name = 'Windspeed@10m'
	windspeed_10m.standard_name = '10-m_wind_speed'
	windspeed_10m.coordinates = 'longitude latitude'
	windspeed_10m.cell_methods = 'time: mean'

	wind_sensor_height_1.units = 'meter'
	wind_sensor_height_1.long_name = 'Wind Sensor Height 1'
	wind_sensor_height_1.standard_name = 'n/a'
	wind_sensor_height_1.coordinates = 'longitude latitude'
	wind_sensor_height_1.cell_methods = 'time: mean'

	wind_sensor_height_2.units = 'meter'
	wind_sensor_height_2.long_name = 'Wind Sensor Height 2'
	wind_sensor_height_2.standard_name = 'n/a'
	wind_sensor_height_2.coordinates = 'longitude latitude'
	wind_sensor_height_2.cell_methods = 'time: mean'

	albedo.units = '1'
	albedo.long_name = 'Albedo'
	albedo.standard_name = 'surface_albedo'
	albedo.coordinates = 'longitude latitude'
	albedo.cell_methods = 'time: mean'

	zenith_angle.units = 'degree'
	zenith_angle.long_name = 'Zenith Angle'
	zenith_angle.standard_name = 'solar_zenith_angle'
	zenith_angle.coordinates = 'longitude latitude'
	zenith_angle.cell_methods = 'time: mean'

	qc1.units = '1'
	qc1.long_name = 'Quality Control variables 01-08'
	qc1.coordinates = 'longitude latitude'

	qc9.units = '1'
	qc9.long_name = 'Quality Control variables 09-16'
	qc9.coordinates = 'longitude latitude'

	qc17.units = '1'
	qc17.long_name = 'Quality Control variables 17-24'
	qc17.coordinates = 'longitude latitude'

	qc25.units = '1'
	qc25.long_name = 'Quality Control variables 25-27'
	qc25.coordinates = 'longitude latitude'

	qc_swdn.units = '1'
	qc_swdn.long_name = 'Quality Control flag for Shortwave Flux down'

	qc_swup.units = '1'
	qc_swup.long_name = 'Quality Control flag for Shortwave Flux up'

	qc_netradiation.units = '1'
	qc_netradiation.long_name = 'Quality Control flag for Net Radiation'

	qc_ttc1.units = '1'
	qc_ttc1.long_name = 'Quality Control flag for TC-1 Air Temperature'

	qc_ttc2.units = '1'
	qc_ttc2.long_name = 'Quality Control flag for TC-2 Air Temperature'

	qc_tcs1.units = '1'
	qc_tcs1.long_name = 'Quality Control flag for CS500-1 Air Temperature'

	qc_tcs2.units = '1'
	qc_tcs2.long_name = 'Quality Control flag for CS500-2 Air Temperature'

	qc_rh1.units = '1'
	qc_rh1.long_name = 'Quality Control flag for Relative Humidity 1'

	qc_rh2.units = '1'
	qc_rh2.long_name = 'Quality Control flag for Relative Humidity 2'

	qc_u1.units = '1'
	qc_u1.long_name = 'Quality Control flag for U1 Wind Speed'

	qc_u2.units = '1'
	qc_u2.long_name = 'Quality Control flag for U2 Wind Speed'

	qc_ud1.units = '1'
	qc_ud1.long_name = 'Quality Control flag for U Direction 1'

	qc_ud2.units = '1'
	qc_ud2.long_name = 'Quality Control flag for U Direction 2'

	qc_pressure.units = '1'
	qc_pressure.long_name = 'Quality Control flag for Atmospheric Pressure'

	qc_snowheight1.units = '1'
	qc_snowheight1.long_name = 'Quality Control flag for Snow Height 1'

	qc_snowheight2.units = '1'
	qc_snowheight2.long_name = 'Quality Control flag for Snow Height 2'

	qc_tsnow1.units = '1'
	qc_tsnow1.long_name = 'Quality Control flag for T Snow 1'

	qc_tsnow2.units = '1'
	qc_tsnow2.long_name = 'Quality Control flag for T Snow 2'

	qc_tsnow3.units = '1'
	qc_tsnow3.long_name = 'Quality Control flag for T Snow 3'

	qc_tsnow4.units = '1'
	qc_tsnow4.long_name = 'Quality Control flag for T Snow 4'

	qc_tsnow5.units = '1'
	qc_tsnow5.long_name = 'Quality Control flag for T Snow 5'

	qc_tsnow6.units = '1'
	qc_tsnow6.long_name = 'Quality Control flag for T Snow 6'

	qc_tsnow7.units = '1'
	qc_tsnow7.long_name = 'Quality Control flag for T Snow 7'

	qc_tsnow8.units = '1'
	qc_tsnow8.long_name = 'Quality Control flag for T Snow 8'

	qc_tsnow9.units = '1'
	qc_tsnow9.long_name = 'Quality Control flag for T Snow 9'

	qc_tsnow10.units = '1'
	qc_tsnow10.long_name = 'Quality Control flag for T Snow 10'

	qc_battery.units = '1'
	qc_battery.long_name = 'Quality Control flag for Battery Voltage'

	
	print("converting data...")

	num_lines =  sum(1 for line in open(args.input_file or args.fl_in)) - 54
	#54 is the number of lines before the data starts in input file

	i,j = 0,0
	convert_temp = 273.15
	convert_press = 100
	check_na = 999.0
	hour_exception = 0.99
	hour_conversion = (100/4)		#Divided by 4 because each hour value is a multiple of 4 and then multiplied by 100 to convert decimal to integer

	idx_stnnum, idx_year, idx_jdt, idx_swdn, idx_swup, idx_netrad, idx_tc1, idx_tc2, idx_cs1, idx_cs2, idx_rh1, idx_rh2, idx_windspd1, idx_windspd2, idx_dir1, idx_dir2 = range(16)
	idx_atmospress, idx_snowht1, idx_snowht2, idx_tsnow1, idx_tsnow2, idx_tsnow3, idx_tsnow4, idx_tsnow5, idx_tsnow6, idx_tsnow7, idx_tsnow8, idx_tsnow9, idx_tsnow10, idx_batvolt, idx_swdnmax, idx_swupmax = range(16,32)
	idx_netradmax, idx_maxtemp1, idx_maxtemp2, idx_mintemp1, idx_mintemp2, idx_maxwindspd1, idx_maxwindspd2, idx_sdwindspd1, idx_sdwindspd2, idx_reftemp, idx_windspd2m, idx_windspd10m, idx_sensorht1, idx_sensorht2, idx_albedo, idx_zenang = range(32,48)
	idx_qc1, idx_qc9, idx_qc17, idx_qc25 = range(48,52)

	temp1 = [0]*num_lines
	temp9 = [0]*num_lines
	temp17 = [0]*num_lines
	temp25 = [0]*num_lines

	ip_file = open(str(args.input_file or args.fl_in), 'r')

	while i < 54:
	    ip_file.readline()
	    i += 1

	for line in ip_file:
	    
		line = line.strip()
		columns = line.split()
		columns = [float(x) for x in columns]
		
		station_number[0] = columns[idx_stnnum]
		year[j] = columns[idx_year]
		julian_decimal_time[j] = columns[idx_jdt]
		sw_down[j] = columns[idx_swdn]
		sw_up[j] = columns[idx_swup]
		net_radiation[j] = columns[idx_netrad]
		
		if columns[idx_tc1] == check_na:
			temperature_tc_1[j] = columns[idx_tc1]
		else:
			temperature_tc_1[j] = columns[idx_tc1] + convert_temp

		if columns[idx_tc2] == check_na:
			temperature_tc_2[j] = columns[idx_tc2]
		else:
			temperature_tc_2[j] = columns[idx_tc2] + convert_temp

		if columns[idx_cs1] == check_na:
			temperature_cs500_1[j] = columns[idx_cs1]
		else:
			temperature_cs500_1[j] = columns[idx_cs1] + convert_temp

		if columns[idx_cs2] == check_na:
			temperature_cs500_2[j] = columns[idx_cs2]
		else:
			temperature_cs500_2[j] = columns[idx_cs2] + convert_temp

		relative_humidity_1[j] = columns[idx_rh1]
		relative_humidity_2[j] = columns[idx_rh2]
		u1_wind_speed[j] = columns[idx_windspd1]
		u2_wind_speed[j] = columns[idx_windspd2]
		u_direction_1[j] = columns[idx_dir1]
		u_direction_2[j] = columns[idx_dir2]
		
		if columns[idx_atmospress] == check_na:
			atmos_pressure[j] = columns[idx_atmospress]
		else:
			atmos_pressure[j] = columns[idx_atmospress] * convert_press
		
		snow_height_1[j] = columns[idx_snowht1]
		snow_height_2[j] = columns[idx_snowht2]
		
		if columns[idx_tsnow1] == check_na:
			t_snow_01[j] = columns[idx_tsnow1]
		else:
			t_snow_01[j] = columns[idx_tsnow1] + convert_temp

		if columns[idx_tsnow2] == check_na:
			t_snow_02[j] = columns[idx_tsnow2]
		else:
			t_snow_02[j] = columns[idx_tsnow2] + convert_temp

		if columns[idx_tsnow3] == check_na:
			t_snow_03[j] = columns[idx_tsnow3]
		else:
			t_snow_03[j] = columns[idx_tsnow3] + convert_temp
		
		if columns[idx_tsnow4] == check_na:
			t_snow_04[j] = columns[idx_tsnow4]
		else:
			t_snow_04[j] = columns[idx_tsnow4] + convert_temp
		
		if columns[idx_tsnow5] == check_na:
			t_snow_05[j] = columns[idx_tsnow5]
		else:
			t_snow_05[j] = columns[idx_tsnow5] + convert_temp
		
		if columns[idx_tsnow6] == check_na:
			t_snow_06[j] = columns[idx_tsnow6]
		else:
			t_snow_06[j] = columns[idx_tsnow6] + convert_temp
		
		if columns[idx_tsnow7] == check_na:
			t_snow_07[j] = columns[idx_tsnow7]
		else:
			t_snow_07[j] = columns[idx_tsnow7] + convert_temp
		
		if columns[idx_tsnow8] == check_na:
			t_snow_08[j] = columns[idx_tsnow8]
		else:
			t_snow_08[j] = columns[idx_tsnow8] + convert_temp
		
		if columns[idx_tsnow9] == check_na:
			t_snow_09[j] = columns[idx_tsnow9]
		else:
			t_snow_09[j] = columns[idx_tsnow9] + convert_temp
		
		if columns[idx_tsnow10] == check_na:
			t_snow_10[j] = columns[idx_tsnow10]
		else:
			t_snow_10[j] = columns[idx_tsnow10] + convert_temp
		
		battery_voltage[j] = columns[idx_batvolt]
		sw_down_max[j] = columns[idx_swdnmax]
		sw_up_max[j] = columns[idx_swupmax]
		net_radiation_max[j] = columns[idx_netradmax]
		
		if columns[idx_maxtemp1] == check_na:
			max_air_temperature_1[j] = columns[idx_maxtemp1]
		else:
			max_air_temperature_1[j] = columns[idx_maxtemp1] + convert_temp
		
		if columns[idx_maxtemp2] == check_na:
			max_air_temperature_2[j] = columns[idx_maxtemp2]
		else:
			max_air_temperature_2[j] = columns[idx_maxtemp2] + convert_temp
		
		if columns[idx_mintemp1] == check_na:
			min_air_temperature_1[j] = columns[idx_mintemp1]
		else:
			min_air_temperature_1[j] = columns[idx_mintemp1] + convert_temp
		
		if columns[idx_mintemp2] == check_na:
			min_air_temperature_2[j] = columns[idx_mintemp2]
		else:
			min_air_temperature_2[j] = columns[idx_mintemp2] + convert_temp
		
		max_windspeed_u1[j] = columns[idx_maxwindspd1]
		max_windspeed_u2[j] = columns[idx_maxwindspd2]
		stdev_windspeed_u1[j] = columns[idx_sdwindspd1]
		stdev_windspeed_u2[j] = columns[idx_sdwindspd2]
		
		if columns[idx_reftemp] == check_na:
			ref_temperature[j] = columns[idx_reftemp]
		else:
			ref_temperature[j] = columns[idx_reftemp] + convert_temp
		
		windspeed_2m[j] = columns[idx_windspd2m]
		windspeed_10m[j] = columns[idx_windspd10m]
		wind_sensor_height_1[j] = columns[idx_sensorht1]
		wind_sensor_height_2[j] = columns[idx_sensorht1]
		albedo[j] = columns[idx_albedo]
		zenith_angle[j] = columns[idx_zenang]
		qc1[j] = columns[idx_qc1]
		temp1[j] = columns[idx_qc1]
		qc9[j] = columns[idx_qc9]
		temp9[j] = columns[idx_qc9]
		qc17[j] = columns[idx_qc17]
		temp17[j] = columns[idx_qc17]
		qc25[j] = columns[idx_qc25]
		temp25[j] = columns[idx_qc25]

		temp_hour = (columns[idx_jdt]-int(columns[idx_jdt]))

		if temp_hour == hour_exception:
			hour[j] = 0
		else:
			hour[j] = int(temp_hour*hour_conversion)
		
		j += 1

	if station_number[0] == 1:
		temp_stn = 'gcnet_swiss'
	elif station_number[0] == 2:
		temp_stn = 'gcnet_crawford'
	elif station_number[0] == 3:
		temp_stn = 'gcnet_nasa-u'
	elif station_number[0] == 4:
		temp_stn = 'gcnet_gits'
	elif station_number[0] == 5:
		temp_stn = 'gcnet_humboldt'
	elif station_number[0] == 6:
		temp_stn = 'gcnet_summit'
	elif station_number[0] == 7:
		temp_stn = 'gcnet_tunu-n'
	elif station_number[0] == 8:
		temp_stn = 'gcnet_dye2'
	elif station_number[0] == 9:
		temp_stn = 'gcnet_jar'
	elif station_number[0] == 10:
		temp_stn = 'gcnet_saddle'
	elif station_number[0] == 11:
		temp_stn = 'gcnet_dome'
	elif station_number[0] == 12:
		temp_stn = 'gcnet_nasa-e'
	elif station_number[0] == 13:
		temp_stn = 'gcnet_cp2'
	elif station_number[0] == 14:
		temp_stn = 'gcnet_ngrip'
	elif station_number[0] == 15:
		temp_stn = 'gcnet_nasa-se'
	elif station_number[0] == 16:
		temp_stn = 'gcnet_kar'
	elif station_number[0] == 17:
		temp_stn = 'gcnet_jar2'
	elif station_number[0] == 18:
		temp_stn = 'gcnet_kulu'
	elif station_number[0] == 19:
		temp_stn = 'gcnet_jar3'
	elif station_number[0] == 20:
		temp_stn = 'gcnet_aurora'
	elif station_number[0] == 21 or 26:
		temp_stn = 'gcnet_petermann-gl'
	elif station_number[0] == 22:
		temp_stn = 'gcnet_peterman-ela'
	elif station_number[0] == 23:
		temp_stn = 'gcnet_neem'
	elif station_number[0] == 30:
		temp_stn = 'gcnet_lar1'
	elif station_number[0] == 31:
		temp_stn = 'gcnet_lar2'
	elif station_number[0] == 32:
		temp_stn = 'gcnet_lar3'
	
	latitude[0] = (station_dict.get(temp_stn)[0])
	longitude[0] = (station_dict.get(temp_stn)[1])

	if args.station_name:
		print('Default station name overrided by user provided station name')
	else:
		for y in range(0, len(station_dict.get(temp_stn)[2])): station_name[y] = (station_dict.get(temp_stn)[2])[y]
	

	print("extracting quality control variables...")

	qc1_str = [str(e) for e in temp1]
	qc9_str = [str(e) for e in temp9]
	qc17_str = [str(e) for e in temp17]
	qc25_str = [str(e) for e in temp25]
	
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
	

	
	print("calculating day and month...")
	
	def get_month_day(year, day, one_based=False):
		if one_based:  # if Jan 1st is 1 instead of 0
			day -= 1
		dt = datetime(year, 1, 1) + timedelta(days=day)
		return dt.month, dt.day

	n = 0
	while n < num_lines:
		month[n] = get_month_day(int(year[n]), int(julian_decimal_time[n]), True)[0]
		day[n] = get_month_day(int(year[n]), int(julian_decimal_time[n]), True)[1]
		
		time[n] = time_calc(year[n], month[n], day[n], hour[n])
		time_bounds[n] = (time[n]-3600, time[n])
		
		sza[n] = solar(year[n], month[n], day[n], hour[n], latitude[0], longitude[0])
		n += 1
		
	root_grp.close()
