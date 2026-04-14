import smtplib

smtpObj = smtplib.SMTP_SSL("smtp.gmail.com", 465)
smtpObj.login("ajotastd@gmail.com", "")

# dtyo rxnv xbmw tvml

res = smtpObj.verify("ajotastd@gmail.com")

print(res)

smtpObj.sendmail("ajotastd@gmail.com", "novielloagustin@gmail.com", "prueba")

# smtpObj.quit() // with SMTP([host [, port]]) as smtp: -> De esta segunda forma, no es necesario smtpObj.quit()