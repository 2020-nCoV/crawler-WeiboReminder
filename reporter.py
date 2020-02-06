import smtplib
from email.header import Header
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from setting import mailConfig


def send(mail_msg, title):
    config = mailConfig()
    mail_host = config["mail_host"]
    mail_user = config["mail_user"]
    mail_pass = config["mail_pass"]

    sender = mail_user
    receivers = config["receivers"]

    smtpObj = SMTP_SSL(mail_host)
    smtpObj.ehlo()
    smtpObj.login(mail_user, mail_pass)

    message = MIMEText(mail_msg, 'plain', 'utf-8')
    message['From'] = Header("爬虫工具开发团队", 'utf-8')
    message['To'] = Header("新闻团队", 'utf-8')

    subject = title
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("[INFO] MAIL SENT SUCCESSGULLY")
    except smtplib.SMTPException as e:
        print(e)
        print("[ERROR] ,MAIL SENT FAILED)