from datetime import date
import os

def aaws2nc(args, op_file, root_grp, station_name, latitude, longitude, time, time_bounds):

	#Global Attributes
	root_grp.source = 'surface observation'
	root_grp.featureType = 'timeSeries'
	root_grp.institution = 'UW SSEC'
	root_grp.reference = 'https://amrc.ssec.wisc.edu/'
	root_grp.Conventions = 'CF-1.7'
	root_grp.start_time = ''
	root_grp.end_time = ''
	root_grp.data_type = 'q1h'

	# variables
	air_temp = root_grp.createVariable('air_temp', 'f4', ('time',), fill_value = -999)
	vtempdiff = root_grp.createVariable('vtempdiff', 'f4', ('time',), fill_value = -999)
	rh = root_grp.createVariable('rh', 'f4', ('time',), fill_value = -999)
	pressure = root_grp.createVariable('pressure', 'f4', ('time',), fill_value = -999)
	wind_dir = root_grp.createVariable('wind_dir', 'f4', ('time',), fill_value = -999)
	wind_spd = root_grp.createVariable('wind_spd', 'f4', ('time',), fill_value = -999)
		
	
	station_name.long_name = 'name of station'
	station_name.cf_role = 'timeseries_id'

	latitude.units = 'degrees_north'
	latitude.standard_name = 'latitude'

	longitude.units = 'degrees_east'
	longitude.standard_name = 'longitude'

	time.units = 'seconds since 1970-01-01T00:00:00Z'
	time.long_name = 'time of measurement'
	time.standard_name = 'time'
	time.bounds = 'time_bounds'
	time.calendar = 'standard'
	
	air_temp.units = 'kelvin'
	air_temp.long_name = 'air temperature'
	air_temp.standard_name = 'air_temperature'
	air_temp.coordinates = 'longitude latitude'
	air_temp.cell_methods = 'time: mean'
	
	vtempdiff.units = '1'
	vtempdiff.long_name = 'vertical temperature differential'
	vtempdiff.coordinates = 'longitude latitude'
	vtempdiff.cell_methods = 'time: mean'
	
	rh.units = '1'
	rh.long_name = 'relative humidity'
	rh.standard_name = 'relative_humidity'
	rh.coordinates = 'longitude latitude'
	rh.cell_methods = 'time: mean'

	pressure.units = 'pascal'
	pressure.long_name = 'air pressure'
	pressure.standard_name = 'air_pressure'
	pressure.coordinates = 'longitude latitude'
	pressure.cell_methods = 'time: mean'

	wind_dir.units = 'degree'
	wind_dir.long_name = 'wind direction'
	wind_dir.standard_name = 'wind_from_direction'
	wind_dir.coordinates = 'longitude latitude'
	wind_dir.cell_methods = 'time: mean'

	wind_spd.units = 'meter second-1'
	wind_spd.long_name = 'wind speed'
	wind_spd.standard_name = 'wind_speed'
	wind_spd.coordinates = 'longitude latitude'
	wind_spd.cell_methods = 'time: mean'
	
	print("converting data...")

	num_lines =  sum(1 for line in open(args.input) if len(line.strip()) != 0) - 8
	#8 is the number of lines before the data starts in input file

	i,j = 0,0
	ip_file = open(str(args.input), 'r')

	while i < 8:
	    ip_file.readline()
	    i += 1

	for line in ip_file:
	    
	    line = line.strip()
	    columns = line.split(',')
	    
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

	
	if args.station_name:
		y = 0
		while y < len(args.station_name):
			station_name[y] = args.station_name[y]
			y += 1
	else:
		f = open(args.input)
		f.readline()
		for line in f:
			x = list(line[12:].strip('\n'))
			station_name[0:len(x)] = x
			break
		f.close()

	
	f = open(args.input)
	f.readline()
	for line in f:
		x = str(line[12:].strip('\n'))
		break
	f.close()


	if x == ['AGO-4']:
		latitude[0] = -82.010
		longitude[0] = 96.760
	elif x == ['Alexander Tall Tower!']:
		latitude[0] = -79.012
		longitude[0] = 170.723
	elif x == ['Austin']:
		latitude[0] = -75.995
		longitude[0] = -87.470
	elif x == ['Baldrick']:
		latitude[0] = -82.774
		longitude[0] = -13.054
	elif x == ['Bear Peninsula']:
		latitude[0] = -74.546
		longitude[0] = -111.885
	elif x == ['Byrd']:
		latitude[0] = -80.011
		longitude[0] = -119.438
	elif x == ['Cape Bird']:
		latitude[0] = -77.217
		longitude[0] = 166.439
	elif x == ['Cape Denison']:
		latitude[0] = -67.009
		longitude[0] = 142.664
	elif x == ['Cape Hallett']:
		latitude[0] = -72.190
		longitude[0] = 170.160
	elif x == ['D-10']:
		latitude[0] = -66.705
		longitude[0] = 139.841
	elif x == ['D-47']:
		latitude[0] = -67.385
		longitude[0] = 138.729
	elif x == ['D-85']:
		latitude[0] = -70.426
		longitude[0] = 134.149
	elif x == ['Dismal Island']:
		latitude[0] = -68.088
		longitude[0] = -68.826
	elif x == ['Dome C II']:
		latitude[0] = -75.106
		longitude[0] = 123.346
	elif x == ['Dome Fuji']:
		latitude[0] = -77.310
		longitude[0] = 39.700
	elif x == ['Elaine']:
		latitude[0] = -83.094
		longitude[0] = 174.285
	elif x == ['Elizabeth']:
		latitude[0] = -82.607
		longitude[0] = -137.078
	elif x == ['Emilia']:
		latitude[0] = -78.426
		longitude[0] = 173.186
	elif x == ['Emma']:
		latitude[0] = -83.997
		longitude[0] = -175.047
	elif x == ['Erin']:
		latitude[0] = -84.902
		longitude[0] = -128.860
	elif x == ['Evans Knoll']:
		latitude[0] = -74.850
		longitude[0] = -100.404
	elif x == ['Ferrell']:
		latitude[0] = -77.803
		longitude[0] = 170.817
	elif x == ['Gill']:
		latitude[0] = -79.879
		longitude[0] = -178.565
	elif x == ['Harry']:
		latitude[0] = -83.005
		longitude[0] = -121.407
	elif x == ['Henry']:
		latitude[0] = -89.001
		longitude[0] = -0.391
	elif x == ['Janet']:
		latitude[0] = -77.174
		longitude[0] = -123.390
	elif x == ['JASE2007']:
		latitude[0] = -75.888
		longitude[0] = 25.834
	elif x == ['Kathie']:
		latitude[0] = -77.995
		longitude[0] = -97.268
	elif x == ['Kominko-Slade']:
		latitude[0] = -79.466
		longitude[0] = -112.106
	elif x == ['Laurie II']:
		latitude[0] = -77.439
		longitude[0] = 170.750
	elif x == ['Lettau']:
		latitude[0] = -82.475
		longitude[0] = -174.587
	elif x == ['Linda']:
		latitude[0] = -78.394
		longitude[0] = 168.446
	elif x == ['Lorne']:
		latitude[0] = -78.195
		longitude[0] = 170.028
	elif x == ['Manuela']:
		latitude[0] = -74.946
		longitude[0] = 163.687
	elif x == ['Marble Point']:
		latitude[0] = -77.439
		longitude[0] = 163.754
	elif x == ['Marble Point II']:
		latitude[0] = -77.439
		longitude[0] = 163.759
	elif x == ['Margaret']:
		latitude[0] = -79.981
		longitude[0] = -165.099
	elif x == ['Marilyn']:
		latitude[0] = -79.913
		longitude[0] = 165.657
	elif x == ['Minna Bluff']:
		latitude[0] = -78.555
		longitude[0] = 166.691
	elif x == ['Mizuho']:
		latitude[0] = -70.700
		longitude[0] = 44.290
	elif x == ['Nico']:
		latitude[0] = -89.000
		longitude[0] = 90.024
	elif x == ['PANDA-South']:
		latitude[0] = -82.325
		longitude[0] = 75.989
	elif x == ['Phoenix']:
		latitude[0] = -77.948
		longitude[0] = 166.758
	elif x == ['Port Martin']:
		latitude[0] = -66.820
		longitude[0] = 141.390
	elif x == ['Possession Island']:
		latitude[0] = -71.891
		longitude[0] = 171.210
	elif x == ['Relay Station']:
		latitude[0] = -74.017
		longitude[0] = 43.062
	elif x == ['Sabrina']:
		latitude[0] = -84.247
		longitude[0] = -170.068
	elif x == ['Schwerdtfeger']:
		latitude[0] = -79.816
		longitude[0] = 170.358
	elif x == ['Siple Dome']:
		latitude[0] = -81.652
		longitude[0] = -148.992
	elif x == ['Theresa']:
		latitude[0] = -84.602
		longitude[0] = -115.841
	elif x == ['Thurston Island']:
		latitude[0] = -72.532
		longitude[0] = -97.545
	elif x == ['Vito']:
		latitude[0] = -78.408
		longitude[0] = 177.829
	elif x == ['White Island']:
		latitude[0] = -78.076
		longitude[0] = 167.451
	elif x == ['Whitlock']:
		latitude[0] = -76.142
		longitude[0] = 168.394
	elif x == ['Willie Field']:
		latitude[0] = -77.868
		longitude[0] = 166.921
	elif x == ['Windless Bight']:
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
