import requests
from static.constant import geo_dict
url = "https://airnowgovapi.com/weather/get"

payload = {'latitude': '37.87320',
'longitude': '-122.27296',
'stateCode': 'CA',
'maxDistance': '50'}
files = [

]
headers = {
  'Content-Type': 'application/json',
}

response = requests.request("GET", url, headers=headers, data = payload, files = files)



def get_weather_data(lat, lng):
    payload = {'latitude': lat, 'longitude': lng, 'stateCode': 'CA', 'maxDistance': '50'}
    headers = { 'Content-Type': 'application/json'}
    url = "https://airnowgovapi.com/weather/get"
    data = requests.post(url, data=payload)
    if data.status_code == 500:
        return None
    else:
        return data.json()


cities = ['Albany', 'Avenal', 'Fremont', 'Half Moon Bay', 'Lodi', 'Milpitas', 'Newark', 'Newman', 'Oroville', 'Palo Alto', 'San Jacinto', 'Saratoga', 'Sebastopol', 'South Gate', 'Wheatland']
for city in cities:
    data = geo_dict[city]

    print(f"city: {city} value: {get_weather_data(data['lat'], data['lon'])}")


# print(geo_dict['San Jose'])
# failed_cities = []
# for k, v in geo_dict.items():
#     data = get_weather_data(v['lat'], v['lon'])
#     print(f"city:{k} data:{data}")
#     if data == None:
#         failed_cities.append(k)
    
# print(failed_cities)
# print(len(failed_cities))
