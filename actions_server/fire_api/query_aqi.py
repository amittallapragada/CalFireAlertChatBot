import requests

url = "https://airnowgovapi.com/reportingarea/get"
payload = {'latitude': '37.87320','longitude': '122.27296', 'stateCode': 'CA', 'maxDistance': '50'}

response = requests.post(url, data = payload)
print(response.content)
