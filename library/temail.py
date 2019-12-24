import smtplib
from email.mime.text import MIMEText

from public_config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVERS


def send_email(env, content):
    title = f'tcloud警告 from {env}'
    sender = EMAIL_SENDER
    password = EMAIL_PASSWORD
    receivers = EMAIL_RECEIVERS
    smtp_server = 'smtp.163.com'
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = sender
    msg['To'] = ';'.join(receivers)
    msg['Subject'] = title
    server = smtplib.SMTP_SSL(smtp_server, 465)
    # server.set_debuglevel(1)
    server.login(sender, password)
    server.sendmail(sender, receivers, msg.as_string())
    server.quit()
