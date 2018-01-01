import argparse
from netCDF4 import Dataset
from datetime import date
from astropy.io import ascii

def aaws2nc(args):

	data = ascii.read(args.input)

	f = open(args.input)
	count = 0
	for line in f:
		if line[0] == '#':
			continue
		else:
			count += 1
	f.close()

	# NC file setup
	op_file = str((args.input).split('.')[0])+'.nc'
	if args.output:
		op_file = str(args.output)
	root_grp = Dataset(op_file, 'w', format='NETCDF4')
	root_grp.SOURCE = 'surface observation'
	root_grp.featureType = 'timeSeries'
	root_grp.INSTITUTION = 'UW SSEC'
	root_grp.REFERENCE = 'https://amrc.ssec.wisc.edu/'
	root_grp.Conventions = 'CF-1.6'
	root_grp.start_time = ''
	root_grp.end_time = ''
	root_grp.data_type = 'q1h'

	# dimension
	root_grp.createDimension('station', 1)
	root_grp.createDimension('time', count)

	# variables
	station_name = root_grp.createVariable('station_name', 'S20', ('station',))
	time = root_grp.createVariable('time', 'i4', ('time',))
	air_temp = root_grp.createVariable('air_temp', 'f4', ('station','time',), fill_value = -999)
	vtempdiff = root_grp.createVariable('vtempdiff', 'f4', ('station','time',), fill_value = -999)
	rh = root_grp.createVariable('rh', 'f4', ('station','time',), fill_value = -999)
	pressure = root_grp.createVariable('pressure', 'f4', ('station','time',), fill_value = -999)
	wind_dir = root_grp.createVariable('wind_dir', 'f4', ('station','time',), fill_value = -999)
	wind_spd = root_grp.createVariable('wind_spd', 'f4', ('station','time',), fill_value = -999)
	
	
	
	station_name.long_name = 'name of station'
	station_name.cf_role = 'timeseries_id'

	time.units = 'seconds since 1970-01-01T00:00:00Z'
	time.long_name = 'time of measurement'
	time.standard_name = 'time'
	time.calendar = 'standard'
	
	air_temp.units = 'degC'
	air_temp.long_name = 'air temperature'
	air_temp.standard_name = 'air_temperature'
	
	vtempdiff.units = '1'
	vtempdiff.long_name = 'vertical temperature differential'
	
	rh.units = '%'
	rh.long_name = 'relative humidity'
	rh.standard_name = 'relative_humidity'

	pressure.units = 'hPa'
	pressure.long_name = 'air pressure'
	pressure.standard_name = 'air_pressure'

	wind_dir.units = 'deg'
	wind_dir.long_name = 'wind direction'
	wind_dir.standard_name = 'wind_from_direction'

	wind_spd.units = 'ms-1'
	wind_spd.original_var_name = 'wind speed'
	wind_spd.standard_name = 'wind_speed'
	
	
	for i in data:
		air_temp[:] = data['col2']
		vtempdiff[:] = data['col3']
		rh[:] = data['col4']
		pressure[:] = data['col5']
		wind_dir[:] = data['col6']
		wind_spd[:] = data['col7']
		
	f = open(args.input)
	f.readline()
	for line in f:
		station_name[0] = line[12:17]
		break
	f.close()

	f = open(args.input)
	a,b = 0,0
	while a < 8:
		f.readline()
		a += 1
	for line in f:
		time[b] = ((date(int(line[0:4]), int(line[5:7]), int(line[8:10])) - date(1970,1,1)).days)*86400
		if line[11:13] == '00':
			b += 1			
		elif line[11:13] == '01':
			time[b] += (3600*1)
			b += 1
		elif line[11:13] == '02':
			time[b] += (3600*2)
			b += 1
		elif line[11:13] == '03':
			time[b] += (3600*3)
			b += 1
		elif line[11:13] == '04':
			time[b] += (3600*4)
			b += 1
		elif line[11:13] =='05':
			time[b] += (3600*5)
			b += 1
		elif line[11:13] == '06':
			time[b] += (3600*6)
			b += 1
		elif line[11:13] == '07':
			time[b] += (3600*7)
			b += 1
		elif line[11:13] == '08':
			time[b] += (3600*8)
			b += 1
		elif line[11:13] == '09':
			time[b] += (3600*9)
			b += 1
		elif line[11:13] == '10':
			time[b] += (3600*10)
			b += 1
		elif line[11:13] == '11':
			time[b] += (3600*11)
			b += 1
		elif line[11:13] == '12':
			time[b] += (3600*12)
			b += 1
		elif line[11:13] == '13':
			time[b] += (3600*13)
			b += 1
		elif line[11:13] == '14':
			time[b] += (3600*14)
			b += 1
		elif line[11:13] == '15':
			time[b] += (3600*15)
			b += 1
		elif line[11:13] == '16':
			time[b] += (3600*16)
			b += 1
		elif line[11:13] == '17':
			time[b] += (3600*17)
			b += 1
		elif line[11:13] == '18':
			time[b] += (3600*18)
			b += 1
		elif line[11:13] == '19':
			time[b] += (3600*19)
			b += 1
		elif line[11:13] == '20':
			time[b] += (3600*20)
			b += 1
		elif line[11:13] == '21':
			time[b] += (3600*21)
			b += 1
		elif line[11:13] == '22':
			time[b] += (3600*22)
			b += 1
		elif line[11:13] == '23':
			time[b] += (3600*23)
			b += 1
	f.close()

	root_grp.close()
