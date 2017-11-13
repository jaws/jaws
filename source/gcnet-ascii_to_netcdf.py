
# coding: utf-8

# In[1]:


from netCDF4 import Dataset
import numpy as np


# In[2]:


# NC file setup
root_grp = Dataset('ascii.nc', 'w', format='NETCDF4')
root_grp.TITLE = 'Surface Radiation Data from Greenland Climate Network'
root_grp.SOURCE = 'Surface Observations'
root_grp.INSTITUTION = 'Cooperative Institute for Research in Enviornmental Sciences'
root_grp.REFERENCE = 'http://cires.colorado.edu/science/groups/steffen/gcnet/'
root_grp.URL = 'http://cires.colorado.edu/science/groups/steffen/gcnet/'
#root_grp.History = 'Created on '
#root_grp.CREATED_BY = 'Created by'
root_grp.Conventions = 'CF-v46'


# In[3]:


# dimension
root_grp.createDimension('time', 12183)


# In[4]:


# variables
station = root_grp.createVariable('station', 'u1', ('time',))
year = root_grp.createVariable('year', 'i8', ('time',))
julian_time = root_grp.createVariable('jdtime', 'f4', ('time',))
sw_down = root_grp.createVariable('sw_down', 'f4', ('time',))
sw_up = root_grp.createVariable('sw_up', 'f4', ('time',))
net_radiation = root_grp.createVariable('netrad', 'f4', ('time',))
tc_air_temperature1 = root_grp.createVariable('tc_airtemp1', 'f4', ('time',))
tc_air_temperature2 = root_grp.createVariable('tc_airtemp2', 'f4', ('time',))
cs500_air_temperature1 = root_grp.createVariable('cs500_airtemp1', 'f4', ('time',))
cs500_air_temperature2 = root_grp.createVariable('cs500_airtemp2', 'f4', ('time',))
relative_humidity1 = root_grp.createVariable('rh1', 'f4', ('time',))
relative_humidity2 = root_grp.createVariable('rh2', 'f4', ('time',))
u1_wind_speed = root_grp.createVariable('u1_windspeed', 'f4', ('time',))
u2_wind_speed = root_grp.createVariable('u2_windspeed', 'f4', ('time',))
u_direction1 = root_grp.createVariable('udir1', 'f4', ('time',))
u_direction2 = root_grp.createVariable('udir2', 'f4', ('time',))
atmospheric_pressure = root_grp.createVariable('atmos_press', 'f4', ('time',))
snow_height1 = root_grp.createVariable('snow_height1', 'f4', ('time',))
snow_height2 = root_grp.createVariable('snow_height2', 'f4', ('time',))
tsnow1 = root_grp.createVariable('tsnow1', 'f4', ('time',))
tsnow2 = root_grp.createVariable('tsnow2', 'f4', ('time',))
tsnow3 = root_grp.createVariable('tsnow3', 'f4', ('time',))
tsnow4 = root_grp.createVariable('tsnow4', 'f4', ('time',))
tsnow5 = root_grp.createVariable('tsnow5', 'f4', ('time',))
tsnow6 = root_grp.createVariable('tsnow6', 'f4', ('time',))
tsnow7 = root_grp.createVariable('tsnow7', 'f4', ('time',))
tsnow8 = root_grp.createVariable('tsnow8', 'f4', ('time',))
tsnow9 = root_grp.createVariable('tsnow9', 'f4', ('time',))
tsnow10 = root_grp.createVariable('tsnow10', 'f4', ('time',))
battery_voltage = root_grp.createVariable('bat_volt', 'f4', ('time',))
unknown31 = root_grp.createVariable('unknown_31_rad', 'f4', ('time',))
unknown32 = root_grp.createVariable('unknown_32_rad', 'f4', ('time',))
netradmax = root_grp.createVariable('netradmax', 'f4', ('time',))
max_air_temperature1 = root_grp.createVariable('max_airtemp1', 'f4', ('time',))
max_air_temperature2 = root_grp.createVariable('max_airtemp2', 'f4', ('time',))
min_air_temperature1 = root_grp.createVariable('min_airtemp1', 'f4', ('time',))
min_air_temperature2 = root_grp.createVariable('min_airtemp2', 'f4', ('time',))
max_windspeed_u1 = root_grp.createVariable('max_wind1', 'f4', ('time',))
max_windspeed_u2 = root_grp.createVariable('max_wind2', 'f4', ('time',))
stdev_windspeed_u1 = root_grp.createVariable('sd_wind1', 'f4', ('time',))
stdev_windspeed_u2 = root_grp.createVariable('sd_wind2', 'f4', ('time',))
ref_temperature = root_grp.createVariable('refrence_temp', 'f4', ('time',))
windspeed_2m = root_grp.createVariable('windspeed2m', 'f4', ('time',))
windspeed_10m = root_grp.createVariable('windspeed10m', 'f4', ('time',))
wind_sensor_height1 = root_grp.createVariable('windsensor_ht1', 'f4', ('time',))
wind_sensor_height2 = root_grp.createVariable('windsensor_ht2', 'f4', ('time',))
albedo = root_grp.createVariable('albedo', 'f4', ('time',))
zenith_angle = root_grp.createVariable('zenith_angle', 'f4', ('time',))
qc1 = root_grp.createVariable('qc1', 'f4', ('time',))
qc9 = root_grp.createVariable('qc9', 'f4', ('time',))
qc17 = root_grp.createVariable('qc17', 'f4', ('time',))
qc25 = root_grp.createVariable('qc25', 'f4', ('time',))


time = root_grp.createVariable('time', 'f4', ('time',))


# In[5]:


#station.units = ''
station.original_var_name = 'station_number'

#year.units = ''
year.original_var_name = 'Year'

julian_time.units = 'decimal time'
julian_time.original_var_name = 'Julian Decimal Time'
julian_time.note = 'Not really standard Julian time'

sw_down.units = 'W m-2'
sw_down.original_var_name = 'SW_down'
sw_down.long_name = 'downwelling_shortwave_flux_in_air'

sw_up.units = 'W m-2'
sw_up.original_var_name = 'SW_up'
sw_up.long_name = 'upwelling_shortwave_flux_in_air'

net_radiation.units = 'W m-2'
net_radiation.original_var_name = 'Net Radiation'
net_radiation.long_name = 'surface_net_downward_shortwave_flux'

tc_air_temperature1.units = 'degC'
tc_air_temperature1.original_var_name = 'TC Air 1 G Air Temperature'
tc_air_temperature1.long_name = 'air_temperature'

tc_air_temperature2.units = 'degC'
tc_air_temperature2.original_var_name = 'TC Air 2 H Air Temperature'
tc_air_temperature2.long_name = 'air_temperature'

cs500_air_temperature1.units = 'degC'
cs500_air_temperature1.original_var_name = 'CS500 T Air 1 I Air Temperature'
cs500_air_temperature1.long_name = 'air_temperature'

cs500_air_temperature2.units = 'degC'
cs500_air_temperature2.original_var_name = 'CS500 T Air 2 J Air Temperature'
cs500_air_temperature2.long_name = 'air_temperature'

relative_humidity1.units = '%'
relative_humidity1.original_var_name = 'RH 1 K Relative Humidity'
relative_humidity1.long_name = 'realtive_humidity'

relative_humidity2.units = '%'
relative_humidity2.original_var_name = 'RH 2 L Relative Humidity'
relative_humidity2.long_name = 'realtive_humidity'

u1_wind_speed.units = 'm/s'
u1_wind_speed.long_name = 'U1 Wind Speed'

u2_wind_speed.units = 'm/s'
u2_wind_speed.long_name = 'U2 Wind Speed'

u_direction1.units = 'deg'
u_direction1.long_name = 'U Dir 1'

u_direction2.units = 'deg'
u_direction2.long_name = 'U Dir 2'

atmospheric_pressure.units = 'mbar'
atmospheric_pressure.long_name = 'Atmospheric Pressure'

snow_height1.units = 'm'
snow_height1.long_name = 'Snow Height 1'

snow_height2.units = 'm'
snow_height2.long_name = 'Snow Height 2'

tsnow1.units = 'degC'
tsnow1.long_name = 'T Snow 1'

tsnow2.units = 'degC'
tsnow2.long_name = 'T Snow 2'

tsnow3.units = 'degC'
tsnow3.long_name = 'T Snow 3'

tsnow4.units = 'degC'
tsnow4.long_name = 'T Snow 4'

tsnow5.units = 'degC'
tsnow5.long_name = 'T Snow 5'

tsnow6.units = 'degC'
tsnow6.long_name = 'T Snow 6'

tsnow7.units = 'degC'
tsnow7.long_name = 'T Snow 7'

tsnow8.units = 'degC'
tsnow8.long_name = 'T Snow 8'

tsnow9.units = 'degC'
tsnow9.long_name = 'T Snow 9'

tsnow10.units = 'degC'
tsnow10.long_name = 'T Snow 10'

battery_voltage.units = 'V'
battery_voltage.long_name = 'Battery Voltage'

unknown31.units = 'W m-2'
unknown31.long_name = 'N/A'

unknown32.units = 'W m-2'
unknown32.long_name = 'N/A'

netradmax.units = 'W m-2'
netradmax.long_name = 'Net Radiation Max'

max_air_temperature1.units = 'degC'
max_air_temperature1.long_name = 'Max Air Temperture 1'

max_air_temperature2.units = 'degC'
max_air_temperature2.long_name = 'Max Air Temperture 2'

min_air_temperature1.units = 'degC'
min_air_temperature1.long_name = 'Min Air Temperture 1'

min_air_temperature2.units = 'degC'
min_air_temperature2.long_name = 'Min Air Temperture 2'

max_windspeed_u1.units = 'm/s'
max_windspeed_u1.original_var_name = 'Max Windspeed-U1'
max_windspeed_u1.long_name = 'wind_speed'

max_windspeed_u2.units = 'm/s'
max_windspeed_u2.original_var_name = 'Max Windspeed-U2'
max_windspeed_u2.long_name = 'wind_speed'

stdev_windspeed_u1.units = 'm/s'
stdev_windspeed_u1.original_var_name = 'StdDev Windspeed-U1'
stdev_windspeed_u1.long_name = 'wind_speed'

stdev_windspeed_u2.units = 'm/s'
stdev_windspeed_u2.original_var_name = 'StdDev Windspeed-U2'
stdev_windspeed_u2.long_name = 'wind_speed'

ref_temperature.units = 'degC'
ref_temperature.original_var_name = 'Ref Temperature'
ref_temperature.note = 'Need to ask network manager about long name'

windspeed_2m.units = 'm/s'
windspeed_2m.original_var_name = 'Windspeed@2m'
windspeed_2m.long_name = 'wind_speed'

windspeed_10m.units = 'm/s'
windspeed_10m.original_var_name = 'Windspeed@10m'
windspeed_10m.long_name = 'wind_speed'

wind_sensor_height1.units = 'm'
wind_sensor_height2.original_var_name = 'WindSensorHeight1'
wind_sensor_height2.long_name = 'n/a'

wind_sensor_height2.units = 'm'
wind_sensor_height2.original_var_name = 'WindSensorHeight2'
wind_sensor_height2.long_name = 'n/a'

albedo.units = '1'
albedo.original_var_name = 'Albedo'
albedo.long_name = 'surface_albedo'

zenith_angle.units = 'deg'
zenith_angle.original_var_name = 'Zenith Angle'
zenith_angle.long_name = 'solar_zenith_angle'

#qc1.units = ''
qc1.original_var_name = 'QCl01-08'

#qc9.units = ''
qc9.original_var_name = 'QCl09-16'

#qc17.units = ''
qc17.original_var_name = 'QCl17-24'

#qc25.units = ''
qc25.original_var_name = 'QCl25-27'

time.units = 'days since 1995-01-01 00:00:00'
time.long_name = 'time'
time.calendar = 'noleap'
time.bounds = 'time_bnds'
time.note = 'Created new derived variable'


# In[6]:


j = 0
f = open('aist_gcnet.txt', 'r')

while j < 54:
    f.readline()
    j += 1

i = 0
for line in f:
    line = line.strip()
    columns = line.split()
    station[i] = columns[0]
    year[i] = columns[1]
    julian_time[i] = columns[2]
    sw_down[i] = columns[3]
    sw_up[i] = columns[4]
    net_radiation[i] = columns[5]
    tc_air_temperature1[i] = columns[6]
    tc_air_temperature2[i] = columns[7]
    cs500_air_temperature1[i] = columns[8]
    cs500_air_temperature2[i] = columns[9]
    relative_humidity1[i] = columns[10]
    relative_humidity2[i] = columns[11]
    u1_wind_speed[i] = columns[12]
    u2_wind_speed[i] = columns[13]
    u_direction1[i] = columns[14]
    u_direction2[i] = columns[15]
    atmospheric_pressure[i] = columns[16]
    snow_height1[i] = columns[17]
    snow_height2[i] = columns[18]
    tsnow1[i] = columns[19]
    tsnow2[i] = columns[20]
    tsnow3[i] = columns[21]
    tsnow4[i] = columns[22]
    tsnow5[i] = columns[23]
    tsnow6[i] = columns[24]
    tsnow7[i] = columns[25]
    tsnow8[i] = columns[26]
    tsnow9[i] = columns[27]
    tsnow10[i] = columns[28]
    battery_voltage[i] = columns[29]
    unknown31[i] = columns[30]
    unknown32[i] = columns[31]
    netradmax[i] = columns[32]
    max_air_temperature1[i] = columns[33]
    max_air_temperature2[i] = columns[34]
    min_air_temperature1[i] = columns[35]
    min_air_temperature2[i] = columns[36]
    max_windspeed_u1[i] = columns[37]
    max_windspeed_u2[i] = columns[38]
    stdev_windspeed_u1[i] = columns[39]
    stdev_windspeed_u2[i] = columns[40]
    ref_temperature[i] = columns[41]
    windspeed_2m[i] = columns[42]
    windspeed_10m[i] = columns[43]
    wind_sensor_height1[i] = columns[44]
    wind_sensor_height2[i] = columns[45]
    albedo[i] = columns[46]
    zenith_angle[i] = columns[47]
    qc1[i] = columns[48]
    qc9[i] = columns[49]
    qc17[i] = columns[50]
    qc25[i] = columns[51]
    i+= 1


# In[7]:


from datetime import date

d0 = date(1995, 1, 1)
d1 = date(2012, 12, 31)
offset = (d1 - d0).days

k = 0
for item in julian_time:
    time[k] = offset + int(julian_time[k])
    k += 1


# In[8]:


root_grp.close()

