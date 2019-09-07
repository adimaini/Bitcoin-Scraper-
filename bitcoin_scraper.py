import requests
import json
import bs4
import time 
import boto3
from botocore.exceptions import ClientError

RATE_THRESHOLD = 10000
SENDER = 'eddiemaini@gmail.com'
RECIPIENT = 'adimaini@vt.edu'
AWS_REGION = 'us-east-1'


def check_rate(rate):
    if rate > RATE_THRESHOLD:
        return True 
    else: return False 


def email_me(rate):

    # The subject line for the email.
    SUBJECT = "BITCOIN PRICE ALERT!"
    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = str.format('Bitcoin price is now {}', rate)

    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
      <h1>Bitcoin value is USD %f</h1>
    </body>
    </html>
                """%(rate)
    # The character encoding for the email.
    CHARSET = "UTF-8"
    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)
    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT
                ]
            }, 

            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    }, 
                    'Text': {
                            'Charset': CHARSET,
                            'Data': BODY_TEXT
                    }
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT
                }
            },

            Source=SENDER)

    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])



while True: 
    # pull the coinbase API and store the dict in 'response'
    response = json.loads(requests.get("https://api.coindesk.com/v1/bpi/currentprice.json").text)

    # parse the dict to get the USD rate of Bitcoin
    rate = float(response['bpi']['USD']['rate'].replace(',', ''))

    if check_rate(rate): email_me(rate)

    # wait some time before looping again
    time.sleep(30)


