import argparse
import gcnet2nc
import promice2nc
import aaws2nc
import os
from netcdf4 import Dataset

def Main():
	parser = argparse.ArgumentParser()
	parser.add_argument("input", help="The PROMICE file you wish to convert to netCDF.", type=str)
	parser.add_argument("-o", "--output", "--fl_out", help="Path where you want to store the output file", type=str)
	parser.add_argument("-3", "--format3", "--3", "--fl_fmt=classic", help="NETCDF3_CLASSIC", action="store_true")
	parser.add_argument("-4", "--format4", "--4", "--netcdf4", "--fl_fmt=netcdf4", help="NETCDF4", action="store_true")
	parser.add_argument("-5", "--format5", "--5", "--64bit_data", "--fl_fmt=64bit_data", "--fl_fmt=cdf5", help="NETCDF3_64BIT_DATA", action="store_true")
	parser.add_argument("-6", "--format6", "--6", "--64bit_offset", "--fl_fmt=64bit_offset", help="NETCDF3_64BIT_OFFSET", action="store_true")
	parser.add_argument("-7", "--format7", "--7", "--fl_fmt=netcdf4_classic", help="NETCDF4_CLASSIC", action="store_true")
	parser.add_argument("-s","--station_name", help = "name of station if you want to change")

	args = parser.parse_args()

	######################################################################

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
	
	######################################################################

	with open(str(args.input),'r') as f:
		line = f.readline()

	if line[0] == 'D':
		gcnet2nc.gcnet2nc(args, op_file, root_grp)

	elif line[0] == 'Y':
		promice2nc.promice2nc(args, op_file, root_grp)

	elif line[0] == '#':
		aaws2nc.aaws2nc(args, op_file, root_grp)

	print("Converted " + str(os.path.basename(args.input)) + " to netCDF format")


if __name__ == '__main__':
    Main()
