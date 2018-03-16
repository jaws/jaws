import pandas as pd
import xarray as xr
from datetime import datetime
import pytz
from sunposition import sunpos
from common import write_data, time_common
import common

def aaws2nc(args, op_file, station_dict, station_name):

	freezing_point_temp = common.freezing_point_temp
	pascal_per_millibar = common.pascal_per_millibar
	seconds_in_hour = common.seconds_in_hour
	
	if args.fillvalue_float:
		fillvalue_float = args.fillvalue_float
	else:
		fillvalue_float = common.fillvalue_float
	
	header_rows = 8

	column_names = ['timestamp', 'air_temp', 'vtempdiff', 'rh', 'pressure', 'wind_dir', 'wind_spd']

	df = pd.read_csv(args.input_file or args.fl_in, skiprows = header_rows, skip_blank_lines=True, header=None, names = column_names)
	df.index.name = 'time'
	df.loc[:,'air_temp'] += freezing_point_temp
	df.loc[:,'pressure'] *= pascal_per_millibar
	df =  df.where((pd.notnull(df)), fillvalue_float)

	ds = xr.Dataset.from_dataframe(df)
	ds = ds.drop('time')


	# Intializing variables
	num_rows =  df['timestamp'].size
	time, time_bounds, sza = ([0]*num_rows for x in range(3))
	
	
	if args.dbg_lvl > 2:
		print('Retrieving latitude, longitude and station name')
	
	f = open(args.input_file or args.fl_in)
	f.readline()
	for line in f:
		x = str(line[12:].strip('\n'))
		break
	f.close()

	latitude = (station_dict.get(x)[0])
	longitude = (station_dict.get(x)[1])

	
	if args.station_name:
		print('Default station name overrided by user provided station name')
	else:
		station_name = x


	if args.dbg_lvl > 3:
		print('Calculating time and sza')
	
	dtime_1970, tz = time_common(args.timezone)
	i = 0
	
	with open(args.input_file or args.fl_in, "r") as infile:
		for line in infile.readlines()[header_rows:]:
			temp_dtime = datetime.strptime(line.strip().split(",")[0], '%Y-%m-%dT%H:%M:%SZ')
			temp_dtime = tz.localize(temp_dtime.replace(tzinfo=None))		
			time[i] = (temp_dtime-dtime_1970).total_seconds()
			
			time_bounds[i] = (time[i]-seconds_in_hour, time[i])
			
			sza[i] = sunpos(temp_dtime,latitude,longitude,0)[1]
			
			i += 1

	ds['time'] = (('time'),time)
	ds['time_bounds'] = (('time', 'nbnd'),time_bounds)
	ds['sza'] = (('time'),sza)
	ds['station_name'] = ((),station_name)
	ds['latitude'] = ((),latitude)
	ds['longitude'] = ((),longitude)
	

	ds.attrs = {'source':'surface observation', 'featureType':'timeSeries', 'institution':'UW SSEC', 'reference':'https://amrc.ssec.wisc.edu/', 'Conventions':'CF-1.7', 'data_type':'q1h', 'time_convention':"'time: point' variables are valid for exactly the time value stored in the time coordinate, whereas 'time: mean' variables are valid for the mean time within the time_bounds variable." + " For example, air_temp was continuously measured at high frequency and then averaged over each period contained in the time_bounds variable into the store hourly-mean values."}

	ds['air_temp'].attrs= {'units':'kelvin', 'long_name':'air temperature', 'standard_name':'air_temperature', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['vtempdiff'].attrs= {'units':'1', 'long_name':'vertical temperature differential', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['rh'].attrs= {'units':'1', 'long_name':'relative humidity', 'standard_name':'relative_humidity', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['pressure'].attrs= {'units':'pascal', 'long_name':'air pressure', 'standard_name':'air_pressure', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['wind_dir'].attrs= {'units':'degree', 'long_name':'wind direction', 'standard_name':'wind_from_direction', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['wind_spd'].attrs= {'units':'meter second-1', 'long_name':'wind speed', 'standard_name':'wind_speed', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['time'].attrs= {'units':'seconds since 1970-01-01 00:00:00', 'long_name':'Time',	'standard_name':'time', 'bounds':'time_bounds', 'calendar':'leap'}
	ds['sza'].attrs= {'units':'degree', 'long_name':'Solar Zenith Angle', 'standard_name':'solar_zenith_angle', 'coordinates':'longitude latitude', 'cell_methods':'time: mean'}
	ds['station_name'].attrs= {'long_name':'Station Name', 'cf_role':'timeseries_id'}
	ds['latitude'].attrs= {'units':'degrees_north', 'long_name':'Latitude', 'standard_name':'latitude'}
	ds['longitude'].attrs= {'units':'degrees_east', 'long_name':'Longitude', 'standard_name':'longitude'}
	

	encoding = common.get_encoding('aaws', fillvalue_float)

	write_data(args, ds, op_file, encoding)
