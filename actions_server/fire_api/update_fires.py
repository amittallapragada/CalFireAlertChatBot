import requests
import os
import boto3
import json
from decimal import Decimal
from datetime import datetime

AWSAccessKeyId=os.environ.get('AWSAccessKeyId')
AWSSecretKey=os.environ.get('AWSSecretKey')

client = boto3.resource(
    'dynamodb',
    aws_access_key_id=AWSAccessKeyId,
    aws_secret_access_key=AWSSecretKey,
    region_name='us-east-2'
)

fires_table = client.Table("fires")

url = "https://www.fire.ca.gov/umbraco/Api/IncidentApi/GetIncidents"
r = requests.get(url, allow_redirects=True)

fire_data = json.loads(r.content)

for fire in fire_data['ListIncidents']:
	try:
		for county in fire['Counties']:
			item = {}
			item['county'] = county
			item['uuid'] = fire['UniqueId']
			item['url'] = 'https://www.fire.ca.gov/' + fire['CanonicalUrl']
			item['name'] = fire['Name']
			item['description'] = fire['SearchDescription']
			item['status'] = fire['Status']
			item['final'] = fire['Final']

			item['updated'] = fire['Updated']

			item['started'] = Decimal(datetime.strptime(fire['Started'][:19] + 'Z', '%Y-%m-%dT%H:%M:%SZ').timestamp())
			item['updated'] = Decimal(datetime.strptime(fire['Updated'][:19] + 'Z', '%Y-%m-%dT%H:%M:%SZ').timestamp())

			if fire['AcresBurned']:
				item['acres-burned'] = Decimal(fire['AcresBurned'])
			if fire['PercentContained']:
				item['percent-contained'] = Decimal(fire['PercentContained'])
			
			item['record-updated'] = int(datetime.now().timestamp())
			fires_table.put_item(Item=item)
	except Exception:
		pass
