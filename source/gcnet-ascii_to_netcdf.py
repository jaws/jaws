
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
station_number = root_grp.createVariable('station_number', 'u1', ('time',))
year = root_grp.createVariable('year', 'i8', ('time',))
julian_decimal_time = root_grp.createVariable('julian_decimal_time', 'f4', ('time',))
sw_down = root_grp.createVariable('sw_down', 'f4', ('time',))
sw_up = root_grp.createVariable('sw_up', 'f4', ('time',))
net_radiation = root_grp.createVariable('net_radiation', 'f4', ('time',))
temperature_tc_1 = root_grp.createVariable('temperature_tc_1', 'f4', ('time',))
temperature_tc_2 = root_grp.createVariable('temperature_tc_2', 'f4', ('time',))
temperature_cs500_1 = root_grp.createVariable('temperature_cs500_1', 'f4', ('time',))
temperature_cs500_2 = root_grp.createVariable('temperature_cs500_2', 'f4', ('time',))
relative_humidity_1 = root_grp.createVariable('relative_humidity_1', 'f4', ('time',))
relative_humidity_2 = root_grp.createVariable('relative_humidity_2', 'f4', ('time',))
u1_wind_speed = root_grp.createVariable('u1_wind_speed', 'f4', ('time',))
u2_wind_speed = root_grp.createVariable('u2_wind_speed', 'f4', ('time',))
u_direction_1 = root_grp.createVariable('u_direction_1', 'f4', ('time',))
u_direction_2 = root_grp.createVariable('u_direction_2', 'f4', ('time',))
pressure = root_grp.createVariable('pressure', 'f4', ('time',))
snow_height_1 = root_grp.createVariable('snow_height_1', 'f4', ('time',))
snow_height_2 = root_grp.createVariable('snow_height_2', 'f4', ('time',))
t_snow_01 = root_grp.createVariable('t_snow_01', 'f4', ('time',))
t_snow_02 = root_grp.createVariable('t_snow_02', 'f4', ('time',))
t_snow_03 = root_grp.createVariable('t_snow_03', 'f4', ('time',))
t_snow_04 = root_grp.createVariable('t_snow_04', 'f4', ('time',))
t_snow_05 = root_grp.createVariable('t_snow_05', 'f4', ('time',))
t_snow_06 = root_grp.createVariable('t_snow_06', 'f4', ('time',))
t_snow_07 = root_grp.createVariable('t_snow_07', 'f4', ('time',))
t_snow_08 = root_grp.createVariable('t_snow_08', 'f4', ('time',))
t_snow_09 = root_grp.createVariable('t_snow_09', 'f4', ('time',))
t_snow_10 = root_grp.createVariable('t_snow_10', 'f4', ('time',))
battery_voltage = root_grp.createVariable('battery_voltage', 'f4', ('time',))
unknown31 = root_grp.createVariable('unknown_31_rad', 'f4', ('time',))
unknown32 = root_grp.createVariable('unknown_32_rad', 'f4', ('time',))
net_radiation_max = root_grp.createVariable('net_radiation_max', 'f4', ('time',))
max_air_temperature_1 = root_grp.createVariable('max_air_temperature_1', 'f4', ('time',))
max_air_temperature_2 = root_grp.createVariable('max_air_temperature_2', 'f4', ('time',))
min_air_temperature_1 = root_grp.createVariable('min_air_temperature_1', 'f4', ('time',))
min_air_temperature_2 = root_grp.createVariable('min_air_temperature_2', 'f4', ('time',))
max_windspeed_u1 = root_grp.createVariable('max_windspeed_u1', 'f4', ('time',))
max_windspeed_u2 = root_grp.createVariable('max_windspeed_u2', 'f4', ('time',))
stdev_windspeed_u1 = root_grp.createVariable('stdev_windspeed_u1', 'f4', ('time',))
stdev_windspeed_u2 = root_grp.createVariable('stdev_windspeed_u2', 'f4', ('time',))
ref_temperature = root_grp.createVariable('ref_temperature', 'f4', ('time',))
windspeed_2m = root_grp.createVariable('windspeed_2m', 'f4', ('time',))
windspeed_10m = root_grp.createVariable('windspeed_10m', 'f4', ('time',))
wind_sensor_height_1 = root_grp.createVariable('wind_sensor_height_1', 'f4', ('time',))
wind_sensor_height_2 = root_grp.createVariable('wind_sensor_height_2', 'f4', ('time',))
albedo = root_grp.createVariable('albedo', 'f4', ('time',))
zenith_angle = root_grp.createVariable('zenith_angle', 'f4', ('time',))
qc1 = root_grp.createVariable('qc1', 'f4', ('time',))
qc9 = root_grp.createVariable('qc9', 'f4', ('time',))
qc17 = root_grp.createVariable('qc17', 'f4', ('time',))
qc25 = root_grp.createVariable('qc25', 'f4', ('time',))


time = root_grp.createVariable('time', 'f4', ('time',))


# In[5]:


#station_number.units = ''
station_number.original_var_name = 'Station Number'

#year.units = ''
year.original_var_name = 'Year'

julian_decimal_time.units = 'decimal time'
julian_decimal_time.original_var_name = 'Julian Decimal Time'
julian_decimal_time.note = 'Not really standard Julian time'

sw_down.units = 'W m-2'
sw_down.original_var_name = 'SW_down'
sw_down.long_name = 'downwelling_shortwave_flux_in_air'

sw_up.units = 'W m-2'
sw_up.original_var_name = 'SW_up'
sw_up.long_name = 'upwelling_shortwave_flux_in_air'

net_radiation.units = 'W m-2'
net_radiation.original_var_name = 'Net Radiation'
net_radiation.long_name = 'surface_net_downward_shortwave_flux'

temperature_tc_1.units = 'degC'
temperature_tc_1.original_var_name = 'TC Air 1 Air Temperature'
temperature_tc_1.long_name = 'air_temperature'

temperature_tc_2.units = 'degC'
temperature_tc_2.original_var_name = 'TC Air 2 Air Temperature'
temperature_tc_2.long_name = 'air_temperature'

temperature_cs500_1.units = 'degC'
temperature_cs500_1.original_var_name = 'CS500 T Air 1 Air Temperature'
temperature_cs500_1.long_name = 'air_temperature'

temperature_cs500_2.units = 'degC'
temperature_cs500_2.original_var_name = 'CS500 T Air 2 Air Temperature'
temperature_cs500_2.long_name = 'air_temperature'

relative_humidity_1.units = '%'
relative_humidity_1.original_var_name = 'RH 1 Relative Humidity'
relative_humidity_1.long_name = 'realtive_humidity'

relative_humidity_2.units = '%'
relative_humidity_2.original_var_name = 'RH 2 Relative Humidity'
relative_humidity_2.long_name = 'realtive_humidity'

u1_wind_speed.units = 'm/s'
u1_wind_speed.original_var_name = 'U1 Wind Speed'
u1_wind_speed.long_name = 'wind_speed'

u2_wind_speed.units = 'm/s'
u2_wind_speed.original_var_name = 'U2 Wind Speed'
u2_wind_speed.long_name = 'wind_speed'

u_direction_1.units = 'deg'
u_direction_1.original_var_name = 'U Dir 1'
u_direction_1.long_name = ''

u_direction_2.units = 'deg'
u_direction_2.original_var_name = 'U Dir 2'
u_direction_2.long_name = ''

pressure.units = 'mbar'
pressure.original_var_name = 'Atmos Pressure'
pressure.long_name = 'surface_air_pressure'

snow_height_1.units = 'm'
snow_height_1.original_var_name = 'Snow Height 1'
snow_height_1.long_name = 'surface_snow_thickness'

snow_height_2.units = 'm'
snow_height_2.original_var_name = 'Snow Height 2'
snow_height_2.long_name = 'surface_snow_thickness'

t_snow_01.units = 'degC'
t_snow_01.original_var_name = 'T Snow 1'
t_snow_01.long_name = 'temperature_in_surface_snow'

t_snow_02.units = 'degC'
t_snow_02.original_var_name = 'T Snow 2'
t_snow_02.long_name = 'temperature_in_surface_snow'

t_snow_03.units = 'degC'
t_snow_03.original_var_name = 'T Snow 3'
t_snow_03.long_name = 'temperature_in_surface_snow'

t_snow_04.units = 'degC'
t_snow_04.original_var_name = 'T Snow 4'
t_snow_04.long_name = 'temperature_in_surface_snow'

t_snow_05.units = 'degC'
t_snow_05.original_var_name = 'T Snow 5'
t_snow_05.long_name = 'temperature_in_surface_snow'

t_snow_06.units = 'degC'
t_snow_06.original_var_name = 'T Snow 6'
t_snow_06.long_name = 'temperature_in_surface_snow'

t_snow_07.units = 'degC'
t_snow_07.original_var_name = 'T Snow 7'
t_snow_07.long_name = 'temperature_in_surface_snow'

t_snow_08.units = 'degC'
t_snow_08.original_var_name = 'T Snow 8'
t_snow_08.long_name = 'temperature_in_surface_snow'

t_snow_09.units = 'degC'
t_snow_09.original_var_name = 'T Snow 9'
t_snow_09.long_name = 'temperature_in_surface_snow'

t_snow_10.units = 'degC'
t_snow_10.original_var_name = 'T Snow 10'
t_snow_10.long_name = 'temperature_in_surface_snow'

battery_voltage.units = 'V'
battery_voltage.original_var_name = 'Battery Voltage'
battery_voltage.long_name = 'battery_voltage'

unknown31.units = 'W m-2'
unknown31.original_var_name = 'N/A'
unknown31.long_name = 'N/A'

unknown32.units = 'W m-2'
unknown32.original_var_name = 'N/A'
unknown32.long_name = 'N/A'

net_radiation_max.units = 'W m-2'
net_radiation_max.original_var_name = 'NetRadMax'
net_radiation_max.long_name = 'net_radiation_maximum'

max_air_temperature_1.units = 'degC'
max_air_temperature_1.original_var_name = 'Max Air Temperture 1'
max_air_temperature_1.long_name = 'air_temperature'

max_air_temperature_2.units = 'degC'
max_air_temperature_2.original_var_name = 'Max Air Temperture 2'
max_air_temperature_2.long_name = 'air_temperature'

min_air_temperature_1.units = 'degC'
min_air_temperature_1.original_var_name = 'Min Air Temperture 1'
min_air_temperature_1.long_name = 'air_temperature'

min_air_temperature_2.units = 'degC'
min_air_temperature_2.original_var_name = 'Min Air Temperture 2'
min_air_temperature_2.long_name = 'air_temperature'

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

wind_sensor_height_1.units = 'm'
wind_sensor_height_1.original_var_name = 'WindSensorHeight1'
wind_sensor_height_1.long_name = 'n/a'

wind_sensor_height_2.units = 'm'
wind_sensor_height_2.original_var_name = 'WindSensorHeight2'
wind_sensor_height_2.long_name = 'n/a'

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
    station_number[i] = columns[0]
    year[i] = columns[1]
    julian_decimal_time[i] = columns[2]
    sw_down[i] = columns[3]
    sw_up[i] = columns[4]
    net_radiation[i] = columns[5]
    temperature_tc_1[i] = columns[6]
    temperature_tc_2[i] = columns[7]
    temperature_cs500_1[i] = columns[8]
    temperature_cs500_2[i] = columns[9]
    relative_humidity_1[i] = columns[10]
    relative_humidity_2[i] = columns[11]
    u1_wind_speed[i] = columns[12]
    u2_wind_speed[i] = columns[13]
    u_direction_1[i] = columns[14]
    u_direction_2[i] = columns[15]
    pressure[i] = columns[16]
    snow_height_1[i] = columns[17]
    snow_height_2[i] = columns[18]
    t_snow_01[i] = columns[19]
    t_snow_02[i] = columns[20]
    t_snow_03[i] = columns[21]
    t_snow_04[i] = columns[22]
    t_snow_05[i] = columns[23]
    t_snow_06[i] = columns[24]
    t_snow_07[i] = columns[25]
    t_snow_08[i] = columns[26]
    t_snow_09[i] = columns[27]
    t_snow_10[i] = columns[28]
    battery_voltage[i] = columns[29]
    unknown31[i] = columns[30]
    unknown32[i] = columns[31]
    net_radiation_max[i] = columns[32]
    max_air_temperature_1[i] = columns[33]
    max_air_temperature_2[i] = columns[34]
    min_air_temperature_1[i] = columns[35]
    min_air_temperature_2[i] = columns[36]
    max_windspeed_u1[i] = columns[37]
    max_windspeed_u2[i] = columns[38]
    stdev_windspeed_u1[i] = columns[39]
    stdev_windspeed_u2[i] = columns[40]
    ref_temperature[i] = columns[41]
    windspeed_2m[i] = columns[42]
    windspeed_10m[i] = columns[43]
    wind_sensor_height_1[i] = columns[44]
    wind_sensor_height_2[i] = columns[45]
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
for item in julian_decimal_time:
    time[k] = offset + int(julian_decimal_time[k])
    k += 1


# In[8]:


root_grp.close()

