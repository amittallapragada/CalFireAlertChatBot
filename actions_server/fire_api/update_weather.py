import requests
import os
import boto3
import json
from static.constant import geo_dict
import time
from decimal import Decimal
from decimal import localcontext
from decimal import Inexact
from decimal import Rounded
from datetime import datetime
from datetime import tzinfo
import pytz
import requests

AWSAccessKeyId=os.environ.get('AWSAccessKeyId')
AWSSecretKey=os.environ.get('AWSSecretKey')

client = boto3.resource(
    'dynamodb',
    aws_access_key_id=AWSAccessKeyId,
    aws_secret_access_key=AWSSecretKey,
    region_name='us-east-2'
)

weather_table = client.Table("weather")

def get_weather_data(lat, lon):
    payload = {'latitude': lat, 'longitude': lon, 'stateCode': 'CA', 'maxDistance': '50'}
    url = "https://airnowgovapi.com/weather/get"
    data = requests.post(url, data=payload)
    if data.status_code == 500:
        return None
    else:
        return data.json()

def degToCompass(num):
    val=int((num/22.5)+.5)
    arr=["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    return arr[(val % 16)]

for city in geo_dict:
    val = geo_dict[city]
    county = val["county"]
    lat = val["lat"]
    lon = val["lon"]

    item = {}
    item['city'] = city

    payload = {'latitude': lat,'longitude': lon, 
               'stateCode': 'CA','maxDistance': '50'}

    url = "https://airnowgovapi.com/reportingarea/get"
    response = requests.post(url, data = payload)
    time.sleep(1)

    data = json.loads(response.content)
    for d in data:
        if 'PM2.5' == d['parameter']:
            row = d

            date = row['issueDate']
            timezone = row['timezone']
            category = row['category']

            if 'stateCode' in row and row['stateCode'] == 'CA':
                if 'aqi' in row:
                    item['aqi'] = row['aqi']
                else:
                    item['aqi'] = None

                item['category'] = category
                break
            else:
                print (row['stateCode'])

    if 'id' in geo_dict[city]:
        url = "http://api.openweathermap.org/data/2.5/weather?id={}&APPID=30c4638a4c36a568656cb0410d4a388f".format(geo_dict[city]['id'])
        response = requests.get(url)
        resp = json.loads(response.content)

        print(resp)

        if resp['name'] == city:
            if "weather" in resp and len(resp["weather"]) > 0 and "main" in resp["weather"][0]:
                item['weather'] = str(resp["weather"][0]["main"])

            if "main" in resp and "temp" in resp["main"]:
                item['temp'] = str((resp["main"]["temp"] - 273.15) * ( 9 / 5 ) + 32)

            if "main" in resp and "humidity" in resp["main"]:
                item['humidity']  = str(resp["main"]["humidity"])
    
    resp = get_weather_data(lat=lat, lon=lon)
    print(resp)
    if resp is not None:
        if resp.get("temperature", None):
            item['temp'] = str(resp['temperature'])
        if resp.get("description", None):
            item['weather'] = resp['description']

    pst_timezone = pytz.timezone("US/Pacific")
    item['time'] = datetime.now(pst_timezone).strftime('%m/%d/%YT%H:%MZ')

    print(item)
    weather_table.put_item(Item=item)