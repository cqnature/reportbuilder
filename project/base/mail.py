#!/usr/bin/env python
# coding=utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#gmail邮箱smtp服务器
host_server = 'smtp.gmail.com:587'
#发件人邮箱
fromaddr = 'cqnature@gmail.com'
username = 'cqnature@gmail.com'
password = 'fsajhtsznoqplupj'
#收件人邮箱
toaddrs = ['nero@peakxgames.com','bear@peakxgames.com', 'eli@peakxgames.com', 'near@peakxgames.com', 'leon@peakxgames.com', 'kinder@peakxgames.com', 'young@peakxgames.com', 'xiaobai@peakxgames.com']

def send_mail(subject, htmlBody):
    #邮件的正文内容
    mail_content = ""
    #邮件正文内容
    msg = MIMEMultipart('related')
    msg["Subject"] = Header(subject, 'utf-8')
    msg["From"] = fromaddr
    msg["To"] = Header("Report Group", 'utf-8') ## 接收者的别名

    msgAlternative = MIMEMultipart('alternative')
    msg.attach(msgAlternative)

    msgText = (MIMEText(htmlBody, 'html', 'utf-8'))
    msgAlternative.attach(msgText)

    #ssl登录
    smtp = SMTP(host_server)
    smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(fromaddr, toaddrs, msg.as_string())
    smtp.quit()
