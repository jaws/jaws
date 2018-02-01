import argparse
import gcnet2nc
import promice2nc
import aaws2nc
import os
from netCDF4 import Dataset
import sys

def Main():
	parser = argparse.ArgumentParser()
	parser.add_argument("input", nargs = '?', help="The PROMICE file you wish to convert to netCDF.", type=str)
	parser.add_argument("output", nargs = '?', help="Path where you want to store the output file", type=str)
	parser.add_argument("-i","--fl_in", help="The PROMICE file you wish to convert to netCDF.", type=str)
	parser.add_argument("-o", "--fl_out", help="Path where you want to store the output file", type=str)
	parser.add_argument("-3", "--format3", "--3", "--fl_fmt=classic", help="NETCDF3_CLASSIC", action="store_true")
	parser.add_argument("-4", "--format4", "--4", "--netcdf4", "--fl_fmt=netcdf4", help="NETCDF4", action="store_true")
	parser.add_argument("-5", "--format5", "--5", "--64bit_data", "--fl_fmt=64bit_data", "--fl_fmt=cdf5", help="NETCDF3_64BIT_DATA", action="store_true")
	parser.add_argument("-6", "--format6", "--6", "--64bit_offset", "--fl_fmt=64bit_offset", help="NETCDF3_64BIT_OFFSET", action="store_true")
	parser.add_argument("-7", "--format7", "--7", "--fl_fmt=netcdf4_classic", help="NETCDF4_CLASSIC", action="store_true")
	parser.add_argument("-s","--station_name", help = "name of station if you want to change")

	args = parser.parse_args()

	if (args.input or args.fl_in):
		pass
	else:
		print('Error: You failed to provide input file!')
		sys.exit(1)

	######################################################################

	station_dict = {
		'gcnet_swiss': [69.56833, -49.31582, 'Swiss Camp'],
		'gcnet_crawford': [69.87975, -46.98667, 'Crawford Pt.'],
		'gcnet_nasa-u': [73.84189, -49.49831, 'NASA-U'],
		'gcnet_gits': [77.13781, -61.04113, 'GITS'],
		'gcnet_humboldt': [78.5266, -56.8305, 'Humboldt'],
		'gcnet_summit': [72.57972, -38.50454, 'Summit'],
		'gcnet_tunu-n': [78.01677, -33.99387, 'TUNU-N'],
		'gcnet_dye2': [66.48001, -46.27889, 'DYE-2'],
		'gcnet_jar': [69.498358, -49.68156, 'JAR'],
		'gcnet_saddle': [65.99947, -44.50016, 'Saddle'],
		'gcnet_dome': [63.14889, -44.81717, 'South Dome'],
		'gcnet_nasa-e': [75.00000, -29.99972, 'NASA-E'],
		'gcnet_cp2': [69.87968, -46.98692, 'CP2'],
		'gcnet_ngrip': [75.09975, -42.33256, 'NGRIP'],
		'gcnet_nasa-se': [66.4797, -42.5002, 'NASA-SE'],
		'gcnet_kar': [69.69942, -33.00058, 'KAR'],
		'gcnet_jar2': [69.42000, -50.05750, 'JAR 2'],
		'gcnet_kulu': [65.75845, -39.60177, 'KULU'],
		'gcnet_jar3': [69.39444, 50.31000, 'JAR3',],
		'gcnet_aurora': [67.13583, 47.29222, 'Aurora',],
		'gcnet_petermann-gl': [80.68361, 60.29305, 'Petermann Gl.',],
		'gcnet_peterman-ela': [80.08305, 58.07277, 'Peterman ELA',],
		'gcnet_neem': [77.50222, 50.87444, 'NEEM',],
		'gcnet_lar1': [68.14111, 63.95194, 'LAR1',],
		'gcnet_lar2': [67.57638, 63.25750, 'LAR2',],
		'gcnet_lar3': [67.03166, 62.65027, 'LAR3',],

		'promice_egp': [75.6247, 35.9748, 'EGP'],
		'promice_kanb': [67.1252, 50.1832, 'KAN_B'],
		'promice_kanl': [67.0955, 49.9513, 'KAN_L'],
		'promice_kanm': [67.0670, 48.8355, 'KAN_M'],
		'promice_kanu': [67.0003, 47.0253, 'KAN_U'],
		'promice_kpcl': [79.9108, 24.0828, 'KPC_L'],
		'promice_kpcu': [79.8347, 25.1662, 'KPC_U'],
		'promice_mit': [65.6922, 37.8280, 'MIT'],
		'promice_nukk': [64.1623, 51.3587, 'NUK_K'],
		'promice_nukl': [64.4822, 49.5358, 'NUK_L'],
		'promice_nukn': [64.9452, 49.8850, 'NUK_N'],
		'promice_nuku': [64.5108, 49.2692, 'NUK_U'],
		'promice_qasa': [61.2430, 46.7328, 'QAS_A'],
		'promice_qasl': [61.0308, 46.8493, 'QAS_L'],
		'promice_qasm': [61.0998, 46.8330, 'QAS_M'],
		'promice_qasu': [61.1753, 46.8195, 'QAS_U'],
		'promice_scol': [72.2230, 26.8182, 'SCO_L'],
		'promice_scou': [72.3933, 27.2333, 'SCO_U'],
		'promice_tasa': [65.7790, 38.8995, 'TAS_A'],
		'promice_tasl': [65.6402, 38.8987, 'TAS_L'],
		'promice_tasu': [65.6978, 38.8668, 'TAS_U'],
		'promice_thul': [76.3998, 68.2665, 'THU_L'],
		'promice_thuu': [76.4197, 68.1463, 'THU_U'],
		'promice_upel': [72.8932, 54.2955, 'UPE_L'],
		'promice_upeu': [72.8878, 53.5783, 'UPE_U'],
		'promice_cen': [0, 0, 'CEN'],

		'aaws_ago4': [-82.010, 96.760, 'AGO-4'],
		'aaws_alexander': [-79.012, 170.723, 'Alexander Tall Tower!'],
		'aaws_austin': [-75.995, -87.470, 'Austin'],
		'aaws_baldrick': [-82.774, -13.054, 'Baldrick'],
		'aaws_bearpeninsula': [-74.546, -111.885, 'Bear Peninsula'],
		'aaws_bonapartepoint': [-64.778, -64.067, 'Bonaparte Point'],
		'aaws_byrd': [-80.011, -119.438, 'Byrd'],
		'aaws_capebird': [-77.217, 166.439, 'Cape Bird'],
		'aaws_capedenison': [-67.009, 142.664, 'Cape Denison'],
		'aaws_capehallett': [-72.190, 170.160, 'Cape Hallett'],
		'aaws_d10': [-66.705, 139.841, 'D-10'],
		'aaws_d47': [-67.385, 138.729, 'D-47'],
		'aaws_d85': [-70.426, 134.149, 'D-85'],
		'aaws_dismalisland': [-68.088, -68.826, 'Dismal Island'],
		'aaws_domecII': [-75.106, 123.346, 'Dome C II'],
		'aaws_domefuji': [-77.310, 39.700, 'Dome Fuji'],
		'aaws_elaine': [-83.094, 174.285, 'Elaine'],
		'aaws_elizabeth': [-82.607, -137.078, 'Elizabeth'],
		'aaws_emilia': [-78.426, 173.186, 'Emilia'],
		'aaws_emma': [-83.997, -175.047, 'Emma'],
		'aaws_erin': [-84.902, -128.860, 'Erin'],
		'aaws_evansknoll': [-74.850, -100.404, 'Evans Knoll'],
		'aaws_ferrell': [-77.803, 170.817, 'Ferrell'],
		'aaws_gill': [-79.879, -178.565, 'Gill'],
		'aaws_harry': [-83.005, -121.407, 'Harry'],
		'aaws_henry': [-89.001, -0.391, 'Henry'],
		'aaws_janet': [-77.174, -123.390, 'Janet'],
		'aaws_jase2007': [-75.888, 25.834, 'JASE2007'],
		'aaws_kathie': [-77.995, -97.268, 'Kathie'],
		'aaws_kominkoslade': [-79.466, -112.106, 'Kominko-Slade'],
		'aaws_laurieII': [-77.439, 170.750, 'Laurie II'],
		'aaws_lettau': [-82.475, -174.587, 'Lettau'],
		'aaws_linda': [-78.394, 168.446, 'Linda'],
		'aaws_lorne': [-78.195, 170.028, 'Lorne'],
		'aaws_manuela': [-74.946, 163.687, 'Manuela'],
		'aaws_marblepoint': [-77.439, 163.754, 'Marble Point'],
		'aaws_marblepointII': [-77.439, 163.759, 'Marble Point II'],
		'aaws_margaret': [-79.981, -165.099, 'Margaret'],
		'aaws_marilyn': [-79.913, 165.657, 'Marilyn'],
		'aaws_minnabluff': [-78.555, 166.691, 'Minna Bluff'],
		'aaws_mizuho': [-70.700, 44.290, 'Mizuho'],
		'aaws_mountsiple': [-73.198, -127.052, 'Mount Siple'],
		'aaws_nico': [-89.000, 90.024, 'Nico'],
		'aaws_pandasouth': [-82.325, 75.989, 'PANDA-South'],
		'aaws_pegasusnorth': [-77.957, 166.515, 'Pegasus North'],
		'aaws_phoenix': [-77.948, 166.758, 'Phoenix'],
		'aaws_portmartin': [-66.820, 141.390, 'Port Martin'],
		'aaws_possessionisland': [-71.891, 171.210, 'Possession Island'],
		'aaws_relaystation': [-74.017, 43.062, 'Relay Station'],
		'aaws_sabrina': [-84.247, -170.068, 'Sabrina'],
		'aaws_schwerdtfeger': [-79.816, 170.358, 'Schwerdtfeger'],
		'aaws_sipledome': [-81.652, -148.992, 'Siple Dome'],
		'aaws_theresa': [-84.602, -115.841, 'Theresa'],
		'aaws_thurstonisland': [-72.532, -97.545, 'Thurston Island'],
		'aaws_vito': [-78.408, 177.829, 'Vito'],
		'aaws_whiteisland': [-78.076, 167.451, 'White Island'],
		'aaws_whitlock': [-76.142, 168.394, 'Whitlock'],
		'aaws_williefield': [-77.868, 166.921, 'Willie Field'],
		'aaws_windlessbight': [-77.728, 167.676, 'Windless Bight']

	}

	# NC file setup
	if (args.output or args.fl_out):
		op_file = str(args.output or args.fl_out)

	else:
		get_name = str((os.path.basename(args.input or args.fl_in)).split('.')[0])
		
		if get_name == '01c':
			op_file = list(station_dict.keys())[0] + '.nc' 
		elif get_name == '02c':
			op_file = list(station_dict.keys())[1] + '.nc' 
		elif get_name == '03c':
			op_file = list(station_dict.keys())[2] + '.nc' 
		elif get_name == '04c':
			op_file = list(station_dict.keys())[3] + '.nc' 
		elif get_name == '05c':
			op_file = list(station_dict.keys())[4] + '.nc' 
		elif get_name == '06c':
			op_file = list(station_dict.keys())[5] + '.nc' 
		elif get_name == '07c':
			op_file = list(station_dict.keys())[6] + '.nc' 
		elif get_name == '08c':
			op_file = list(station_dict.keys())[7] + '.nc' 
		elif get_name == '09c':
			op_file = list(station_dict.keys())[8] + '.nc' 
		elif get_name == '10c':
			op_file = list(station_dict.keys())[9] + '.nc' 
		elif get_name == '11c':
			op_file = list(station_dict.keys())[10] + '.nc' 
		elif get_name == '12c':
			op_file = list(station_dict.keys())[11] + '.nc' 
		elif get_name == '13c':
			op_file = list(station_dict.keys())[12] + '.nc' 
		elif get_name == '14c':
			op_file = list(station_dict.keys())[13] + '.nc' 
		elif get_name == '15c':
			op_file = list(station_dict.keys())[14] + '.nc' 
		elif get_name == '16c':
			op_file = list(station_dict.keys())[15] + '.nc' 
		elif get_name == '17c':
			op_file = list(station_dict.keys())[16] + '.nc' 
		elif get_name == '18c':
			op_file = list(station_dict.keys())[17] + '.nc' 
		elif get_name == '19c':
			op_file = list(station_dict.keys())[18] + '.nc' 
		elif get_name == '20c':
			op_file = list(station_dict.keys())[19] + '.nc' 
		elif get_name == '21c':
			op_file = list(station_dict.keys())[20] + '.nc' 
		elif get_name == '22c':
			op_file = list(station_dict.keys())[21] + '.nc' 
		elif get_name == '23c':
			op_file = list(station_dict.keys())[22] + '.nc' 
		elif get_name == '30c':
			op_file = list(station_dict.keys())[23] + '.nc' 
		elif get_name == '31c':
			op_file = list(station_dict.keys())[24] + '.nc' 
		elif get_name == '32c':
			op_file = list(station_dict.keys())[25] + '.nc'
		else:
			op_file = get_name + '.nc'
	

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

	# dimension
	stn_nm_lng_max=25
	root_grp.createDimension('time', None)
	root_grp.createDimension('nbnd', 2)
	root_grp.createDimension('station', 1)
	root_grp.createDimension('stn_nm_lng_max', stn_nm_lng_max)

	# Common variables
	station_name = root_grp.createVariable('station_name', 'S1', ('stn_nm_lng_max',))
	latitude = root_grp.createVariable('latitude', 'f4')
	longitude = root_grp.createVariable('longitude', 'f4')
	time = root_grp.createVariable('time', 'i4', ('time',))
	time_bounds = root_grp.createVariable('time_bounds', 'i4', ('time','nbnd'))
	sza = root_grp.createVariable('sza', 'f4', ('time',))

	# Variable attributes
	station_name.long_name = 'Station Name'
	station_name.cf_role = 'timeseries_id'

	latitude.units = 'degrees_north'
	latitude.standard_name = 'latitude'

	longitude.units = 'degrees_east'
	longitude.standard_name = 'longitude'

	time.units = 'seconds since 1970-01-01 00:00:00'
	time.long_name = 'time of measurement'
	time.standard_name = 'time'
	time.bounds = 'time_bounds'
	time.calendar = 'noleap'
	
	sza.units = 'degree'
	sza.long_name = 'Solar Zenith Angle'
	sza.standard_name = 'solar_zenith_angle'
	sza.coordinates = 'longitude latitude'
	sza.cell_methods = 'time: mean'



	if args.station_name:
		y = 0
		while y < len(args.station_name):
			station_name[y] = args.station_name[y]
			y += 1

	######################################################################

	with open(str(args.input or args.fl_in),'r') as f:
		line = f.readline()

	if line[0] == 'D':
		gcnet2nc.gcnet2nc(args, op_file, root_grp, station_name, latitude, longitude, time, time_bounds, sza, station_dict)

	elif line[0] == 'Y':
		promice2nc.promice2nc(args, op_file, root_grp, station_name, latitude, longitude, time, time_bounds, sza, station_dict)

	elif line[0] == '#':
		aaws2nc.aaws2nc(args, op_file, root_grp, station_name, latitude, longitude, time, time_bounds, sza, station_dict)

	print("Converted " + str(os.path.basename(args.input or args.fl_in)) + " to netCDF format")


if __name__ == '__main__':
    Main()
