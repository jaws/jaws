import xarray
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import argparse
import datetime

mpl.rc('figure', figsize = (14, 7))
mpl.rc('font', size = 14)
mpl.rc('axes.spines', top = False, right = False)
mpl.rc('axes', grid = False)
mpl.rc('axes', facecolor = 'white')

parser = argparse.ArgumentParser()
parser.add_argument("input", help="The PROMICE file you wish to convert to netCDF.", type=str)
parser.add_argument('var', help = 'variable you want to analyse', type = str)
args = parser.parse_args()

ds = xarray.open_dataset(args.input)
df = ds.to_dataframe()

month = df['month']

df['temperature_tc_1'].replace([999.00], [245], inplace=True)
var_day_avg = df[args.var].groupby(month).mean()
var_day_sd = df[args.var].groupby(month).std()

months_choices = []
for i in range(1,13):
    months_choices.append(datetime.date(2008, i, 1).strftime('%b'))

months = range(1,13)

plt.errorbar(months, var_day_avg, yerr = var_day_sd, fmt='--o', ecolor= 'lightskyblue', color='k', capthick=5, snap=True)
plt.legend(loc='best', fancybox=True, framealpha=0.3)
plt.xticks(months)
plt.xlabel('Month')
plt.ylabel('Temperature [Kelvin]')
plt.title("Climatological seasonal cycle at Summit")

plt.show()