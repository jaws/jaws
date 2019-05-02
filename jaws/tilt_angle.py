from datetime import datetime
import os
import requests
import time

import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline
import xarray as xr

try:
    from itertools import izip as zip
except ImportError:  # Python 3.x
    pass

try:
    from jaws import common, sunposition
except ImportError:
    import common, sunposition


def deg_to_rad(list_deg):
    """Convert degrees to radians"""
    list_rad = [np.radians(i) for i in list_deg]

    return list_rad


def rad_to_deg(list_rad):
    """Convert radians to degrees"""
    list_deg = [np.degrees(i) for i in list_rad]

    return list_deg


def get_rrtm_file(jaws_path, dir_rrtm, stn_name, sfx):
    """Download RRTM file for requested station"""
    url = jaws_path + dir_rrtm + stn_name + sfx
    try:
        rrtm_file = requests.get(url, allow_redirects=True)
    except requests.ConnectionError:
        print('ERROR: Unable to download RRTM file from web-server, please check your internet connection \n'
              'HINT: Internet connection is needed only when performing RIGB operation')
        os._exit(1)

    return rrtm_file


def get_rrtm_df(stn_name, sfx, rrtm_file):
    """Store the downloaded RRTM file into a dataframe"""
    open(stn_name + sfx, 'wb').write(rrtm_file.content)
    rrtm_df = xr.open_dataset(stn_name + sfx).to_dataframe()

    return  rrtm_df


def main(dataset, latitude, longitude, clr_df, args):
    ddr = 0.25
    rho = 0.8
    smallest_double = 2.2250738585072014e-308
    dtime_1970, tz = common.time_common(args.tz)

    clrprd_file = clr_df
    # Combine date, start_hour and end_hour into a single string, e.g. 20080103_16_23
    clrprd = [(str(x)+'_'+str(y)+'_'+str(z)) for x, y, z in
              zip(clrprd_file['date'].tolist(), clrprd_file['start_hour'].tolist(), clrprd_file['end_hour'].tolist())]

    hours = list(range(24))
    half_hours = (list(np.arange(0, 24, 0.5)))

    ds = dataset.drop('time_bounds')  # Drop time_bounds dimension so that we don't have double entries of same data
    df = ds.to_dataframe()  # Convert to dataframe

    date_hour = [datetime.fromtimestamp(i, tz) for i in df.index.values]  # Index is seconds since 1970
    dates = [i.date() for i in date_hour]  # Get dates
    df['dates'] = dates  # Add as new column

    # Create new dataframe to store tilt_direction and tilt_angle
    tilt_df = pd.DataFrame(index=dates, columns=['tilt_direction', 'tilt_angle'])

    lat = latitude
    lon = longitude

    # Drop 'time' as index to do proper indexing for station_name
    df.reset_index(level=['time'], inplace=True)
    stn_name = df['station_name'][0]
    # Replace fillvalue with nan for calculations
    df[['fsds']] = df[['fsds']].replace(common.fillvalue_float, np.nan)

    jaws_path = 'http://jaws.ess.uci.edu/jaws/rigb_data/'
    dir_rrtm = 'rrtm-airx3std/'
    sfx = '.rrtm.nc'

    if args.merra:
        dir_rrtm = 'rrtm-merra/'

    rrtm_file = get_rrtm_file(jaws_path, dir_rrtm, stn_name, sfx)

    if rrtm_file:
        rrtm_df = get_rrtm_df(stn_name, sfx, rrtm_file)
    else:  # If no AIRS RRTM file, try MERRA RRTM file
        dir_rrtm = 'rrtm-merra/'
        rrtm_file = get_rrtm_file(jaws_path, dir_rrtm, stn_name, sfx)
        if rrtm_file:
            rrtm_df = get_rrtm_df(stn_name, sfx, rrtm_file)
        else:
            print('ERROR: RRTM data not available for this station. Please report it on github.com/jaws/jaws/issues')
            os._exit(1)

    start_time = time.time()

    ########################################################################################
    #                   Tilt Angle and Tilt Direction Calculations                         #

    #                           ########PART-1#############                                #

    for line in clrprd:
        clrdate = line.split('_')[0]
        clrhr_start = int(line.split('_')[1])
        clrhr_end = int(line.split('_')[2])
        clrhr_end = clrhr_end + 1  # To make sure we include the last hour when slicing the data
        year = int(clrdate[:4])
        month = int(clrdate[4:6])
        day = int(clrdate[6:])
        current_date_hour = datetime(year, month, day).date()

        fsds_rrtm = rrtm_df.loc[str(year) + '-' + str(month) + '-' + str(day):
                                str(year) + '-' + str(month) + '-' + str(day)]['fsds'].values.tolist()
        if fsds_rrtm:
            if args.dbg_lvl > 6:
                print(clrdate)
            else:
                current_time = time.time()
                if (current_time-start_time) > 10*60:
                    print('Still working...')
                    start_time = current_time
        else:
            continue

        # Subset dataframe
        df_sub = df[df.dates == current_date_hour]

        fsds_jaws_nonmsng = df_sub['fsds'].dropna().tolist()
        indexMissingJAWS = np.where(df_sub['fsds'].isna())
        indexMissingJAWS = [a for b in indexMissingJAWS for a in b]  # Convert to list

        hours_nonmsng = np.where(df_sub['fsds'].notnull())
        hours_nonmsng = [a for b in hours_nonmsng for a in b]  # Convert to list
        hours_nonmsng = [i+0.5 for i in hours_nonmsng]  # Half-hour values

        # Interpolate fsds and sza for half-hour values
        if len(fsds_jaws_nonmsng) < 2:
            if args.dbg_lvl > 6:
                print("Skipping this day as there is only 1 value of fsds")
            continue
        else:
            fsds_intrp = CubicSpline(hours_nonmsng, fsds_jaws_nonmsng, extrapolate=True)(half_hours)
        fsds_intrp = [a for a in fsds_intrp]  # Convert to list

        # Calculate azimuth angle
        az = []
        sza = []
        for hour in hours:
            dtime = datetime(year, month, day, hour, 0)
            az.append(sunposition.sunpos(dtime, lat, lon, 0)[0])
            sza.append(sunposition.sunpos(dtime, lat, lon, 0)[1])
            dtime = datetime(year, month, day, hour, 30)
            az.append(sunposition.sunpos(dtime, lat, lon, 0)[0])
            sza.append(sunposition.sunpos(dtime, lat, lon, 0)[1])

        az = [(i-180) for i in az]

        alpha = [(90-i) for i in sza]

        beta = list(np.arange(0.25, 45.25, 0.25))

        sza_noon = [np.cos(np.radians(i)) for i in sza]

        # Check if measured solar noon time > true solar noon time
        if fsds_intrp.index(max(fsds_intrp)) > sza_noon.index(max(sza_noon)):
            aw = list(np.arange(0, 180, 0.25))
        else:
            aw = list(np.arange(-179.75, 0.25, 0.25))

        az = deg_to_rad(az)
        alpha = deg_to_rad(alpha)
        beta = deg_to_rad(beta)
        aw = deg_to_rad(aw)

        # Make pairs of aw,beta
        pairs = []
        for i in aw:
            for j in beta:
                pairs.append(tuple((i, j)))

        # Find all possible pairs using correct fsds
        possible_pairs = []
        daily_avg_diff = []
        best_pairs = []
        fsds_possiblepair_dict = {}

        for pair in pairs:
            count = 0
            cos_i = []
            fsds_correct = []
            while count < len(alpha):
                cos_i.append((np.cos(alpha[count])*np.cos(az[count]-pair[0])*np.sin(pair[1])+(
                        np.sin(alpha[count])*np.cos(pair[1]))))
                nmr = fsds_intrp[count]*(np.sin(alpha[count])+ddr)
                dnmr = cos_i[count]+(ddr*(1+np.cos(pair[1]))/2.)+(rho*(np.sin(alpha[count])+ddr)*(1-np.cos(pair[1]))/2.)
                if dnmr == 0:
                    dnmr = smallest_double
                fsds_correct.append(nmr/dnmr)

                count += 1

            if (abs(cos_i.index(max(cos_i)) - fsds_intrp.index(max(fsds_intrp))) <= 1 and 
               abs(fsds_correct.index(max(fsds_correct)) - sza_noon.index(max(sza_noon))) <= 1):
                possible_pairs.append(pair)

                fsds_correct_half = fsds_correct[1::2]
                fsds_possiblepair_dict[pair] = fsds_correct_half

                for msng_idx in indexMissingJAWS:
                    try:
                        fsds_correct_half.pop(msng_idx)
                    except:
                        common.log(args, 9, 'Warning: missing index fsds_correct_half')
                    try:
                        fsds_rrtm.pop(msng_idx)
                    except:
                        common.log(args, 9, 'Warning: missing index fsds_rrtm')

                diff = [abs(x-y) for x,y in zip(fsds_correct_half[clrhr_start:clrhr_end],
                                                fsds_rrtm[clrhr_start:clrhr_end])]
                daily_avg_diff.append(np.nanmean(diff))

        #                           ########PART-2#############                                #

        dailyavg_possiblepair_dict = dict(zip(daily_avg_diff, possible_pairs))

        if not dailyavg_possiblepair_dict.keys():
            continue  # Skip day if no possible pair
        else:
            if min(dailyavg_possiblepair_dict.keys()) <= 50:
                for val in dailyavg_possiblepair_dict.keys():
                    if val <= min(dailyavg_possiblepair_dict.keys())+5:
                        best_pairs.append(dailyavg_possiblepair_dict.get(val))

        #                           ########PART-3#############                                #

        fsds_bestpair_dict = {k: fsds_possiblepair_dict[k] for k in best_pairs}

        bestpair_dailyavg_dict = dict((bp, [key for (key, value) in dailyavg_possiblepair_dict.items() if value == bp])
                                      for bp in best_pairs)

        num_spikes = []
        for pair in fsds_bestpair_dict:
            fsds_correct_top = fsds_bestpair_dict[pair]
            counter = 0
            spike_hrs = 0
            diff_top = [abs(x-y) for x, y in zip(fsds_correct_top[clrhr_start:clrhr_end],
                                                 fsds_rrtm[clrhr_start:clrhr_end])]
            fsds_rrtm_10 = [ij*0.1 for ij in fsds_rrtm[clrhr_start:clrhr_end]]
            for val in diff_top:
                if diff_top[counter] > fsds_rrtm_10[counter]:
                    spike_hrs += 1
                counter += 1
            
            num_spikes.append((spike_hrs, bestpair_dailyavg_dict[pair]))

        try:
            top_pair = best_pairs[num_spikes.index(min(num_spikes))]

            tilt_df.at[current_date_hour, 'tilt_direction'] = top_pair[0]
            tilt_df.at[current_date_hour, 'tilt_angle'] = top_pair[1]
        except:
            common.log(args, 9, 'Warning: no top pair found')
            continue  # Skip day if no top pair

    ########################################################################################

    tilt_df['tilt_direction'] = pd.to_numeric(tilt_df['tilt_direction'], errors='coerce')
    tilt_df['tilt_angle'] = pd.to_numeric(tilt_df['tilt_angle'], errors='coerce')

    tilt_df = tilt_df.interpolate(limit_direction='both')  # Interpolate missing values
    tilt_direction_values = tilt_df['tilt_direction'].tolist()
    tilt_angle_values = tilt_df['tilt_angle'].tolist()

    tilt_direction_values = rad_to_deg(tilt_direction_values)
    dataset['tilt_direction_raw'] = 'time', tilt_direction_values  # Raw values to be used in fsds_adjust script

    # Change tilt_direction to 0 pointing north. These values will be in output netCDF file
    tilt_direction_values = [270-d for d in tilt_direction_values]
    tilt_direction_values = [d-360 if d > 360 else d for d in tilt_direction_values]

    tilt_angle_values = rad_to_deg(tilt_angle_values)

    # Add tilt_direction and tilt_angle to output file
    dataset['tilt_direction'] = 'time', tilt_direction_values
    dataset['tilt_angle'] = 'time', tilt_angle_values

    try:  # Remove downloaded rrtm_df file
        os.remove(stn_name + sfx)
    except:  # Windows
        pass

    return dataset
