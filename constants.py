import datetime

TIMETABLE = (datetime.datetime.combine(datetime.date.today(), datetime.time(8)),
			 datetime.datetime.combine(datetime.date.today(), datetime.time(20)))

CYCLE = (600, 300, 300, 30, 300, 30)

CYCLE_OUTPUTS = ('Garden   ', 'Sideways ', 'Backyard ', 'Empty    ', 'Frontyard', 'Empty    ')

TEST_CYCLE = (10, 10, 10, 10, 10, 10)

GAP = 10
SECONDS_ONE_DAY = 86400

WELCOME = "Irrigation Program working\n--------------------------\n Enter any command below:"

WRONG_COMMAND = "Command not found. Type help to see a\nlist of all the available commands."

COMMAND_LIST = {"" : 0, "exit" : 1 , "help" : 2, "schedule" : 3, "next run" : 4, "cycle timing" : 5}

COMMAND_HELP = ("...")

HELP = "List of commands:\n"

SCHEDULE = "\nSchedule:\n---------\nDate and time: {}\n\nIrrigation hours:    Remaining time:"

TEST_WARNING = "Testing all six water outputs..."

NEXT_RUN = "\nNext irrigation cycle running in:\n {}"

CYCLE_INFO = "\nIrrigation cycle:\n-----------------\n\nOutput:    Irrigation time(s):"

MAIL = 'raspberrymunicoy@gmail.com'

MAIL_PSSWD = '447-Kyc-VqP-epy'

MAIL_MSG = 'Raspberry Pi activated the electrovalve successfully on {}. More information about the irrigation schedule can be found below:\n'

MAIL_ENDING = '\n\nRaspberry Pi.'

MAIL_SUBJECT = 'Irrigation Notification'