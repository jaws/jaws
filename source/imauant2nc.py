from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import xarray as xr

import common
from sunposition import sunpos

def get_fillvalue(args):
	if args.fll_val_flt:
		return args.fll_val_flt
	return common.fillvalue_float


def init_dataframe(args, input_file):
	check_na = -9999

	df = common.load_dataframe('imauant', input_file, 0)
	df.index.name = 'time'
	df.replace(check_na, np.nan, inplace=True)

	temperature_keys = [
		'temp_cnr1', 'air_temp', 
		'snow_temp_1a', 'snow_temp_2a', 'snow_temp_3a', 'snow_temp_4a', 'snow_temp_5a',
		'snow_temp_1b', 'snow_temp_2b', 'snow_temp_3b', 'snow_temp_4b', 'snow_temp_5b',
		'temp_logger']
	df.loc[:, temperature_keys] += common.freezing_point_temp
	df.loc[:, 'air_pressure'] *= common.pascal_per_millibar
	df = df.where((pd.notnull(df)), get_fillvalue(args))

	return df

def imauant2nc(args, input_file, output_file, stations):
	df = init_dataframe(args, input_file)
	ds = xr.Dataset.from_dataframe(df)
	ds = ds.drop('time')

	comp_level = args.dfl_lvl
	
	common.load_dataset_attributes('imauant', ds)
	encoding = common.get_encoding('imauant', get_fillvalue(args), comp_level)

	common.write_data(args, ds, output_file, encoding)
