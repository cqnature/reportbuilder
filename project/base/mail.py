#!/usr/bin/env python
# coding=utf-8

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP
from os import path

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
# toaddrs = ['nero@peakxgames.com','bear@peakxgames.com', 'eli@peakxgames.com', 'near@peakxgames.com', 'kinder@peakxgames.com', 'young@peakxgames.com', 'xiaobai@peakxgames.com']
toaddrs = ['bear@peakxgames.com']

def send_mail(subject, htmlBody, attachments = [], receivers = []):
    #邮件的正文内容
    mail_content = ""
    #邮件正文内容
    msg = MIMEMultipart('related')
    msg["Subject"] = Header(subject, 'utf-8')
    msg["From"] = fromaddr
    msg["To"] = Header("Report Group", 'utf-8') ## 接收者的别名

    msgAlternative = MIMEMultipart('alternative')
    msg.attach(msgAlternative)

    #设置html正文
    msgText = (MIMEText(htmlBody, 'html', 'utf-8'))
    msgAlternative.attach(msgText)

    #设置附件
    for attachment in attachments:
        # 构造附件，传送指定文件
        att = MIMEText(open(attachment, 'rb').read(), 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = 'attachment; filename="{0}"'.format(path.basename(attachment))
        msg.attach(att)

    #没有指定收件人则使用默认邮件组
    if len(receivers) == 0:
        receivers.extend(toaddrs)

    #ssl登录
    smtp = SMTP(host_server)
    smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(fromaddr, receivers, msg.as_string())
    smtp.quit()
