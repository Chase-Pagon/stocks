# Import requests (to download the page)
import requests

# Import BeautifulSoup (to parse what we download)
from bs4 import BeautifulSoup

# Import Time (to add a delay between the times the scape runs)
from datetime import datetime, timedelta
import time
from pytz import timezone


import pandas as pd

# Import smtplib (to allow us to email)
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders



eastern = timezone('US/Eastern')
url = "http://openinsider.com/insider-purchases"

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, "lxml")

last_hash = soup.__hash__()

while True:
    url = "http://openinsider.com/insider-purchases"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "lxml")

    curr_hash = soup.__hash__()

    if curr_hash == last_hash:
        print("Nothing has changed")
        time.sleep(3600)

    else:
        print("Sending email now...")
        time.sleep(1)
        table_rows = soup.find_all('tr')
        header = table_rows[33].find_all('th')
        header_row = [t.text.replace(u'\xa0', u' ').replace(u'\u0394', u'') for t in header]
        header_row = header_row[0:len(header_row) - 4]
        open_insider_changes = [header_row]

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("chase.pagon@gmail.com", "yrhswencdqprrbiv")

        for tr in soup.find_all('tr')[34:134]:
            td = tr.find_all('td')
            date = datetime.strptime(td[1].text, '%Y-%m-%d %H:%M:%S')
            if date > (datetime.now(eastern) - timedelta(minutes=61)):
                td = tr.find_all('td')
                row = [t.text for t in td]
                open_insider_changes.append(row)

        df = pd.DataFrame(open_insider_changes)
        df.columns = df.iloc[0]
        df = df[1:]
        df.to_csv('open_insider_changes.csv')

        fromaddr = 'chase.pagon@gmail.com'
        toaddrs = 'chase.pagon@gmail.com'

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddrs
        msg['Subject'] = "Latest Open Insider Updates"

        part = MIMEBase('application', "octet-stream")
        part.set_payload(open('./open_insider_changes.csv', "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename='open_insider_changes.csv')
        msg.attach(part)

        server.sendmail(fromaddr, toaddrs, msg.as_string())
        server.quit()

    last_hash = curr_hash
