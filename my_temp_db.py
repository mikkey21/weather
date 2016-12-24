#!/usr/bin/python

# Google Spreadsheet DHT Sensor Data-logging Example

# Depends on the 'gspread' and 'oauth2client' package being installed.  If you 
# have pip installed execute:
#   sudo pip install gspread oauth2client

# Also it's _very important_ on the Raspberry Pi to install the python-openssl
# package because the version of Python is a bit old and can fail with Google's
# new OAuth2 based authentication.  Run the following command to install the
# the package:
#   sudo apt-get update
#   sudo apt-get install python-openssl

# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import json
import sys
import time
import datetime

import Adafruit_BMP.BMP085 as BMP085
import Adafruit_DHT

import MySQLdb


# Type of sensor, can be Adafruit_DHT.DHT11, Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
DHT_TYPE = Adafruit_DHT.DHT11

# Example of sensor connected to Raspberry Pi pin 23
DHT_PIN  = 4
# Example of sensor connected to Beaglebone Black pin P8_11
#DHT_PIN  = 'P8_11'


# How long to wait (in seconds) between measurements.
FREQUENCY_SECONDS      = 1800


db = MySQLdb.connect("localhost", "monitor", "password", "temps")
curs=db.cursor()


# Create sensor instance with default I2C bus (On Raspberry Pi either 0 or
# 1 based on the revision, on Beaglebone Black default to 1).
bmp = BMP085.BMP085()
# initialize some float values for humidity and temp2 to work around None value problem below
temp2 = 0.0
humidity = 0.0

print 'Logging sensor measurements to tempdat  every {0} seconds.'.format(FREQUENCY_SECONDS)
print 'Press Ctrl-C to quit.'

while True:
        print 'Time:       ',datetime.datetime.now()
                
	# Attempt to get sensor readings.
	temp = bmp.read_temperature()
	pressure = bmp.read_pressure()
	altitude = bmp.read_altitude()
        temp_f = (temp*9)/5+32
	print 'Temperature: {0:0.1f} C'.format(temp_f)
	print 'Pressure:    {0:0.1f} Pa'.format(pressure)
	print 'Altitude:    {0:0.1f} m'.format(altitude)

	# Attempt to get sensor reading.
        # check if DHT read returned floating type values as expected
        # otherwise use the old values of temp and humidity
        # sometimes it seems to return a string type 'None'
	new_humidity, new_temp2 = Adafruit_DHT.read(DHT_TYPE, DHT_PIN) 
        if (isinstance(new_temp2,float) and isinstance(new_humidity,float)):
           temp2 = new_temp2
           humidity = new_humidity
        
        print 'temp2C: ',format(temp2)
        print 'humidity:    {0:0.1f} %'.format(humidity)
        temp2_f = (temp2*9)/5+32
	print 'Temp2F: {0:0.1f} F'.format(temp2_f)

        my_str = "(CURRENT_DATE(), NOW(), "+str(temp_f)+", "+str(temp2_f)+", "+str(humidity)+", "+str(pressure)+")"
        print my_str
        
	# Append the data in the spreadsheet, including a timestamp
        with db:
#                curs.execute ("""INSERT INTO tempdat
#                values(%s""", [my_str])

                curs.execute ("""INSERT INTO tempdat
                values(CURRENT_DATE(), NOW(), %s, %s, %s, %s)""",
                              (str(temp_f), str(temp2_f), str(humidity), str(pressure)))


#                curs.execute ("""INSERT INTO tempdat
#                values(CURRENT_DATE(), NOW(), %(temp_f)s, %(temp2_f)s, %(humidity)s, %(pressure)s""",
#                [temp_f)


                
	# Wait 30 seconds before continuing
	print "Added an entry in the database"
	time.sleep(FREQUENCY_SECONDS)
