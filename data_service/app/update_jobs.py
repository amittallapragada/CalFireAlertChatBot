from update_weather import updateWeather 
from update_fires import updateFires
import schedule 
import time 

schedule.every(10).seconds.do(updateWeather)
schedule.every(10).seconds.do(updateFires)


while True:
    schedule.run_pending()
    time.sleep(1)