import requests
import json
import bs4

response = json.loads(requests.get("https://api.coindesk.com/v1/bpi/currentprice.json").text)
print(response)