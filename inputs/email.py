from imap_tools import MailBox, A
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading

sender_email = None
receiver_email = None
password = None
email_id = None
sub = "Hello"

translate_speech = None

listen_for_mail = True

def email_init(interperet_speech):
    global translate_speech
    translate_speech = interperet_speech

    mail_checking = threading.Thread(target = mail_listen_loop)
    mail_checking.start()

def mail_listen_loop():
    while listen_for_mail:
        translate_speech(read_message())

def read_message():
    global email_id
    global sub

    with MailBox('imap.gmail.com').login(sender_email, password, 'INBOX') as mailbox:
        responses = mailbox.idle.wait(timeout=600)
        if responses:
            for msg in mailbox.fetch(A(seen = False), mark_seen = True):
                if ('ideck802' in msg.from_):
                    email_id = msg.uid
                    sub = msg.subject
                    print(msg.subject)
                    print(msg.text.rstrip())
                    return msg.text.rstrip()


def send_email(msg):
    message = MIMEMultipart('mixed')
    body = MIMEMultipart('alternative')
    body.attach(MIMEText(msg, 'plain'))
    message['to'] = receiver_email
    message['from'] = sender_email
    message['subject'] = sub
    message['In-Reply-To'] = email_id
    message.attach(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(sender_email, password)

        server.sendmail(sender_email, receiver_email, message.as_string())
