import argparse
import gcnet2nc
import promice2nc
import aaws2nc

def Main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="The PROMICE file you wish to convert to netCDF.", type=str)
    parser.add_argument("-o", "--output", help="Path where you want to store the output file", type=str)
    parser.add_argument("-f", "-format", help="netCDF format in which you want to store. Option '3' = NETCDF3_CLASSIC, '4' = NETCDF4, '5' = NETCDF3_64BIT_DATA, '6' = NETCDF3_64BIT_OFFSET, '7' = NETCDF4_CLASSIC", 
    	type=int)

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
