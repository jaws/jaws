from datetime import datetime
from itertools import groupby
from operator import itemgetter

import Ngl
import numpy as np
import pandas as pd
import scipy.interpolate


def interpolate(x, y):
    dv = scipy.interpolate.interp1d(x, y, fill_value='extrapolate')
    alpha = 0.01
    dv_left, dv_right, tg_left, tg_right = ([None]*len(x) for _ in range(4))
    i = 0
    for hour in x:
        dv_left[i] = float(dv(i-alpha))
        dv_right[i] = float(dv(i+alpha))
        tg_left[i] = (y[i] - dv_left[i])/alpha
        tg_right[i] = (dv_right[i] - y[i])/alpha
        i += 1
    diff = [x1 - x2 for (x1, x2) in zip(tg_left, tg_right)]
    return diff


def clr_prd(dat_sza, tg_fsds, tg_sza, date, stn_name, outfile):
    para_file = pd.read_csv('../resources/lst_para_rdn.txt')

    scale = para_file.loc[para_file['stn_name'] == stn_name, 'scale'].iloc[0]
    offset = para_file.loc[para_file['stn_name'] == stn_name, 'offset'].iloc[0]
    offset_range = para_file.loc[para_file['stn_name'] == stn_name, 'offset_range'].iloc[0]

    tg_sza_scale = [i*scale for i in tg_sza]
    tg_sza_up = [i-offset+offset_range for i in tg_sza_scale]
    tg_sza_dn = [i-offset-offset_range for i in tg_sza_scale]

    clr_hrs = []
    daylight = []
    hours = list(range(len(dat_sza)))
    for hour in hours:
        if dat_sza[hour] > 0:
            daylight.append(hour)

        if hour == 0:
            clr_hrs.append(hour)
        elif (hour > 0) and (hour < 23):
            if (tg_fsds[hour] < tg_sza_up[hour]) and (tg_fsds[hour] > tg_sza_dn[hour]):
                clr_hrs.append(hour)
        elif hour == 23:
            clr_hrs.append(hour)
    
    cons_clr_hrs = []
    for k, g in groupby(enumerate(clr_hrs), lambda ix: ix[0] - ix[1]):
        cons_clr_hrs.append(list(map(itemgetter(1), g)))
    
    final_hrs, clr_lst = write_to_file(cons_clr_hrs, daylight, date)
    
    return final_hrs, clr_lst


def clr_shift(dat_sza, dat_fill, hrs, date, stn_name):
    dat_sza_shift = list(range(len(dat_sza)))

    shift = [1, 2, 3]

    for i in shift:
        if dat_sza.index(max(dat_sza)) < dat_fill.argmax():
            dat_sza_shift[-i:] = [0] * (len(dat_sza_shift) - i)
            dat_sza_shift[:-i] = dat_sza[i:]

        elif dat_sza.index(max(dat_sza)) > dat_fill.argmax():
            dat_sza_shift[:i] = [0] * (len(dat_sza_shift) - i)
            dat_sza_shift[i:] = dat_sza[:-i]

        tg_sza_shift = interpolate(hrs,dat_sza_shift)

        cons_clr_hrs, clr_lst = clr_prd(dat_sza, tg_fsds, tg_sza_shift, date, stn_name)

        if cons_clr_hrs:
            break

    return clr_lst


def write_to_file(cons_clr_hrs, daylight, date):
    final_hrs = []

    if len(daylight) <= 12:
        min_clrhrs_needed = 6
    elif 12 < len(daylight) < 16:
        min_clrhrs_needed = 7
    elif len(daylight) >= 16:
        min_clrhrs_needed = 8
    
    for group in cons_clr_hrs:
        if len(group) >= min_clrhrs_needed:
            final_hrs.append(group)

            clr_lst.append(["{}-{}-{}".format(
                date.year, '{:02d}'.format(date.month), '{:02d}'.format(date.day)), group[0], group[-1]])

    return final_hrs, clr_lst


def main(dataset):
    global tg_fsds, dat_sza, dat_fill, hrs, year, clr_lst

    clr_lst = []

    ds = dataset.drop('time_bounds')
    df = ds.to_dataframe()

    stn_name = df['station_name'][0]
 
    df.reset_index(level=['time'], inplace=True)
    date_hour = df['time'].tolist()
    dates = [i.date() for i in date_hour]
    dates = sorted(set(dates), key=dates.index)

    for date in dates:
        df_temp = df[(df.year == date.year) & (df.month == date.month) & (df.day == date.day)]

        dat = df_temp['sw_down'].tolist()
        dat_rmvmsng = df_temp['sw_down'].dropna().tolist()
        hrs = list(range(len(dat)))
        hrs_rmvmsng = list(range(len(dat_rmvmsng)))
        dat_fill = Ngl.ftcurv(hrs_rmvmsng, dat_rmvmsng, hrs)
        dat_sza = [np.cos(np.radians(i)) for i in df_temp['sza'].tolist()]

        tg_fsds = interpolate(hrs,dat_fill)
        tg_sza = interpolate(hrs,dat_sza)

        final_hrs, clr_lst = clr_prd(dat_sza, tg_fsds, tg_sza, date, stn_name)

        if not final_hrs:
            clr_lst = clr_shift(dat_sza, dat_fill, hrs, date, stn_name)

    clr_df = pd.DataFrame(clr_lst)

    return clr_df
