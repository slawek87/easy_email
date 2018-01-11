import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename

from easy_email.clients.interface import Client
from easy_email.clients.gmail import Gmail


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

        self.attachment = Attachment(attachments)

        self.set_attachments()

    def get_message(self):
        """
        :return MIMEMultipart: prepared message ready to send by smtplib.SMTP client.
        """
        return self.body.as_string()

    def set_message(self):
        """
        Validates message type and setup message for given type.
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
        """
        :return string: separated receivers by `,`.
        """
        self.body['To'] = ','.join(self.receivers)

    def set_attachments(self):
        for attachment in self.attachment.get_attachments():
            self.body.attach(attachment)

    def set_text_message(self):
        self.body.attach(MIMEText(self.message, 'plain'))

    def set_html_message(self):
        self.body.attach(MIMEText(self.message, 'html'))

    def is_html_message(self):
        return self.message_type == self.MESSAGE_HTML

    def is_text_message(self):
        return self.message_type == self.MESSAGE_TEXT


class Attachment(object):
    """
    Attachment opens files and setup them to attachment content type.

    :param list attachments: List of path files.
    """
    def __init__(self, attachments=None):
        self.attachments = attachments

    def get_attachments(self):
        """
        :return list: Method returns list of files with setup attachment's content type.
        """
        attachments = []

        if not self.attachments:
            return attachments

        for seed in self.attachments:
            with open(seed, "rb") as opened_attachment:
                attachment = MIMEApplication(opened_attachment.read(), Name=basename(seed))
                attachment['Content-Disposition'] = 'attachment; filename="%s"' % basename(seed)
                attachments.append(attachment)

        return attachments


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
    def __init__(self, client, sender, receivers, subject, message,
                 message_type=Message.MESSAGE_HTML, attachments=None):
        if not isinstance(client, Client):
            raise TypeError("client instance has incorrect type.")

        if not isinstance(receivers, list):
            raise TypeError("receivers has incorrect type.")

        if message_type not in [Message.MESSAGE_HTML, Message.MESSAGE_TEXT]:
            raise TypeError("message_type has incorrect type.")

        if attachments and not isinstance(attachments, list):
            raise TypeError("attachments has incorrect type.")

        self.client = client
        self.sender = sender
        self.receivers = receivers
        self.message = Message(sender, receivers, subject, message, message_type, attachments)

    def send(self):
        return self.client.send_mail(self.receivers, self.message.get_message())

