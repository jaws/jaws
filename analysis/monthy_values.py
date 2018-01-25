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
parser.add_argument('-y', '--year', help = 'Year you want to select', type = int)
parser.add_argument('-m', '--month', help = 'Month you want to select', type = int)
parser.add_argument('var', help = 'variable you want to analyse', type = str)
args = parser.parse_args()

ds = xarray.open_dataset(args.input)
df = ds.to_dataframe()

if args.year:
    df = df[df.year == args.year]
if args.month:
    df = df[df.month == args.month]

day = df['day']
year = df['year']

df['temperature_tc_1'].replace([999.00], [245], inplace=True)

temp_day_avg = df[args.var].groupby(day).mean()
temp_day_max = df[args.var].groupby(day).max()
temp_day_min = df[args.var].groupby(day).min()

days = range(1,29)

df['month'] = df['month'].astype(str)
month = df['month']
if month[0][0][0] == '1':
    month[0][0][0] = 'Jan'
    days = range(1,32)
elif month[0][0][0] == '2':
    month[0][0][0] = 'Feb'
    days = range(1,29)
elif month[0][0][0] == '3':
    month[0][0][0] = 'Mar'
    days = range(1,32)
elif month[0][0][0] == '4':
    month[0][0][0] = 'Apr'
    days = range(1,31)
elif month[0][0][0] == '5':
    month[0][0][0] = 'May'
    days = range(1,32)
elif month[0][0][0] == '6':
    month[0][0][0] = 'Jun'
    days = range(1,31)
elif month[0][0][0] == '7':
    month[0][0][0] = 'Jul'
    days = range(1,32)
elif month[0][0][0] == '8':
    month[0][0][0] = 'Aug'
    days = range(1,32)
elif month[0][0][0] == '9':
    month[0][0][0] = 'Sep'
    days = range(1,31)
elif month[0][0][0] == '10':
    month[0][0][0] = 'Oct'
    days = range(1,32)
elif month[0][0][0] == '11':
    month[0][0][0] = 'Nov'
    days = range(1,31)
elif month[0][0][0] == '12':
    month[0][0][0] = 'Dec'
    days = range(1,32)


plt.plot(days,temp_day_avg, label='mean', color ='black')
plt.fill_between(days,temp_day_max, temp_day_min, label='max-min', facecolor='darkseagreen', alpha=0.3)
#plt.plot(days,temp_day_max, label='max', color = 'darkseagreen')
#plt.plot(days,temp_day_min, label='min', color = 'lightskyblue')
plt.legend(loc='best', fancybox=True, framealpha=0.4)
plt.xticks(days)
plt.xlabel('Day of month')
plt.ylabel('Temperature [Kelvin]')
plt.title('Temperature at Summit for {}-{}'.format(month[0][0][0],year[0][0][0]))

plt.show()


