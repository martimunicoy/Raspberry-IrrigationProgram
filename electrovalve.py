import RPi.GPIO as GPIO
import logging

class Electrovalve(object):

	def __init__(self, pin=27, sim=False, test=False):
		self.sim = sim
		self.pin = pin
		if self.sim:
			return
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(self.pin,GPIO.OUT)
		GPIO.output(self.pin,GPIO.LOW)
		logging.info('Electrovalve configurated')

	def open(self):
		if self.sim:
			return
		GPIO.output(27,GPIO.HIGH)
		logging.info('Electrovalve turned on')

	def close(self):
		if self.sim:
			return
		GPIO.output(self.pin,GPIO.LOW)
		logging.info('Electrovalve switched off')

