from email import encoders
from email.mime.base import MIMEBase

import pandas as pd
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart  # sending email
from email.mime.text import MIMEText


def bank_report(username):
    print(username)
    ex = pd.read_csv("C:\\Users\\RPA Testing\\Desktop\\Bank_approvals_csv.csv")
    dat = datetime.date.today()
    count = 0
    for i, row in ex.iterrows():
        date_time_str = dat.strftime("%d-%m-%Y")
        print(date_time_str)
        Time = datetime.strptime(str(row['Date']), "%d-%m-%Y")
        print(Time)
        print(row['Username'])
        if str(row['Date']) == str(date_time_str) and row['Username'] == username:
            count = count + 1
    replace_value = count * 10
    print(replace_value)

    print(date_time_str)

    file_path = open("D:\\PySelenium_bank\\dashboard_template_txt.txt")

    data = file_path.read()
    print(data)

    def substitute(key, value):
        return data.replace(key, str(value))

    def replace_cal_values(key, value):
        switcher = {
            'process_date': substitute(key, value),
            'Records_Count': substitute(key, value),
            'success_transactions': substitute(key, value),
            'Failure _Count': substitute(key, value),
            'kn_code': substitute(key, value),
            'APPROVAL_TYPE': substitute(key, value),
        }
        return switcher.get(key, "nothing")

    data = replace_cal_values("process_date", str(date_time_str))
    data = replace_cal_values("Records_Count", str(replace_value))
    data = replace_cal_values("success_transactions", str(replace_value))
    data = replace_cal_values("Failure _Count", str(0))
    data = replace_cal_values("kn_code", username)
    data = replace_cal_values("APPROVAL_TYPE", "QZONE & Portal")

    print(data)

    msg = MIMEMultipart()
    html = data
    subject = 'Bank Report Dashboard'
    sender = 'rpa@quesscorp.com'
    recipients = ['mahendra.ramisetty@quesscorp.com', 'gracia.velangani@quesscorp.com', 'jabiulla.s@quesscorp.com']
    recipientscc = []
    BCC = ['manoj.ramisetty@quesscorp.com', 'anjana.kovoor@quesscorp.com', 'Shankar.S@quesscorp.com',
           'anand.srinivasan@quesscorp.com']

    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)
    msg['Cc'] = ", ".join(recipientscc)
    # msg['Bcc'] = ", ".join(BCC)44444
    # part1 = MIMEText(mailBody, 'plain')
    part2 = MIMEText(html, 'html')
    # msg.attach(part1)
    msg.attach(part2)
    i = "C:\\Users\\RPA Testing\\Desktop\\Bank_approvals_csv.csv"
    attachment = open(i, "rb")
    p = MIMEBase('application', 'octet-stream')
    # To change the payload into encoded form
    p.set_payload((attachment).read())
    # encode into base64
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % i)
    # attach the instance 'p' to instance 'msg'
    msg.attach(p)
    s = smtplib.SMTP('smtp.office365.com', 587)
    s.starttls()
    s.login(sender, "Que$$2018")
    recipients.extend(recipientscc)
    recipients.extend(BCC)
    s.sendmail(sender, recipients, msg.as_string())
    print("Mail Sent")
    s.quit()


def transfers_report(username):
    cur_date = datetime.date.today()
    today = cur_date.strftime("%d-%m-%Y")
    print(today)
    count = 0

    readig_excel = pd.read_csv("C:\\Users\\RPA Testing\\Desktop\\transfer_approved_cases.csv")
    for i, row in readig_excel.iterrows():
        if str(row['Date']) == str(cur_date.strftime("%d-%m-%Y")) and row['LoginUser'] == username:
            count = count + 1
    replace = count * 1
    print(replace)

    if replace % 5 == 0:
        file_path = open("D:\PySelenium_bank\dashboard_template_Transfers_txt.txt")
        data = file_path.read()
        print(data)

        def substitute(key, value):
            return data.replace(key, str(value))

        def replace_cal_values(key, value):
            switcher = {
                'process_date': substitute(key, value),
                'Records_Count': substitute(key, value),
                'success_transactions': substitute(key, value),
                'Failure _Count': substitute(key, value),
                'kn_code': substitute(key, value),
            }
            return switcher.get(key, "nothing")

        data = replace_cal_values("process_date", today)
        data = replace_cal_values("Records_Count", str(replace))
        data = replace_cal_values("success_transactions", str(replace))
        data = replace_cal_values("Failure _Count", str(0))
        data = replace_cal_values("kn_code", username)

        print(data)

        msg = MIMEMultipart()
        html = data
        sender = 'rpa@quesscorp.com'
        subject = 'Transfer approvals Report Dashboard'
        recipients = ['mahendra.ramisetty@quesscorp.com', 'gracia.velangani@quesscorp.com', 'jabiulla.s@quesscorp.com']
        recipientscc = []
        BCC = ['manoj.ramisetty@quesscorp.com', 'anjana.kovoor@quesscorp.com', 'Shankar.S@quesscorp.com',
               'anand.srinivasan@quesscorp.com', 'pritam.b@quesscorp.com']

        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ", ".join(recipients)
        msg['Cc'] = ", ".join(recipientscc)
        # msg['Bcc'] = ", ".join(BCC)44444
        # part1 = MIMEText(mailBody, 'plain')
        part2 = MIMEText(html, 'html')
        # msg.attach(part1)
        msg.attach(part2)
        i = "C:\\Users\\RPA Testing\\Desktop\\transfer_approved_cases.csv"
        attachment = open(i, "rb")
        p = MIMEBase('application', 'octet-stream')
        # To change the payload into encoded form
        p.set_payload((attachment).read())
        # encode into base64
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % i)
        # attach the instance 'p' to instance 'msg'
        msg.attach(p)
        s = smtplib.SMTP('smtp.office365.com', 587)
        s.starttls()
        s.login(sender, "Que$$2018")
        recipients.extend(recipientscc)
        recipients.extend(BCC)
        s.sendmail(sender, recipients, msg.as_string())
        print("Mail Sent")
        s.quit()
    else:
        pass


def error_report():
    data = "Hi Team," + \
           " please find the excel containing the error records " + \
           "Regards," + \
           "RPA Team"

    print(data)
    msg = MIMEMultipart()
    html = data
    sender = 'rpa@quesscorp.com'
    subject = 'Records failed from '
    recipients = ['mahendra.ramisetty@quesscorp.com', 'gracia.velangani@quesscorp.com',
                  'jabiulla.s@quesscorp.com']
    recipientscc = []
    BCC = ['manoj.ramisetty@quesscorp.com']  # 'anjana.kovoor@quesscorp.com'] #'Shankar.S@quesscorp.com',
    # 'anand.srinivasan@quesscorp.com', #'pritam.b@quesscorp.com']
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)
    msg['Cc'] = ", ".join(recipientscc)
    # msg['Bcc'] = ", ".join(BCC)44444
    # part1 = MIMEText(mailBody, 'plain')
    part2 = MIMEText(html, 'html')
    # msg.attach(part1)
    msg.attach(part2)
    i = "C:\\Users\\RPA Testing\\Desktop\\Bank_rejected_records.csv"
    attachment = open(i, "rb")
    p = MIMEBase('application', 'octet-stream')
    # To change the payload into encoded form
    p.set_payload((attachment).read())
    # encode into base64
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % i)
    # attach the instance 'p' to instance 'msg'
    msg.attach(p)
    s = smtplib.SMTP('smtp.office365.com', 587)
    s.starttls()
    s.login(sender, "Que$$2018")
    recipients.extend(recipientscc)
    recipients.extend(BCC)
    s.sendmail(sender, recipients, msg.as_string())
    print("Mail Sent")
    s.quit()



