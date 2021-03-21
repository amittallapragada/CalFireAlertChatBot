import requests
import os
import json
from datetime import datetime
from connect import Database



fires_table = Database(collection_name="fires")


def updateFires():
    print("Update fires: Starting run at", datetime.now())
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

                item['started'] = datetime.strptime(fire['Started'][:19] + 'Z', '%Y-%m-%dT%H:%M:%SZ').timestamp()
                item['updated'] = datetime.strptime(fire['Updated'][:19] + 'Z', '%Y-%m-%dT%H:%M:%SZ').timestamp()

                if fire['AcresBurned']:
                        item['acres-burned'] = fire['AcresBurned']
                if fire['PercentContained']:
                        item['percent-contained'] = fire['PercentContained']

                item['record-updated'] = int(datetime.now().timestamp())
                print(item)
                fires_table.put_item(Item=item)
        except Exception as e:
            print("update fires Exception!", e)
            pass