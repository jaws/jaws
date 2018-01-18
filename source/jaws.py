import argparse
import gcnet2nc
import promice2nc
import aaws2nc

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
    #parser.add_argument("-f", "--format", help="netCDF format in which you want to store. Option '3' = NETCDF3_CLASSIC, '4' = NETCDF4, '5' = NETCDF3_64BIT_DATA, '6' = NETCDF3_64BIT_OFFSET, '7' = NETCDF4_CLASSIC", type=int)

    args = parser.parse_args()

    with open(str(args.input),'r') as f:
    	line = f.readline()


    if line[0] == 'D': 
    	gcnet2nc.gcnet2nc(args)

    elif line[0] == 'Y':
    	promice2nc.promice2nc(args)
    
    elif line[0] == '#':
    	aaws2nc.aaws2nc(args)
    
    print "The file " + str(args.input) + " is converted into netCDF format."


if __name__ == '__main__':
    Main()
