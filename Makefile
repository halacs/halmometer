PORT_DEVICE='/dev/ttyUSB0'

push:
	ls *.py | xargs -n 1 -I{} bash -c 'echo {}; ampy --port ${PORT_DEVICE} put {}'
#	ampy --port ${PORT_DEVICE} reset
