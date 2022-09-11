# HalMometer

## Summary
Goal of HalMometer is to send temperature, humidity and air pressiure measurements via [MQTT](https://mosquitto.org/) with low cost and with low energy consumption.

This project is written in Python on top of [MicroPython](http://micropython.org) and Wemos D1 mini (ESP8266) baseboard.

## Install
### Hardware
First, you need to assemble the board to have a 200K resistor in between the A0 and 5V ports of the Wemos baseborad. This is how we can measure the battery voltage.


With a jumpre wire, connect D0 pin to the RST pin. This is needed to save energy when working from battery: ensure we wake up from the deep sleep mode.


BME280 is the I2C sensor prodides temperature, humidity and air pressure measurements. When you buy it from ebay, take care. There are many seller advertising their item as BME280 but in reality many of them are BMP280 which doesn't provide the humidity value.
SCL pin of the sensor goes to the D1 pin of the baseborad, while SDA to the D2. GND and VCC are quite strateforward but VCC here must go to 3V3 pin on the baseboard.

Reagrind the battery: I had many issues with the battery capacity in the winter so there is a chance that my batteries are not meets quailty expectations just the cost...
This is why I use AC/DC adaptor to feed it instead of solar panels. I found it rock solid this way.

### Software
Download stable image from [MicroPython](http://micropython.org)'s website and flash it with esptool command line tool.

  ```
  apt install esptool -y
  esptool --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 /tmp/esp8266-20191220-v1.12.bin
  ```

then with help of Makefile you can found in the root directory of this project you can copy all the files to the baseboard.
Note, that ```make``` and ```ampy``` must be installed on your system.

  ```
  apt install make python-pip -y
  pip install adafruit-ampy
  make
  ```

If you need further assistance who to do the above steps please refer the tools' documentations.

## Commands
Responds are sent to the same topic as periodic measurements.
There are three MQTT topic you can send your messages to: topic unique per device by design, group topic which shared by several devices and last but not least a backup topic which cannot be changed.

### Reboot the board
* Topic: '/wemos/cmds/all/reboot'
* Message: 'yes'

### Make current configuration changes permanent
* Topic: '/wemos/cmds/all/save'
* Message: 'yes'

### Get configuration
You can query any of the configuration values defined in the config dictionary of config.py module.
* Topic: '/wemos/cmds/all/[key]'
* Message: empty

### Set configuration
You can set any of the configuration values defined in the config dictionary of config.py module by sending.
* Topic: '/wemos/cmds/all/[key]'
* Message: the new value you want to set. Cannot be empty.

## Links
* [MicroPython](http://micropython.org)
* [MicroPython Documentation](http://docs.micropython.org)
* [MQTT library (robust)](https://github.com/micropython/micropython-lib/tree/master/umqtt.robust)
* [MQTT library (simple)](https://github.com/micropython/micropython-lib/tree/master/umqtt.simple)
* [Wemos D1 mini PIN layout](https://diyi0t.com/what-is-the-esp8266-pinout-for-different-boards/#elementor-toc__heading-anchor-6)
* [Mosquitto MQTT broker server](https://mosquitto.org/)
* [esptool](https://github.com/espressif/esptool)
* [ampy](https://github.com/scientifichackers/ampy)
