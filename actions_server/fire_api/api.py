import os
import boto3
from datetime import datetime
from datetime import timedelta
from actions.fire_api.static.constant import geo_dict
from actions.fire_api.connect import fires_table, weather_table
# from fire_api.static.constant import geo_dict
# from fire_api.connect import fires_table, weather_table
from boto3.dynamodb.conditions import Key


class Client:
    
    def __init__(self, city):
        
        if city in geo_dict:
            self.city_name  = city
            self.county_name = geo_dict[self.city_name]['county']
        else:
            raise Exception("City Name not found: " + str(city))


    def get_fires(self):
            
        one_day_ago = int((datetime.now() - timedelta(days=1)).timestamp())

        response = fires_table.query(
            KeyConditionExpression=Key('county').eq(self.county_name)
        )

        result = []

        for item in response['Items']:
            if one_day_ago < item['record-updated']:
                new_item = {}
                new_item['county'] = item['county']
                if 'percent-contained' in item:
                    new_item['percent-contained'] = str(item['percent-contained'])
                if 'updated' in item:
                    new_item['updated'] = str(item['updated'])
                if 'final' in item:
                    new_item['final'] = str(item['final'])
                if 'acres-burned' in item:
                    new_item['acres-burned'] = str(item['acres-burned'])
                if 'status' in item:
                    new_item['status'] = str(item['status'])
                if 'description' in item:
                    new_item['description'] = str(item['description'])
                if 'started' in item:
                    new_item['started'] = str(item['started'])
                if 'url' in item:
                    new_item['url'] = str(item['url'])
                if 'name' in item:
                    new_item['name'] = str(item['name'])

                result.append(new_item)

        return result


    def get_weather(self):

        response = weather_table.query(
            KeyConditionExpression=Key('city').eq(self.city_name),
            ScanIndexForward=False,
            Limit=1
        )

        result = response['Items']
        return result

