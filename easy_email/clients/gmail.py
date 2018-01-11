import socket

from easy_email.clients.interface import Client


class Gmail(Client):
    """
    Gmail Client with default configuration.
    """
    SMTP_HOST = 'smtp.gmail.com'
    SMTP_PORT = 587

    def __init__(self, username, password, email, host=SMTP_HOST, port=SMTP_PORT, local_hostname=None,
                 timeout=socket._GLOBAL_DEFAULT_TIMEOUT, source_address=None):
        super().__init__(username, password, email, host, port, local_hostname, timeout, source_address)
        self.host = self.SMTP_HOST
        self.port = self.SMTP_PORT

    def send_mail(self, receivers, message):
        self.ehlo()
        self.starttls()
        self.login(self.username, self.password)
        self.sendmail(self.email, receivers, message)
        self.quit()
