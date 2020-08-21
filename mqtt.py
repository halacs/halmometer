import ubinascii
import machine
import network
from umqtt.robust import MQTTClient
from config import config
from config import configConst
from config import mac
import json

CLIENT_ID = ubinascii.hexlify(machine.unique_id())
client = MQTTClient(CLIENT_ID, config['mqttServer'], config['mqttPort'], config['mqttUserName'], config['mqttPassword'])

mqttGroupTopic = (config['mqttGroupTopic'] + "/+").format(mac = mac).encode()
mqttTopic = (config['mqttTopic'] + "/+").format(mac = mac).encode()
mqttBackupTopic = (configConst['mqttBackupTopic'] + "/+").format(mac = mac).encode()

timer = machine.Timer(1)

def timer_callback(id):
	client.check_msg()

def sub_cb(topic, message):
	print((topic, message))

	topic = topic.decode()
	message = message.decode().strip("\"' ")

	print((topic, message))

	command = topic.split('/')[-1].strip("\"' ")
	print("command: ", command)

	if (command == "reboot"):
		# Reboot command
		if (message == "yes"):
			mqttSend("Reboot command received. Rebooting...")
			machine.reset()
		else:
			mqttSend("Reboot command received but the message is not as expected so ignore. Message: " + message)
	elif (command == "save"):
		if (message == "yes"):
			mqttSend("Save current configuration into file.")
			saveConfig()
		else:
			mqttSend("Save command received but the message is not as expected so ignore. Message: " + message)
	# Check if received command is known as a configuration name
	elif (command in config.keys()):
		key = command
		newValue = message
		oldValue = config[key]
		if (newValue == ""):
			mqttSend("{key} = {oldValue}".format(key = key, oldValue = oldValue))
		else:
			config[key] = newValue
			mqttSend("{key} has been updated to {newValue} from {oldValue}".format(key = key, oldValue = oldValue, newValue = newValue))
			saveConfig()
	else:
		# Unknown command
		mqttSend("Unknown command: {command}. Ignore.".format(command = command))

def mqttConnect():
	client.set_callback(sub_cb)
        client.connect()

	print("Subscribe to ", mqttGroupTopic)
	client.subscribe(mqttGroupTopic)
	
	print("Subscribe to ", mqttTopic)
	client.subscribe(mqttTopic)
	
	print("Subscribe to ", mqttBackupTopic)
	client.subscribe(mqttBackupTopic)
	
	timer.init(period=config['mqttIncommingPeriod'], callback=timer_callback)

def mqttDisconnect():
	timer.deinit()
        client.disconnect()

def mqttSend(message):
	rawMsg = json.dumps(message).encode()
	print(rawMsg)
        client.publish(config['mqttSendTopic'].format(mac = mac).encode(), rawMsg)

