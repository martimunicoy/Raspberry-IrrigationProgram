import datetime
import constants as co
import logging as log

def today():
	return datetime.datetime.now()

class Schedule(object):

	def __init__(self, sch_dir, test=False, sim=False):
		self.sch_dir = sch_dir

		if test:
			log.debug(co.SCHEDULE_TEST)
			self.timetable = [today() + datetime.timedelta(seconds=1)]
			self.cycle = co.TEST_CYCLE
		elif self.sch_dir is None:
			log.info(co.SCHEDULE_DIR)
			self.timetable = co.TIMETABLE
			self.cycle = co.CYCLE
		else:
			self.parser()

		self.log_info()

	def parser(self):
		log.info(co.SCHEDULE_PARSER.format(self.sch_dir))		
		with open(self.sch_dir) as f:
			for line in f:
				line = line.strip()
				if line.startswith('CYCLE'):
					self.cycle = line.split(" ")[1:]
				elif line.startswith('TIMETABLE'):
					hours = [hour.split(",") for hour in line.split(" ")[1:]]
					self.timetable = []
					today_date = datetime.date.today()
					for hour in hours:
						trigger_time = datetime.time(*map(int, hour))
						self.timetable.append(datetime.datetime.combine(today_date, trigger_time))

	def next_timer(self):
		delays = []
		for hour in self.timetable:
			delay = (hour - today()).total_seconds()
			if delay <= 0:
				delay += co.SECONDS_ONE_DAY
			delays.append(delay)
		delays.sort()
		return delays

	def log_info(self):
		time_now = today().replace(microsecond=0)
		sch_str = ""
		for delay in self.next_timer():
					hour = (datetime.timedelta(seconds=delay) + today()).replace(microsecond=0)
					remaining = (datetime.datetime(1970,1,1) + datetime.timedelta(seconds=delay)).replace(microsecond=0)
					sch_str += "\n    {}            {}".format(hour.time(), remaining.time())
		cyc_str = ""
		for output, tm in zip(co.CYCLE_OUTPUTS, self.cycle):
			cyc_str += "\n{}         {}".format(output, tm)
		log.info(co.SCHEDULE.format(time_now) + sch_str + "\n" + co.CYCLE_INFO + cyc_str)

