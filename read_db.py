#!/usr/bin/env python

# mysql -u root -p = root
# mysql -u monitor -p, password=password
# mysql> use temps
# mysql> show tables
#mysql> SHOW COLUMNS FROM tempdat
#+----------+---------------+------+-----+---------+-------+
#| Field    | Type          | Null | Key | Default | Extra |
#+----------+---------------+------+-----+---------+-------+
#| tdate    | date          | YES  |     | NULL    |       |
#| ttime    | time          | YES  |     | NULL    |       |
#| zone     | text          | YES  |     | NULL    |       |
#| temp1    | decimal(10,0) | YES  |     | NULL    |       |
#| temp2    | decimal(10,0) | YES  |     | NULL    |       |
#| pressure | decimal(10,0) | YES  |     | NULL    |       |
#| humidity | decimal(10,0) | YES  |     | NULL    |       |
#+----------+---------------+------+-----+---------+-------+
# $ mysql -u monitor -p

import MySQLdb
import matplotlib.pyplot as plt
import datetime

db = MySQLdb.connect("localhost", "monitor", "password", "temps")
curs=db.cursor()


#with db:
#    curs.execute ("""INSERT INTO tempdat
#            values(CURRENT_DATE() - INTERVAL 1 DAY, NOW(), 75.1, 78.2, 25.2, 80)""")
#    curs.execute ("""INSERT INTO tempdat 
#            values(CURRENT_DATE() - INTERVAL 1 DAY, NOW(), 24.5, 34.5, 26.3, 75)""")

#curs.execute ("SELECT * FROM tempdat")

#print "\nDate            Time        Temp1   Temp2  Pressure  Humidity"
#print "======================================================="

#for reading in curs.fetchall():
#    print str(reading[0])+"	"+str(reading[1])+"    "+\
#        str(reading[2])+"      "+str(reading[3])+"     "+\
#        str(reading[4])+"       "+str(reading[5])

dates = []
times = []
temp1 = []
pressure = []
humidity = []
dattime = []

curs.execute ("SELECT tdate,ttime,temp1,pressure,humidity FROM tempdat")

print "\nDate            Time        Temp1   Temp2  Pressure  Humidity"
print "======================================================="

for reading in curs.fetchall():
    dates.append(reading[0])
    times.append(reading[1])
    temp1.append(reading[2])
    pressure.append(reading[3])
    humidity.append(reading[4])
    dt = datetime.datetime.combine(reading[0], datetime.time(0))+reading[1]
    print dt
    dattime.append(dt)
    
    
#times = [datetime.timedelta(0, 75061), datetime.timedelta(0, 75091), datetime.timedelta(0, 75122)]
#times = [datetime.datetime.now() + datetime.timedelta(hours=i) for i in range(3)]
#temp1 = [35,16,44]

print dattime
print times
print temp1

#plt.figure()
plt.plot(dattime, temp1,'r-')
plt.plot(dattime, pressure,'b-')

plt.show()

db.close()
