#!/usr/bin/python
# encoding=utf-8

from library import lnetatmo
from library import lametric
from library import SunriseSunset
import os
import datetime
import time
import json
import logging
import ConfigParser

# Netatmo / LaMetric Proxy
# Author : Stanislav Likavcan, likavcan@gmail.com

# A simple client which turns LaMetric into Netamo display. This client calls Netatmo API and updates LaMetric display 
# Easiest way to keep the LaMetric display updated is via cron task:
# */10 * * * * /home/lametric/updateLaMetric.py
# Don't forget to create an app within both Netatmo and LaMetric (credentials are in the file config.ini)

# Load the config.ini file
path = os.path.dirname(__file__)
config = ConfigParser.ConfigParser()
config.read(path + '/config.ini')

# Configure logging
loglevel = config.get('general','loglevel')
numeric_level = getattr(logging, loglevel.upper(), None)
logging.basicConfig(format='%(levelname)s: %(message)s',level=numeric_level)

# Netatmo authentication
client_id     = config.get('netatmo','client_id')
client_secret = config.get('netatmo','client_secret')
username      = config.get('netatmo','username')
password      = config.get('netatmo','password')
logging.debug('Netatmo credentials: %s', config.items('netatmo'))

# LaMetric authentication
access_token  = config.get('lametric','access_token')
app_id        = config.get('lametric','app_id')
logging.debug('LaMetric credentials: %s', config.items('lametric'))

# Display preferences
temp_units    = config.get('general','temperature_units')

# Use Celsius unless the config file is attempting to set things to Farenheit
temp_units = 'C' if temp_units[0].upper() != 'F' else 'F'

# Initiate Netatmo client
authorization = lnetatmo.ClientAuth(client_id, client_secret, username, password)
devList = lnetatmo.DeviceList(authorization)
theData = devList.lastData()
logging.debug('Netatmo data: %s', theData)

# Netatmo station GPS coordinates
longitude, latitude = devList.locationData()['location']
logging.info('Station coordinates are latitude: %s, longitude: %s', latitude, longitude)

# Determine the local TZ offset to GMT
localOffset = int(time.strftime('%z')[:3])
localTZ = time.strftime('%Z')
logging.info('Local TZ is %s. The offset to GMT is %s hour(s)', localTZ, localOffset)

# Calculate sunrise and sunset time based on location and TZ
ro = SunriseSunset.Setup(datetime.datetime.now(), latitude, longitude, localOffset)
rise_time, set_time = ro.calculate()
logging.info('Sunrise is %s and Sunset at %s', rise_time.strftime("%H:%M"), set_time.strftime("%H:%M"))

for module in theData.keys():
    m_id = theData[module]['id']
    m_type = theData[module]['type']
    m_data_type = theData[module]['data_type']
    m_data = ', '.join(m_data_type)
    if (m_type == 'NAMain'):
        station_name = module
        station_id   = m_id
        logging.info('Station: %s [%s] %s with features: %s', module, m_id, m_type, m_data)
    elif (m_type == 'NAModule1' and 'CO2' not in m_data_type):
        module_name = module
        module_id   = m_id
        logging.info('Module: %s [%s] %s with features: %s', module, m_id, m_type, m_data)
    else:
        logging.warning('Other: %s [%s] %s with features: %s', module, m_id, m_type, m_data)

# Retrieve data from midnight until now
#today = time.strftime("%Y-%m-%d")
#today = int(time.mktime(time.strptime(today,"%Y-%m-%d")))

# Retrieve data for last 36hours (LaMetric display is 36x8 pixels)
now = time.time();
last_day  = now - 36 * 3600;

measure = devList.getMeasure(station_id, '1hour', 'Temperature', module_id, date_begin = last_day, date_end = now, optimize = True)

# Convert temperature values returned by Netatmo to simple field
hist_temp = [int(round(v[0],0)) for v in measure['body'][0]['value']]

# Retrieve current sensor data
outdoor = {}

indoorTemp = theData[station_name]['Temperature']
outdoorTemp = theData[module_name]['Temperature']

# Convert to Farenheit as needed
if temp_units == 'F' :
    indoorTemp  = indoorTemp  * 1.8 + 32
    outdoorTemp = outdoorTemp * 1.8 + 32

outdoor['temperature'] = str(outdoorTemp) + "°" + temp_units
outdoor['humidity']    = str(theData[module_name]['Humidity'])+'%'
outdoor['pressure']    = str(theData[station_name]['Pressure'])+'mb'
outdoor['trend']       = str(theData[station_name]['pressure_trend'])
logging.debug('Outdoor metrics: %s', outdoor)

# Icons definition
icon = {'temp': 'i2355', 'tempC': 'i2056', 'humi': 'i863', 'stable': 'i401', 'up': 'i120', 'down': 'i124', 'sunrise': 'a485', 'sunset': 'a486'}

time_format = config.get('general','time_format')

# Finally, post the data to LaMetric
lametric = lametric.Setup()
lametric.addTextFrame(icon['temp'],outdoor['temperature'])
lametric.addSparklineFrame(hist_temp)
lametric.addTextFrame(icon['humi'],outdoor['humidity'])
lametric.addTextFrame(icon[outdoor['trend']],outdoor['pressure'])
lametric.addTextFrame(icon['sunrise'],rise_time.strftime(time_format))
lametric.addTextFrame(icon['sunset'],set_time.strftime(time_format))
lametric.push(app_id, access_token)
exit()
