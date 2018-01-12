import argparse
from netCDF4 import Dataset
from datetime import date
import os

def aaws2nc(args):

	'''data = ascii.read(args.input)

	f = open(args.input)
	count = 0
	for line in f:
		if line[0] == '#':
			continue
		else:
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
	
	root_grp.source = 'surface observation'
	root_grp.featureType = 'timeSeries'
	root_grp.institution = 'UW SSEC'
	root_grp.reference = 'https://amrc.ssec.wisc.edu/'
	root_grp.Conventions = 'CF-1.6'
	root_grp.start_time = ''
	root_grp.end_time = ''
	root_grp.data_type = 'q1h'

	# dimension
	root_grp.createDimension('station', 25)
	root_grp.createDimension('time', None)
	root_grp.createDimension('nbnd', 2)
	root_grp.createDimension('latitude', 1)
	root_grp.createDimension('longitude', 1)

	# variables
	latitude = root_grp.createVariable('latitude', 'f4', ('latitude',))
	longitude = root_grp.createVariable('longitude', 'f4', ('latitude',))
	station_name = root_grp.createVariable('station_name', 'S1', ('station',))
	time = root_grp.createVariable('time', 'i4', ('time',))
	time_bounds = root_grp.createVariable('time_bounds', 'i4', ('time','nbnd'))
	#stamp = root_grp.createVariable('stamp', 'S20', ('time',))
	air_temp = root_grp.createVariable('air_temp', 'f4', ('time',), fill_value = -999)
	vtempdiff = root_grp.createVariable('vtempdiff', 'f4', ('time',), fill_value = -999)
	rh = root_grp.createVariable('rh', 'f4', ('time',), fill_value = -999)
	pressure = root_grp.createVariable('pressure', 'f4', ('time',), fill_value = -999)
	wind_dir = root_grp.createVariable('wind_dir', 'f4', ('time',), fill_value = -999)
	wind_spd = root_grp.createVariable('wind_spd', 'f4', ('time',), fill_value = -999)
		
	
	station_name.long_name = 'name of station'
	station_name.cf_role = 'timeseries_id'

	latitude.units = 'degree_north'
	latitude.standard_name = 'latitude'

	longitude.units = 'degree_east'
	longitude.standard_name = 'longitude'

	time.units = 'seconds since 1970-01-01T00:00:00Z'
	time.long_name = 'time of measurement'
	time.standard_name = 'time'
	time.bounds = 'time_bounds'
	time.calendar = 'standard'
	
	#stamp.long_name = 'Timestamp'

	air_temp.units = 'kelvin'
	air_temp.long_name = 'air temperature'
	air_temp.standard_name = 'air_temperature'
	
	vtempdiff.units = '1'
	vtempdiff.long_name = 'vertical temperature differential'
	
	rh.units = '1'
	rh.long_name = 'relative humidity'
	rh.standard_name = 'relative_humidity'

	pressure.units = 'pascal'
	pressure.long_name = 'air pressure'
	pressure.standard_name = 'air_pressure'

	wind_dir.units = 'degree'
	wind_dir.long_name = 'wind direction'
	wind_dir.standard_name = 'wind_from_direction'

	wind_spd.units = 'meter second-1'
	wind_spd.long_name = 'wind speed'
	wind_spd.standard_name = 'wind_speed'
	
	i,j = 0,0
	ip_file = open(str(args.input), 'r')

	while i < 8:
	    ip_file.readline()
	    i += 1

	for line in ip_file:
	    
	    line = line.strip()
	    columns = line.split(',')
	    
	    '''if columns[0] == '':
	    	 stamp[j] = 'n/a'
	    else:
	   		stamp[j] = columns[0]'''
	    
	    if columns[1] == '':
	    	 air_temp[j] = -999
	    else:
	   		air_temp[j] = float(columns[1]) + 273.15
	    
	    if columns[2] == '':
	    	 vtempdiff[j] = -999
	    else:
	   		vtempdiff[j] = columns[2]
	    
	    if columns[3] == '':
	    	 rh[j] = -999
	    else:
	   		rh[j] = columns[3]
	    
	    if columns[4] == '':
	    	 pressure[j] = -999
	    else:
	   		pressure[j] = float(columns[4]) * 100
	    
	    if columns[5] == '':
	    	 wind_dir[j] = -999
	    else:
	   		wind_dir[j] = columns[5]
	    
	    if columns[6] == '':
	    	 wind_spd[j] = -999
	    	 j += 1
	    else:
	   		wind_spd[j] = columns[6]
	   		j += 1

	'''for i in data:
		air_temp[:] = data['col2']
		vtempdiff[:] = data['col3']
		rh[:] = data['col4']
		pressure[:] = data['col5']
		wind_dir[:] = data['col6']
		wind_spd[:] = data['col7']
	'''	
	f = open(args.input)
	f.readline()
	for line in f:
		x = list(line[12:].strip('\n'))
		station_name[0:len(x)] = x
		break
	f.close()

	if x == ['A','G','O','-','4']:
		latitude[0] = -82.010
		longitude[0] = 96.760
	elif x == ['A','l','e','x','a','n','d','e','r',' ','T','a','l','l',' ','T','o','w','e','r','!']:
		latitude[0] = -79.012
		longitude[0] = 170.723
	elif x == ['A','u','s','t','i','n']:
		latitude[0] = -75.995
		longitude[0] = -87.470
	elif x == ['B','a','l','d','r','i','c','k']:
		latitude[0] = -82.774
		longitude[0] = -13.054
	elif x == ['B','e','a','r',' ','P','e','n','i','n','s','u','l','a']:
		latitude[0] = -74.546
		longitude[0] = -111.885
	elif x == ['B','y','r','d']:
		latitude[0] = -80.011
		longitude[0] = -119.438
	elif x == ['C','a','p','e',' ','B','i','r','d']:
		latitude[0] = -77.217
		longitude[0] = 166.439
	elif x == ['C','a','p','e',' ','D','e','n','i','s','o','n']:
		latitude[0] = -67.009
		longitude[0] = 142.664
	elif x == ['C','a','p','e',' ','H','a','l','l','e','t','t']:
		latitude[0] = -72.190
		longitude[0] = 170.160
	elif x == ['D','-','1','0']:
		latitude[0] = -66.705
		longitude[0] = 139.841
	elif x == ['D','-','4','7']:
		latitude[0] = -67.385
		longitude[0] = 138.729
	elif x == ['D','-','8','5']:
		latitude[0] = -70.426
		longitude[0] = 134.149
	elif x == ['D','i','s','m','a','l',' ','I','s','l','a','n','d']:
		latitude[0] = -68.088
		longitude[0] = -68.826
	elif x == ['D','o','m','e',' ','C',' ','I','I']:
		latitude[0] = -75.106
		longitude[0] = 123.346
	elif x == ['D','o','m','e',' ','F','u','j','i']:
		latitude[0] = -77.310
		longitude[0] = 39.700
	elif x == ['E','l','a','i','n','e']:
		latitude[0] = -83.094
		longitude[0] = 174.285
	elif x == ['E','l','i','z','a','b','e','t','h']:
		latitude[0] = -82.607
		longitude[0] = -137.078
	elif x == ['E','m','i','l','i','a']:
		latitude[0] = -78.426
		longitude[0] = 173.186
	elif x == ['E','m','m','a']:
		latitude[0] = -83.997
		longitude[0] = -175.047
	elif x == ['E','r','i','n']:
		latitude[0] = -84.902
		longitude[0] = -128.860
	elif x == ['E','v','a','n','s',' ','K','n','o','l','l']:
		latitude[0] = -74.850
		longitude[0] = -100.404
	elif x == ['F','e','r','r','e','l','l']:
		latitude[0] = -77.803
		longitude[0] = 170.817
	elif x == ['G','i','l','l']:
		latitude[0] = -79.879
		longitude[0] = -178.565
	elif x == ['H','a','r','r','y']:
		latitude[0] = -83.005
		longitude[0] = -121.407
	elif x == ['H','e','n','r','y']:
		latitude[0] = -89.001
		longitude[0] = -0.391
	elif x == ['J','a','n','e','t']:
		latitude[0] = -77.174
		longitude[0] = -123.390
	elif x == ['J','A','S','E','2','0','0','7']:
		latitude[0] = -75.888
		longitude[0] = 25.834
	elif x == ['K','a','t','h','i','e']:
		latitude[0] = -77.995
		longitude[0] = -97.268
	elif x == ['K','o','m','i','n','k','o','-','S','l','a','d','e']:
		latitude[0] = -79.466
		longitude[0] = -112.106
	elif x == ['L','a','u','r','i','e',' ','I','I']:
		latitude[0] = -77.439
		longitude[0] = 170.750
	elif x == ['L','e','t','t','a','u']:
		latitude[0] = -82.475
		longitude[0] = -174.587
	elif x == ['L','i','n','d','a']:
		latitude[0] = -78.394
		longitude[0] = 168.446
	elif x == ['L','o','r','n','e']:
		latitude[0] = -78.195
		longitude[0] = 170.028
	elif x == ['M','a','n','u','e','l','a']:
		latitude[0] = -74.946
		longitude[0] = 163.687
	elif x == ['M','a','r','b','l','e',' ','P','o','i','n','t']:
		latitude[0] = -77.439
		longitude[0] = 163.754
	elif x == ['M','a','r','b','l','e',' ','P','o','i','n','t',' ','I','I']:
		latitude[0] = -77.439
		longitude[0] = 163.759
	elif x == ['M','a','r','g','a','r','e','t']:
		latitude[0] = -79.981
		longitude[0] = -165.099
	elif x == ['M','a','r','i','l','y','n']:
		latitude[0] = -79.913
		longitude[0] = 165.657
	elif x == ['M','i','n','n','a',' ','B','l','u','f','f']:
		latitude[0] = -78.555
		longitude[0] = 166.691
	elif x == ['M','i','z','u','h','o']:
		latitude[0] = -70.700
		longitude[0] = 44.290
	elif x == ['N','i','c','o']:
		latitude[0] = -89.000
		longitude[0] = 90.024
	elif x == ['P','A','N','D','A','-','S','o','u','t','h']:
		latitude[0] = -82.325
		longitude[0] = 75.989
	elif x == ['P','h','o','e','n','i','x']:
		latitude[0] = -77.948
		longitude[0] = 166.758
	elif x == ['P','o','r','t',' ','M','a','r','t','i','n']:
		latitude[0] = -66.820
		longitude[0] = 141.390
	elif x == ['P','o','s','s','e','s','s','i','o','n',' ','I','s','l','a','n','d']:
		latitude[0] = -71.891
		longitude[0] = 171.210
	elif x == ['R','e','l','a','y',' ','S','t','a','t','i','o','n']:
		latitude[0] = -74.017
		longitude[0] = 43.062
	elif x == ['S','a','b','r','i','n','a']:
		latitude[0] = -84.247
		longitude[0] = -170.068
	elif x == ['S','c','h','w','e','r','d','t','f','e','g','e','r']:
		latitude[0] = -79.816
		longitude[0] = 170.358
	elif x == ['S','i','p','l','e',' ','D','o','m','e']:
		latitude[0] = -81.652
		longitude[0] = -148.992
	elif x == ['T','h','e','r','e','s','a']:
		latitude[0] = -84.602
		longitude[0] = -115.841
	elif x == ['T','h','u','r','s','t','o','n',' ','I','s','l','a','n','d']:
		latitude[0] = -72.532
		longitude[0] = -97.545
	elif x == ['V','i','t','o']:
		latitude[0] = -78.408
		longitude[0] = 177.829
	elif x == ['W','h','i','t','e',' ','I','s','l','a','n','d']:
		latitude[0] = -78.076
		longitude[0] = 167.451
	elif x == ['W','h','i','t','l','o','c','k']:
		latitude[0] = -76.142
		longitude[0] = 168.394
	elif x == ['W','i','l','l','i','e',' ','F','i','e','l','d']:
		latitude[0] = -77.868
		longitude[0] = 166.921
	elif x == ['W','i','n','d','l','e','s','s',' ','B','i','g','h','t']:
		latitude[0] = -77.728
		longitude[0] = 167.676
	


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

	c = 0
	while c < len(time):
		time_bounds[c] = (time[c]-3600, time[c])
		c += 1
		
	root_grp.close()
