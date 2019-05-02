from datetime import datetime
import os
import requests

import numpy as np
import scipy.interpolate
import xarray as xr

try:
    from jaws import common
except ImportError:
    import common


def deg_to_rad(list_deg):
    """Convert degrees to radians"""
    list_rad = [np.radians(i) for i in list_deg]

    return list_rad


def first_order_derivative(tm, var):
    """Calculate slope of first order derivative"""
    dv = scipy.interpolate.interp1d(tm, var, fill_value='extrapolate')  # Interpolate missing values
    alpha = 0.01  # Step to left and right
    dv_left, dv_right = ([None] * len(tm) for _ in range(2))
    i = 0
    for hour in tm:
        dv_left[i] = float(dv(hour - alpha))
        dv_right[i] = float(dv(hour + alpha))
        i += 1
    slope = [(x1 - x2) / (2 * alpha) for (x1, x2) in zip(dv_right, dv_left)]
    return slope


def post_process(df, dates, stn_name, sfx, args):
    """Calculate fsus_adjusted and quality check for fsds_adjusted"""
    # Initialize new variables
    df['fsds_adjusted_new'] = np.float()
    df['fsus_adjusted'] = np.float()
    thrsh = 0.1  # Threshold
    outer_idx = 0

    for date in dates:
        year = date.year
        month = date.month
        day = date.day

        # Open downloaded ceres file as dataframe
        ceres_df = xr.open_dataset(stn_name + sfx).to_dataframe()
        # Get toa values for each day; dataframe index is date
        toa = ceres_df.loc[
             str(year)+'-'+str(month)+'-'+str(day):str(year)+'-'+str(month)+'-'+str(day)
             ][toa_incoming_shortwave_flux].values.tolist()

        # Subset dataframe for each day
        df_sub = df[df.dates == date]

        # Get fsds_adjusted and fsus values for that day and substitute NaN with fillvalue_float
        fsds_adjusted = df_sub['fsds_adjusted'].tolist()
        fsds_adjusted = [common.fillvalue_float if np.isnan(i) else i for i in fsds_adjusted]

        fsus_jaws = df_sub['fsus'].tolist()
        fsus_jaws = [common.fillvalue_float if np.isnan(i) else i for i in fsus_jaws]

        sza = df_sub['sza'].tolist()
        sza = deg_to_rad(sza)

        # Calculate albedo
        fsds_alb = fsds_adjusted
        idx_alb = 0
        while idx_alb < len(fsds_adjusted):
            if (fsds_adjusted[idx_alb] <= 0) or (fsus_jaws[idx_alb] < 0):
                fsds_alb[idx_alb] = common.fillvalue_float

            idx_alb += 1

        albedo = [x/y for x, y in zip(fsus_jaws, fsds_alb)]
        albedo = [abs(i) for i in albedo]

        # Calculate number of hours
        hours = np.arange(len(albedo))

        idx = 0
        # If less than 2 values for a day, derivative not possible, continue to next day without quality check
        if len(albedo) < 2:
            while idx < len(fsds_adjusted):
                df.at[outer_idx, 'fsds_adjusted_new'] = fsds_adjusted[idx]
                df.at[outer_idx, 'fsus_adjusted'] = fsus_jaws[idx]
                outer_idx += 1
                idx += 1
            continue
        else:  # Calculate second-order derivative of albedo
            alb_second_derv = first_order_derivative(hours, first_order_derivative(hours, albedo))

        # Check all following conditions for each hour
        while idx < len(fsds_adjusted):
            try:
                if np.cos(sza[idx]) <= 0:
                    fsds_adjusted[idx] = 0
                if abs(alb_second_derv[idx]) > thrsh:
                    fsds_adjusted[idx] = common.fillvalue_float
                if fsds_adjusted[idx] > toa[idx]:
                    fsds_adjusted[idx] = common.fillvalue_float
                if (fsds_adjusted[idx] < toa[idx]*0.05) and (fsds_adjusted[idx] != 0):
                    fsds_adjusted[idx] = common.fillvalue_float
                    fsus_jaws[idx] = common.fillvalue_float
                if (fsus_jaws[idx] > fsds_adjusted[idx]*0.95) or (fsus_jaws[idx] < fsds_adjusted[idx]*0.05):
                    fsus_jaws[idx] = common.fillvalue_float
                if fsds_adjusted[idx] < 0:
                    fsds_adjusted[idx] = 0
                if fsus_jaws[idx] == 0:
                    fsds_adjusted[idx] = 0
                if fsds_adjusted[idx] == 0:
                    fsus_jaws[idx] = 0

                # Insert calculated values
                df.at[outer_idx, 'fsds_adjusted_new'] = fsds_adjusted[idx]
                df.at[outer_idx, 'fsus_adjusted'] = fsus_jaws[idx]
            except:  # Exception for list index out of range toa[idx]
                common.log(args, 9, 'Warning: list index out of range for toa[idx]')

            idx += 1
            outer_idx += 1

    fsds_adjusted_values_new = df['fsds_adjusted_new'].tolist()
    fsus_adjusted_values = df['fsus_adjusted'].tolist()

    return fsds_adjusted_values_new, fsus_adjusted_values


def main(dataset, args):
    """Calculate adjusted downwelling and upwelling shortwave flux"""
    # Constants
    rho = 0.8  # reflectance
    smallest_double = 2.2250738585072014e-308
    fillvalue_double = 9.969209968386869e+36
    dtime_1970, tz = common.time_common(args.tz)
    idx_count = 0

    ds = dataset
    ds = ds.drop('time_bounds')  # Drop time_bounds dimension so that we don't have double entries of same data
    df = ds.to_dataframe()  # Convert to dataframe

    date_hour = [datetime.fromtimestamp(i, tz) for i in df.index.values]  # Index is seconds since 1970
    dates = [i.date() for i in date_hour]
    df['dates'] = dates  # Add dates column to dataframe
    dates = sorted(set(dates), key=dates.index)  # Get unique dates in increasing order

    # Create new columns
    df['fsds_adjusted'] = np.float()
    df['cloud_fraction'] = np.float()

    # Drop 'time' as index to do proper indexing for station_name
    df.reset_index(level=['time'], inplace=True)
    stn_name = df['station_name'][0]

    jaws_path = 'http://jaws.ess.uci.edu/jaws/rigb_data/'

    global toa_incoming_shortwave_flux
    if args.merra:
        dir_ceres = 'cf_toa/merra/'
        sfx = '.merra_cf_toa.nc'
        cloud_fraction_var = 'CLDTOT'
        toa_incoming_shortwave_flux = 'SWTDN'
    else:
        dir_ceres = 'cf_toa/ceres/'
        sfx = '.ceres_cf_toa.nc'
        cloud_fraction_var = 'cldarea_total_1h'
        toa_incoming_shortwave_flux = 'adj_atmos_sw_down_all_toa_1h'

    url = jaws_path + dir_ceres + stn_name + sfx
    try:  # Download CF_TOA file for requested station
        ceres_file = requests.get(url, allow_redirects=True)
    except requests.ConnectionError:
        print('ERROR: Unable to download CERES file from web-server, please check your internet connection \n'
              'HINT: Internet connection is needed only when performing RIGB operation')
        os._exit(1)

    # Write contents of CF_TOA file to a netCDF file
    open(stn_name + sfx, 'wb').write(ceres_file.content)

    for date in dates:
        year = date.year
        month = date.month
        day = date.day

        # Open downloaded ceres file as dataframe
        ceres_df = xr.open_dataset(stn_name + sfx).to_dataframe()
        # Get cf values for each day; dataframe index is date
        cf = ceres_df.loc[
             str(year)+'-'+str(month)+'-'+str(day):str(year)+'-'+str(month)+'-'+str(day)
             ][cloud_fraction_var].values.tolist()

        if args.merra:
            pass
        else:  # Divide cf by 100 for ceres files
            cf = [0.9999999 if i == 100 else i/100 for i in cf]

        # Subset dataframe for each day
        df_sub = df[df.dates == date]

        # Get fsds_jaws for that day and substitute NaN with fillvalue_float
        fsds_jaws = df_sub['fsds'].tolist()
        fsds_jaws = [fillvalue_double if np.isnan(i) else i for i in fsds_jaws]

        sza = df_sub['sza'].tolist()
        az = df_sub['az'].tolist()

        az = [(i - 180) for i in az]

        alpha = [(90 - i) for i in sza]

        aw = df_sub['tilt_direction_raw'].tolist()

        beta = df_sub['tilt_angle'].tolist()

        az = deg_to_rad(az)
        alpha = deg_to_rad(alpha)
        beta = deg_to_rad(beta)
        aw = deg_to_rad(aw)

        count = 0
        while count < len(alpha):
            if len(cf) == len(alpha):
                cos_i = (np.cos(alpha[count]) * np.cos(az[count] - aw[count]) * np.sin(beta[count]) + (
                        np.sin(alpha[count]) * np.cos(beta[count])))

                ddr = (0.2+0.8*cf[count])/(0.8-0.8*cf[count])

                nmr = fsds_jaws[count] * (np.sin(alpha[count]) + ddr)

                dnmr = cos_i + (ddr * (1 + np.cos(beta[count])) / 2.) + (
                            rho * (np.sin(alpha[count]) + ddr) * (1 - np.cos(beta[count])) / 2.)
                if dnmr == 0 or np.isnan(dnmr):
                    dnmr = smallest_double

                df.at[idx_count, 'fsds_adjusted'] = nmr/dnmr
                df.at[idx_count, 'cloud_fraction'] = cf[count]

            count += 1
            idx_count += 1

    cloud_fraction_values = df['cloud_fraction'].tolist()
    dataset['cloud_fraction'] = 'time', cloud_fraction_values

    fsds_adjusted_values_new, fsus_adjusted_values = post_process(df, dates, stn_name, sfx, args)
    dataset['fsds_adjusted'] = 'time', fsds_adjusted_values_new
    dataset['fsus_adjusted'] = 'time', fsus_adjusted_values

    # Drop tilt_direction_raw because it was needed only for calculations here
    dataset = dataset.drop('tilt_direction_raw')

    try:
        os.remove(stn_name + sfx)
    except:  # Windows
        pass

    return dataset
