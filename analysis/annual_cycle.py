import xarray
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import argparse

mpl.rc('figure', figsize = (15, 10))
mpl.rc('font', size = 12)
mpl.rc('axes.spines', top = False, right = False)
mpl.rc('axes', grid = False)
mpl.rc('axes', facecolor = 'white')


parser = argparse.ArgumentParser()
parser.add_argument("input", help="The PROMICE file you wish to convert to netCDF.", type=str)
parser.add_argument('year', help = 'Month you want to select', type = int)
parser.add_argument('var', help = 'variable you want to analyse', type = str)
args = parser.parse_args()

ds = xarray.open_dataset(args.input)
df = ds.to_dataframe()
df = df[df.year == args.year]

df['julian_decimal_time'] = df['julian_decimal_time'].astype(int)

year = df['year']
jdt = df['julian_decimal_time']

df['temperature_tc_1'].replace([999.00], [245], inplace=True)

var_day_avg = df[args.var].groupby(jdt).mean()
var_day_max = df[args.var].groupby(jdt).max()
var_day_min = df[args.var].groupby(jdt).min()

if year[0][0][0]%4 == 0:
	days = range(1,367)
else:
	days = range(1,366)

plt.plot(days,var_day_avg, label='mean', color ='black')
#plt.fill_between(days,var_day_max, var_day_min, label='max-min', facecolor='green', alpha=0.3)
plt.plot(days,var_day_max, label='max', color = 'darkseagreen')
plt.plot(days,var_day_min, label='min', color = 'lightskyblue')
plt.legend(loc='best')
plt.xlabel('Day of year')
plt.ylabel('Temperature [Kelvin]')
plt.title('Temperature at Summit for {}'.format(year[0][0][0]))

plt.show()