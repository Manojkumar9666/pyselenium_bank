from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.headerregistry import Address
import smtplib
import time
import pandas as pd
from email.mime.base import MIMEBase
from email import encoders
import os

def send_mail(mail_subject, mail_message, admin_status=True):
    df = pd.read_excel(r"D:\\PySelenium_bank\\configuration_file.xlsx", sheet_name='Mailer Details')
    # create message object instance
    msg = MIMEMultipart()
    message = mail_message
    # setup the parameters of the message
    password = df["Password"][0]
    msg['From'] = df["From Address"][0]
    recipients = ""
    if admin_status is True:
        recipients = str(df["Admin Address"][0])
        msg['To'] = recipients
        print(msg['To'])

    else:
        recipients = str(df["To Address"][0])
        print(recipients)
        msg['To'] = recipients

    msg['Subject'] = mail_subject
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
    msg.attach(MIMEText(mail_message))
    # part = MIMEBase('application', "octet-stream")
    # part.set_payload(
    #     open(error_attachment_path,
    #          "rb").read())
    # encoders.encode_base64(part)
    # part.add_header('Content-Disposition', 'attachment; filename="Customer Support Dashboard.xlsx"')
    # msg.attach(part)

    # create server
    server = smtplib.SMTP("smtp.office365.com", 587)
    #server = smtplib.SMTP(str(df["Outgoing Server"][0]).strip()+":"+str(df["Port"][0]).strip())
    server.starttls()
    # Login Credentials for sending the mail
    server.login(msg['From'], password)
    # send the message via the server.
    server.sendmail(msg['From'], recipients.split(','), msg.as_string())
    server.quit()
    # del df
def send_mail_with_attachment(mail_subject,mail_message,error_attachment_path,uploaded_cases_attachment,admin_status=True):
    df = pd.read_excel(r"D:\\PySelenium_bank\\configuration_file.xlsx", sheet_name='Mailer Details')
    # create message object instance
    attachments = [error_attachment_path,uploaded_cases_attachment]
    msg = MIMEMultipart()
    message = mail_message
    # setup the parameters of the message
    password = df["Password"][0]
    msg['From'] = df["From Address"][0]
    recipients = ""
    if admin_status is True:
        recipients = str(df["Admin Address"][0])
        msg['To'] = recipients
        print(msg['To'])

    else:
        recipients = str(df["To Address"][0])
        msg['To'] = recipients

    msg['Subject'] = mail_subject
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
    msg.attach(MIMEText(mail_message))
    for filename in attachments:
        if filename!="":
            f = filename
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(f, "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
            msg.attach(part)

    # create server
    server = smtplib.SMTP(str(df["Outgoing Server"][0]).strip() + ":" + str(df["Port"][0]).strip())
    server.starttls()
    # Login Credentials for sending the mail
    server.login(msg['From'], password)
    # send the message via the server.
    server.sendmail(msg['From'], recipients.split(','), msg.as_string())
    server.quit()

    del df
# Source : https://code.tutsplus.com/tutorials/sending-emails-in-python-with-smtp--cms-29975