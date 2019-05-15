from metpy.units import units
from metpy.calc import potential_temperature, density
from metpy.calc import mixing_ratio_from_relative_humidity, specific_humidity_from_mixing_ratio
import numpy as np
import pandas as pd
import xarray as xr

try:
    from jaws import common, sunposition, clearsky, tilt_angle, fsds_adjust
except ImportError:
    import common, sunposition, clearsky, tilt_angle, fsds_adjust


def init_dataframe(args, input_file):
    """Initialize dataframe with data from input file; convert temperature and pressure to SI units"""
    check_na = 999.0

    global header_rows
    header_rows = 0
    with open(input_file) as stream:
        for line in stream:
            header_rows += 1
            if len(line.strip()) == 0 :
                break

    df, columns = common.load_dataframe('gcnet', input_file, header_rows)

    # Convert only if this column is present in input file
    try:
        df['qc25'] = df['qc25'].astype(str)  # To avoid 999 values marked as N/A
    except Exception:
        pass

    df.replace(check_na, np.nan, inplace=True)

    temperature_vars = [
        'ta_tc1', 'ta_tc2', 'ta_cs1', 'ta_cs2',
        'tsn1', 'tsn2', 'tsn3','tsn4', 'tsn5',
        'tsn6', 'tsn7', 'tsn8', 'tsn9', 'tsn10',
        'ta_max1', 'ta_max2', 'ta_min1','ta_min2', 'ref_temp']
    if not args.celsius:
        df.loc[:, temperature_vars] += common.freezing_point_temp  # Convert units to Kelvin

    pressure_vars = ['ps']
    if not args.mb:
        df.loc[:, pressure_vars] *= common.pascal_per_millibar  # Convert units to millibar/hPa

    df = df.where((pd.notnull(df)), common.get_fillvalue(args))

    try:
        df['qc25'] = df['qc25'].astype(int)  # Convert it back to int
    except Exception:
        pass

    return df, temperature_vars, pressure_vars


def get_station(args, input_file, stations):
    """Get latitude, longitude and name for each station"""
    df, columns = common.load_dataframe('gcnet', input_file, header_rows)
    station_number = df['station_number'][0]

    if 30 <= station_number <= 32:
        name = 'gcnet_lar{}'.format(station_number - 29)
        station = stations[name]
    else:
        station = list(stations.values())[station_number]

    return common.parse_station(args, station)


def fill_dataset_quality_control(dataframe, dataset, input_file):
    """Create new separate quality control variables for each variable from qc1, qc9, qc17, qc25"""
    temp_df, columns = common.load_dataframe('gcnet', input_file, header_rows)

    keys = common.read_ordered_json('resources/gcnet/quality_control.json')
    for key, attributes in keys.items():
        # Check if qc variables are present in input file
        if key in columns:
            values = [list(map(int, i)) for i in zip(*map(str, dataframe[key]))]
            for attr, value in zip(attributes, values):
                dataset[attr] = 'time', value


def get_time_and_sza(args, dataframe, longitude, latitude):
    """Calculate additional time related variables"""
    dtime_1970, tz = common.time_common(args.tz)
    num_rows = dataframe['year'].size
    sza, az = ([0] * num_rows for _ in range(2))

    hour_conversion = 100 / 4
    last_hour = 23
    hour = dataframe['julian_decimal_time']
    hour = [round(i - int(i), 3) * hour_conversion for i in hour]
    hour = [int(h) if int(h) <= last_hour else 0 for h in hour]

    temp_dtime = pd.to_datetime(dataframe['year']*1000 + dataframe['julian_decimal_time'].astype(int), format='%Y%j')

    dataframe['hour'] = hour
    dataframe['dtime'] = temp_dtime

    dataframe['dtime'] = pd.to_datetime(dataframe.dtime)
    dataframe['dtime'] += pd.to_timedelta(dataframe.hour, unit='h')
    # Each timestamp is average of previous and current hour values i.e. value at hour=5 is average of hour=4 and hour=5
    # Our 'time' variable will represent values at half-hour i.e. 4.5 in above case, so subtract 30 minutes from all.
    dataframe['dtime'] -= pd.to_timedelta(common.seconds_in_half_hour, unit='s')

    dataframe['dtime'] = [tz.localize(i.replace(tzinfo=None)) for i in dataframe['dtime']]  # Set timezone

    time = (dataframe['dtime'] - dtime_1970) / np.timedelta64(1, 's')  # Seconds since 1970
    time_bounds = [(i-common.seconds_in_half_hour, i+common.seconds_in_half_hour) for i in time]

    month = pd.DatetimeIndex(dataframe['dtime']).month.values
    day = pd.DatetimeIndex(dataframe['dtime']).day.values
    minutes = pd.DatetimeIndex(dataframe['dtime']).minute.values
    dates = list(pd.DatetimeIndex(dataframe['dtime']).date)
    dates = [int(d.strftime("%Y%m%d")) for d in dates]
    first_date = min(dates)
    last_date = max(dates)

    for idx in range(num_rows):
        solar_angles = sunposition.sunpos(dataframe['dtime'][idx], latitude, longitude, 0)
        az[idx] = solar_angles[0]
        sza[idx] = solar_angles[1]

    return month, day, hour, minutes, time, time_bounds, sza, az, first_date, last_date


# Just a framework, need to do calculations
'''
def extrapolate_temp(dataframe):
    ht1 = dataframe['wind_sensor_height_1']
    ht2 = dataframe['wind_sensor_height_2']
    temp_ht1 = dataframe['ta_tc1']
    temp_ht2 = dataframe['ta_tc1']

    surface_temp = temp_ht1 - (((temp_ht2 - temp_ht1)/(ht2 - ht1))*ht1)
    return surface_temp
'''


def gradient_fluxes(df):  # This method is very sensitive to input data quality
    """Returns Sensible Heat Flux and Latent Heat Flux based on Steffen & DeMaria (1996) method"""
    g = 9.81  # m/s**2
    cp = 1005  # J/kg/K
    k = 0.4  # von Karman
    Lv = 2.50e6  # J/kg

    fillvalue = common.fillvalue_float

    ht_low, ht_high, ta_low, ta_high, wspd_low, wspd_high, rh_low, rh_high, phi_m, phi_h = ([] for _ in range(10))

    # Average temp from both sensors for height1 and height2
    ta1 = df.loc[:, ("ta_tc1", "ta_cs1")]
    ta2 = df.loc[:, ("ta_tc2", "ta_cs2")]
    df['ta1'] = ta1.mean(axis=1)
    df['ta2'] = ta2.mean(axis=1)

    # Assign low and high depending on height of sensors
    idx = 0
    while idx < len(df):
        if df['wind_sensor_height_1'][idx] == fillvalue or df['wind_sensor_height_2'][idx] == fillvalue:
            ht_low.append(np.nan)
            ht_high.append(np.nan)
            ta_low.append(df['ta1'][idx])
            ta_high.append(df['ta2'][idx])
            wspd_low.append(df['wspd1'][idx])
            wspd_high.append(df['wspd2'][idx])
            rh_low.append(df['rh1'][idx])
            rh_high.append(df['rh2'][idx])
        elif df['wind_sensor_height_1'][idx] > df['wind_sensor_height_2'][idx]:
            ht_low.append(df['wind_sensor_height_2'][idx])
            ht_high.append(df['wind_sensor_height_1'][idx])
            ta_low.append(df['ta2'][idx])
            ta_high.append(df['ta1'][idx])
            wspd_low.append(df['wspd2'][idx])
            wspd_high.append(df['wspd1'][idx])
            rh_low.append(df['rh2'][idx])
            rh_high.append(df['rh1'][idx])
        else:
            ht_low.append(df['wind_sensor_height_1'][idx])
            ht_high.append(df['wind_sensor_height_2'][idx])
            ta_low.append(df['ta1'][idx])
            ta_high.append(df['ta2'][idx])
            wspd_low.append(df['wspd1'][idx])
            wspd_high.append(df['wspd2'][idx])
            rh_low.append(df['rh1'][idx])
            rh_high.append(df['rh2'][idx])

        idx += 1

    # Convert lists to arrays
    ht_low = np.asarray(ht_low)
    ht_high = np.asarray(ht_high)
    ta_low = np.asarray(ta_low)
    ta_high = np.asarray(ta_high)
    wspd_low = np.asarray(wspd_low)
    wspd_high = np.asarray(wspd_high)
    rh_low = np.asarray(rh_low)
    rh_high = np.asarray(rh_high)
    ps = np.asarray(df['ps'].values)

    # Potential Temperature
    pot_tmp_low = potential_temperature(ps * units.pascal, ta_low * units.kelvin).magnitude
    pot_tmp_high = potential_temperature(ps * units.pascal, ta_high * units.kelvin).magnitude
    pot_tmp_avg = (pot_tmp_low + pot_tmp_high)/2
    ta_avg = (ta_low + ta_high)/2

    # Ri
    du = wspd_high-wspd_low
    du = np.asarray([fillvalue if i == 0 else i for i in du])
    pot_tmp_avg = np.asarray([fillvalue if i == 0 else i for i in pot_tmp_avg])
    ri = g*(pot_tmp_high - pot_tmp_low)*(ht_high - ht_low)/(pot_tmp_avg*du)

    # Phi
    for val in ri:
        if val < -0.03:
            phi = (1-18*val)**-0.25
            phi_m.append(phi)
            phi_h.append(phi/1.3)
        elif -0.03 <= val < 0:
            phi = (1-18*val)**-0.25
            phi_m.append(phi)
            phi_h.append(phi)
        else:
            phi = (1-5.2*val)**-1
            phi_m.append(phi)
            phi_h.append(phi)

    phi_e = phi_h

    # air density
    rho = density(ps * units.pascal, ta_avg * units.kelvin, 0).magnitude  # Use average temperature

    # SH
    ht_low = np.asarray([fillvalue if i == 0 else i for i in ht_low])
    num = np.asarray([-a1 * cp * k**2 * (b1 - c1) * (d1 - e1) for a1, b1, c1, d1, e1 in
           zip(rho, pot_tmp_high, pot_tmp_low, wspd_high, wspd_low)])
    dnm = [a2 * b2 * np.log(c2 / d2)**2 for a2, b2, c2, d2 in
           zip(phi_h, phi_m, ht_high, ht_low)]
    dnm = np.asarray([fillvalue if i == 0 else i for i in dnm])
    sh = num/dnm
    sh = [fillvalue if abs(i) >= 100 else i for i in sh]

    # Specific Humidity
    mixing_ratio_low = mixing_ratio_from_relative_humidity(rh_low, ta_low * units.kelvin, ps * units.pascal)
    mixing_ratio_high = mixing_ratio_from_relative_humidity(rh_high, ta_high * units.kelvin, ps * units.pascal)
    q_low = specific_humidity_from_mixing_ratio(mixing_ratio_low).magnitude
    q_high = specific_humidity_from_mixing_ratio(mixing_ratio_high).magnitude
    q_low = q_low/100  # Divide by 100 to make it in range [0,1]
    q_high = q_high/100

    # LH
    num = np.asarray([-a1 * Lv * k**2 * (b1 - c1) * (d1 - e1) for a1, b1, c1, d1, e1 in
           zip(rho, q_high, q_low, wspd_high, wspd_low)])
    dnm = [a2 * b2 * np.log(c2 / d2)**2 for a2, b2, c2, d2 in
           zip(phi_e, phi_m, ht_high, ht_low)]
    dnm = np.asarray([fillvalue if i == 0 else i for i in dnm])
    lh = num/dnm
    lh = [fillvalue if abs(i) >= 100 else i for i in lh]

    return sh, lh


def gcnet2nc(args, input_file, output_file, stations):
    """Main function to convert GCNet ascii file to netCDF"""
    df, temperature_vars, pressure_vars = init_dataframe(args, input_file)
    station_number = df['station_number'][0]
    df.drop('station_number', axis=1, inplace=True)

    ds = xr.Dataset.from_dataframe(df)
    ds = ds.drop('time')

    # surface_temp = extrapolate_temp(df)

    common.log(args, 2, 'Retrieving latitude, longitude and station name')
    latitude, longitude, station_name = get_station(args, input_file, stations)

    common.log(args, 3, 'Calculating time and sza')
    month, day, hour, minutes, time, time_bounds, sza, az, first_date, last_date = get_time_and_sza(
        args, df, longitude, latitude)

    common.log(args, 4, 'Calculating quality control variables')
    fill_dataset_quality_control(df, ds, input_file)

    if args.flx:
        common.log(args, 5, 'Calculating Sensible and Latent Heat Fluxes')
        sh, lh = gradient_fluxes(df)
        ds['sh'] = 'time', sh
        ds['lh'] = 'time', lh

    if args.no_drv_tm:
        pass
    else:
        ds['month'] = 'time', month
        ds['day'] = 'time', day
        ds['hour'] = 'time', hour
        ds['minutes'] = 'time', minutes

    ds['time'] = 'time', time
    ds['time_bounds'] = ('time', 'nbnd'), time_bounds
    ds['sza'] = 'time', sza
    ds['az'] = 'time', az
    ds['station_number'] = tuple(), station_number
    ds['station_name'] = tuple(), station_name
    ds['latitude'] = tuple(), latitude
    ds['longitude'] = tuple(), longitude
    # ds['surface_temp'] = 'time', surface_temp

    rigb_vars = []
    if args.rigb:
        ds, rigb_vars = common.call_rigb(
            args, station_name, first_date, last_date, ds, latitude, longitude, rigb_vars)

    comp_level = args.dfl_lvl

    common.load_dataset_attributes('gcnet', ds, args, rigb_vars=rigb_vars, temperature_vars=temperature_vars,
                                   pressure_vars=pressure_vars)
    encoding = common.get_encoding('gcnet', common.get_fillvalue(args), comp_level, args)

    common.write_data(args, ds, output_file, encoding)
