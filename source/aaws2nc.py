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
	
	common.load_ds_attrs('aaws', ds)
	encoding = common.get_encoding('aaws', fillvalue_float)

	write_data(args, ds, op_file, encoding)
