import smtplib
import socket


class Client(smtplib.SMTP):
    """
    Interface for whole client what you gonna use in this library.
    """
    def __init__(self, username, password, email, host='', port=0, local_hostname=None,
                 timeout=socket._GLOBAL_DEFAULT_TIMEOUT, source_address=None):
        self.username = username
        self.password = password
        self.email = email

        super().__init__(host=host, port=port, local_hostname=local_hostname,
                         timeout=timeout, source_address=source_address)

    def send_mail(self, receivers, message):
        """
        :param list receivers: List of receivers emails.
        :param MIMEMultipart message: MIMEMultipart included mail body.

        example:
            self.login(self.username, self.password)
            self.sendmail(self.email, receivers, message)
            self.quit()
        """
        raise NotImplemented("Method must be implemented.")
