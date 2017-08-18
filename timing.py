import datetime
import constants as co

def today():
	return datetime.datetime.now()

class Schedule(object):

	def __init__(self, sch_dir, test=False, sim=False):
		self.sch_dir = sch_dir
		if test:
			self.timetable = [today() + datetime.timedelta(seconds=1)]
			self.cycle = co.TEST_CYCLE
		elif self.sch_dir is None:
			self.timetable = co.TIMETABLE
			self.cycle = co.CYCLE
		else:
			self.parser()

	def parser(self):
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
