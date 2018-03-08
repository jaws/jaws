import unittest
import tempfile
import netCDF4
import os.path
import os

import subprocess


def convert(infile, *args):
    """
    Convert sample file.

    This is a helper function used by other tests. It takes in a filename
    and any command line arguments, and uses them to run jaws.py.

    It then reads the output data and returns it as an netCDF4 object.
    """
    # change the current working directory
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    
    # check that the input file exists
    if not os.path.isfile(infile):
        raise FileNotFoundError

    # make a temporary output file
    outfile = tempfile.NamedTemporaryFile(suffix='.nc', delete=True)

    # generate command line arguments for jaws
    jawargs = [infile, outfile.name] + list(args)

    # run the jaws command
    subprocess.call(['python', '../source/jaws.py'] + jawargs)

    # read the result of the call.
    # if the file was malformed or not converted correctly
    # this will rise an error and the test will fail.
    with open(outfile.name, 'rb') as stream:
        if not stream.read():
            raise RuntimeError('Output File is Empty')

    return netCDF4.Dataset(outfile.name)


class TestJaws(unittest.TestCase):
    """
    Test jaws.py

    This class contains methods used for testing the application itself,
    separate from individual format converters. At this time, this mostly
    consists of testing various command line options and if they work correctly.
    """

    def test_format3(self):
        """Test that --format3 option works correctly."""
        nc = convert('../sample_data/AAWS_AGO-4_20161130.txt', '-3')
        self.assertEqual(nc.file_format, 'NETCDF3_CLASSIC')

    def test_format4(self):
        """Test that --format4 option works correctly."""
        nc = convert('../samples/AAWS_AGO-4_20161130.txt', '-4')
        self.assertEqual(nc.file_format, 'NETCDF4')

    def test_format5(self):
        """Test that --format5 option works correctly."""
        nc = convert('../samples/AAWS_AGO-4_20161130.txt', '-5')
        self.assertEqual(nc.file_format, 'NETCDF3_64BIT_OFFSET')

    def test_station_name(self):
        """Test overriding default station name."""
        nc = convert('../samples/AAWS_AGO-4_20161130.txt', '-s', 'TestStation')
        station = nc.variables['station_name'].getValue()
        self.assertEqual(station, 'TestStation')


