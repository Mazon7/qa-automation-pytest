import logging
from jsonschema import validate

from admin_apis.requests import Client
from admin_apis.subscription.model import ResponseModel

logger = logging.getLogger("api")


class AdminSubscription:
    def __init__(self, url):
        self.url = url
        self.client = Client()

    # SUBJECTS
    MAIN = "/subscriptions"

    def get_subscriptions_by_subject(self, subjects_pk: str, headers: dict):
        response = self.client.custom_request("GET", f"{self.url}/subjects/{subjects_pk}{self.MAIN}", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())


    def create_subscription(self, body: dict, subjects_pk: str, headers: dict):
        response = self.client.custom_request(
            "POST", f"{self.url}/subjects/{subjects_pk}{self.MAIN}", json=body, headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def delete_subscription(self, id: str, headers: dict):
        response = self.client.custom_request(
            "DELETE", f"{self.url}{self.MAIN}/{id}", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response)
        return ResponseModel(status=response.status_code, response=response)
