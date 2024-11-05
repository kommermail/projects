# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions




from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from datetime import datetime
from geopy.geocoders import Nominatim
import pytz
from tzwhere import tzwhere




class ActionShowTimeZone(Action):

    def name(self) -> Text:
        return "show_time_zone"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city=tracker.get_slot("city")

        geolocate= Nominatim(user_agent="codeSignal")
        location= geolocate.geocode(city,timeout=10000)
        x=location.latitude
        y=location.longitude
        tzwher=tzwhere.tzwhere()
        timezone_str= tzwher.tzNameAt(x,y) 
        sigag= datetime.now(pytz.timezone(timezone_str))
        sigagfix=sigag.strftime("%H:%M:%S")
        output= "Location {} is in the {} timezone and the current time is {}".format(city,timezone_str,sigagfix)

        dispatcher.utter_message(text=output)

        return []
