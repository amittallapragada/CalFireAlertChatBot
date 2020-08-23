# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Tracker
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from actions.fire_api.static.cities_list import cities 
from actions.fire_api.api import Client
# from fire_api.static.cities_list import cities 
# from fire_api.api import Client 
from fuzzywuzzy import fuzz
from datetime import timedelta, datetime 
from pytz import timezone

#
#
class ActionFireUpdate(FormAction):

    def name(self):
        return "action_fire_update"

    @staticmethod
    def required_slots(tracker):
        """A list of required slots that the form has to fill"""
        return ["city"]

    def slot_mappings(self):
        return {"city": self.from_text(intent='fire_update')}
    

    def get_last_user_utterance(self, tracker:Tracker):
        events = tracker.events 
        events.reverse()
        for i in range(len(events)):
            if events[i]['event'] == 'user':
                return events[i]['text']

    def validate_city(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        user_utterance = self.get_last_user_utterance(tracker)
        potential_city = user_utterance.split(" ")[1:]
        potential_city = " ".join(potential_city)
        best_guess = None 
        max_sim = -10000    
        for city in cities:
            sim = fuzz.ratio(potential_city.lower().strip(), city.lower())
            if sim > max_sim:
                max_sim = sim 
                best_guess = city
        print(f"user input: {potential_city} and {best_guess} is our best guess: {max_sim}")
        if max_sim > 70:
            return {'city':best_guess}
        else:
            dispatcher.utter_message(f"We could not find {potential_city}. please try again. Note: this is only for California.")
            return {"city":None}
         


    def fire_response_handler(self, fire_data, dispatcher):
        if len(fire_data) == 0:
            response_text = "Your city has no forest fire warnings currently. Please stay alert and try us again as more news develops."
            
        elif len(fire_data) == 1:
            response_text = f"There is 1 fire that {fire_data[0]['county']} could be impacted by."
        else:
            response_text = f"There are {len(fire_data)} fires that {fire_data[0]['county']} could be impacted by."
        #utter header 
        dispatcher.utter_message(response_text)

        if len(fire_data) != 0:
            for fire in fire_data:
                fire_name=fire.get("name", None)
                percent_contained=fire.get("percent-contained", None)
                evac_url= fire.get("url", None)
                timestamp = fire.get("updated", None)
                
                message = ""
                if fire_name:
                    message += f"-Fire Name: {fire_name}\n"
                if percent_contained:
                    message += f"-Percent Contained: {int(percent_contained)}%\n"
                if evac_url:
                    message += f"-Fire Map: {evac_url}\n"
                if timestamp:
                    date_format='%m/%d/%Y %H:%M %p'
                    timestamp = datetime.fromtimestamp(int(timestamp))
                    pst = timestamp + timedelta(hours=7)
                    pst_str = pst.strftime(date_format)
                    message += f"-Last Updated: {pst_str}"

                dispatcher.utter_message(message)

    def weather_response_handler(self, city, weather_data, dispatcher):
        if len(weather_data) != 0:
            weather_data = weather_data[0]
            hum = weather_data.get('humidity', None)
            temp = weather_data.get("temp", None)
            weather = weather_data.get("weather", None)
            aqi = weather_data.get("aqi", None)
            message = f"Current {city} weather conditons:\n"
            if weather:
                message += f"-Air Quality: {weather}\n"
            if aqi:
                message += f"-AQI: {aqi}\n"
            if temp:
                temp = '%.2f'%(float(temp))
                message += f"-Temp: {temp}\n"
            message += "For an update on the same or different city type 'update city_name'\n"
            dispatcher.utter_message(message)


                
                        

        





    def submit(self, dispatcher, tracker, domain):
        # type: (CollectingDispatcher, Tracker, Dict[Text, Any]) -> List[Dict]
        """Define what the form has to do
            after all required slots are filled"""
        city = tracker.get_slot("city")
        fire_tracker = Client(city=city)
        fire_data = fire_tracker.get_fires()
        weather_data = fire_tracker.get_weather()
        self.fire_response_handler(fire_data, dispatcher)
        self.weather_response_handler(city, weather_data, dispatcher)
        return []


