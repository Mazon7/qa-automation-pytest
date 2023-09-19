import logging
from jsonschema import validate

from admin_apis.requests import Client
from admin_apis.subject.model import ResponseModel

logger = logging.getLogger("api")


class AdminSubject:
    def __init__(self, url):
        self.url = url
        self.client = Client()

    # SUBJECTS
    MAIN = "/subjects"

    def create_subject(self, body: dict, headers: dict):
        response = self.client.custom_request(
            "POST", f"{self.url}{self.MAIN}", json=body, headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def delete_subject(self, id: str, headers: dict):
        response = self.client.custom_request(
            "DELETE", f"{self.url}{self.MAIN}/{id}", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response)
        return ResponseModel(status=response.status_code, response=response)