import os
from sunposition import sunpos
from datetime import date, datetime

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
	
	#date_derived = root_grp.createVariable('date_derived', 'S10', ('time',))
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

	#date_derived.note = 'Created date from year and julian decimal time.'
	
	print("converting data...")

	num_lines =  sum(1 for line in open(args.input_file or args.fl_in)) - 54
	#54 is the number of lines before the data starts in input file

	i,j = 0,0
	temp1 = [0]*num_lines
	temp9 = [0]*num_lines
	temp17 = [0]*num_lines
	temp25 = [0]*num_lines
	temp_jdt = [0]*num_lines
	ip_file = open(str(args.input_file or args.fl_in), 'r')

	while i < 54:
	    ip_file.readline()
	    i += 1

	for line in ip_file:
	    
		line = line.strip()
		columns = line.split()
		
		station_number[0] = columns[0]
		year[j] = columns[1]
		julian_decimal_time[j] = columns[2]
		temp_jdt[j] = float(columns[2])
		sw_down[j] = columns[3]
		sw_up[j] = columns[4]
		net_radiation[j] = columns[5]
		
		if columns[6] in {'999.0','999.00','999.000','999.0000'}:
			temperature_tc_1[j] = columns[6]
		else:
			temperature_tc_1[j] = float(columns[6]) + 273.15

		if columns[7] in {'999.0','999.00','999.000','999.0000'}:
			temperature_tc_2[j] = columns[7]
		else:
			temperature_tc_2[j] = float(columns[7]) + 273.15

		if columns[8] in {'999.0','999.00','999.000','999.0000'}:
			temperature_cs500_1[j] = columns[8]
		else:
			temperature_cs500_1[j] = float(columns[8]) + 273.15

		if columns[9] in {'999.0','999.00','999.000','999.0000'}:
			temperature_cs500_2[j] = columns[9]
		else:
			temperature_cs500_2[j] = float(columns[9]) + 273.15

		relative_humidity_1[j] = columns[10]
		relative_humidity_2[j] = columns[11]
		u1_wind_speed[j] = columns[12]
		u2_wind_speed[j] = columns[13]
		u_direction_1[j] = columns[14]
		u_direction_2[j] = columns[15]
		
		if columns[16] in {'999.0','999.00','999.000','999.0000'}:
			atmos_pressure[j] = columns[16]
		else:
			atmos_pressure[j] = float(columns[16]) * 100
		
		snow_height_1[j] = columns[17]
		snow_height_2[j] = columns[18]
		
		if columns[19] in {'999.0','999.00','999.000','999.0000'}:
			t_snow_01[j] = columns[19]
		else:
			t_snow_01[j] = float(columns[19]) + 273.15

		if columns[20] in {'999.0','999.00','999.000','999.0000'}:
			t_snow_02[j] = columns[20]
		else:
			t_snow_02[j] = float(columns[20]) + 273.15

		if columns[21] in {'999.0','999.00','999.000','999.0000'}:
			t_snow_03[j] = columns[21]
		else:
			t_snow_03[j] = float(columns[2]) + 273.15
		
		if columns[22] in {'999.0','999.00','999.000','999.0000'}:
			t_snow_04[j] = columns[22]
		else:
			t_snow_04[j] = float(columns[22]) + 273.15
		
		if columns[23] in {'999.0','999.00','999.000','999.0000'}:
			t_snow_05[j] = columns[23]
		else:
			t_snow_05[j] = float(columns[23]) + 273.15
		
		if columns[24] in {'999.0','999.00','999.000','999.0000'}:
			t_snow_06[j] = columns[24]
		else:
			t_snow_06[j] = float(columns[24]) + 273.15
		
		if columns[25] in {'999.0','999.00','999.000','999.0000'}:
			t_snow_07[j] = columns[25]
		else:
			t_snow_07[j] = float(columns[25]) + 273.15
		
		if columns[26] in {'999.0','999.00','999.000','999.0000'}:
			t_snow_08[j] = columns[26]
		else:
			t_snow_08[j] = float(columns[26]) + 273.15
		
		if columns[27] in {'999.0','999.00','999.000','999.0000'}:
			t_snow_09[j] = columns[27]
		else:
			t_snow_09[j] = float(columns[27]) + 273.15
		
		if columns[28] in {'999.0','999.00','999.000','999.0000'}:
			t_snow_10[j] = columns[28]
		else:
			t_snow_10[j] = float(columns[28]) + 273.15
		
		battery_voltage[j] = columns[29]
		sw_down_max[j] = columns[30]
		sw_up_max[j] = columns[31]
		net_radiation_max[j] = columns[32]
		
		if columns[33] in {'999.0','999.00','999.000','999.0000'}:
			max_air_temperature_1[j] = columns[33]
		else:
			max_air_temperature_1[j] = float(columns[33]) + 273.15
		
		if columns[34] in {'999.0','999.00','999.000','999.0000'}:
			max_air_temperature_2[j] = columns[34]
		else:
			max_air_temperature_2[j] = float(columns[34]) + 273.15
		
		if columns[35] in {'999.0','999.00','999.000','999.0000'}:
			min_air_temperature_1[j] = columns[35]
		else:
			min_air_temperature_1[j] = float(columns[35]) + 273.15
		
		if columns[36] in {'999.0','999.00','999.000','999.0000'}:
			min_air_temperature_2[j] = columns[36]
		else:
			min_air_temperature_2[j] = float(columns[36]) + 273.15
		
		max_windspeed_u1[j] = columns[37]
		max_windspeed_u2[j] = columns[38]
		stdev_windspeed_u1[j] = columns[39]
		stdev_windspeed_u2[j] = columns[40]
		
		if columns[41] in {'999.0','999.00','999.000','999.0000'}:
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
		temp1[j] = columns[48]
		qc9[j] = columns[49]
		temp9[j] = columns[49]
		qc17[j] = columns[50]
		temp17[j] = columns[50]
		qc25[j] = columns[51]
		temp25[j] = columns[51]

		columns[2] = float(columns[2])
		if str(columns[2]-int(columns[2]))[1:4] in {'.0', '.00', '.02','.99'}:
			hour[j] = 0
		elif str(columns[2]-int(columns[2]))[1:4] in {'.04', '.05'}:
			hour[j] = 1
		elif str(columns[2]-int(columns[2]))[1:4] in {'.08', '.07'}:
			hour[j] = 2
		elif str(columns[2]-int(columns[2]))[1:4] in {'.12', '.10'}:
			hour[j] = 3
		elif str(columns[2]-int(columns[2]))[1:4] in {'.16', '.15'}:
			hour[j] = 4
		elif str(columns[2]-int(columns[2]))[1:4] in {'.20'}:
			hour[j] = 5
		elif str(columns[2]-int(columns[2]))[1:4] in {'.25', '.24'}:
			hour[j] = 6
		elif str(columns[2]-int(columns[2]))[1:4] in {'.29'}:
			hour[j] = 7
		elif str(columns[2]-int(columns[2]))[1:4] in {'.33'}:
			hour[j] = 8
		elif str(columns[2]-int(columns[2]))[1:4] in {'.37'}:
			hour[j] = 9
		elif str(columns[2]-int(columns[2]))[1:4] in {'.41'}:
			hour[j] = 10
		elif str(columns[2]-int(columns[2]))[1:4] in {'.45', '.48'}:
			hour[j] = 11
		elif str(columns[2]-int(columns[2]))[1:4] in {'.5', '.49'}:
			hour[j] = 12
		elif str(columns[2]-int(columns[2]))[1:4] in {'.54'}:
			hour[j] = 13
		elif str(columns[2]-int(columns[2]))[1:4] in {'.58'}:
			hour[j] = 14
		elif str(columns[2]-int(columns[2]))[1:4] in {'.62'}:
			hour[j] = 15
		elif str(columns[2]-int(columns[2]))[1:4] in {'.66'}:
			hour[j] = 16
		elif str(columns[2]-int(columns[2]))[1:4] in {'.70', '.71'}:
			hour[j] = 17
		elif str(columns[2]-int(columns[2]))[1:4] in {'.75', '.74'}:
			hour[j] = 18
		elif str(columns[2]-int(columns[2]))[1:4] in {'.79'}:
			hour[j] = 19
		elif str(columns[2]-int(columns[2]))[1:4] in {'.83'}:
			hour[j] = 20
		elif str(columns[2]-int(columns[2]))[1:4] in {'.87'}:
			hour[j] = 21
		elif str(columns[2]-int(columns[2]))[1:4] in {'.91'}:
			hour[j] = 22
		elif str(columns[2]-int(columns[2]))[1:4] in {'.95'}:
			hour[j] = 23
		
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
	print("calculating time...")
	m = 0
	while m < len(temp_jdt):
		if hour[m] == 0:
			time[m] = ((date(year[m], 1, 1) - date(1970, 1, 1)).days + int(temp_jdt[m]))*86400
			m += 1
		elif hour[m] == 1:
			time[m] = ((date(year[m], 1, 1) - date(1970, 1, 1)).days + int(temp_jdt[m]))*86400 + (3600*1)
			m += 1
		elif hour[m] == 2:
			time[m] = ((date(year[m], 1, 1) - date(1970, 1, 1)).days + int(temp_jdt[m]))*86400 + (3600*2)
			m += 1
		elif hour[m] == 3:
			time[m] = ((date(year[m], 1, 1) - date(1970, 1, 1)).days + int(temp_jdt[m]))*86400 + (3600*3)
			m += 1
		elif hour[m] == 4:
			time[m] = ((date(year[m], 1, 1) - date(1970, 1, 1)).days + int(temp_jdt[m]))*86400 + (3600*4)
			m += 1
		elif hour[m] == 5:
			time[m] = ((date(year[m], 1, 1) - date(1970, 1, 1)).days + int(temp_jdt[m]))*86400 + (3600*5)
			m += 1
		elif hour[m] == 6:
			time[m] = ((date(year[m], 1, 1) - date(1970, 1, 1)).days + int(temp_jdt[m]))*86400 + (3600*6)
			m += 1
		elif hour[m] == 7:
			time[m] = ((date(year[m], 1, 1) - date(1970, 1, 1)).days + int(temp_jdt[m]))*86400 + (3600*7)
			m += 1
		elif hour[m] == 8:
			time[m] = ((date(year[m], 1, 1) - date(1970, 1, 1)).days + int(temp_jdt[m]))*86400 + (3600*8)
			m += 1
		elif hour[m] == 9:
			time[m] = ((date(year[m], 1, 1) - date(1970, 1, 1)).days + int(temp_jdt[m]))*86400 + (3600*9)
			m += 1
		elif hour[m] == 10:
			time[m] = ((date(year[m], 1, 1) - date(1970, 1, 1)).days + int(temp_jdt[m]))*86400 + (3600*10)
			m += 1
		elif hour[m] == 11:
			time[m] = ((date(year[m], 1, 1) - date(1970, 1, 1)).days + int(temp_jdt[m]))*86400 + (3600*11)
			m += 1
		elif hour[m] == 12:
			time[m] = ((date(year[m], 1, 1) - date(1970, 1, 1)).days + int(temp_jdt[m]))*86400 + (3600*12)
			m += 1
		elif hour[m] == 13:
			time[m] = ((date(year[m], 1, 1) - date(1970, 1, 1)).days + int(temp_jdt[m]))*86400 + (3600*13)
			m += 1
		elif hour[m] == 14:
			time[m] = ((date(year[m], 1, 1) - date(1970, 1, 1)).days + int(temp_jdt[m]))*86400 + (3600*14)
			m += 1
		elif hour[m] == 15:
			time[m] = ((date(year[m], 1, 1) - date(1970, 1, 1)).days + int(temp_jdt[m]))*86400 + (3600*15)
			m += 1
		elif hour[m] == 16:
			time[m] = ((date(year[m], 1, 1) - date(1970, 1, 1)).days + int(temp_jdt[m]))*86400 + (3600*16)
			m += 1
		elif hour[m] == 17:
			time[m] = ((date(year[m], 1, 1) - date(1970, 1, 1)).days + int(temp_jdt[m]))*86400 + (3600*17)
			m += 1
		elif hour[m] == 18:
			time[m] = ((date(year[m], 1, 1) - date(1970, 1, 1)).days + int(temp_jdt[m]))*86400 + (3600*18)
			m += 1
		elif hour[m] == 19:
			time[m] = ((date(year[m], 1, 1) - date(1970, 1, 1)).days + int(temp_jdt[m]))*86400 + (3600*19)
			m += 1
		elif hour[m] == 20:
			time[m] = ((date(year[m], 1, 1) - date(1970, 1, 1)).days + int(temp_jdt[m]))*86400 + (3600*20)
			m += 1
		elif hour[m] == 21:
			time[m] = ((date(year[m], 1, 1) - date(1970, 1, 1)).days + int(temp_jdt[m]))*86400 + (3600*21)
			m += 1
		elif hour[m] == 22:
			time[m] = ((date(year[m], 1, 1) - date(1970, 1, 1)).days + int(temp_jdt[m]))*86400 + (3600*22)
			m += 1
		elif hour[m] == 23:
			time[m] = ((date(year[m], 1, 1) - date(1970, 1, 1)).days + int(temp_jdt[m]))*86400 + (3600*23)
			m += 1
		
	x = 0
	while x < len(time):
		time_bounds[x] = (time[x]-3600, time[x])
		x += 1	
		

	print("calculating day and month...")
	
	def get_month_day(year, day, one_based=False):
		if one_based:  # if Jan 1st is 1 instead of 0
			day -= 1
		dt = datetime(year, 1, 1) + timedelta(days=day)
		return dt.month, dt.day

	n = 0
	for item in temp_jdt:
		month[n] = get_month_day(int(year[n]), int(temp_jdt[n]), True)[0]
		day[n] = get_month_day(int(year[n]), int(temp_jdt[n]), True)[1]
		n += 1
		
	l = 0
	while l < num_lines:
		temp_datetime = datetime(year[l], month[l], day[l], hour[l])
		sza[l] = sunpos(temp_datetime,latitude[0],longitude[0],0)[1]
		l += 1

	root_grp.close()
