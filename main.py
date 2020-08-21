import network
import time
from time import sleep
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import BME280
from config import config
import mqtt
import json

FIRMWARE_VERSION=10100
CONFIG_FILE_NAME='config.json'

i2c = I2C(scl=Pin(5), sda=Pin(4))
oled = SSD1306_I2C(config['screenWidth'], config['screenHeight'], i2c)

def loadConfig():
	print('orig: ', config)

	try:
		with open(CONFIG_FILE_NAME) as infile:
			data = json.load(infile)
			config.update(data)
		
	except:
		print('There might be no saved config yet.')
#		saveConfig()
	else:
		print('diff: ', data)
		print('new: ', config)

def saveConfig():
	print('Save config to ' + CONFIG_FILE_NAME + 'file.')

	with open(CONFIG_FILE_NAME, "w") as outfile:
		json.dump(config, outfile)

def connectWifi():
	station = network.WLAN(network.STA_IF)
	
	station.active(True)
	station.connect(config['ssid'], config['password'])
	
	while station.isconnected() == False:
	  pass
	
	print('Connection successful')
	print(station.ifconfig())

def getSensor():
	# ESP8266 - Pin assignment
	i2c = I2C(scl=Pin(5), sda=Pin(4), freq=10000)

	bme = BME280.BME280(i2c=i2c)
	return {'temperature' : bme.temperature, 'humidity': bme.humidity, 'pressure' : bme.pressure}

# print new line
print('')

oled.fill(0)
oled.text("Starting...", 0, 20)
oled.show()

#saveConfig()
loadConfig()
connectWifi()
mqtt.mqttConnect()

while True:
	values = getSensor()

	oled.fill(0)
 	oled.text(values['temperature'] + " C", 0, 0)
	oled.text(values['humidity'] + " %", 0, 10)
	oled.text(values['pressure'] + " hPa", 0, 20)
	oled.show()
	
	# measure bettery voltage - https://docs.micropython.org/en/latest/esp8266/tutorial/adc.html
	adc = machine.ADC(0)
  	voltage = adc.read() * config['VOLTAGE_MULTIPLIER'];
  	#voltage = adc.read() * 0.00489861386138613861386138613861;
  
	version = FIRMWARE_VERSION
	nextmeasurement = config['delay']
	values.update( {'voltage' : voltage, 'version' : version, 'nextmeasuremenet' : nextmeasurement } )

	mqtt.mqttSend(values)

	sleep(config['delay'])

mqttDisconnect()

