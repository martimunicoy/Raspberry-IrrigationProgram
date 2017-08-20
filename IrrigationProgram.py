import constants as co
import logging as log
from electrovalve import Electrovalve
from terminal_interface import TerminalInterface, StatusBulb
from optparse import OptionParser
from timing import Schedule, initiate_timer


def main():
    mystatusbulb = StatusBulb()
    mystatusbulb.open()

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
    log_level = args_dict['log_level']
    if log_level is None:
        log_level = 'INFO'
    log.basicConfig(filename=log_dir, level=log_level,
                    format='%(asctime)s %(message)s')
    log.info(co.SEPARATOR)
    log.info(co.MAIN_INFO)

    kwargs = {}
    for key, item in args_dict.iteritems():
        if item is True:
            kwargs[key] = item

    sch_dir = args_dict['sch_dir']

    myschedule = Schedule(sch_dir, **kwargs)

    myelectrovalve = Electrovalve(myschedule, pin=27, **kwargs)

    myinterface = TerminalInterface(myschedule, myelectrovalve, mystatusbulb,
                                    **kwargs)

    initiate_timer(myschedule, myelectrovalve, myinterface, **kwargs)


if __name__ == "__main__":
    main()
