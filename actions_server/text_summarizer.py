# from bs4 import BeautifulSoup
# import requests

# resp = requests.get("https://www.fire.ca.gov/umbraco/Api/IncidentApi/GetIncidents")
# fires = resp.json()

# updates = [fire['ConditionStatement'] for fire in fires['Incidents']]


# def latest_update(data):
#     soup = BeautifulSoup(data)
#     paragraphs = soup.find_all("p")
#     bold_stmts = [p.find('b') for p in paragraphs]
#     count = 0 
#     edges = []
#     for i in range(len(bold_stmts)):
#         if bold_stmts[i] != None and count < 2:
#             if i != 0 and bold_stmts[i-1] == None:
#                 edges.append(i)
#                 count +=1 
#         if count > 2:
#             break

#     raw_update = paragraphs[edges[0]:edges[1]]
#     for line in raw_update:
#         print(line.text.strip())


# for update in updates:
#     if update != None:
#         latest_update(update)
#         print("#"*100)

# #find bounds
# # p_bounds = {'s':None, 'e':None}

# # for i in range(len(paragraphs)):
# #     p = paragraphs[i]
# #     if p.find('b') != None:
# #         p_bounds

from datetime import datetime, timedelta
from pytz import timezone

date_format='%m/%d/%Y %H:%M %p'

test = datetime.fromtimestamp(1598190442)
pst = test + timedelta(hours=7)
datetime_obj_utc = test.replace(tzinfo=timezone('US/Pacific'))
datetime_obj_utc = datetime_obj_utc.strftime(date_format)
# # print(datetime_obj_utc)
# date = datetime_obj_utc.astimezone(timezone('US/Pacific'))
# print(date)
# # test = test.replace(tzinfo=timezone('US/Pacific'))
# print('Local date & time is  :' + date.strftime(date_format))
# now = datetime.now()
# ams_dt = now.astimezone(timezone('US/Pacific'))
# print(ams_dt)
# datetime = datetime_obj_utc + timedelta(hours=2)
print(datetime_obj_utc)