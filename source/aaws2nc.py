from datetime import date
import os
from sunposition import sunpos
from datetime import datetime

def aaws2nc(args, op_file, root_grp, station_name, latitude, longitude, time, time_bounds, sza, station_dict):

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
		print('Default station name overrided by user provided station name')
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

	print(x)
	if x == 'AGO-4':
		temp_stn = 'aaws_ago4'
	elif x == 'Alexander Tall Tower!':
		temp_stn = 'aaws_alexander'
	elif x == 'Austin':
		temp_stn = 'aaws_austin'
	elif x == 'Baldrick':
		temp_stn = 'aaws_baldrick'
	elif x == 'Bear Peninsula':
		temp_stn = 'aaws_bearpeninsula'
	elif x == 'Byrd':
		temp_stn = 'aaws_byrd'
	elif x == 'Cape Bird':
		temp_stn = 'aaws_capebird'
	elif x == 'Cape Denison':
		temp_stn = 'aaws_capedenison'
	elif x == 'Cape Hallett':
		temp_stn = 'aaws_capehallett'
	elif x == 'D-10':
		temp_stn = 'aaws_d10'
	elif x == 'D-47':
		temp_stn = 'aaws_d47'
	elif x == 'D-85':
		temp_stn = 'aaws_d85'
	elif x == 'Dismal Island':
		temp_stn = 'aaws_dismalisland'
	elif x == 'Dome C II':
		temp_stn = 'aaws_domecII'
	elif x == 'Dome Fuji':
		temp_stn = 'aaws_domefuji'
	elif x == 'Elaine':
		temp_stn = 'aaws_elaine'
	elif x == 'Elizabeth':
		temp_stn = 'aaws_elizabeth'
	elif x == 'Emilia':
		temp_stn = 'aaws_emilia'
	elif x == 'Emma':
		temp_stn = 'aaws_emma'
	elif x == 'Erin':
		temp_stn = 'aaws_erin'
	elif x == 'Evans Knoll':
		temp_stn = 'aaws_evansknoll'
	elif x == 'Ferrell':
		temp_stn = 'aaws_ferrell'
	elif x == 'Gill':
		temp_stn = 'aaws_gill'
	elif x == 'Harry':
		temp_stn = 'aaws_harry'
	elif x == 'Henry':
		temp_stn = 'aaws_henry'
	elif x == 'Janet':
		temp_stn = 'aaws_janet'
	elif x == 'JASE2007':
		temp_stn = 'aaws_jase2007'
	elif x == 'Kathie':
		temp_stn = 'aaws_kathie'
	elif x == 'Kominko-Slade':
		temp_stn = 'aaws_kominkoslade'
	elif x == 'Laurie II':
		temp_stn = 'aaws_laurieII'
	elif x == 'Lettau':
		temp_stn = 'aaws_lettau'
	elif x == 'Linda':
		temp_stn = 'aaws_linda'
	elif x == 'Lorne':
		temp_stn = 'aaws_lorne'
	elif x == 'Manuela':
		temp_stn = 'aaws_manuela'
	elif x == 'Marble Point':
		temp_stn = 'aaws_marblepoint'
	elif x == 'Marble Point II':
		temp_stn = 'aaws_marblepointII'
	elif x == 'Margaret':
		temp_stn = 'aaws_margaret'
	elif x == 'Marilyn':
		temp_stn = 'aaws_marilyn'
	elif x == 'Minna Bluff':
		temp_stn = 'aaws_minnabluff'
	elif x == 'Mizuho':
		temp_stn = 'aaws_mizuho'
	elif x == 'Nico':
		temp_stn = 'aaws_nico'
	elif x == 'PANDA-South':
		temp_stn = 'aaws_pandasouth'
	elif x == 'Phoenix':
		temp_stn = 'aaws_phoenix'
	elif x == 'Port Martin':
		temp_stn = 'aaws_portmartin'
	elif x == 'Possession Island':
		temp_stn = 'aaws_possessionisland'
	elif x == 'Relay Station':
		temp_stn = 'aaws_relaystation'
	elif x == 'Sabrina':
		temp_stn = 'aaws_sabrina'
	elif x == 'Schwerdtfeger':
		temp_stn = 'aaws_schwerdtfeger'
	elif x == 'Siple Dome':
		temp_stn = 'aaws_sipledome'
	elif x == 'Theresa':
		temp_stn = 'aaws_theresa'
	elif x == 'Thurston Island':
		temp_stn = 'aaws_thurstonisland'
	elif x == 'Vito':
		temp_stn = 'aaws_vito'
	elif x == 'White Island':
		temp_stn = 'aaws_whiteisland'
	elif x == 'Whitlock':
		temp_stn = 'aaws_whitlock'
	elif x == 'Willie Field':
		temp_stn = 'aaws_williefield'
	elif x == 'Windless Bight':
		temp_stn = 'aaws_windlessbight'
	
	latitude[0] = (station_dict.get(temp_stn)[0])
	longitude[0] = (station_dict.get(temp_stn)[1])

	f = open(args.input)
	a,b = 0,0
	while a < 8:
		f.readline()
		a += 1
	for line in f:
		
		temp_datetime = datetime(int(line[0:4]), int(line[5:7]), int(line[8:10]), int(line[11:13]))
		sza[b] = sunpos(temp_datetime,latitude[0],longitude[0],0)[1]

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
