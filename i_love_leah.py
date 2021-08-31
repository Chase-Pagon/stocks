import smtplib
from datetime import datetime, timedelta

dt_string = '9/13/2021 17:30:00'
s = (datetime.strptime(dt_string, "%m/%d/%Y %H:%M:%S") - datetime.now()).total_seconds()
days, remainder = divmod(s, 86400)
hours, remainder = divmod(remainder, 3600)
minutes, seconds = divmod(remainder, 60)
time_until = '{:02} days, {:02} hours, {:02} minutes, and {:02} seconds'.format(int(days), int(hours), int(minutes), int(seconds))

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "chase.pagon@gmail.com"
receiver_email = "leahgriffith123@gmail.com"
password = "yrhswencdqprrbiv"
message = """\
Subject: I love you

I miss you baby! I love you so much and I'll talk to you soon! See you in exactly this much time """ + time_until + """ 

Love, Chase"""

with smtplib.SMTP(smtp_server, port) as server:
    server.ehlo()  # Can be omitted
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
