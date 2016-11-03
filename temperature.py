import os
import glob
import datetime
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#device paths
lst = []
lst.append('/sys/bus/w1/devices/28-0115723a97ff/w1_slave')

#log path
temp_log = '/home/pi/Desktop/temp_logger/temp_data.csv'
date_log = str(datetime.datetime.now())

def get_temp(device):
  #to read the sensor data, just open the w1_slave file
  f = open(device, 'r')
  data = f.readlines()
  f.close()
  deg_f = ''
  if data[0].strip()[-3:] == 'YES':
    temp = data[1][data[1].find('t=')+2:]
    #if temp is 0 or non numeric an exception
    #will occur so lets hand it gracefully
    try:
      if float(temp)==0:
        deg_f = 32
      else:
        deg_f = (float(temp)/1000)*9/5+32
    except:
      print "Error with t=", temp
      pass
  return deg_f

for device in lst:
  device_name = device.split('/')[5]
  with open(temp_log, 'a') as f:
    s = device_name + ','
    s += date_log + ','
    s += str(get_temp(device)) + '/r/n'
    print(s)
    f.write(s)
  #when there are multiple devices, a short pause
  #interval between readings sensors seems to work best
  time.sleep(1)