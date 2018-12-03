from datetime import datetime
import requests

import Ngl
import numpy as np
import pandas as pd

import sunposition

try:
    from itertools import izip as zip
except ImportError:  # Python 3.x
    pass

try:
    from jaws import common
except ImportError:
    import common


def deg_to_rad(list_deg):
    list_rad = [np.radians(i) for i in list_deg]

    return list_rad


def main(dataset, latitude, longitude, clr_df, args):
    ddr = 0.25
    rho = 0.8
    smallest_double = 2.2250738585072014e-308
    dtime_1970, tz = common.time_common(args.tz)

    clrprd_file = clr_df
    clrprd = [(str(x)+'_'+str(y)+'_'+str(z)) for x, y, z in
              zip(clrprd_file[0].tolist(), clrprd_file[1].tolist(), clrprd_file[2].tolist())]

    hours = list(range(24))
    half_hours = list(np.arange(0, 24, 0.5))

    ds = dataset.drop('time_bounds')
    df = ds.to_dataframe()

    date_hour = [datetime.fromtimestamp(i, tz) for i in df.index.values]
    dates = [i.date() for i in date_hour]

    tilt_df = pd.DataFrame(index=dates, columns=['tilt_direction', 'tilt_angle'])

    lat = latitude
    lon = longitude

    df.reset_index(level=['time'], inplace=True)
    stn_name = df['station_name'][0]

    grele_path = 'http://grele.ess.uci.edu/jaws/rigb_data/'
    dir_rrtm = 'rrtm-airx3std/'

    for line in clrprd:
        clrdate = line.split('_')[0]
        clrhr_start = int(line.split('_')[1])
        clrhr_end = int(line.split('_')[2])
        year = int(clrdate[:4])
        month = int(clrdate[5:7])
        day = int(clrdate[8:10])
        current_date_hour = datetime(year, month, day).date()

        try:
            rrtm_file = requests.get(grele_path+dir_rrtm+stn_name+'.'+clrdate.replace('-', '')+'.txt')
            fsds_rrtm = rrtm_file.text.strip().split(',')
            fsds_rrtm = [float(i) for i in fsds_rrtm]
        except:
            continue

        # Subset dataframe
        df_sub = df[(df.year == year) & (df.month == month) & (df.day == day)]

        fsds_jaws_nonmsng = df_sub['sw_down'].dropna().tolist()
        indexMissingJAWS = np.where(df_sub['sw_down'].isna())
        indexMissingJAWS = [a for b in indexMissingJAWS for a in b]  # Convert to list

        hours_nonmsng = list(range(len(fsds_jaws_nonmsng)))

        # Interpolate fsds and sza for half-hour values
        fsds_intrp = list(Ngl.ftcurv(hours_nonmsng, fsds_jaws_nonmsng, half_hours))

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
                    fsds_correct_half.pop(msng_idx)
                    fsds_rrtm.pop(msng_idx)

                diff = [abs(x-y) for x,y in zip(fsds_correct_half[clrhr_start:clrhr_end],
                                                fsds_rrtm[clrhr_start:clrhr_end])]
                daily_avg_diff.append(np.nanmean(diff))


        #########PART-2#############

        dailyavg_possiblepair_dict = dict(zip(daily_avg_diff, possible_pairs))

        if not dailyavg_possiblepair_dict.keys():
            continue  # Skip day if no possible pair
        else:
            if min(dailyavg_possiblepair_dict.keys()) <= 50:
                for val in dailyavg_possiblepair_dict.keys():
                    if val <= min(dailyavg_possiblepair_dict.keys())+5:
                        best_pairs.append(dailyavg_possiblepair_dict.get(val))


        #########PART-3#############

        fsds_bestpair_dict = {k: fsds_possiblepair_dict[k] for k in best_pairs}

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
            
            num_spikes.append(spike_hrs)

        try:
            top_pair = best_pairs[num_spikes.index(min(num_spikes))]

            tilt_df.at[current_date_hour, 'tilt_direction'] = top_pair[0]
            tilt_df.at[current_date_hour, 'tilt_angle'] = top_pair[1]
        except:
            continue  # Skip day if no top pair

    tilt_df['tilt_direction'] = pd.to_numeric(tilt_df['tilt_direction'], errors='coerce')
    tilt_df['tilt_angle'] = pd.to_numeric(tilt_df['tilt_angle'], errors='coerce')

    tilt_df = tilt_df.interpolate()
    tilt_direction_values = tilt_df['tilt_direction'].tolist()
    tilt_angle_values = tilt_df['tilt_angle'].tolist()

    dataset['tilt_direction'] = 'time', tilt_direction_values
    dataset['tilt_angle'] = 'time', tilt_angle_values

    return dataset
