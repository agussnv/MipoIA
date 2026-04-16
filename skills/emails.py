import smtplib
from email.mime.text import MIMEText
from skills.voz import hablar
from dotenv import load_dotenv
import traceback
import os

load_dotenv()

sender="ajotastd@gmail.com"
password=os.getenv('PASSWORD_GMAIL_SMTP')

def send_email(recipient, body, subject):
    try:
        msg = MIMEText(body)
        msg['Subject']=subject
        msg['From']=sender
        msg['To']=recipient
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtpObj:
            smtpObj.login(sender, password)
            smtpObj.sendmail(sender, recipient, msg.as_string())
            hablar("Email enviado!")
    except Exception as e:
        traceback.print_exc()

# smtpObj.quit() // with SMTP([host [, port]]) as smtp: -> De esta segunda forma, no es necesario smtpObj.quit()