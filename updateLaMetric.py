#!/usr/bin/python
# encoding=utf-8

from library import lnetatmo
from library import lametric
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

# Obtain station and module names plus MAC addresses
for module in theData.keys():
    if 'Pressure' in theData[module]['data_type']:
        device_name = module
        device_id = theData[module]['id']
        print "Detected station module: %s '%s'" % (device_id, device_name)
    else:
        module_name = module
        module_id   = theData[module]['id']
        print "Detected outdoor module: %s '%s'" % (module_id, module_name)

######################## USER SPECIFIC INFORMATION ######################
# In case you have multiple Netatmo stations or external modules the above code migh fail
# You can always provide your Netatmo specific IDs/MACs below
#device_id   = '...' # Station MAC
#device_name = '...' # Station name
#module_id   = '...' # Outdoor module MAC
#module_name = '...' # Outdoor module name
#########################################################################

# Retrieve 30min data from midnight until now
now   = time.time();
today = time.strftime("%Y-%m-%d")
today = int(time.mktime(time.strptime(today,"%Y-%m-%d")))
measure = devList.getMeasure(device_id, '30min', 'Temperature', module_id, date_begin = today, date_end = now, optimize = True)

# Convert temperature values returned by Netatmo to a simple list
hist_temp = [v[0] for v in measure['body'][0]['value']]

# Retrieve current sensors data
outdoor_temp   = str(theData[module_name]['Temperature'])+"°C"
outdoor_humi   = str(theData[module_name]['Humidity'])+'%'
pressure_value = str(theData[device_name]['Pressure'])+'mbar'
pressure_trend = str(theData[device_name]['pressure_trend'])

# Icons definition
icon = {'temp': 'i2056', 'humi': 'i863', 'stable': 'i401', 'up': 'i120', 'down': 'i124'}

# Post data to LaMetric
lametric = lametric.Setup()
lametric.addTextFrame(icon['temp'],outdoor_temp)
lametric.addSparklineFrame(hist_temp)
lametric.addTextFrame(icon['humi'],outdoor_humi)
lametric.addTextFrame(icon[pressure_trend],pressure_value)
lametric.push(app_id, access_token)
