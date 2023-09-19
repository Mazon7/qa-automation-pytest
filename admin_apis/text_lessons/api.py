import logging
from jsonschema import validate

from admin_apis.requests import Client
from admin_apis.text_lessons.model import ResponseModel

logger = logging.getLogger("api")


class AdminTextLessons:
    def __init__(self, url):
        self.url = url
        self.client = Client()

    # SUBJECTS
    MAIN = "/text_lessons"

    def create_text_lesson(self, body: dict, headers: dict):
        response = self.client.custom_request(
            "POST", f"{self.url}{self.MAIN}", json=body, headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())
