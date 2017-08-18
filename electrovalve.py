import RPi.GPIO as GPIO
import logging as log

class Electrovalve(object):

	def __init__(self, pin=27, sim=False, test=False):
		self.sim = sim
		self.pin = pin
		if self.sim:
			log.info(co.ELECTROVALVE_SIMULATION)
			return
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(self.pin,GPIO.OUT)
		GPIO.output(self.pin,GPIO.LOW)
		log.info(co.ELECTROVALVE_CONFIG.format(str(self.pin)))

	def open(self):
		if self.sim:
			return
		GPIO.output(27,GPIO.HIGH)
		log.debug(co.ELECTROVALVE_ON)

	def close(self):
		if self.sim:
			return
		GPIO.output(self.pin,GPIO.LOW)
		log.debug(co.ELECTROVALVE_OFF)

