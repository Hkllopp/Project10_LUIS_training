from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient
from azure.cognitiveservices.language.luis.authoring.models import (
    ApplicationCreateObject,
)
from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.language.luis.authoring.models import WordListObject

from config import DefaultConfig

import json, time, uuid


class Luis_manager:
    def __init__(self, version_id):
        self.version_id = version_id
        self.config = DefaultConfig()
        self.authoring_key = self.config.LUIS_API_KEY
        self.authoring_endpoint = self.config.LUIS_API_HOST_NAME
        self.prediction_key = self.config.LUIS_API_KEY
        self.prediction_endpoint = self.config.LUIS_API_HOST_NAME
        self.app_id = self.config.LUIS_APP_ID
        self.authoring_client = LUISAuthoringClient(
            self.authoring_endpoint, CognitiveServicesCredentials(self.authoring_key)
        )
        self.prediction_client = LUISRuntimeClient(
            self.prediction_endpoint, CognitiveServicesCredentials(self.prediction_key)
        )

    def add_example(self, example):
        print("Adding example: " + str(example["text"]))
        self.authoring_client.examples.add(
            self.app_id, self.version_id, example, enable_nested_children=True
        )

    def train(self):
        self.authoring_client.train.train_version(self.app_id, self.version_id)
        waiting = True
        time_waiting = 0
        while waiting:
            info = self.authoring_client.train.get_status(self.app_id, self.version_id)

            # get_status returns a list of training statuses, one for each model. Loop through them and make sure all are done.
            waiting = any(
                map(
                    lambda x: "Queued" == x.details.status
                    or "InProgress" == x.details.status,
                    info,
                )
            )
            if waiting:
                print(f"Waiting {time_waiting} seconds for training to complete...")
                time.sleep(1)
                time_waiting += 1
            else:
                print("trained")
                waiting = False

    def publish(self):
        self.authoring_client.apps.publish(
            self.app_id, self.version_id, is_staging=False
        )
        print("published")

    def get_prediction(self, query):
        return self.prediction_client.prediction.get_slot_prediction(
            self.app_id, "Production", query
        )

    def get_examples_list(self):
        return self.authoring_client.examples.list(self.app_id, self.version_id)

    def get_intents_list(self):
        return self.authoring_client.model.list_intents(self.app_id, self.version_id)

    def get_closed_list(self, name):
        return self.authoring_client.model.get_closed_list(
            self.app_id, self.version_id, name
        )

    def list_closed_lists(self):
        return self.authoring_client.model.list_closed_lists(
            self.app_id, self.version_id
        )

    def update_closed_list(self, entity_id, closed_list):
        already_list = [
            sublist.canonical_form.upper()
            for sublist in self.get_closed_list(entity_id).sub_lists
        ]
        for item in closed_list:
            if item["canonicalForm"].upper() not in already_list:
                print("Adding " + item["canonicalForm"])
                try:

                    self.authoring_client.model.patch_closed_list(
                            app_id=self.app_id,
                            version_id=self.version_id,
                            cl_entity_id=entity_id,
                            sub_lists=[
                                WordListObject(
                                    canonical_form=item["canonicalForm"], list=item["list"]
                                )
                            ],
                        )
                except:
                    print("Error adding " + item["canonicalForm"])
                    continue
        return "Finished adding closed list"
