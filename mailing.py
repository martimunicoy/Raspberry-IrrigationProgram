import smtplib
import constants as co
import timing
import datetime
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


class Mail(object):

    def __init__(self, schedule, issuer=co.MAIL, psswd=co.MAIL_PSSWD):
        self.schedule = schedule
        self.issuer = issuer
        self.psswd = psswd
        self.server = smtplib.SMTP('smtp.gmail.com', 587)

        self.server.starttls()
        self.server.login(issuer, psswd)

    def send_success(self, receiver='martimunicoy@gmail.com'):
        msg = MIMEMultipart()
        msg['From'] = self.issuer
        msg['To'] = receiver
        msg['Subject'] = co.MAIL_SUBJECT

        time_now = timing.today().replace(microsecond=0)
        sch_str = ""
        for delay in self.schedule.next_timer():
            hour = (datetime.timedelta(seconds=delay) +
                    timing.today()).replace(microsecond=0)
            remaining = (datetime.datetime(1970, 1, 1) + datetime.timedelta(
                seconds=delay)).replace(microsecond=0)
            sch_str += "\n    {}            {}".format(hour.time(),
                                                       remaining.time())
        cyc_str = ""
        for output, tm in zip(co.CYCLE_OUTPUTS, self.schedule.cycle):
            cyc_str += "\n{}         {}".format(output, tm)
        body = "Hi,\n" + co.MAIL_MSG.format(time_now) +\
            co.SCHEDULE.format(time_now) + sch_str + "\n" +\
            co.CYCLE_INFO + cyc_str + co.MAIL_ENDING
        msg.attach(MIMEText(body, 'plain'))

        self.server.sendmail(self.issuer, receiver, msg.as_string())
