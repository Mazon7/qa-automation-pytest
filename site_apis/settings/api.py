import logging
from jsonschema import validate

from site_apis.requests import Client
from site_apis.settings.model import ResponseModel

logger = logging.getLogger("api")


class Settings:
    def __init__(self, url):
        self.url = url
        self.client = Client()

    USER_ECHO = "/userecho"

    def get_userecho_categories(self, headers: dict, schema: dict):
        response = self.client.custom_request(
            "GET", f"{self.url}{self.USER_ECHO}/categories", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    # Multipart/form-data request
    def create_userecho_message(self, data: dict, files: dict, headers: dict, schema: dict):
        response = self.client.custom_request(
            "POST", f"{self.url}{self.USER_ECHO}/create_ticket", data=data, files=files, headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response)
        return ResponseModel(status=response.status_code, response=response)

    def get_locale_json(self, lang: str, headers: dict, schema: dict):
        response = self.client.custom_request(
            "GET", f"{self.url}/locales/{lang}/common.json", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def get_site_settings(self, headers: dict, schema: dict):
        response = self.client.custom_request(
            "GET", f"{self.url}/labstu/settings", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())

    def get_site_page(self, slug: str, headers: dict, schema: dict):
        response = self.client.custom_request(
            "GET", f"{self.url}/page/{slug}", headers=headers)
        # validate(instance=response.json(), schema=schema)
        logger.info(response.json())
        return ResponseModel(status=response.status_code, response=response.json())
