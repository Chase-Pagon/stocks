import requests

url = "https://quotient.p.rapidapi.com/intraday"

querystring = {"end":"2021-02-12 12:00","interval":"5","symbol":"AAPL","start":"2021-02-12 10:00"}

headers = {
    'x-rapidapi-key': "5bbd5f9e9emsh0294708c8d5809fp1fff58jsn2cb91d91ccb4",
    'x-rapidapi-host': "quotient.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)