import requests
from bs4 import BeautifulSoup
import json 
page = requests.get("https://en.wikipedia.org/wiki/List_of_cities_and_towns_in_California")
soup = BeautifulSoup(page.text)

tables = soup.find_all('table')

for table in tables:
    ths = table.find_all('th')
    headings = [th.text.strip() for th in ths]
    if headings[:3] == ["Name", "Type", "County"]:
        # print(headings)
        break
    #     break
headings = headings[8::]
trs = table.find_all('tr')
count = 0 
city_dict = {}
for i in range(len(trs)):
    tr = trs[i]
    tds = tr.find_all('td')
    if not tds:
        continue
    else:
        loc_type, county = [td.text.strip() for td in tds[:2]]
        name = headings[count]
        print(name, loc_type, county)
        city_dict[name] = county
        count+= 1

print(city_dict)
print(len(city_dict))

from static.constant import geo_dict
from scrape_lat_long import get_lat_lng
import json 
import time
geo_dict_keys = set(list(geo_dict.keys()))
city_dict_keys = set(list(city_dict.keys()))
new_keys = city_dict_keys - geo_dict_keys


for key in new_keys:
    print(key)
    lat_lng = get_lat_lng(key)
    geo_dict[key] = {"county": city_dict[key], "lat":lat_lng[0], "lon":lat_lng[1]}
    time.sleep(1)

with open("constant.json", "w") as fp:
     json.dump(geo_dict, fp, indent=4)
