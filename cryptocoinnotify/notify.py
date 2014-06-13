# -*- coding: utf-8 -*-
from email.mime.text import MIMEText
import smtplib

from cryptocoinnotify.config import config


class MailNotify(object):
    def __init__(self, text):
        self.msg = MIMEText(text)
        self.msg['To'] = config.get('notify', 'mail_to').strip()
        self.msg['From'] = config.get('notify', 'mail_from').strip()
        self.msg['Subject'] = config.get('notify', 'mail_subject').strip()

        self.sender = smtplib.SMTP(
            config.get('notify', 'smtp_host'), config.get('notify', 'smtp_port')
        )

        if config.has_option('notify', 'smtp_username') and \
                config.get('notify', 'smtp_username') and \
                config.has_option('notify', 'smtp_password') and \
                config.get('notify', 'smtp_password'):
            self.sender.login(
                config.get('notify', 'smtp_username'), config.get('notify', 'smtp_password')
            )

    def send(self):
        self.sender.sendmail(
            config.get('notify', 'mail_from').strip(),
            config.get('notify', 'mail_to').strip().split(','),
            self.msg.as_string()
        )


class ClickatellNotify(object):
    def __init__(self, text):
        message = """
User: {user}
Password: {password}
Api_ID: {api_id}
To: {to}
Reply: {reply}
Text: {text}
""".format(
            user=config.get('notify', 'clickatell_user'),
            password=config.get('notify', 'clickatell_password'),
            api_id=config.get('notify', 'clickatell_api_id'),
            to=config.get('notify', 'clickatell_to'),
            reply=config.get('notify', 'clickatell_reply_to'),
            text=text
        )
        self.msg = MIMEText(message)
        self.msg['TO'] = [v.strip() for v in config.get('notify', 'mail_to').strip().split(',')]
        self.msg['FROM'] = config.get('notify', 'mail_from').strip()
        self.msg['SUBJECT'] = config.get('notify', 'mail_subject').strip()

        self.sender = smtplib.SMTP(
            config.get('notify', 'smtp_host'), config.get('notify', 'smtp_port')
        )

        if config.has_option('notify', 'smtp_username') and \
                config.get('notify', 'smtp_username') and \
                config.has_option('notify', 'smtp_password') and \
                config.get('notify', 'smtp_password'):
            self.sender.login(
                config.get('notify', 'smtp_username'), config.get('notify', 'smtp_password')
            )

    def send(self):
        self.sender.sendmail(
            self.msg['FROM'], 'sms@messaging.clickatell.com', self.msg
        )


NOTIFIERS = {
    'smtp': MailNotify,
    'clickatell': ClickatellNotify,
}