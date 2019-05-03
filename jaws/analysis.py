from calendar import monthrange, month_abbr, isleap
import sys

import matplotlib as mpl
import matplotlib.pyplot as plt
import xarray


def plot_setup():
    mpl.rc('figure', figsize=(18, 12))
    mpl.rc('font', size=24)
    mpl.rc('axes.spines', top=True, right=True)
    mpl.rc('axes', grid=False)
    mpl.rc('axes', facecolor='white')


def diurnal(args, df):
    hour = df['hour']
    var_hour_avg = df[args.var].groupby(hour).mean()
    var_hour_sd = df[args.var].groupby(hour).std()

    hours = range(0, 24)
    if len(var_hour_avg) != len(hours):
        print('ERROR: Provide data for each hour of the day')
        sys.exit(1)

    return var_hour_avg, var_hour_sd, hours


def monthly(args, df):
    day = df['day']
    var_day_avg = df[args.var].groupby(day).mean()
    var_day_max = df[args.var].groupby(day).max()
    var_day_min = df[args.var].groupby(day).min()

    days = range(0, monthrange(args.anl_yr, args.anl_mth)[1])
    if len(var_day_avg) != len(days):
        print('ERROR: Provide data for each day of the month')
        sys.exit(1)

    return var_day_avg, var_day_max, var_day_min, days


def annual(args, df):
    try:
        df['day_of_year'] = df['julian_decimal_time'].astype(int)  # GCNet
        doy = df['day_of_year']
    except:
        doy = df['day_of_year']
    var_doy_avg = df[args.var].groupby(doy).mean()
    var_doy_max = df[args.var].groupby(doy).max()
    var_doy_min = df[args.var].groupby(doy).min()

    days_year = range(1, 367) if isleap(args.anl_yr) else range(1, 366)
    if len(var_doy_avg) != len(days_year):
        print('ERROR: Provide data for each day of the year')
        sys.exit(1)

    return var_doy_avg, var_doy_max, var_doy_min, days_year


def seasonal(args, df):
    month = df['month']
    var_month_avg = df[args.var].groupby(month).mean()
    var_month_sd = df[args.var].groupby(month).std()

    months = range(1, 13)
    if len(var_month_avg) != len(months):
        print('ERROR: Provide data for all the months')
        sys.exit(1)

    return var_month_avg, var_month_sd, months


def main(args):

    if not args.var:
        print('ERROR: Please provide variable name to analyze')
        sys.exit(1)

    ds = xarray.open_dataset(args.input_file)
    ds = ds.drop('time_bounds')
    df = ds.to_dataframe()

    stn_nm = df.station_name[0]

    if len(df.day) == 24:
        if args.anl != 'diurnal':
            print('ERROR: This is a single day file and you can only run diurnal analysis on it')
            sys.exit(1)
    else:
        if not args.anl_yr and args.anl in ['diurnal', 'monthly', 'annual']:
            print('ERROR: Provide a year using --anl_yr argument to do the analysis')
            sys.exit(1)
        if not args.anl_mth and args.anl in ['diurnal', 'monthly']:
            print('ERROR: Provide a month using --anl_mth argument to do the analysis')
            sys.exit(1)

    if args.anl_yr:
        df = df[df.year == args.anl_yr]
        year = args.anl_yr
    if args.anl_mth:
        df = df[df.month == args.anl_mth]
        month = args.anl_mth

    if df.size == 0:
        print('ERROR: Provide a valid year and month')
        sys.exit(1)

    plot_setup()

    if args.anl == 'diurnal':
        var_hour_avg, var_hour_sd, hours = diurnal(args, df)
        if len(df.day) == 24:
            plt.plot(hours, var_hour_avg, '--', marker='.', markersize=15, color='k')
            plt.title('Diurnal cycle at {} for {}-{}-{}'.format(stn_nm, df.day[0], month_abbr[df.month[0]], df.year[0]))
        else:
            plt.errorbar(hours, var_hour_avg, yerr=var_hour_sd, fmt='--o', ecolor='lightskyblue', color='k')
            plt.title('Diurnal cycle at {} for {}-{}'.format(stn_nm, month_abbr[month], year))
        plt.xticks(hours)
        plt.xlabel('Hour of the day')

    elif args.anl == 'monthly':
        var_day_avg, var_day_max, var_day_min, days = monthly(args, df)
        plt.plot(days, var_day_avg, label='mean', color='black')
        plt.fill_between(days, var_day_max, var_day_min, label='max-min', facecolor='darkseagreen', alpha=0.3)
        plt.xticks(days)
        plt.xlabel('Day of month')
        plt.title('Temperature at {} for {}-{}'.format(stn_nm, month_abbr[month], year))

    elif args.anl == 'annual':
        var_doy_avg, var_doy_max, var_doy_min, days_year = annual(args, df)
        plt.plot(days_year, var_doy_avg, label='mean', color ='black')
        # plt.fill_between(days_year, var_doy_max, var_doy_min, label='max-min', facecolor='green', alpha=0.3)
        plt.plot(days_year, var_doy_max, label='max', color='darkseagreen')
        plt.plot(days_year, var_doy_min, label='min', color='lightskyblue')
        plt.xlabel('Day of year')
        plt.title('Temperature at {} for {}'.format(stn_nm, year))

    elif args.anl == 'seasonal':
        var_month_avg, var_month_sd, months = seasonal(args, df)
        plt.errorbar(months, var_month_avg, yerr=var_month_sd, fmt='--o', ecolor='lightskyblue', color='k')
        plt.xticks(months)
        plt.xlabel('Month')
        plt.title('Climatological seasonal cycle at {}'.format(stn_nm))

    else:
        print("ERROR: Please choose a valid argument for analysis from ['diurnal', 'monthly', 'annual', 'seasonal']")
        sys.exit(1)

    plt.legend(loc='best', fancybox=True, framealpha=0.3)
    plt.ylabel('{} [{}]'.format(ds[args.var].long_name, ds[args.var].units))

    plt.show()
