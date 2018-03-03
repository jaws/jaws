import os, sys
import argparse
import gcnet2nc, promice2nc, aaws2nc
from collections import OrderedDict
from datetime import datetime

def Main():
	start_time = datetime.now()
	
	parser = argparse.ArgumentParser()
	parser.add_argument("input_file", nargs = '?', help="Raw L2 data file to convert to netCDF (or use -i option)", type=str)
	parser.add_argument("output_file", nargs = '?', help="Output netCDF file (or use -o option)", type=str)
	parser.add_argument("-i","--fl_in", "--input", help="Raw L2 data file to convert to netCDF (or use first positional argument)", type=str)
	parser.add_argument("-o", "--fl_out", "--output", help="Output netCDF file (or use last positional argument)", type=str)
	parser.add_argument("-3", "--format3", "--3", "--fl_fmt=classic", help="Output file in netCDF3 CLASSIC (32-bit offset) storage format", action="store_true")
	parser.add_argument("-4", "--format4", "--4", "--netcdf4", help="Output file in netCDF4 (HDF5) storage format", action="store_true")
	parser.add_argument("-5", "--format5", "--5", "--fl_fmt=64bit_data", help="Output file in netCDF3 64-bit data (i.e., CDF5, PnetCDF) storage format", action="store_true")
	parser.add_argument("-6", "--format6", "--6", "--64", "--fl_fmt=64bit_offset", help="Output file in netCDF3 64-bit offset storage format", action="store_true")
	parser.add_argument("-7", "--format7", "--7", "--fl_fmt=netcdf4_classic", help="Output file in netCDF4 CLASSIC format (3+4=7)", action="store_true")
	parser.add_argument("-d","--derive_times", help = "For GCNet, extra variables ('month', 'day' and 'hour') will be derived for further analysis. It will take more time", action="store_true")
	parser.add_argument("-s","--station_name", help = "Override default station name", type=str)
	parser.add_argument("-t","--timezone", help = "Change the timezone, default is UTC", default='UTC', type=str)
	parser.add_argument("-f","--fillvalue_float", help = "Override default float _FillValue", type=float)
	parser.add_argument("-D","--dbg_lvl","--debuglevel", help = "Debug-level is lvl", default=0, type=int)

	args = parser.parse_args()

	if (args.input_file or args.fl_in):
		pass
	else:
		print('Error: You failed to provide input file!\n')
		parser.print_help()
		print('\nPost questions, suggestions, patches at  https://github.com/jaws/jaws')
		sys.exit(1)

	######################################################################

	station_dict = {
		'blank': [],
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
		'gcnet_jar3': [69.39444, -50.31000, 'JAR3',],
		'gcnet_aurora': [67.13583, -47.29222, 'Aurora',],
		'gcnet_petermann-gl': [80.68361, -60.29305, 'Petermann Gl.',],
		'gcnet_peterman-ela': [80.08305, -58.07277, 'Peterman ELA',],
		'gcnet_neem': [77.50222, -50.87444, 'NEEM',],
		'gcnet_lar1': [68.14111, -63.95194, 'LAR1',],
		'gcnet_lar2': [67.57638, -63.25750, 'LAR2',],
		'gcnet_lar3': [67.03166, -62.65027, 'LAR3',],

		'promice_egp': [75.6247, -35.9748, 'EGP'],
		'promice_kanb': [67.1252, -50.1832, 'KAN_B'],
		'promice_kanl': [67.0955, -49.9513, 'KAN_L'],
		'promice_kanm': [67.0670, -48.8355, 'KAN_M'],
		'promice_kanu': [67.0003, -47.0253, 'KAN_U'],
		'promice_kpcl': [79.9108, -24.0828, 'KPC_L'],
		'promice_kpcu': [79.8347, -25.1662, 'KPC_U'],
		'promice_mit': [65.6922, -37.8280, 'MIT'],
		'promice_nukk': [64.1623, -51.3587, 'NUK_K'],
		'promice_nukl': [64.4822, -49.5358, 'NUK_L'],
		'promice_nukn': [64.9452, -49.8850, 'NUK_N'],
		'promice_nuku': [64.5108, -49.2692, 'NUK_U'],
		'promice_qasa': [61.2430, -46.7328, 'QAS_A'],
		'promice_qasl': [61.0308, -46.8493, 'QAS_L'],
		'promice_qasm': [61.0998, -46.8330, 'QAS_M'],
		'promice_qasu': [61.1753, -46.8195, 'QAS_U'],
		'promice_scol': [72.2230, -26.8182, 'SCO_L'],
		'promice_scou': [72.3933, -27.2333, 'SCO_U'],
		'promice_tasa': [65.7790, -38.8995, 'TAS_A'],
		'promice_tasl': [65.6402, -38.8987, 'TAS_L'],
		'promice_tasu': [65.6978, -38.8668, 'TAS_U'],
		'promice_thul': [76.3998, -68.2665, 'THU_L'],
		'promice_thuu': [76.4197, -68.1463, 'THU_U'],
		'promice_upel': [72.8932, -54.2955, 'UPE_L'],
		'promice_upeu': [72.8878, -53.5783, 'UPE_U'],
		'promice_cen': [0, 0, 'CEN'],

		'AGO-4': [-82.010, 96.760],
		'Alexander Tall Tower!': [-79.012, 170.723],
		'Austin': [-75.995, -87.470],
		'Baldrick': [-82.774, -13.054],
		'Bear Peninsula': [-74.546, -111.885],
		'Bonaparte Point': [-64.778, -64.067],
		'Byrd': [-80.011, -119.438],
		'Cape Bird': [-77.217, 166.439],
		'Cape Denison': [-67.009, 142.664],
		'Cape Hallett': [-72.190, 170.160],
		'D-10': [-66.705, 139.841],
		'D-47': [-67.385, 138.729],
		'D-85': [-70.426, 134.149],
		'Dismal Island': [-68.088, -68.826],
		'Dome C II': [-75.106, 123.346],
		'Dome Fuji': [-77.310, 39.700],
		'Elaine': [-83.094, 174.285],
		'Elizabeth': [-82.607, -137.078],
		'Emilia': [-78.426, 173.186],
		'Emma': [-83.997, -175.047],
		'Erin': [-84.902, -128.860],
		'Evans Knoll': [-74.850, -100.404],
		'Ferrell': [-77.803, 170.817],
		'Gill': [-79.879, -178.565],
		'Harry': [-83.005, -121.407],
		'Henry': [-89.001, -0.391],
		'Janet': [-77.174, -123.390],
		'JASE2007': [-75.888, 25.834],
		'Kathie': [-77.995, -97.268],
		'Kominko-Slade': [-79.466, -112.106],
		'Laurie II': [-77.439, 170.750],
		'Lettau': [-82.475, -174.587],
		'Linda': [-78.394, 168.446],
		'Lorne': [-78.195, 170.028],
		'Manuela': [-74.946, 163.687],
		'Marble Point': [-77.439, 163.754],
		'Marble Point II': [-77.439, 163.759],
		'Margaret': [-79.981, -165.099],
		'Marilyn': [-79.913, 165.657],
		'Minna Bluff': [-78.555, 166.691],
		'Mizuho': [-70.700, 44.290],
		'Mount Siple': [-73.198, -127.052],
		'Nico': [-89.000, 90.024],
		'PANDA-South': [-82.325, 75.989],
		'Pegasus North': [-77.957, 166.515],
		'Phoenix': [-77.948, 166.758],
		'Port Martin': [-66.820, 141.390],
		'Possession Island': [-71.891, 171.210],
		'Relay Station': [-74.017, 43.062],
		'Sabrina': [-84.247, -170.068],
		'Schwerdtfeger': [-79.816, 170.358],
		'Siple Dome': [-81.652, -148.992],
		'Theresa': [-84.602, -115.841],
		'Thurston Island': [-72.532, -97.545],
		'Vito': [-78.408, 177.829],
		'White Island': [-78.076, 167.451],
		'Whitlock': [-76.142, 168.394],
		'Willie Field': [-77.868, 166.921],
		'Windless Bight': [-77.728, 167.676]

	}

	order_of_keys = ['blank', 'gcnet_swiss', 'gcnet_crawford', 'gcnet_nasa-u', 'gcnet_gits', 'gcnet_humboldt', 'gcnet_summit', 'gcnet_tunu-n', 'gcnet_dye2', 'gcnet_jar', 
	'gcnet_saddle', 'gcnet_dome', 'gcnet_nasa-e', 'gcnet_cp2', 'gcnet_ngrip', 'gcnet_nasa-se', 'gcnet_kar', 'gcnet_jar2', 'gcnet_kulu', 'gcnet_jar3', 'gcnet_aurora', 
	'gcnet_petermann-gl', 'gcnet_peterman-ela', 'gcnet_neem', 'gcnet_lar1', 'gcnet_lar2', 'gcnet_lar3', 
	'promice_egp', 'promice_kanb', 'promice_kanl', 'promice_kanm', 'promice_kanu', 'promice_kpcl', 'promice_kpcu', 'promice_mit', 'promice_nukk', 'promice_nukl', 
	'promice_nukn', 'promice_nuku', 'promice_qasa', 'promice_qasl', 'promice_qasm', 'promice_qasu', 'promice_scol', 'promice_scou', 'promice_tasa', 'promice_tasl', 
	'promice_tasu', 'promice_thul', 'promice_thuu', 'promice_upel', 'promice_upeu', 'promice_cen', 
	'AGO-4', 'Alexander Tall Tower!', 'Austin', 'Baldrick', 'Bear Peninsula', 'Bonaparte Point', 'Byrd', 'Cape Bird', 'Cape Denison', 'Cape Hallett', 'D-10', 'D-47', 'D-85', 
	'Dismal Island', 'Dome C II', 'Dome Fuji', 'Elaine', 'Elizabeth', 'Emilia', 'Emma', 'Erin', 'Evans Knoll', 'Ferrell', 'Gill', 'Harry', 'Henry', 'Janet', 'JASE2007', 
	'Kathie', 'Kominko-Slade', 'Laurie II', 'Lettau', 'Linda', 'Lorne', 'Manuela', 'Marble Point', 'Marble Point II', 'Margaret', 'Marilyn', 'Minna Bluff', 'Mizuho', 
	'Mount Siple', 'Nico', 'PANDA-South', 'Pegasus North', 'Phoenix', 'Port Martin', 'Possession Island', 'Relay Station', 'Sabrina', 'Schwerdtfeger', 'Siple Dome', 
	'Theresa', 'Thurston Island', 'Vito', 'White Island', 'Whitlock', 'Willie Field', 'Windless Bight']

	list_of_tuples = [(key, station_dict[key]) for key in order_of_keys]
	station_dict = OrderedDict(list_of_tuples)

	# NC file setup
	if (args.output_file or args.fl_out):
		op_file = str(args.output_file or args.fl_out)

	else:
		get_name = str((os.path.basename(args.input_file or args.fl_in)).split('.')[0])
		
		try: 
			get_name_int = int(get_name[:2])
			if get_name_int > 0 and get_name_int < 24:
				op_file = list(station_dict.keys())[get_name_int] + '.nc'
			elif get_name == '30c':
				op_file = list(station_dict.keys())[24] + '.nc' 
			elif get_name == '31c':
				op_file = list(station_dict.keys())[25] + '.nc' 
			elif get_name == '32c':
				op_file = list(station_dict.keys())[26] + '.nc'
			else:
				op_file = get_name + '.nc'
		except:
			op_file = get_name + '.nc'
	
	
	if args.station_name:
		station_name = args.station_name
	else:
		station_name = ''


	######################################################################

	with open(str(args.input_file or args.fl_in),'r') as f:
		line = f.readline()

	if line[0] == 'D':
		gcnet2nc.gcnet2nc(args, op_file, station_dict, station_name)

	elif line[0] == 'Y':
		promice2nc.promice2nc(args, op_file, station_dict, station_name)

	elif line[0] == '#':
		aaws2nc.aaws2nc(args, op_file, station_dict, station_name)

	######################################################################
	if args.dbg_lvl > 0:
		print('Elapsed time: {}'.format(datetime.now()-start_time))

	if args.dbg_lvl > 1:
		print("Converted " + str(os.path.basename(args.input_file or args.fl_in)) + " to {}".format(op_file))


if __name__ == '__main__':
    Main()
