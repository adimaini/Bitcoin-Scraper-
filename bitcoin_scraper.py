import requests
import json
import bs4
import time 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

RATE_THRESHOLD = 10000
MY_ADDRESS = 'eddiemaini@gmail.com'
TO_ADDRESS = 'adimaini@vt.edu'
PASSWORD = 'chunkyPBJ3-'


def check_rate(rate):
	if rate > RATE_THRESHOLD:
		return True 
	else: return False 


def email_me(rate):
	s = smtplib.SMTP(host='smtp.gmail.com', port=587)
	s.starttls()
	s.login(MY_ADDRESS, PASSWORD)

	message = str.format('Bitcoin price is {}', rate)

	msg = MIMEMultipart()
	msg['From']=MY_ADDRESS
	msg['To']=TO_ADDRESS
	msg['Subject']="BITCOIN PRICE ALERT"
	msg.attach(MIMEText(message, 'plain'))

	s.send_message(msg)
	del msg

while True: 
	# pull the coinbase API and store the dict in 'response'
	response = json.loads(requests.get("https://api.coindesk.com/v1/bpi/currentprice.json").text)

	# parse the dict to get the USD rate of Bitcoin
	rate = float(response['bpi']['USD']['rate'].replace(',', ''))

	if check_rate(rate): email_me(rate)

	# wait some time before looping again
	time.sleep(60*30)

