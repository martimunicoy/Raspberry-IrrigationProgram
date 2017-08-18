import sys
import constants as co
import threading
import timing
import datetime


class TerminalInterface(object):

	def __init__(self, timer, schedule):
		self.thread = threading.Thread(target=self.run, args=())
		self.thread.daemon = True
		self.timer = timer
		self.schedule = schedule
		self.thread.start()

		print co.WELCOME

	def run(self):
		try:
			com = raw_input('\n >> ')
			key = co.COMMAND_LIST[com]
			if key == 1:
				self.timer.cancel()
				sys.exit(0)
			elif key == 2:
				print co.HELP
				print co.COMMAND_LIST
				print co.COMMAND_HELP
			elif key == 3:
				print co.SCHEDULE.format(timing.today().replace(microsecond=0))
				for delay in self.schedule.next_timer():
					hour = (datetime.timedelta(seconds=delay) + timing.today()).replace(microsecond=0)
					remaining = (datetime.datetime(1970,1,1) + datetime.timedelta(seconds=delay)).replace(microsecond=0)
					print "    {}            {}".format(hour.time(), remaining.time())
			elif key == 4:
				remaining = (datetime.datetime(1970,1,1) + datetime.timedelta(seconds=self.schedule.next_timer()[0])).replace(microsecond=0)
				print co.NEXT_RUN.format(remaining.time())
			elif key == 5:
				print co.CYCLE_INFO
				for output, tm in zip(co.CYCLE_OUTPUTS, self.schedule.cycle):
					print "{}         {}".format(output, tm)
		except (EOFError, KeyError):
			print co.WRONG_COMMAND
		
		self.run()

