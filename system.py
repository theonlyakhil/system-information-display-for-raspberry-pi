#!/usr/bin/env python

from lib_oled96 import ssd1306
import time
import os
from PIL import ImageFont, ImageDraw, Image
#import sys
from time import sleep
from PIL import ImageFont, ImageDraw#, Image

from smbus import SMBus
i2cbus = SMBus(1)        # 1 = Raspberry Pi but NOT early REV1 board

oled = ssd1306(i2cbus)   # create oled object, nominating the correct I2C bus, default address
draw = oled.canvas   # "draw" onto this canvas, then call display() to send the canvas contents to the hardware.

#Setup fonts
#font = ImageFont.load_default()
font1 = ImageFont.truetype('FreeSans.ttf', 40)
font2 = ImageFont.truetype('FreeSans.ttf', 17)
font3 = ImageFont.truetype('FreeSans.ttf', 14)
font4 = ImageFont.truetype('FreeSans.ttf', 16)

# put border around the screen:
#oled.canvas.rectangle((0, 0, oled.width-1, oled.height-1), outline=1, fill=0)
logo = Image.open('pi_logo.png')
draw.bitmap((32, 0), logo,fill=1)
oled.display()
sleep(4)
oled.cls()
 
while True:
	
	#print time.strftime("%I:%M:%S %p")
	
	draw.rectangle((0, 0, 128, 64), outline=1, fill=0)

	draw.text((0, 0), time.strftime("%I:%M"), font=font1, fill=1)
	if time.strftime("%I")[:1] == '0':		#remove leading 0 for hour
		draw.text((0, 0), '0', font=font1, fill=0)
	#draw.text((105, 20), time.strftime("%S"), font=font2, fill=1)
	draw.text((106, 8), time.strftime("%p"), font=font3, fill=1)
	draw.text((40 , 45), time.strftime("%b ,%d, %Y"), font=font3, fill=1)#b for month in text and d for date  y for year
	
	oled.display()
	
	time.sleep(-time.time() % 1)
	sleep(4)
	oled.cls()
	draw.text((12,0), "network info" ,font=font2, fill=1)
	
	oled.display()
	
	# to display network information
	ssid=os.popen("iwconfig wlan0 | grep 'ESSID' | awk '{print $4}' | awk -F\\\" '{print $2}'").read()
	ipaddress=os.popen("ifconfig wlan0 | grep 'inet addr' | awk -F: '{print $2}' | awk '{print $1}'").read()
	draw.text((12,25),"SSID="+ssid,font=font4,fill=1)
	draw.text((14,50),ipaddress,font=font3,fill=1)
	oled.display()
	sleep(4)
	oled.cls()
	temp=os.popen("vcgencmd measure_temp").read()
	#to display the cpu temperature and CPU usage
	draw.text((10,24),temp,font=font2,fill=1)
	oled.display()
	sleep(4)
	oled.cls()
	cpu=os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline()
	draw.text((12,0),"CPU USE",font=font2,fill=1)
	draw.text((10,24),cpu+"%",font=font1,fill=1)
	oled.display()
	sleep(4)
	
	
	
