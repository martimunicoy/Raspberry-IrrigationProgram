import constants as co
import sys
import timing
import time
import logging as log
from electrovalve import Electrovalve
from terminal_interface import TerminalInterface
from mailing import Mail
from optparse import OptionParser
from threading import Timer


def main():
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="sch_dir",
                      help="directory of the Schedule file",
                      metavar="FILE_DIRECTORY")
    parser.add_option("-l", "--log", dest="log_level",
                      help="set the logging level",
                      metavar="DEBUG, INFO, WARNING, ERROR, CRITICAL")
    parser.add_option("-t", "--test", dest="test", action='store_true',
                      help="functional test")
    parser.add_option("-s", "--simulation", dest="sim",
                      action='store_true',
                      help='simulation mode where actually no ' +
                           'relay is turned on')
    parser.add_option("-d", "--log_dir", dest="log_dir",
                      help="directory of the log file",
                      metavar="FILE_DIRECTORY")
    args_dict = parser.parse_args()[0].__dict__

    log_dir = args_dict['log_dir']
    if log_dir is None:
        log_dir = 'IrrigationProgram.log'
    log.basicConfig(filename=log_dir, level=args_dict['log_level'],
                    format='%(asctime)s %(message)s')
    log.info(co.MAIN_INFO)

    kwargs = {}
    for key, item in args_dict.iteritems():
        if item is True:
            kwargs[key] = item

    sch_dir = args_dict['sch_dir']

    myschedule = timing.Schedule(sch_dir, **kwargs)

    myelectrovalve = Electrovalve(pin=27, **kwargs)

    timer = cycle(myschedule, myelectrovalve, **kwargs)

    TerminalInterface(timer, myschedule)


def cycle(schedule, electrovalve, test=False, sim=False):
    delay = schedule.next_timer()[0]

    log.debug(co.CYCLE_DEBUG.format(delay))

    mytimer = Timer(delay, water, args=(schedule, electrovalve, test, sim))
    mytimer.start()

    if test:
        print co.TEST_WARNING
        log.info(co.TEST_WARNING)

    return mytimer


def water(schedule, electrovalve, test, sim):
    for span in map(float, schedule.cycle):
        electrovalve.open()
        time.sleep(span)
        electrovalve.close()
        time.sleep(co.GAP)

    try:
        mymail = Mail(schedule)
        mymail.send_success()
    except Exception:
        log.logger.error(co.MAIL_ERROR)

    if test:
        sys.exit(0)
    # Add a condition to exit if wanted
    cycle(schedule, electrovalve, test, sim)


if __name__ == "__main__":
    main()
