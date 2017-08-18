import constants as co
import getopt
import sys
import timing
import time
import logging

from electrovalve import Electrovalve
from terminal_interface import TerminalInterface
from mailing import Mail

from optparse import OptionParser
from threading import Timer

no_interface = True

def main():
	parser = OptionParser()
	parser.add_option("-f", "--file", dest="sch_dir", help="directory of the Schedule file", metavar="FILE_DIRECTORY")
	parser.add_option("-t", "--test", dest="test", action='store_true', help="functional test")
	parser.add_option("-s", "--simulation", dest="sim", action='store_true', help='simulation mode where actually no relay is turned on')
	parser.add_option("-l", "--log", dest="log_dir", help="directory of the log file", metavar="FILE_DIRECTORY")
	args_dict = parser.parse_args()[0].__dict__

	log_dir = args_dict['log_dir']

	if log_dir is None:
		log_dir = 'IrrigationProgram.log'

	logging.basicConfig(filename=log_dir)

	kwargs = {}
	
	for key, item in args_dict.iteritems():
		if item == True:
			kwargs[key] = item
	
	sch_dir = args_dict['sch_dir']

	myschedule = timing.Schedule(sch_dir, **kwargs)

	myelectrovalve = Electrovalve(pin=27, **kwargs)

	timer(myschedule, myelectrovalve, **kwargs)


def timer(schedule, electrovalve, test=False, sim=False):
	global no_interface
	delay = schedule.next_timer()[0]
	t = Timer(delay, water, args=(schedule, electrovalve, test))
	t.start()
	if test:
		print co.TEST_WARNING
	elif no_interface:
		myinterface = TerminalInterface(t, schedule)
		no_interface = False


def water(schedule, electrovalve, test):
	for span in map(float, schedule.cycle):
		electrovalve.open()
		time.sleep(span)
		electrovalve.close()
		time.sleep(co.GAP)

	mymail = Mail(schedule)
	mymail.send_success()

	if test:
		sys.exit(0)
	# Add a condition to exit if wanted
	main()

if __name__ == "__main__":
	main()
