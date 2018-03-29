import unittest
import tempfile
import netCDF4
import os.path
import os

import sys
sys.path.append('../source/')
import jaws

import subprocess


def convert(infile, *args):
    """
    Convert sample file.

    This is a helper function used by other tests. It takes in a filename
    and any command line arguments, and uses them to run jaws.py.

    Returns the NamedTemporaryFile object containing the output.
    """
    # change the current working directory
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    
    # check that the input file exists
    if not os.path.isfile(infile):
        try:
            raise FileNotFoundError
        except NameError:  # python2
            raise IOError

    # make a temporary output file
    outfile = tempfile.NamedTemporaryFile(suffix='.nc', delete=False)

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

    return outfile


def convert_to_dataset(input_file, *args):
    """Converts the file and loads the results into a netCDF4 Dataset."""
    outfile = convert(input_file, *args)
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
        nc = convert_to_dataset('../sample_data/AAWS_AGO-4_20161130.txt', '-3')
        self.assertEqual(nc.file_format, 'NETCDF3_CLASSIC')

    def test_format4(self):
        """Test that --format4 option works correctly."""
        nc = convert_to_dataset('../sample_data/AAWS_AGO-4_20161130.txt', '-4')
        self.assertEqual(nc.file_format, 'NETCDF4')

    def test_format5(self):
        """Test that --format5 option works correctly."""
        nc = convert_to_dataset('../sample_data/AAWS_AGO-4_20161130.txt', '-5')
        self.assertEqual(nc.file_format, 'NETCDF3_64BIT_OFFSET')

    def test_station_name(self):
        """Test overriding default station name."""
        nc = convert_to_dataset('../sample_data/AAWS_AGO-4_20161130.txt', '-s', 'TestStation')
        station = nc.variables['station_name'][:]
        self.assertEqual(''.join(station), 'TestStation')

    def test_compression(self):
        """Test overriding default station name."""
        nc = convert_to_dataset('../sample_data/AAWS_AGO-4_20161130.txt', '-L', '5')
        self.assertTrue(nc)

    def test_all_options(self):
        """Test overriding default station name."""
        nc = convert_to_dataset('../sample_data/AAWS_AGO-4_20161130.txt', '-3', '-d', '-s', 'TestStation', '-t' ,'America/Los_Angeles', '-D', '1', '-L', '5')
        self.assertTrue(nc)


class TestInputOutputArguments(unittest.TestCase):
    """
    Test command line arguments for input and output files.

    Ensures that both positional and keyword notation is supported,
    and that the output file is constructed correctly if not explicitly
    specified.
    """
    def filetest(self, args, assert_input=None, assert_output=None):
        """Helper method that performs the specified assertions."""
        args = jaws.parse_args(list(args))
        input_file = jaws.get_input_file(args)
        if assert_input:
            self.assertEqual(input_file, assert_input)
        if assert_output:
            stations = jaws.get_stations()
            output_file = jaws.get_output_file(args, input_file, stations)
            self.assertEqual(output_file, assert_output)

    def test_input_positional(self):
        self.filetest(['test_input.txt'], assert_input='test_input.txt')

    def test_input_optional(self):
        self.filetest(['--input', 'test_input.txt'],
                      assert_input='test_input.txt')

    def test_output_positional(self):
        self.filetest(['test_input.txt', 'test_output.txt'],
                      assert_output='test_output.txt')

    def test_output_optional(self):
        self.filetest(['test_input.txt', '--fl_out', 'test_output.txt'],
                      assert_output='test_output.txt')

    def test_output_omitted_simple(self):
        """
        Test generation of omitted output file.

        In the simplest case, the output file has the same name as the
        input file, but with the extension changed to .nc.
        """
        self.filetest(['test_file.txt'], assert_output='test_file.nc')

    def test_output_omitted_numeral_1(self):
        """
        Test omitted output file with numeric-prefixed input file.

        If the input file is prefixed with number between 1 and 24,
        then the output file's name is taken from the station list.
        """
        self.filetest(['04_test_file.txt'], assert_output='gcnet_gits.nc')

    def test_output_omitted_numeral_2(self):
        self.filetest(['11_test_file.txt'], assert_output='gcnet_dome.nc')

    def test_output_omitted_c_suffix(self):
        self.filetest(['31c.txt'], assert_output='gcnet_lar2.nc')



class TestConverter(unittest.TestCase):
    """Parent class for Converter testers."""

    def check_output(self, input_file, output_sample):
        """
        Check that output matches known value.

        Converts input_file, and compares the results of the conversion to the
        contents of output_sample, which is a known good conversion of the
        input file.
        """
        output_file = convert(input_file)
        with open(output_file.name, 'rb') as stream:
            reference = stream.read()
        with open(output_file.name, 'rb') as stream:
            data = stream.read()
        self.assertEqual(data, reference)


class TestAAWS(TestConverter):
    """
    Test AAWS.

    This class test the correct conversion of the AAWS format. This involves
    converting multiple sample AAWS input files, and checking that the
    output values are what's expected.
    """

    def test_reference_sample(self):
        """
        Test the first sample input file.
        """
        self.check_output('../sample_data/AAWS_AGO-4_20161130.txt', '../sample_data/converted/AAWS_AGO-4_20161130.nc')


class TestGCNet(TestConverter):
    """
    Test GCNet.

    See the docstring for TestAAWS for details.
    """

    def test_reference_sample(self):
        """
        Test the first sample input file.
        """
        self.check_output('../sample_data/GCNET_Summit_20140601.txt', '../sample_data/converted/GCNET_Summit_20140601.nc')


class TestPROMICE(TestConverter):
    """
    Test PROMICE.

    See the docstring for TestAAWS for details.
    """

    def test_reference_sample(self):
        """
        Test the first sample input file.
        """
        self.check_output('../sample_data/PROMICE_EGP_20160501.txt', '../sample_data/converted/PROMICE_EGP_20160501.nc')


if __name__ == '__main__':
    unittest.main(verbosity=3)
