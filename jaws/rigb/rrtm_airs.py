from datetime import datetime, timedelta
import os

import climlab
from climlab.domain.field import Field
from climlab.domain import domain
import numpy as np
import pandas as pd
import xarray as xr

import sunposition

import warnings
warnings.filterwarnings('ignore')

'''
Run RRTM using processed AIRS data from nomiss_airs.py
- run 24 hour twice (A and D)
- cal SZA
- output netCDF
'''


def make_column(lev=None,  ps=1013, tmp=None, ts=None):
    state = climlab.column_state(lev=lev)
    num_lev = np.array(lev).size
    lev = state.Tatm.domain.lev

    lev_values = lev.points
    lev_dfs = np.zeros(num_lev)
    lev_dfs[1:] = np.diff(lev_values)
    lev_dfs[0] = lev_values[0]
    lev_dfs = lev_dfs/2.

    lev.bounds = np.full(num_lev+1, ps)
    lev.bounds[:-1] = lev_values-lev_dfs
    lev.delta = np.abs(np.diff(lev.bounds))
    sfc, atm = domain.single_column(lev=lev)
    state['Ts'] = Field(ts, domain=sfc)
    state['Tatm'] = Field(tmp, domain=atm)
    
    return state


def main():
    indir = "nomiss-airx3std/"
    outdir = "rrtm-airx3std/"
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
    absorber_vmr['CFC11'] = 0.280/1E9
    absorber_vmr['CFC12'] = 0.503/1E9
    absorber_vmr['CFC22'] = 0.
    absorber_vmr['CCL4'] = 0.

    # stn names and lat/lon
    lst_stn = pd.read_csv('../resources/stations_radiation.txt')
    stn_names = lst_stn['network_name'].tolist()
    latstn = lst_stn['lat'].tolist()
    lonstn = lst_stn['lon'].tolist()

    nstn = len(stn_names)
    '''stn_names = 'imau09'
    latstn = -75.0
    lonstn = 0.0
    nstn = 1'''

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

        clr_dates = cleardays.loc[cleardays['network_name'] == stn, 'date']

        for date in clr_dates:
            sw_dn = []
            sw_up = []
            lw_dn = []
            lw_up = []

            sw_dn_final = [None]*24
            sw_up_final = [None]*24
            lw_dn_final = [None]*24
            lw_up_final = [None]*24
            for sfx in ['A', 'D']:
                flname = indir + stn + '/' + stn + '.' + str(date) + '.' + sfx + '.nc'

                if not os.path.isfile(flname):  # Check if nomiss file exists
                    continue

                fin = xr.open_dataset(flname)

                # Get values from nomiss netCDF file
                tmp = fin['t'].values
                ts = fin['ts'].values
                plev = fin['plev'].values
                ps = fin['ps'].values

                state = make_column(lev=plev, ps=ps, tmp=tmp, ts=ts)

                o3 = fin['o3'].values
                absorber_vmr['O3'] = o3

                h2o_q = fin['q'].values

                aod_count = fin['aod_count'].values

                # knob
                aod = np.zeros((6, 1, 24))
                aod[1, 0, -aod_count:] = 0.12 / aod_count
                aod[5, 0, :15] = 0.0077 / 15

                # Calculate shortwave radiation down for each hour
                for hr in range(24):
                    dtime = datetime.strptime(flname.split('.')[1], "%Y%m%d") + timedelta(hours=hr, minutes=30)

                    sza = sunposition.sunpos(dtime, lat_deg, lon_deg, 0)[1]
                    cossza = np.cos(np.radians(sza))

                    rad = climlab.radiation.RRTMG(name='Radiation', state=state, specific_humidity=h2o_q,
                                                  albedo=alb, coszen=cossza, absorber_vmr=absorber_vmr,
                                                  emissivity=emis, S0=solar_constant, icld=0, iaer=6,
                                                  ecaer_sw=aod)
                    rad.compute_diagnostics()

                    dout = rad.to_xarray(diagnostics=True)
                    sw_dn.append(dout['SW_flux_down_clr'].values[-1])
                    sw_up.append(dout['SW_flux_up_clr'].values[-1])
                    lw_dn.append(dout['LW_flux_down_clr'].values[-1])
                    lw_up.append(dout['LW_flux_up_clr'].values[-1])

            if sw_dn:
                if len(sw_dn) == 24:
                    sw_dn_final = sw_dn  # If only either 'A' or 'D' file present
                    sw_up_final = sw_up  # If only either 'A' or 'D' file present
                    lw_dn_final = lw_dn  # If only either 'A' or 'D' file present
                    lw_up_final = lw_up  # If only either 'A' or 'D' file present
                else:
                    count = 0
                    while count < 24:
                        sw_dn_final[count] = (sw_dn[count]+sw_dn[count+24])/2.0  # Average of both 'A' and 'D'
                        sw_up_final[count] = (sw_up[count]+sw_up[count+24])/2.0  # Average of both 'A' and 'D'
                        lw_dn_final[count] = (lw_dn[count]+lw_dn[count+24])/2.0  # Average of both 'A' and 'D'
                        lw_up_final[count] = (lw_up[count]+lw_up[count+24])/2.0  # Average of both 'A' and 'D'
                        count += 1

                sw_dn_complete.append(sw_dn_final)  # Combine sw_dn_final for multiple days in a single variable
                sw_up_complete.append(sw_up_final)  # Combine sw_up_final for multiple days in a single variable
                lw_dn_complete.append(lw_dn_final)  # Combine lw_dn_final for multiple days in a single variable
                lw_up_complete.append(lw_up_final)  # Combine lw_up_final for multiple days in a single variable

                for hr in range(24):  # Time variable to be written in netCDF file
                    time_op.append(datetime.strptime(str(date), "%Y%m%d") + timedelta(hours=hr, minutes=30))

        if sw_dn_complete:  # Write data

            # Make single list from list of lists
            sw_dn_complete = [item for sublist in sw_dn_complete for item in sublist]
            sw_up_complete = [item for sublist in sw_up_complete for item in sublist]
            lw_dn_complete = [item for sublist in lw_dn_complete for item in sublist]
            lw_up_complete = [item for sublist in lw_up_complete for item in sublist]

            # Get seconds since 1970
            time_op = [(i - datetime(1970, 1, 1)).total_seconds() for i in time_op]

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
