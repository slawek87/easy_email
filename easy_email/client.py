import smtplib
from email.mime.multipart import MIMEMultipart


class Message(object):
    """
    Message prepares message body with attachments

    :param list receivers: List of receivers emails.
    :param str subject: Mail subject.
    :param str message: Mail message.
    :param const message_type: There is two types of mail messages: `Message.MESSAGE_HTML` and `Message.MESSAGE_TEXT`.
    :param list attachments: List of path files.
    """
    MESSAGE_HTML = "html"
    MESSAGE_TEXT = "text"

    body = MIMEMultipart()

    def __init__(self, sender, receivers, subject, message, message_type, attachments):
        self.sender = sender
        self.receivers = receivers
        self.subject = subject

        self.set_sender()
        self.set_receivers()
        self.set_subject()

        self.message = message
        self.message_type = message_type

        self.set_message()

        self.attachments = Attachment(attachments)

        self.set_attachments()

    def get_message(self):
        """
        :return MIMEMultipart: prepared message ready to send by smtplib.SMTP client.
        """
        return self.body

    def set_message(self):
        """
        Validates message type and set message for given type.
        """
        message_types = {
            self.MESSAGE_TEXT: self.set_text_message(),
            self.MESSAGE_HTML: self.set_html_message()
        }

        if message_types.get(self.message_type, False) is False:
            raise ValueError("Given message_type value is not correct.")

    def set_subject(self):
        self.body['Subject'] = self.subject

    def set_sender(self):
        self.body['Fom'] = self.sender

    def set_receivers(self):
        self.body['To'] = self.receivers

    def set_attachments(self):
        pass

    def set_text_message(self):
        pass

    def set_html_message(self):
        pass

    def is_html_message(self):
        return self.message_type == self.MESSAGE_HTML

    def is_text_message(self):
        return self.message_type == self.MESSAGE_TEXT


class Attachment(object):
    def __init__(self, attachments=None):
        self.attachments = attachments

    def open(self, attachment):
        pass

    def prepare(self, attachments):
        pass


#TODO create metaclass where we can check if client instance is smtlib.SMTP client instance.
class EasyEmail(object):
    """
    EasyEmail handles send emails process.

    :param smtplib.SMTP client: Instance wit set settings, ready to connect to SMTP server and send email.
    :param str sender: Email address, should be the same as you set in client instance.
    :param list receivers: List of receivers emails.
    :param str subject: Mail subject.
    :param str message: Mail message.
    :param const message_type: There is two types of mail messages: `Message.MESSAGE_HTML` and `Message.MESSAGE_TEXT`.
    :param list attachments: List of path files.
    """
    def __init__(self, client, sender, receivers, subject, message, message_type=Message.MESSAGE_HTML, attachments=None):
        self.client = client
        self.sender = sender
        self.receivers = receivers
        self.message = Message(sender, receivers, subject, message, message_type, attachments)

    def send(self):
        return self.client.send_mail(self.receivers, self.message)


class Client(smtplib.SMTP):
    def __init__(self, username, password, email, *args, **kwargs):
        self.username = username
        self.password = password
        self.email = email

        super().__init__(*args, **kwargs)

    def send_mail(self, receivers, message):
        self.sendmail(self.email, receivers, message)
        self.close()


class Gmail(object):
    pass
