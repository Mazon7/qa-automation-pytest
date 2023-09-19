import logging
from jsonschema import validate

from site_apis.requests import Client
from site_apis.subject.model import ResponseModel

logger = logging.getLogger("api")


class Subject:
    def __init__(self, url):
        self.url = url
        self.client = Client()

    # SUBJECTS
    MAIN = "/subjects"
    AVAILABLE = MAIN + "/available"
    MY_SUBJECTS = MAIN + "/my"
    SUB_SUBJECTS = "/subscription_subjects"
    CURRENT_JOB = "/current_job"

    def get_subjects(self, headers: dict, schema: dict):
        response = self.client.custom_request(
            "GET", f"{self.url}{self.MAIN}", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def get_subject_id(self, id: str, headers: dict, schema: dict):
        response = self.client.custom_request(
            "GET", f"{self.url}{self.MAIN}/{id}", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def subjects_available(self, headers: dict, schema: dict):
        response = self.client.custom_request(
            "GET", f"{self.url}{self.AVAILABLE}", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response)
        return ResponseModel(status=response.status_code, response=response)

    def my_subjects(self, headers: dict, schema: dict):
        response = self.client.custom_request(
            "GET", f"{self.url}{self.MY_SUBJECTS}", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response)
        return ResponseModel(status=response.status_code, response=response)

    def sub_subjects_id(self, id: str, headers: dict, schema: dict):
        response = self.client.custom_request(
            "GET", f"{self.url}{self.SUB_SUBJECTS}/{id}", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def get_current_job(self, subject_pk: str, headers: dict, schema: dict):
        response = self.client.custom_request(
            "GET", f"{self.url}{self.MAIN}/{subject_pk}{self.CURRENT_JOB}", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())
