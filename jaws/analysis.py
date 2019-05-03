from calendar import monthrange, month_abbr
import sys

import matplotlib as mpl
import matplotlib.pyplot as plt
import xarray


def setup(df):
    mpl.rc('figure', figsize=(18, 12))
    mpl.rc('font', size=24)
    mpl.rc('axes.spines', top=True, right=True)
    mpl.rc('axes', grid=False)
    mpl.rc('axes', facecolor='white')

    global year
    year = df['year']

    # df[args.var].replace([999.00], [245], inplace=True)

    global days_year, months

    if year[0] % 4 == 0:
        days_year = range(1, 367)
    else:
        days_year = range(1, 366)

    months = range(1, 13)


def check_error(var_x, var_y, args):
    if len(var_x) != len(var_y):
        if var_y == range(0, 24):
            print('ERROR: Provide data for each hour of the day')
        elif var_y == monthrange(args.anl_yr, args.anl_mth)[1]:
            print('ERROR: Provide data for each day of the month')
        elif var_y == days_year:
            print('ERROR: Provide data for each day of the year')
        elif var_y == months:
            print('ERROR: Provide data for all the months')

        sys.exit(1)


def diurnal(args, df):
    hour = df['hour']
    var_hour_avg = df[args.var].groupby(hour).mean()
    var_hour_sd = df[args.var].groupby(hour).std()

    hours = range(0, 24)
    check_error(var_hour_avg, hours)

    return var_hour_avg, var_hour_sd, hours


def monthly(args, df):
    day = df['day']
    var_day_avg = df[args.var].groupby(day).mean()
    var_day_max = df[args.var].groupby(day).max()
    var_day_min = df[args.var].groupby(day).min()

    days = range(0, monthrange(args.anl_yr, args.anl_mth)[1])
    check_error(var_day_avg, days, args)

    return var_day_avg, var_day_max, var_day_min, days


def annual(args, df):
    global var_doy_avg, var_doy_max, var_doy_min

    try:
        df['day_of_year'] = df['julian_decimal_time'].astype(int)  # GCNet
        doy = df['day_of_year']
    except:
        doy = df['day_of_year']
    var_doy_avg = df[args.var].groupby(doy).mean()
    var_doy_max = df[args.var].groupby(doy).max()
    var_doy_min = df[args.var].groupby(doy).min()

    check_error(var_doy_avg, days_year)

    return var_doy_avg, var_doy_max, var_doy_min, days_year


def seasonal(args, df):
    global var_month_avg, var_month_sd

    month = df['month']
    var_month_avg = df[args.var].groupby(month).mean()
    var_month_sd = df[args.var].groupby(month).std()

    check_error(var_month_avg, months)

    return var_month_avg, var_month_sd, months


def main(args):

    if not args.var:
        print('ERROR: Please provide variable name to analyze')
        sys.exit(1)

    ds = xarray.open_dataset(args.input_file)
    ds = ds.drop('time_bounds')
    df = ds.to_dataframe()

    stn_nm = df.station_name[0]

    if args.anl_yr:
        df = df[df.year == args.anl_yr]
        year = args.anl_yr
    if args.anl_mth:
        df = df[df.month == args.anl_mth]
        month = args.anl_mth

    if df.size == 0:
        print('ERROR: Provide a valid year and month')
        sys.exit(1)

    setup(df)

    if args.anl == 'diurnal':
        var_hour_avg, var_hour_sd, hours = diurnal(args, df)
        plt.errorbar(hours, var_hour_avg, yerr=var_hour_sd, fmt='--o', ecolor='lightskyblue', color='k')
        plt.xticks(hours)
        plt.xlabel('Hour of the day')
        if len(df.day) == 24:
            plt.title('Diurnal cycle at {} for {}-{}-{}'.format(df.station_name[0], df.day[0], month[0], year[0]))
        else:
            plt.title('Diurnal cycle at {} for {}-{}'.format(df.station_name[0], month[0], year[0]))

    elif args.anl == 'monthly':
        var_day_avg, var_day_max, var_day_min, days = monthly(args, df)
        plt.plot(days, var_day_avg, label='mean', color='black')
        plt.fill_between(days, var_day_max, var_day_min, label='max-min', facecolor='darkseagreen', alpha=0.3)
        plt.xticks(days)
        plt.xlabel('Day of month')
        plt.title('Temperature at {} for {}-{}'.format(stn_nm, month_abbr[month], year))

    elif args.anl == 'annual':
        annual(args, df)
        plt.plot(days_year, var_doy_avg, label='mean', color ='black')
        # plt.fill_between(days_year, var_doy_max, var_doy_min, label='max-min', facecolor='green', alpha=0.3)
        plt.plot(days_year, var_doy_max, label='max', color='darkseagreen')
        plt.plot(days_year, var_doy_min, label='min', color='lightskyblue')
        plt.xlabel('Day of year')
        plt.title('Temperature at {} for {}'.format(df.station_name[0], year[0]))

    elif args.anl == 'seasonal':
        seasonal(args, df)
        plt.errorbar(months, var_month_avg, yerr=var_month_sd, fmt='--o', ecolor='lightskyblue', color='k')
        plt.xticks(months)
        plt.xlabel('Month')
        plt.title('Climatological seasonal cycle at {}'.format(df.station_name[0]))

    else:
        print("ERROR: Please choose a valid argument for analysis from ['diurnal', 'monthly', 'annual', 'seasonal']")
        sys.exit(1)

    plt.legend(loc='best', fancybox=True, framealpha=0.3)
    plt.ylabel('{} [{}]'.format(ds[args.var].long_name, ds[args.var].units))

    plt.show()
