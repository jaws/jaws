import glob
import os

import xarray as xr

import nomiss_airs


def ceres_latlon(infile):
    ds = xr.open_dataset(infile)
    var_lat = ds['lat'].values
    var_lon = ds['lon'].values

    lat_lon_var = []

    for i in var_lat:
        for j in var_lon:
            lat_lon_var.append([i, j])

    return ds, lat_lon_var


def main():
    indir = 'ceres_merra_yearly/'
    outdir = 'ceres-merra/'

    stn_names, lat_lon_stn = nomiss_airs.get_stn_latlonname('stations_radiation.txt')

    for infile in glob.iglob(indir+'merra2.*.nc'):
        print(infile)

        x_coord = 0
        ds, lat_lon_var = ceres_latlon(infile)
        stn_new = nomiss_airs.haversine_np(lat_lon_stn, lat_lon_var)

        for _ in stn_new:
            y_coord = 0

            temp = {'lat': round(stn_new[x_coord][y_coord], 1),
                    'lon': round(stn_new[x_coord][y_coord+1], 3)}

            ds_sub = ds.sel(temp)  # Subset the dataset for only these dimensions

            # Write to netCDF file
            if not os.path.exists(outdir):
                os.makedirs(outdir)
            basename = os.path.basename(infile)
            outfile = outdir+'/'+stn_names[x_coord]+'.'+basename[-7:-3]+'.'+'merra_cf_toa'+'.nc'

            ds_sub.to_netcdf(outfile)

            x_coord += 1


if __name__ == '__main__':
    main()
