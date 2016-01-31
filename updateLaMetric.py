#!/usr/bin/python
# encoding=utf-8

from library import lnetatmo
from library import lametric
from library import SunriseSunset
import datetime
import time
import json

# Netatmo / LaMetric Proxy
# Author : Stanislav Likavcan, likavcan@gmail.com

# A simple client which turns LaMetric into Netamo display. This client calls Netatmo API and updates LaMetric display 
# Easiest way to keep the LaMetric display updated is via cron task:
# */10 * * * * /home/lametric/updateLaMetric.py
# Don't forget to create an app within both Netatmo and LaMetric and provide your credentials here:

######################## USER SPECIFIC INFORMATION ######################

# Netatmo authentication
client_id     = '...' 
client_secret = '...' 
username      = '...' 
password      = '...' 

# LaMetric authentication
access_token  = '...'
app_id        = '...'

#########################################################################

# Initiate Netatmo client
authorization = lnetatmo.ClientAuth(client_id, client_secret, username, password)
devList = lnetatmo.DeviceList(authorization)
theData = devList.lastData()

# Location GPS coordinates from Netatmo
lng, lat = devList.locationData()['location']

ro = SunriseSunset.Setup(datetime.datetime.now(), latitude=lat, longitude=lng, localOffset = 1)
rise_time, set_time = ro.calculate()

for module in theData.keys():
    data_type = theData[module]['data_type']
    if (theData[module]['type'] == 'NAMain'):
        device_name = module
        device_id   = theData[module]['id']
        device_type = ', '.join(data_type)
        print "Detected station: %s '%s' - %s" % (device_id, device_name, device_type)
    elif (theData[module]['type'] == 'NAModule1'):
        module_name = module
        module_id   = theData[module]['id']
        module_type = ', '.join(data_type)
        print "Detected module : %s '%s' - %s" % (module_id, module_name, module_type)
    else:
        m_name = module
        m_id   = theData[module]['id']
        m_type = ', '.join(data_type)
        print "Detected other  : %s '%s' - %s" % (m_id, m_name, m_type)

now   = time.time();
# Retrieve data from midnight until now
#today = time.strftime("%Y-%m-%d")
#today = int(time.mktime(time.strptime(today,"%Y-%m-%d")))
# Retrieve data for last 24hours
last_day  = now - 36 * 3600;

measure = devList.getMeasure(device_id, '1hour', 'Temperature', module_id, date_begin = last_day, date_end = now, optimize = True)

# Convert temperature values returned by Netatmo to simple field
hist_temp = [v[0] for v in measure['body'][0]['value']]

# Retrieve current sensor data
outdoor = {}
outdoor['temperature'] = str(theData[module_name]['Temperature'])+"°C"
outdoor['humidity']    = str(theData[module_name]['Humidity'])+'%'
outdoor['pressure']    = str(theData[device_name]['Pressure'])+'mb'
outdoor['trend']       = str(theData[device_name]['pressure_trend'])

print outdoor

# Icons definition
icon = {'temp': 'i2056', 'humi': 'i863', 'stable': 'i401', 'up': 'i120', 'down': 'i124', 'sunrise': 'a485', 'sunset': 'a486'}

# Post data to LaMetric
lametric = lametric.Setup()
lametric.addTextFrame(icon['temp'],outdoor['temperature'])
lametric.addSparklineFrame(hist_temp)
lametric.addTextFrame(icon['humi'],outdoor['humidity'])
lametric.addTextFrame(icon[outdoor['trend']],outdoor['pressure'])
lametric.addTextFrame(icon['sunrise'],rise_time.strftime("%H:%M"))
lametric.addTextFrame(icon['sunset'],set_time.strftime("%H:%M"))
lametric.push(app_id, access_token)
