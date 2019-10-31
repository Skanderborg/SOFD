import smtplib


class Email_service:
    def __init__(self, username, password, mailserver, port):
        self.username = username
        self.password = password
        self.mailserver = mailserver
        self.port = port

    def send_mail(self, to_adr, subject, message):
        ms = smtplib.SMTP(self.mailserver, self.port)
        ms.ehlo()
        ms.starttls()
        ms.login(self.username, self.password)
        header = 'To:' + to_adr + '\r\n' + 'From:' + \
            self.username + '\r\n' + 'Subject:' + subject + '\r\n\n'
        msgbody = header + message + '\n\n'

        ms.sendmail(self.username, to_adr, msgbody)
        ms.quit()
