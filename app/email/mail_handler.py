from app.email import bp
from app import mailer
from flask_mail import Message


def fill_message(message, message_text, message_html, attachments):
    message.body = message_text
    message.html = message_html

    if attachments:
        for attachment in attachments:
            message.attach(*attachment)
    
    return message



def send_mail(subject, sender, recipients, message_text, message_html, attachments):
    message = Message(subject, sender=sender, recipients=recipients)
    message = fill_message(message, message_text, message_html, attachments)

    mailer.send(message)
