import smtplib


class Client(smtplib.SMTP):
    def __init__(self, username, password, email, *args, **kwargs):
        self.username = username
        self.password = password
        self.email = email

        super().__init__(*args, **kwargs)

    def send_mail(self, receivers, message):
        self.sendmail(self.email, receivers, message)
        self.quit()
