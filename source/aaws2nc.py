import argparse
from netCDF4 import Dataset
from datetime import date
from astropy.io import ascii

def aaws2nc(args):

	data = ascii.read(args.input)

	# NC file setup
	op_file = str((args.input).split('.')[0])+'.nc'
	if args.output:
		op_file = str(args.output)
	root_grp = Dataset(op_file, 'w', format='NETCDF4')
	root_grp.TITLE = 'Weather Station Data'
	root_grp.SOURCE = 'Surface Observations'
	root_grp.INSTITUTION = 'The Antarctic Meteorological Research Center (AMRC) and Automatic Weather Station (AWS)'
	root_grp.REFERENCE = 'https://amrc.ssec.wisc.edu/'
	#root_grp.History = 'Created on '
	#root_grp.CREATED_BY = 'Created by'
	root_grp.Conventions = 'CF-v46'

	# dimension
	root_grp.createDimension('time', args.row_count)

	# variables
	air_temperature = root_grp.createVariable('air_temperature', 'f8', ('time',))
	vtempdiff = root_grp.createVariable('vtempdiff', 'f8', ('time',))
	relative_humidity = root_grp.createVariable('relative_humidity', 'f8', ('time',))
	air_pressure = root_grp.createVariable('air_pressure', 'f8', ('time',))
	wind_direction = root_grp.createVariable('wind_direction', 'f8', ('time',))
	wind_speed = root_grp.createVariable('wind_speed', 'f8', ('time',))
	
	
	time = root_grp.createVariable('time', 'f4', ('time',))


	air_temperature.units = 'degC'
	air_temperature.original_var_name = 'air_temp'
	air_temperature.standard_name = 'air_temperature'
	
	vtempdiff.units = 'degC'
	vtempdiff.original_var_name = 'vtempdiff'
	vtempdiff.standard_name = ''
	
	relative_humidity.units = '%'
	relative_humidity.original_var_name = 'rh'
	relative_humidity.standard_name = 'relative_humidity'

	air_pressure.units = 'mb'
	air_pressure.original_var_name = 'pressure'
	air_pressure.standard_name = 'air_pressure'

	wind_direction.units = 'deg'
	wind_direction.original_var_name = 'wind_dir'
	wind_direction.standard_name = ''

	wind_speed.units = 'ms-1'
	wind_speed.original_var_name = 'wind_spd'
	wind_speed.standard_name = ''
	
	
	time.units = 'days since 1980-01-01 00:00:00'
	time.long_name = 'time'
	time.calendar = 'noleap'
	time.bounds = 'time_bnds'
	time.note = 'Created new derived variable'


	for i in data:
		air_temperature[:] = data['col2']
		#vtempdiff[:] = data['col3']
		relative_humidity[:] = data['col4']
		air_pressure[:] = data['col5']
		wind_direction[:] = data['col6']
		wind_speed[:] = data['col7']
		

	root_grp.close()
