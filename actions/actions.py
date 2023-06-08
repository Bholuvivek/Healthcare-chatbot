from typing import Any, Text, Dict, List
import pandas as pd
import os
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


FILE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(FILE_DIR, 'data', 'diseases_db.csv')

# Load the diseases.csv file into a pandas DataFrame
df = pd.read_csv(DATA_PATH)

class ActionProvideDiseaseInfo(Action):

    def name(self) -> Text:
        return "action_provide_disease_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Extract the user's entity from the tracker
        inquired_disease = tracker.get_slot("disease")

        if not inquired_disease:
            dispatcher.utter_message(text="What disease are you interested in?")
            return []

        # Search for the disease in the DataFrame based on the user's query
        disease_info = df[df["Disease"].str.contains(inquired_disease, case=False)]

        if not disease_info.empty:

            # Check if symptoms_info and treatment_info slots have values
            symptoms_info = tracker.get_slot('symptoms_info')
            treatment_info = tracker.get_slot('treatment_info')

            if symptoms_info:
                symptoms = disease_info['Symptoms'].values[0]
                response = f"The symptoms of {inquired_disease} are:"
                response += f"\n{symptoms}"
                dispatcher.utter_message(text=response)
                return [SlotSet("symptoms_info", None)]

            if treatment_info:
                treatment = disease_info['Treatments'].values[0]
                response = f"The treatment options for {inquired_disease} include:"
                response += f"\n{treatment}"
                dispatcher.utter_message(text=response)
                return [SlotSet("treatment_info", None)]

            # Extract the relevant information from the DataFrame
            response = disease_info["Description"].values[0]
            # Send the response to the user
            dispatcher.utter_message(text=f"Here is some information about {inquired_disease}:\n{response}")

        else:
            dispatcher.utter_message(text="I'm sorry, I couldn't find information about that disease. Is it spelled correctly?")

        return []

