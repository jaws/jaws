import argparse
import gcnet2nc
import promice2nc

def Main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="The PROMICE file you wish to convert to netCDF.", type=str)
    parser.add_argument("row_count", help="Total number of rows in your dataset", type=int)
    parser.add_argument("-o", "--output", help="Path where you want to store the output file", type=str)

    global args
    
    args = parser.parse_args()

    with open(str(args.input),'r') as f:
    	line = f.readline()


    if line[0] == 'D': 
    	gcnet2nc.gcnet2nc(args.input)

    elif line[0] == 'Y':
    	promice2nc.promice2nc(args.input)
    
    print "The file " + str(args.input) + " is converted into netCDF format and is saved at " + op_file


if __name__ == '__main__':
    Main()


