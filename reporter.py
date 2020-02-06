import smtplib
from email.header import Header
from smtplib import SMTP_SSL
from email.mime.text import MIMEText



def send(mail_msg,title):
    mail_host = "smtp.qq.com"
    mail_user = "451459536@qq.com"
    mail_pass = "qsyrrsrdizvscbea"

    sender = mail_user
    receivers = ['ultraxia@foxmail.com']

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
        print ("[INFO] MAIL SNET SUCCESSFULLY")
    except smtplib.SMTPException as e:
        print(e)
        print ("[INFO] Error: MAIL SNET FAILED")
