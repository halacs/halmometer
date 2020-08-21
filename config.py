import ubinascii
import network

"""
delay: secs between two measurements

VOLTAGE_MULTIPLIER:
Using a 200k resistor between the battery voltage and analog input A0 this experimentally
results in the correct voltage being calculated in my setup, this might need to be changed for yours.
"""
config = {
	'ssid' : '',
        'password' : '',	
	
	'mqttServer' : '',
	'mqttPort' : 1883,
	'mqttUserName' : '',
	'mqttPassword' : '',
	'mqttSendTopic' : '/wemos/stats/{mac}',
	'mqttGroupTopic' : '/wemos/cmds/all',
	'mqttTopic' : '/wemos/cmds/{mac}',
	'mqttIncommingPeriod' : 1000,
	
	'screenWidth' : 64,
	'screenHeight' :  48,
	
	'delay' : 1,
	'VOLTAGE_MULTIPLIER' : 0.00489861386138613861386138613861
}

"""
Values what cannot be changed on the fly.
"""
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode().upper()
configConst = {
	'mqttBackupTopic': '/wemos/cmds/{mac}'
}
