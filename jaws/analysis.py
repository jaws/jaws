import xarray
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import argparse
import sys

def setup(args):
	mpl.rc('figure', figsize = (15, 10))
	mpl.rc('font', size = 12)
	mpl.rc('axes.spines', top = False, right = False)
	mpl.rc('axes', grid = False)
	mpl.rc('axes', facecolor = 'white')

	global ds, df
	ds = xarray.open_dataset(args.input)
	df = ds.to_dataframe()

	if args.anl_yr:
		df = df[df.year == args.anl_yr]
	if args.anl_mth:
		df = df[df.month == args.anl_mth]

	if df.size == 0:
		print('ERROR: Provide a valid year and month')
		sys.exit(1)

	global year
	year = df['year']

	#df[args.var].replace([999.00], [245], inplace=True)

	global month, days

	df['month_derived'] = df['month'].astype(str)
	month = df['month_derived']
	if month[0][0] == '1':
		month[0][0] = 'Jan'
		days = range(1,32)
	elif month[0][0] == '2':
		month[0][0] = 'Feb'
		days = range(1,29)
	elif month[0][0] == '3':
		month[0][0] = 'Mar'
		days = range(1,32)
	elif month[0][0] == '4':
		month[0][0] = 'Apr'
		days = range(1,31)
	elif month[0][0] == '5':
		month[0][0] = 'May'
		days = range(1,32)
	elif month[0][0] == '6':
		month[0][0] = 'Jun'
		days = range(1,31)
	elif month[0][0] == '7':
		month[0][0] = 'Jul'
		days = range(1,32)
	elif month[0][0] == '8':
		month[0][0] = 'Aug'
		days = range(1,32)
	elif month[0][0] == '9':
		month[0][0] = 'Sep'
		days = range(1,31)
	elif month[0][0] == '10':
		month[0][0] = 'Oct'
		days = range(1,32)
	elif month[0][0] == '11':
		month[0][0] = 'Nov'
		days = range(1,31)
	elif month[0][0] == '12':
		month[0][0] = 'Dec'
		days = range(1,32)


	global hours, days_year, months

	hours = range(0,24)

	if year[0][0]%4 == 0:
		days_year = range(1,367)
	else:
		days_year = range(1,366)

	months = range(1,13)


def check_error(var_x, var_y):
	if len(var_x) != len(var_y):
		if var_y == hours:
			print('ERROR: Provide data for each hour of the day')
		elif var_y == days:
			print('ERROR: Provide data for each day of the month')
		elif var_y == days_year:
			print('ERROR: Provide data for each day of the year')
		elif var_y == months:
			print('ERROR: Provide data for all the months')
		
		sys.exit(1)


def diurnal(args):
	global var_hour_avg, var_hour_sd
	
	hour = df['hour']
	var_hour_avg = df[args.var].groupby(hour).mean()
	var_hour_sd = df[args.var].groupby(hour).std()

	check_error(var_hour_avg, hours)

	return var_hour_avg, var_hour_sd, hours


def monthly(args):
	global var_day_avg, var_day_max, var_day_min
	
	day = df['day']
	var_day_avg = df[args.var].groupby(day).mean()
	var_day_max = df[args.var].groupby(day).max()
	var_day_min = df[args.var].groupby(day).min()

	check_error(var_day_avg, days)

	return var_day_avg, var_day_max, var_day_min


def annual(args):
	global var_doy_avg, var_doy_max, var_doy_min
	
	try:
		df['day_of_year'] = df['julian_decimal_time'].astype(int)	#GCNet
		doy = df['day_of_year']
	except:
		doy = df['day_of_year']
	var_doy_avg = df[args.var].groupby(doy).mean()
	var_doy_max = df[args.var].groupby(doy).max()
	var_doy_min = df[args.var].groupby(doy).min()

	check_error(var_doy_avg, days_year)

	return var_doy_avg, var_doy_max, var_doy_min, days_year


def seasonal(args):
	global var_month_avg, var_month_sd

	month = df['month']
	var_month_avg = df[args.var].groupby(month).mean()
	var_month_sd = df[args.var].groupby(month).std()

	check_error(var_month_avg, months)

	return var_month_avg, var_month_sd, months


def main(args):
	setup(args)
	
	if args.plot == 'diurnal':
		diurnal(args)
		plt.errorbar(hours, var_hour_avg, yerr = var_hour_sd, fmt='--o', ecolor='lightskyblue', color='k')
		plt.xticks(hours)
		plt.xlabel('Hour of the day')
		plt.title('Diurnal cycle at {} for {}-{}'.format(df.station_name[0][0], month[0][0], year[0][0]))

	elif args.plot == 'monthly':
		monthly(args)
		plt.plot(days,var_day_avg, label='mean', color ='black')
		plt.fill_between(days,var_day_max, var_day_min, label='max-min', facecolor='darkseagreen', alpha=0.3)
		plt.xticks(days)
		plt.xlabel('Day of month')
		plt.title('Temperature at {} for {}-{}'.format(df.station_name[0][0], month[0][0], year[0][0]))

	elif args.plot == 'annual':
		annual(args)
		plt.plot(days_year,var_doy_avg, label='mean', color ='black')
		#plt.fill_between(days_year,var_doy_max, var_doy_min, label='max-min', facecolor='green', alpha=0.3)
		plt.plot(days_year,var_doy_max, label='max', color = 'darkseagreen')
		plt.plot(days_year,var_doy_min, label='min', color = 'lightskyblue')
		plt.xlabel('Day of year')
		plt.title('Temperature at {} for {}'.format(df.station_name[0][0], year[0][0]))

	elif args.plot == 'seasonal':
		seasonal(args)
		plt.errorbar(months, var_month_avg, yerr = var_month_sd, fmt='--o', ecolor= 'lightskyblue', color='k')
		plt.xticks(months)
		plt.xlabel('Month')
		plt.title('Climatological seasonal cycle at {}'.format(df.station_name[0][0]))


	plt.legend(loc='best', fancybox=True, framealpha=0.3)
	plt.ylabel('{} [{}]'.format(ds[args.var].long_name, ds[args.var].units))

	plt.show()