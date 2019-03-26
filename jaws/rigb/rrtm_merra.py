import csv
from datetime import datetime, timedelta
import os

import climlab
from climlab.domain.field import Field
from climlab.domain import domain
import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline
import xarray as xr

import sunposition

import warnings
warnings.filterwarnings('ignore')

'''
Run RRTM using processed MERRA data from nomiss_merra.py
- run for 8 hour and interpolate for 24 hours
- cal SZA
- output sw_dn
'''


def make_column(lev=None, ps=1013, tmp=None, ts=None):
    state = climlab.column_state(lev=lev)
    num_lev = np.array(lev).size
    lev = state.Tatm.domain.lev

    lev_values = lev.points
    lev_dfs = np.zeros(num_lev)
    lev_dfs[1:] = np.diff(lev_values)
    lev_dfs[0] = lev_values[0]
    lev_dfs = lev_dfs / 2.

    lev.bounds = np.full(num_lev + 1, ps)
    lev.bounds[:-1] = lev_values - lev_dfs
    lev.delta = np.abs(np.diff(lev.bounds))
    sfc, atm = domain.single_column(lev=lev)
    state['Ts'] = Field(ts, domain=sfc)
    state['Tatm'] = Field(tmp, domain=atm)

    return state


def main():
    indir = "nomiss-merra/"
    outdir = "rrtm-merra/"
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    # constants
    fillvalue_float = 9.96921e+36
    alb = 0.75
    emis = 0.985
    solar_constant = 1367.0

    absorber_vmr = dict()
    absorber_vmr['CO2'] = 355. / 1E6
    absorber_vmr['CH4'] = 1714. / 1E9
    absorber_vmr['N2O'] = 311. / 1E9
    absorber_vmr['O2'] = 0.21
    absorber_vmr['CFC11'] = 0.280 / 1E9
    absorber_vmr['CFC12'] = 0.503 / 1E9
    absorber_vmr['CFC22'] = 0.
    absorber_vmr['CCL4'] = 0.

    # stn names and lat/lon
    lst_stn = pd.read_csv('../resources/stations_radiation.txt')
    stn_names = lst_stn['network_name'].tolist()
    latstn = lst_stn['lat'].tolist()
    lonstn = lst_stn['lon'].tolist()

    nstn = len(stn_names)
    '''stn_names = 'gcnet_summit'
    latstn = 72.57972
    lonstn = -38.50454
    nstn = 1'''

    hours_merra = [1, 4, 7, 10, 13, 16, 19, 22]
    hours_24 = list(range(24))

    cleardays = pd.read_csv('cleardays.csv')

    # main function
    for i in range(nstn):
        stn = stn_names[i]
        lat_deg = latstn[i]
        lon_deg = lonstn[i]
        '''stn = stn_names
        lat_deg = latstn
        lon_deg = lonstn'''

        fout = outdir + stn + '.rrtm.nc'
        sw_dn_complete = []
        sw_up_complete = []
        lw_dn_complete = []
        lw_up_complete = []
        time_op = []

        flname = indir + stn + '.' + 'merra2.inst3.asm.1991-2018' + '.nc'

        clr_dates = cleardays.loc[cleardays['network_name'] == stn, 'date']

        for date in clr_dates:
            sw_dn = []
            sw_up = []
            lw_dn = []
            lw_up = []

            '''flname = indir + stn + '.' + str(date) + '.nc'

            if not os.path.isfile(flname):
                continue'''

            fin = xr.open_dataset(flname)
            fin = fin.sel(time=str(date))

            tmp = fin['t'].values
            ts = fin['ts'].values
            plev = fin['plev'].values
            ps = fin['ps'].values
            h2o_q = fin['q'].values
            o3_mmr = fin['o3'].values
            o3_vmr = climlab.utils.thermo.mmr_to_vmr(o3_mmr, gas='O3')

            aod_count = int(fin['aod_count'].values[0])

            # knob
            aod = np.zeros((6, 1, 42))
            aod[1, 0, -aod_count:] = 0.12 / aod_count
            aod[5, 0, :20] = 0.0077 / 20

            idx = 0

            for hr in hours_merra:
                dtime = datetime.strptime(str(date), "%Y%m%d") + timedelta(hours=hr, minutes=30)

                sza = sunposition.sunpos(dtime, lat_deg, lon_deg, 0)[1]
                cossza = np.cos(np.radians(sza))

                state = make_column(lev=plev[idx], ps=ps[idx], tmp=tmp[idx], ts=ts[idx])
                absorber_vmr['O3'] = o3_vmr[idx]

                rad = climlab.radiation.RRTMG(name='Radiation', state=state, specific_humidity=h2o_q[idx],
                                              albedo=alb, coszen=cossza, absorber_vmr=absorber_vmr,
                                              emissivity=emis, S0=solar_constant, icld=0, iaer=6,
                                              ecaer_sw=aod)
                rad.compute_diagnostics()

                dout = rad.to_xarray(diagnostics=True)
                sw_dn.append(dout['SW_flux_down_clr'].values[-1])
                sw_up.append(dout['SW_flux_up_clr'].values[-1])
                lw_dn.append(dout['LW_flux_down_clr'].values[-1])
                lw_up.append(dout['LW_flux_up_clr'].values[-1])

                idx += 1

            sw_dn_24 = CubicSpline(hours_merra, sw_dn, extrapolate=True)(hours_24)
            sw_up_24 = CubicSpline(hours_merra, sw_up, extrapolate=True)(hours_24)
            lw_dn_24 = CubicSpline(hours_merra, lw_dn, extrapolate=True)(hours_24)
            lw_up_24 = CubicSpline(hours_merra, lw_up, extrapolate=True)(hours_24)

            sw_dn_complete.append(sw_dn_24)
            sw_up_complete.append(sw_up_24)
            lw_dn_complete.append(lw_dn_24)
            lw_up_complete.append(lw_up_24)

            for hr in range(24):
                time_op.append(datetime.strptime(str(date), "%Y%m%d") + timedelta(hours=hr, minutes=30))

        # Combine fsds for multiple days into single list
        sw_dn_complete = [item for sublist in sw_dn_complete for item in sublist]
        sw_up_complete = [item for sublist in sw_up_complete for item in sublist]
        lw_dn_complete = [item for sublist in lw_dn_complete for item in sublist]
        lw_up_complete = [item for sublist in lw_up_complete for item in sublist]

        # Get seconds since 1970
        time_op = [(i - datetime(1970, 1, 1)).total_seconds() for i in time_op]

        if sw_dn_complete:  # Write data
            ds = xr.Dataset()

            ds['fsds'] = 'time', sw_dn_complete
            ds['fsus'] = 'time', sw_up_complete
            ds['flds'] = 'time', lw_dn_complete
            ds['flus'] = 'time', lw_up_complete
            ds['time'] = 'time', time_op

            ds['fsds'].attrs = {"_FillValue": fillvalue_float, "units": 'watt meter-2',
                                "long_name": 'RRTM simulated shortwave downwelling radiation at surface'}
            ds['fsus'].attrs = {"_FillValue": fillvalue_float, "units": 'watt meter-2',
                                "long_name": 'RRTM simulated shortwave upwelling radiation at surface'}
            ds['flds'].attrs = {"_FillValue": fillvalue_float, "units": 'watt meter-2',
                                "long_name": 'RRTM simulated longwave downwelling radiation at surface'}
            ds['flus'].attrs = {"_FillValue": fillvalue_float, "units": 'watt meter-2',
                                "long_name": 'RRTM simulated longwave upwelling radiation at surface'}
            ds['time'].attrs = {"_FillValue": fillvalue_float, "units": 'seconds since 1970-01-01 00:00:00',
                                "calendar": 'standard'}

            ds.to_netcdf(fout)
            print(fout)


if __name__ == '__main__':
    main()
